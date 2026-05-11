from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

from dotenv import load_dotenv
from markdownify import markdownify as html_to_markdown
from playwright.async_api import Error as PlaywrightError, Page, Request, Response, async_playwright


ROOT = Path(__file__).resolve().parents[2]
HOMEWORK_DIR = ROOT / "homework"
RAW_DIR = HOMEWORK_DIR / "pintia_raw"


TYPE_BY_ORDINAL: dict[int, tuple[str, str]] = {
    1: ("TRUE_OR_FALSE", "判断题"),
    2: ("MULTIPLE_CHOICE", "单选题"),
    # 3 is MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER in Pintia, but this course says it is unused.
    4: ("FILL_IN_THE_BLANK", "填空题"),
    5: ("FILL_IN_THE_BLANK_FOR_PROGRAMMING", "程序填空题"),
    6: ("CODE_COMPLETION", "函数题"),
    7: ("PROGRAMMING", "编程题"),
    8: ("SUBJECTIVE", "主观题"),
}

SECTION_ORDER = [1, 2, 4, 5, 6, 7, 8]
ORDINAL_BY_TYPE = {problem_type: ordinal for ordinal, (problem_type, _) in TYPE_BY_ORDINAL.items()}
CHOICE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ACCEPTED_STATUSES = {"ACCEPTED", "PROBLEM_ACCEPTED", "PROBLEM_ACCEPTED_"}
DEFAULT_MANUAL_ANSWERS = ROOT / "tools" / "pintia_crawler" / "manual_answers.json"


class PintiaError(RuntimeError):
    pass


class PermissionNeeded(PintiaError):
    pass


@dataclass
class TargetFile:
    path: Path
    front_matter: str
    title: str
    link: str
    problem_set_id: str


@dataclass
class ProblemRecord:
    problem: dict[str, Any]
    answer: Any = None
    answer_source: str = ""
    last_submission_detail: dict[str, Any] | None = None
    accepted: bool = False


@dataclass
class CrawlResult:
    target: TargetFile
    problem_set: dict[str, Any] = field(default_factory=dict)
    exam_id: str = ""
    sections: dict[int, list[ProblemRecord]] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return float(raw)


def normalize_path(path_text: str) -> Path:
    path_text = path_text.strip().strip('"')
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path


def default_targets() -> list[Path]:
    return [
        HOMEWORK_DIR / f"2402 - OOP - 上机{i} - Lancer.md"
        for i in range(2, 6)
    ]


def parse_type_ordinals(values: list[str] | None) -> list[int]:
    if not values:
        return list(SECTION_ORDER)

    aliases: dict[str, int] = {}
    for ordinal, (problem_type, section_name) in TYPE_BY_ORDINAL.items():
        aliases[str(ordinal)] = ordinal
        aliases[f"x={ordinal}"] = ordinal
        aliases[f"type/{ordinal}"] = ordinal
        aliases[problem_type.lower()] = ordinal
        aliases[section_name.lower()] = ordinal

    output: list[int] = []
    for raw_value in values:
        for token in re.split(r"[,，\s]+", raw_value.strip()):
            if not token:
                continue
            normalized = token.lower()
            ordinal = aliases.get(normalized)
            if ordinal is None and normalized.isdigit():
                ordinal = int(normalized)
            if ordinal not in TYPE_BY_ORDINAL:
                valid = ", ".join(str(item) for item in SECTION_ORDER)
                raise PintiaError(f"unknown type {token!r}; valid type ordinals are {valid}")
            if ordinal not in output:
                output.append(ordinal)
    return output or list(SECTION_ORDER)


def is_full_type_selection(ordinals: list[int]) -> bool:
    return set(ordinals) == set(SECTION_ORDER)


def load_manual_answers(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("answers"), dict):
        data = data["answers"]
    if not isinstance(data, dict):
        raise PintiaError(f"{path} must contain a JSON object")
    return {str(key): value for key, value in data.items()}


def lookup_manual_answer(manual_answers: dict[str, Any], problem: dict[str, Any]) -> Any:
    keys = [
        str(problem.get("id") or ""),
        str(problem.get("problemSetProblemId") or ""),
        str(problem.get("problemId") or ""),
        normalize_markdown(problem.get("title")).strip(),
    ]
    for key in keys:
        if not key:
            continue
        value = manual_answers.get(key)
        if isinstance(value, dict) and "answers" in value:
            return value.get("answers")
        if value not in (None, "", []):
            return value
    return None


def parse_target_file(path: Path) -> TargetFile:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(?P<yaml>.*?)\n---\s*(?P<body>.*)\Z", text, re.S)
    if not match:
        raise PintiaError(f"{path} does not contain YAML front matter")

    front_matter = match.group("yaml").strip()
    body = match.group("body")
    link_match = re.search(r"(?m)^link:\s*(?P<link>\S+)\s*$", front_matter)
    if not link_match:
        raise PintiaError(f"{path} front matter does not contain link")

    link = link_match.group("link")
    problem_set_match = re.search(r"/problem-sets/(?P<id>\d+)/", link)
    if not problem_set_match:
        raise PintiaError(f"cannot parse problem set id from {link}")

    title_match = re.search(r"(?m)^###\s+(?P<title>.+?)\s*$", body)
    title = title_match.group("title").strip() if title_match else path.stem

    return TargetFile(
        path=path,
        front_matter=front_matter,
        title=title,
        link=link,
        problem_set_id=problem_set_match.group("id"),
    )


def parse_ordinal_from_link(link: str) -> int:
    match = re.search(r"/type/(?P<ordinal>\d+)", link)
    return int(match.group("ordinal")) if match else 0


def slug_for_target(path: Path) -> str:
    return re.sub(r"\s+", "", path.stem)


def safe_filename(name: str, fallback: str) -> str:
    name = name.strip() or fallback
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    return name[:120] or fallback


def compact_blank_lines(lines: list[str]) -> list[str]:
    compacted: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            compacted.append(line.rstrip())
        else:
            blank_count += 1
            if blank_count <= 2:
                compacted.append("")
    while compacted and not compacted[-1].strip():
        compacted.pop()
    return compacted


def normalize_markdown(text: Any) -> str:
    if text is None:
        return ""
    if not isinstance(text, str):
        return json.dumps(text, ensure_ascii=False, indent=2)

    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    # Pintia normally stores Markdown. Convert obvious HTML blocks, but do not
    # treat C/C++ tokens such as <iostream> or <class T> as HTML.
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    html_like = re.search(
        r"</?(?:p|div|span|img|a|strong|em|ul|ol|li|table|thead|tbody|tr|td|th|pre|code|h[1-6])\b[^>]*>",
        text,
        flags=re.I,
    )
    if html_like and "```" not in text:
        text = html_to_markdown(
            text,
            heading_style="ATX",
            escape_asterisks=False,
            escape_underscores=False,
            escape_misc=False,
        ).strip()
    for escaped, plain in {
        r"\*": "*",
        r"\[": "[",
        r"\]": "]",
        r"\_": "_",
    }.items():
        text = text.replace(escaped, plain)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def indent_block(text: str, prefix: str = "   ") -> list[str]:
    if not text.strip():
        return []
    return [prefix + line if line else "" for line in text.splitlines()]


def first_line_and_rest(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip():
            return line.strip(), "\n".join(lines[i + 1 :]).strip()
    return "", ""


def strip_duplicate_title(problem: dict[str, Any], text: str) -> str:
    title = normalize_markdown(problem.get("title")).strip()
    if title and text.strip() == title:
        return title
    return text


def suppress_duplicate_body_title(problem: dict[str, Any], text: str) -> str:
    title = normalize_markdown(problem.get("title")).strip()
    return "" if title and text.strip() == title else text


def find_nested(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = find_nested(value, key)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_nested(value, key)
            if found is not None:
                return found
    return None


def collect_problem_list(obj: Any) -> list[dict[str, Any]]:
    preferred = find_nested(obj, "problemSetProblems")
    if isinstance(preferred, list):
        return [item for item in preferred if isinstance(item, dict) and "id" in item]

    found: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if "id" in value and "type" in value and ("content" in value or "problemConfig" in value):
                found.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return unique_by_id(found)


def unique_by_id(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []
    for item in items:
        item_id = str(item.get("id") or item.get("problemSetProblemId") or "")
        if not item_id or item_id in seen:
            continue
        seen.add(item_id)
        output.append(item)
    return output


def unwrap_detail(data: Any, problem_id: str) -> dict[str, Any]:
    for key in ("problemSetProblem", "problem", "examProblem"):
        value = find_nested(data, key)
        if isinstance(value, dict) and str(value.get("id")) == str(problem_id):
            return value

    problems = collect_problem_list(data)
    for problem in problems:
        if str(problem.get("id")) == str(problem_id):
            return problem
    return {}


def normalize_choice_answer(answer: Any) -> str:
    if answer is None:
        return ""
    if isinstance(answer, list):
        return "".join(normalize_choice_answer(item) for item in answer)
    answer_text = str(answer).strip()
    if not answer_text or answer_text in {"NO_CHOICE_ANSWER", "NO_TRUE_OR_FALSE_ANSWER"}:
        return ""
    if answer_text.isdigit():
        index = int(answer_text)
        if 0 <= index < len(CHOICE_LETTERS):
            return CHOICE_LETTERS[index]
    if answer_text.upper() == "TRUE":
        return "T"
    if answer_text.upper() == "FALSE":
        return "F"
    return answer_text.upper()


def extract_submission_answer(detail: Any, problem_type: str) -> Any:
    if not isinstance(detail, dict):
        return None
    if problem_type == "TRUE_OR_FALSE":
        return normalize_choice_answer((find_nested(detail, "trueOrFalseSubmissionDetail") or {}).get("answer"))
    if problem_type == "MULTIPLE_CHOICE":
        return normalize_choice_answer((find_nested(detail, "multipleChoiceSubmissionDetail") or {}).get("answer"))
    if problem_type == "FILL_IN_THE_BLANK":
        return (find_nested(detail, "fillInTheBlankSubmissionDetail") or {}).get("answers")
    if problem_type == "FILL_IN_THE_BLANK_FOR_PROGRAMMING":
        return (find_nested(detail, "fillInTheBlankForProgrammingSubmissionDetail") or {}).get("answers")
    if problem_type == "CODE_COMPLETION":
        return (find_nested(detail, "codeCompletionSubmissionDetail") or {}).get("program")
    if problem_type == "PROGRAMMING":
        return (find_nested(detail, "programmingSubmissionDetail") or {}).get("program")
    if problem_type == "SQL_PROGRAMMING":
        return (find_nested(detail, "sqlProgrammingSubmissionDetail") or {}).get("program")
    if problem_type == "SUBJECTIVE":
        return (find_nested(detail, "subjectiveSubmissionDetail") or {}).get("answer")
    return None


def judge_config_answer(problem: dict[str, Any]) -> Any:
    problem_type = str(problem.get("type") or "")
    judge_config = problem.get("judgeConfig")
    if not isinstance(judge_config, dict):
        return None

    if problem_type == "TRUE_OR_FALSE":
        return normalize_choice_answer((judge_config.get("trueOrFalseJudgeConfig") or {}).get("answer"))
    if problem_type == "MULTIPLE_CHOICE":
        return normalize_choice_answer((judge_config.get("multipleChoiceJudgeConfig") or {}).get("answer"))
    if problem_type == "FILL_IN_THE_BLANK":
        answers = []
        for blank in (judge_config.get("fillInTheBlankJudgeConfig") or {}).get("answers", []) or []:
            available = blank.get("availableAnswers") if isinstance(blank, dict) else None
            if isinstance(available, list):
                answers.append(" | ".join(str(item) for item in available))
        return answers or None
    if problem_type == "FILL_IN_THE_BLANK_FOR_PROGRAMMING":
        return (judge_config.get("fillInTheBlankForProgrammingJudgeConfig") or {}).get("answers")
    if problem_type == "CODE_COMPLETION":
        return (judge_config.get("codeCompletionJudgeConfig") or {}).get("answer")
    if problem_type == "PROGRAMMING":
        return (judge_config.get("programmingJudgeConfig") or {}).get("answer")
    if problem_type == "SUBJECTIVE":
        return None
    return None


def collect_detail_map(data: Any) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    judge_by_id: dict[str, dict[str, Any]] = {}
    top_status = find_submission_status(data)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            problem_id = value.get("problemSetProblemId")
            if problem_id and any(key.endswith("SubmissionDetail") for key in value):
                details[str(problem_id)] = dict(value)
            if problem_id and ("status" in value or "score" in value):
                judge_by_id[str(problem_id)] = dict(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(data)

    if top_status in ACCEPTED_STATUSES:
        for detail in details.values():
            detail.setdefault("status", top_status)

    for problem_id, judge in judge_by_id.items():
        if problem_id in details:
            details[problem_id]["__judgeResponseContent"] = dict(judge)
    if top_status and len(details) == 1:
        only_detail = next(iter(details.values()))
        only_detail.setdefault("status", top_status)
    return details


def find_submission_status(data: Any) -> str:
    if isinstance(data, dict):
        if "submissionDetails" in data and data.get("status"):
            return str(data.get("status"))
        if "lastSubmissionDetail" in data and data.get("status"):
            return str(data.get("status"))
        for value in data.values():
            status = find_submission_status(value)
            if status:
                return status
    elif isinstance(data, list):
        for value in data:
            status = find_submission_status(value)
            if status:
                return status
    return ""


def collect_standard_answer_map(data: Any, problems: list[dict[str, Any]]) -> dict[str, Any]:
    answer_map: dict[str, Any] = {}
    detail_map = collect_detail_map(data)
    for problem_id, detail in detail_map.items():
        problem_type = str((detail.get("problemType") or "")).strip()
        if not problem_type:
            problem = next((item for item in problems if str(item.get("id")) == problem_id), None)
            problem_type = str((problem or {}).get("type") or "")
        answer = extract_submission_answer(detail, problem_type)
        if answer not in (None, "", []):
            answer_map[problem_id] = answer
    return answer_map


def is_accepted_submission(detail: dict[str, Any], problem: dict[str, Any]) -> bool:
    judge = detail.get("__judgeResponseContent") if isinstance(detail, dict) else None
    status_candidates = [
        detail.get("status"),
        detail.get("problemSubmissionStatus"),
        judge.get("status") if isinstance(judge, dict) else None,
        judge.get("problemSubmissionStatus") if isinstance(judge, dict) else None,
    ]
    if any(status in ACCEPTED_STATUSES for status in status_candidates):
        return True

    if isinstance(judge, dict):
        score = judge.get("score")
        full_score = judge.get("totalScore") or judge.get("fullScore") or problem.get("score")
        try:
            return score is not None and full_score is not None and float(score) >= float(full_score)
        except (TypeError, ValueError):
            return False
    return False


def get_choices(problem: dict[str, Any]) -> list[str]:
    config = problem.get("problemConfig") or {}
    choice_config = (
        config.get("multipleChoiceProblemConfig")
        or config.get("multipleChoiceMoreThanOneAnswerProblemConfig")
        or {}
    )
    choices = choice_config.get("choices") or []
    output: list[str] = []
    for choice in choices:
        if isinstance(choice, str):
            output.append(normalize_markdown(choice))
        elif isinstance(choice, dict):
            value = (
                choice.get("content")
                or choice.get("description")
                or choice.get("text")
                or choice.get("label")
                or choice.get("value")
            )
            output.append(normalize_markdown(value))
        else:
            output.append(str(choice))
    return output


def get_raw_description(problem: dict[str, Any]) -> Any:
    return (
        problem.get("description")
        or problem.get("content")
        or problem.get("title")
        or ""
    )


def get_description(problem: dict[str, Any]) -> str:
    text = normalize_markdown(get_raw_description(problem))
    return strip_duplicate_title(problem, text)


def get_problem_title(problem: dict[str, Any], fallback_index: int) -> str:
    title = normalize_markdown(problem.get("title")).strip()
    if title:
        return title.replace("\n", " ")
    stem, _ = first_line_and_rest(get_description(problem))
    return stem or f"题目{fallback_index}"


def get_blank_config(problem: dict[str, Any], ordinal: int) -> dict[str, Any]:
    config = problem.get("problemConfig") or {}
    keys = []
    if ordinal == 4:
        keys.append("fillInTheBlankProblemConfig")
    if ordinal == 5:
        keys.append("fillInTheBlankForProgrammingProblemConfig")
    keys.extend(["fillInTheBlankProblemConfig", "fillInTheBlankForProgrammingProblemConfig"])
    for key in keys:
        value = config.get(key)
        if isinstance(value, dict):
            return value
    return {}


def format_blank_score(score: Any) -> str:
    if score in (None, ""):
        return "?分"
    try:
        value = float(score)
    except (TypeError, ValueError):
        text = str(score).strip()
        return text if text.endswith("分") else f"{text}分"
    if value.is_integer():
        return f"{int(value)}分"
    return f"{value:g}分"


def blank_scores(problem: dict[str, Any], blank_config: dict[str, Any], count: int) -> list[Any]:
    scores = blank_config.get("scores")
    if isinstance(scores, list) and scores:
        return scores
    try:
        total = float(problem.get("score"))
    except (TypeError, ValueError):
        return []
    return [total / count for _ in range(count)] if count else []


def answer_item_to_text(answer: Any) -> str:
    if answer in (None, ""):
        return "待补"
    if isinstance(answer, list):
        text = " | ".join(answer_item_to_text(item) for item in answer)
    else:
        text = normalize_markdown(answer)
    text = text.strip() or "待补"
    return text.replace("*/", "* /")


def answer_sequence(answer: Any) -> list[str]:
    if answer in (None, "", []):
        return []
    if isinstance(answer, list):
        return [answer_item_to_text(item) for item in answer]
    return [answer_item_to_text(answer)]


def blank_comments(problem: dict[str, Any], answer: Any, ordinal: int) -> tuple[list[dict[str, Any]], list[str]]:
    blank_config = get_blank_config(problem, ordinal)
    blanks = blank_config.get("blanks")
    blank_items = [item for item in blanks if isinstance(item, dict)] if isinstance(blanks, list) else []
    answers = answer_sequence(answer)
    count = max(len(blank_items), len(answers))
    scores = blank_scores(problem, blank_config, count)
    comments: list[str] = []
    for index in range(count):
        answer_text = answers[index] if index < len(answers) else "待补"
        score_text = format_blank_score(scores[index] if index < len(scores) else None)
        comments.append(f"/*（{answer_text}）（{score_text}）*/")
    return blank_items, comments


def append_unplaced_blank_comments(text: str, comments: list[str]) -> str:
    if not comments:
        return text
    suffix = ["", "待填空："]
    suffix.extend(f"{index}. {comment}" for index, comment in enumerate(comments, 1))
    return text.rstrip() + "\n" + "\n".join(suffix) + "\n"


def description_with_blank_comments(problem: dict[str, Any], answer: Any, ordinal: int) -> str:
    raw = get_raw_description(problem)
    text = raw if isinstance(raw, str) else json.dumps(raw, ensure_ascii=False, indent=2)
    blank_items, comments = blank_comments(problem, answer, ordinal)
    if not comments:
        return strip_duplicate_title(problem, normalize_markdown(text))

    pending: list[tuple[int, str]] = []
    indexed_blanks: list[tuple[int, int, str]] = []
    for index, blank in enumerate(blank_items):
        comment = comments[index] if index < len(comments) else ""
        try:
            position = int(blank.get("index"))
        except (TypeError, ValueError):
            pending.append((index, comment))
            continue
        if 0 <= position <= len(text):
            indexed_blanks.append((index, position, comment))
        else:
            pending.append((index, comment))

    for _, position, comment in sorted(indexed_blanks, key=lambda item: item[1], reverse=True):
        text = text[:position] + comment + text[position:]

    if len(comments) > len(blank_items):
        pending.extend((index, comments[index]) for index in range(len(blank_items), len(comments)))
    if pending:
        ordered = [comment for _, comment in sorted(pending, key=lambda item: item[0]) if comment]
        text = append_unplaced_blank_comments(text, ordered)
    return strip_duplicate_title(problem, normalize_markdown(text))


def example_test_datas(problem: dict[str, Any]) -> list[dict[str, Any]]:
    config = problem.get("problemConfig") or {}
    for key in (
        "programmingProblemConfig",
        "codeCompletionProblemConfig",
        "fillInTheBlankForProgrammingProblemConfig",
        "sqlProgrammingProblemConfig",
    ):
        problem_config = config.get(key)
        if isinstance(problem_config, dict) and isinstance(problem_config.get("exampleTestDatas"), list):
            return problem_config["exampleTestDatas"]
    return []


def fenced_block(lang: str, content: Any) -> list[str]:
    text = "" if content is None else str(content).rstrip()
    return [f"```{lang}", text, "```"]


def flatten_inner_headings(text: str) -> str:
    """Convert headings embedded inside a problem body into bold labels."""
    output: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            output.append(line)
            continue
        label = match.group(2).strip()
        label = re.sub(r"^\*\*(.*?)\*\*$", r"\1", label)
        output.append(f"**{label}**")
    return "\n".join(output)


class AssetStore:
    def __init__(self, client: "PintiaClient | None", markdown_path: Path) -> None:
        self.client = client
        self.markdown_path = markdown_path
        self.asset_dir = HOMEWORK_DIR / "image" / slug_for_target(markdown_path)
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.url_to_relative: dict[str, str] = {}
        self.counter = 0

    async def rewrite_markdown_images(self, markdown: str) -> str:
        if not markdown:
            return markdown

        pattern = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
        parts: list[str] = []
        last = 0
        for match in pattern.finditer(markdown):
            parts.append(markdown[last : match.start()])
            alt = match.group("alt")
            src = match.group("src")
            local_src = await self.download(src)
            parts.append(f"![{alt}]({local_src})")
            last = match.end()
        parts.append(markdown[last:])
        return "".join(parts)

    async def download(self, src: str) -> str:
        absolute = urljoin("https://pintia.cn/", src)
        if src.startswith("~/"):
            absolute = "https://images.ptausercontent.com/" + src[2:]
        elif re.fullmatch(r"[\w-]+\.(?:png|jpe?g|gif|webp|svg)", src, re.I):
            absolute = "https://images.ptausercontent.com/" + src
        if absolute in self.url_to_relative:
            return self.url_to_relative[absolute]

        parsed = urlparse(absolute)
        filename = safe_filename(Path(parsed.path).name, f"asset-{self.counter}.bin")
        if "." not in filename:
            filename += ".bin"

        target = self.asset_dir / filename
        if target.exists():
            relative = "./" + target.relative_to(self.markdown_path.parent).as_posix()
            self.url_to_relative[absolute] = relative
            return relative

        if self.client is None or self.client.context is None:
            print(f"[warn] image is not local and --from-raw cannot download it: {src}", file=sys.stderr)
            self.url_to_relative[absolute] = src
            return src

        data, content_type = await self.client.download_bytes(absolute)
        if target.suffix == ".bin":
            ext = {
                "image/png": ".png",
                "image/jpeg": ".jpg",
                "image/gif": ".gif",
                "image/webp": ".webp",
                "image/svg+xml": ".svg",
            }.get(content_type.split(";")[0].lower(), ".bin")
            target = target.with_suffix(ext)

        target.write_bytes(data)
        relative = "./" + target.relative_to(self.markdown_path.parent).as_posix()
        self.url_to_relative[absolute] = relative
        return relative


class PintiaClient:
    def __init__(self) -> None:
        self.playwright = None
        self.context = None
        self.page: Page | None = None
        self.delay = env_float("PINTIA_FETCH_DELAY_SECONDS", 0.35)
        self.exam_ids_by_problem_set: dict[str, str] = {}
        self.api_headers: dict[str, str] = {}
        self.api_cache: list[dict[str, Any]] = []

    async def __aenter__(self) -> "PintiaClient":
        channel = os.getenv("PINTIA_BROWSER_CHANNEL", "chrome").strip() or "chrome"
        chrome_path = os.getenv("PINTIA_CHROME_PATH", "").strip()
        headless = env_bool("PINTIA_HEADLESS", False)
        user_data_dir = normalize_path(os.getenv("PINTIA_USER_DATA_DIR", ".playwright-chrome-profile"))
        user_data_dir.mkdir(parents=True, exist_ok=True)

        if "edge" in channel.lower() or "edge" in chrome_path.lower():
            raise PintiaError("Chrome is required; Edge is not allowed for this crawler.")

        self.playwright = await async_playwright().start()
        launch_kwargs: dict[str, Any] = {
            "headless": headless,
            "accept_downloads": True,
            "viewport": {"width": 1440, "height": 1000},
        }
        if chrome_path:
            launch_kwargs["executable_path"] = chrome_path
        else:
            launch_kwargs["channel"] = channel

        self.context = await self.playwright.chromium.launch_persistent_context(
            str(user_data_dir),
            **launch_kwargs,
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        self.page.on("request", self.capture_request)
        self.page.on("response", lambda response: asyncio.create_task(self.capture_response(response)))
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()

    async def api_get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.page:
            raise PintiaError("client is not started")

        url = self.build_url(path, params)
        await asyncio.sleep(self.delay)
        try:
            payload = await self.page.evaluate(
                """async (url) => {
                    const extraHeaders = window.__PINTIA_CAPTURED_HEADERS__ || {};
                    const response = await fetch(url, {
                        method: 'GET',
                        credentials: 'include',
                        headers: {
                            ...extraHeaders,
                            accept: 'application/json,text/plain,*/*',
                        },
                    });
                    const text = await response.text();
                    return {
                        ok: response.ok,
                        status: response.status,
                        statusText: response.statusText,
                        text,
                    };
                }""",
                url,
            )
        except PlaywrightError as exc:
            raise PintiaError(f"request failed for {url}: {exc}") from exc
        data = self.parse_response_text(payload.get("text", ""))
        status = int(payload.get("status") or 0)
        if status in {401, 403}:
            cached = self.find_cached_response(url)
            if cached is not None:
                return cached
            raise PermissionNeeded(self.extract_error_message(data) or f"permission denied for {url}")
        if status >= 400:
            cached = self.find_cached_response(url)
            if cached is not None:
                return cached
            raise PintiaError(self.extract_error_message(data) or f"GET {url} failed with {status}")
        self.remember_exam_id_from_url(url)
        self.remember_api_cache(url, status, data)
        return data

    async def try_api_get(self, path: str, params: dict[str, Any] | None = None) -> Any | None:
        try:
            return await self.api_get(path, params)
        except PermissionNeeded:
            print(f"[warn] optional API has no permission: {path}", file=sys.stderr)
            return None
        except PintiaError as exc:
            print(f"[warn] skip API {path}: {exc}", file=sys.stderr)
            return None

    async def download_bytes(self, url: str) -> tuple[bytes, str]:
        if not self.context:
            raise PintiaError("client is not started")
        response = await self.context.request.get(url, timeout=30_000)
        if response.status >= 400:
            # Some Pintia Markdown stores root-relative image URLs that are served by the static host.
            parsed = urlparse(url)
            fallback = urlunparse(("https", "static-hs.pintia.cn", parsed.path, "", parsed.query, ""))
            response = await self.context.request.get(fallback, timeout=30_000)
        if response.status >= 400:
            raise PintiaError(f"failed to download image {url}: {response.status}")
        content_type = response.headers.get("content-type", "")
        return await response.body(), content_type

    async def ensure_permission(self, target: TargetFile) -> None:
        if not self.page:
            raise PintiaError("browser page is not available")

        await self.open_problem_page(target)
        try:
            await self.probe_access(target)
            return
        except PermissionNeeded:
            if not env_bool("PINTIA_PAUSE_FOR_LOGIN", True):
                raise

        print("\nPintia requires login or permission refresh.")
        print("A Chrome window has been opened. Log in there; the crawler will continue automatically.")
        wait_seconds = int(env_float("PINTIA_LOGIN_WAIT_SECONDS", 300))
        deadline = time.time() + wait_seconds
        last_error = "Permission Denied"
        while time.time() < deadline:
            await asyncio.sleep(5)
            try:
                await self.open_problem_page(target)
                await self.probe_access(target)
                print("[info] Pintia permission confirmed; continuing crawl")
                return
            except PermissionNeeded as exc:
                last_error = str(exc)
        raise PermissionNeeded(f"{last_error}; login wait timed out after {wait_seconds}s")

    async def open_problem_page(self, target: TargetFile) -> None:
        if not self.page:
            raise PintiaError("browser page is not available")
        await self.page.goto(target.link, wait_until="domcontentloaded")
        await self.page.wait_for_timeout(int(env_float("PINTIA_PAGE_SETTLE_SECONDS", 3) * 1000))
        await self.wait_for_exam_id(target.problem_set_id, timeout_seconds=12)

    async def open_problem_type_page(self, problem_set_id: str, ordinal: int) -> None:
        if not self.page:
            raise PintiaError("browser page is not available")
        url = f"https://pintia.cn/problem-sets/{problem_set_id}/exam/problems/type/{ordinal}"
        await self.page.goto(url, wait_until="domcontentloaded")
        await self.page.wait_for_timeout(int(env_float("PINTIA_PAGE_SETTLE_SECONDS", 3) * 1000))
        await self.wait_for_exam_id(problem_set_id, timeout_seconds=8)

    async def probe_access(self, target: TargetFile) -> None:
        ordinal = parse_ordinal_from_link(target.link)
        probe_ordinals = [ordinal] if ordinal in TYPE_BY_ORDINAL else []
        probe_ordinals.extend(item for item in SECTION_ORDER if item not in probe_ordinals)
        exam_id = self.exam_ids_by_problem_set.get(target.problem_set_id, "")
        last_permission_error: PermissionNeeded | None = None
        last_other_error: PintiaError | None = None
        for probe_ordinal in probe_ordinals:
            problem_type, _ = TYPE_BY_ORDINAL[probe_ordinal]
            params = {"problem_type": problem_type}
            if exam_id:
                params["exam_id"] = exam_id
            try:
                await self.api_get(f"/api/problem-sets/{target.problem_set_id}/exam-problems", params)
                return
            except PermissionNeeded as exc:
                last_permission_error = exc
            except PintiaError as exc:
                last_other_error = exc
        if last_permission_error:
            raise last_permission_error
        if last_other_error:
            raise last_other_error
        raise PermissionNeeded("Permission Denied")

    async def wait_for_exam_id(self, problem_set_id: str, timeout_seconds: int) -> str:
        if self.exam_ids_by_problem_set.get(problem_set_id):
            return self.exam_ids_by_problem_set[problem_set_id]
        if not self.page:
            return ""
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            await asyncio.sleep(0.5)
            urls = await self.page.evaluate(
                """() => performance
                    .getEntriesByType('resource')
                    .map((entry) => entry.name)
                    .filter(Boolean)"""
            )
            for url in urls:
                self.remember_exam_id_from_url(url)
            if self.exam_ids_by_problem_set.get(problem_set_id):
                return self.exam_ids_by_problem_set[problem_set_id]
        return ""

    def capture_request(self, request: Request) -> None:
        url = request.url
        self.remember_exam_id_from_url(url)
        if "/api/" not in url:
            return
        headers = request.headers
        captured: dict[str, str] = {}
        for key, value in headers.items():
            low_key = key.lower()
            if low_key in {
                "accept",
                "content-type",
                "x-requested-with",
            } or low_key.startswith(("x-", "pc-", "pta-")):
                captured[key] = value
        if captured:
            self.api_headers.update(captured)
            if self.page:
                asyncio.create_task(self.publish_captured_headers())

    async def publish_captured_headers(self) -> None:
        if not self.page:
            return
        try:
            await self.page.evaluate(
                "(headers) => { window.__PINTIA_CAPTURED_HEADERS__ = headers; }",
                self.api_headers,
            )
        except PlaywrightError:
            return

    async def capture_response(self, response: Response) -> None:
        url = response.url
        self.remember_exam_id_from_url(url)
        if "/api/" not in url:
            return
        content_type = response.headers.get("content-type", "")
        if "json" not in content_type and "text" not in content_type:
            return
        try:
            text = await response.text()
        except PlaywrightError:
            return
        data = self.parse_response_text(text)
        self.remember_api_cache(url, response.status, data)

    def remember_api_cache(self, url: str, status: int, data: Any) -> None:
        self.api_cache.append({"url": url, "status": status, "data": data, "time": time.time()})
        if len(self.api_cache) > 500:
            self.api_cache = self.api_cache[-500:]

    def find_cached_response(self, requested_url: str) -> Any | None:
        requested = urlparse(requested_url)
        requested_query = dict(parse_qsl(requested.query))
        for item in reversed(self.api_cache):
            if int(item.get("status") or 0) >= 400:
                continue
            cached_url = str(item.get("url") or "")
            cached = urlparse(cached_url)
            if cached.scheme != requested.scheme or cached.netloc != requested.netloc:
                continue
            if cached.path != requested.path:
                continue
            cached_query = dict(parse_qsl(cached.query))
            if all(cached_query.get(key) == value for key, value in requested_query.items()):
                return item.get("data")
        return None

    def remember_exam_id_from_url(self, url: str) -> None:
        try:
            parsed = urlparse(url)
            match = re.search(r"/api/problem-sets/(?P<problem_set_id>\d+)/exam-problems", parsed.path)
            if not match:
                return
            query = dict(parse_qsl(parsed.query))
            exam_id = query.get("exam_id") or query.get("examId")
            if exam_id:
                self.exam_ids_by_problem_set[match.group("problem_set_id")] = exam_id
        except Exception:
            return

    @staticmethod
    def build_url(path: str, params: dict[str, Any] | None = None) -> str:
        url = urljoin("https://pintia.cn/", path)
        if params:
            cleaned = {
                key: value
                for key, value in params.items()
                if value is not None and value != ""
            }
            if cleaned:
                parsed = urlparse(url)
                query = dict(parse_qsl(parsed.query))
                query.update({key: str(value) for key, value in cleaned.items()})
                url = urlunparse(parsed._replace(query=urlencode(query)))
        return url

    @staticmethod
    def parse_response_text(text: str) -> Any:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text

    @staticmethod
    def extract_error_message(payload: Any) -> str:
        if isinstance(payload, dict):
            error = payload.get("error")
            if isinstance(error, dict):
                return str(error.get("message") or error.get("code") or "")
            return str(payload.get("message") or "")
        return ""


async def get_exam_id(client: PintiaClient, problem_set_id: str) -> tuple[str, Any]:
    captured_exam_id = client.exam_ids_by_problem_set.get(problem_set_id, "")
    if captured_exam_id:
        return captured_exam_id, {"source": "captured-from-page-network", "exam_id": captured_exam_id}

    try:
        data = await client.api_get(f"/api/problem-sets/{problem_set_id}/exams")
    except PermissionNeeded as exc:
        print(f"[warn] cannot read /exams for problem set {problem_set_id}: {exc}")
        return "", {"error": str(exc)}
    exam = None
    if isinstance(data, dict):
        for key in ("exam", "problemSetExam"):
            if isinstance(data.get(key), dict):
                exam = data[key]
                break
        if exam is None:
            exams = data.get("exams") or data.get("problemSetExams")
            if isinstance(exams, list) and exams:
                exam = exams[0]
    elif isinstance(data, list) and data:
        exam = data[0]
    exam_id = str((exam or {}).get("id") or "")
    if not exam_id:
        # Some endpoints accept an empty exam id after the exam has ended.
        print(f"[warn] exam id not found for problem set {problem_set_id}; trying type endpoints without it")
    return exam_id, data


async def fetch_problem_type(
    client: PintiaClient,
    problem_set_id: str,
    exam_id: str,
    problem_type: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ordinal = ORDINAL_BY_TYPE.get(problem_type)
    if ordinal and env_bool("PINTIA_NAVIGATE_EACH_TYPE", True):
        await client.open_problem_type_page(problem_set_id, ordinal)
        exam_id = exam_id or client.exam_ids_by_problem_set.get(problem_set_id, "")

    params = {"problem_type": problem_type}
    if exam_id:
        params["exam_id"] = exam_id
    data = await client.try_api_get(f"/api/problem-sets/{problem_set_id}/exam-problems", params)
    if data is None and exam_id:
        data = await client.try_api_get(
            f"/api/problem-sets/{problem_set_id}/exam-problems",
            {"problem_type": problem_type},
        )
    if data is None:
        return [], {"list": None}

    problems = collect_problem_list(data)
    details: list[dict[str, Any]] = []
    for problem in problems:
        problem_id = str(problem.get("id") or "")
        detail_data = await client.try_api_get(f"/api/problem-sets/{problem_set_id}/exam-problems/{problem_id}")
        detail = unwrap_detail(detail_data, problem_id) if detail_data else {}
        merged = dict(problem)
        merged.update(detail)
        details.append(merged)

    raw: dict[str, Any] = {"list": data}
    standard_data = await client.try_api_get(
        f"/api/problem-sets/{problem_set_id}/standard-answers",
        {"problem_type": problem_type},
    )
    if standard_data is None:
        standard_data = await client.try_api_get(
            f"/api/problem-sets/{problem_set_id}/preview/standard-answers",
            {"problem_type": problem_type},
        )
    raw["standard_answers"] = standard_data

    last_submission_data = None
    if exam_id:
        last_submission_data = await client.try_api_get(
            f"/api/exams/{exam_id}/problem-sets/{problem_set_id}/last-submissions",
            {"problem_type": problem_type},
        )
    if last_submission_data is None:
        last_submission_data = await client.try_api_get(
            f"/api/problem-sets/{problem_set_id}/last-submissions",
            {"problem_type": problem_type},
        )
    raw["last_submissions"] = last_submission_data

    if problem_type in {"CODE_COMPLETION", "PROGRAMMING", "SUBJECTIVE", "SQL_PROGRAMMING"}:
        raw["per_problem_last_submissions"] = {}
        raw["per_problem_standard_answers"] = {}
        for problem in details:
            problem_id = str(problem.get("id") or "")
            if not problem_id:
                continue
            raw["per_problem_last_submissions"][problem_id] = await client.try_api_get(
                f"/api/problem-sets/{problem_set_id}/last-submissions",
                {"problem_type": problem_type, "problem_set_problem_id": problem_id},
            )
            standard_detail = await client.try_api_get(
                f"/api/problem-sets/{problem_set_id}/problems/{problem_id}/standard-answer"
            )
            if standard_detail is None:
                standard_detail = await client.try_api_get(
                    f"/api/problem-sets/{problem_set_id}/preview/problems/{problem_id}/standard-answer"
                )
            raw["per_problem_standard_answers"][problem_id] = standard_detail
    return details, raw


def build_problem_records(
    problems: list[dict[str, Any]],
    raw: dict[str, Any],
    problem_type: str,
    manual_answers: dict[str, Any],
) -> list[ProblemRecord]:
    standard_map = collect_standard_answer_map(raw.get("standard_answers"), problems)
    for per_problem_id, per_standard in (raw.get("per_problem_standard_answers") or {}).items():
        per_map = collect_standard_answer_map(per_standard, problems)
        if per_map:
            standard_map.update(per_map)
        else:
            problem = next((item for item in problems if str(item.get("id")) == str(per_problem_id)), None)
            if problem:
                direct_answer = extract_submission_answer(per_standard, str(problem.get("type") or ""))
                if direct_answer not in (None, "", []):
                    standard_map[str(per_problem_id)] = direct_answer

    submission_map = collect_detail_map(raw.get("last_submissions"))
    for per_problem_id, per_submission in (raw.get("per_problem_last_submissions") or {}).items():
        per_map = collect_detail_map(per_submission)
        if per_map:
            submission_map.update(per_map)
        else:
            problem = next((item for item in problems if str(item.get("id")) == str(per_problem_id)), None)
            if problem:
                answer = extract_submission_answer(per_submission, str(problem.get("type") or ""))
                if answer not in (None, "", []):
                    submission_map[str(per_problem_id)] = {
                        "problemSetProblemId": str(per_problem_id),
                        "status": find_submission_status(per_submission),
                        "__directAnswer": answer,
                    }

    records: list[ProblemRecord] = []
    for problem in problems:
        problem_id = str(problem.get("id") or "")
        answer = standard_map.get(problem_id)
        answer_source = "standard-answer" if answer not in (None, "", []) else ""
        if answer in (None, "", []):
            answer = judge_config_answer(problem)
            answer_source = "judge-config" if answer not in (None, "", []) else ""
        detail = submission_map.get(problem_id)
        accepted = bool(detail and is_accepted_submission(detail, problem))
        if answer in (None, "", []) and detail and accepted:
            answer = detail.get("__directAnswer") or extract_submission_answer(detail, problem_type)
            answer_source = "accepted-last-submission" if answer not in (None, "", []) else ""
        if answer in (None, "", []):
            answer = lookup_manual_answer(manual_answers, problem)
            answer_source = "manual-answers" if answer not in (None, "", []) else ""
        records.append(
            ProblemRecord(
                problem=problem,
                answer=answer,
                answer_source=answer_source,
                last_submission_detail=detail,
                accepted=accepted,
            )
        )
    return records


async def crawl_target(
    client: PintiaClient,
    target: TargetFile,
    type_ordinals: list[int],
    manual_answers: dict[str, Any],
) -> CrawlResult:
    await client.ensure_permission(target)
    exam_id, exams_raw = await get_exam_id(client, target.problem_set_id)
    problem_set_raw = await client.try_api_get(f"/api/problem-sets/{target.problem_set_id}") or {}
    result = CrawlResult(
        target=target,
        exam_id=exam_id,
        problem_set=problem_set_raw if isinstance(problem_set_raw, dict) else {},
        raw={"exams": exams_raw, "problem_set": problem_set_raw, "sections": {}},
    )

    for ordinal in type_ordinals:
        problem_type, _ = TYPE_BY_ORDINAL[ordinal]
        print(f"[info] {target.path.name}: fetching {ordinal} {problem_type}")
        problems, raw = await fetch_problem_type(client, target.problem_set_id, exam_id, problem_type)
        if not problems:
            continue

        records = build_problem_records(problems, raw, problem_type, manual_answers)
        result.sections[ordinal] = records
        result.raw["sections"][str(ordinal)] = raw
    return result


def build_result_from_raw(
    target: TargetFile,
    type_ordinals: list[int],
    manual_answers: dict[str, Any],
) -> CrawlResult:
    raw_path = RAW_DIR / f"{slug_for_target(target.path)}.json"
    if not raw_path.exists():
        raise PintiaError(f"raw JSON not found: {raw_path}")
    raw_payload = json.loads(raw_path.read_text(encoding="utf-8"))
    if not isinstance(raw_payload, dict):
        raise PintiaError(f"raw JSON root must be an object: {raw_path}")

    result = CrawlResult(
        target=target,
        exam_id=str(find_nested(raw_payload.get("exams"), "id") or ""),
        problem_set=raw_payload.get("problem_set") if isinstance(raw_payload.get("problem_set"), dict) else {},
        raw=raw_payload,
    )

    raw_sections = raw_payload.get("sections") or {}
    if not isinstance(raw_sections, dict):
        raise PintiaError(f"raw JSON sections must be an object: {raw_path}")

    for ordinal in type_ordinals:
        problem_type, _ = TYPE_BY_ORDINAL[ordinal]
        section_raw = raw_sections.get(str(ordinal))
        if not isinstance(section_raw, dict):
            print(f"[warn] {raw_path.name}: raw section type {ordinal} is missing", file=sys.stderr)
            continue
        problems = collect_problem_list(section_raw.get("list"))
        if not problems:
            print(f"[warn] {raw_path.name}: raw section type {ordinal} has no problems", file=sys.stderr)
            continue
        result.sections[ordinal] = build_problem_records(problems, section_raw, problem_type, manual_answers)
    return result


class MarkdownRenderer:
    def __init__(self, result: CrawlResult, client: PintiaClient | None, section_order: list[int] | None = None) -> None:
        self.result = result
        self.asset_store = AssetStore(client, result.target.path)
        self.section_order = section_order or list(SECTION_ORDER)

    async def render(self) -> str:
        lines: list[str] = [
            "---",
            self.result.target.front_matter,
            "---",
            f"### {self.result.target.title}",
            "",
            "------",
            "",
        ]

        for ordinal in self.section_order:
            records = self.result.sections.get(ordinal) or []
            if not records:
                continue
            lines.extend(await self.render_section_lines(ordinal, records))

        return "\n".join(compact_blank_lines(lines)) + "\n"

    async def render_sections(self) -> dict[int, str]:
        blocks: dict[int, str] = {}
        for ordinal in self.section_order:
            records = self.result.sections.get(ordinal) or []
            if not records:
                continue
            lines = await self.render_section_lines(ordinal, records)
            blocks[ordinal] = "\n".join(compact_blank_lines(lines)) + "\n"
        return blocks

    async def render_section_lines(self, ordinal: int, records: list[ProblemRecord]) -> list[str]:
        _, section_name = TYPE_BY_ORDINAL[ordinal]
        lines = [f"#### {section_name}", ""]
        if ordinal == 1:
            lines.extend(await self.render_true_or_false(records))
        elif ordinal == 2:
            lines.extend(await self.render_multiple_choice(records))
        elif ordinal in {4, 5}:
            lines.extend(await self.render_fill_blanks(records, ordinal))
        else:
            lines.extend(await self.render_coding_or_subjective(records, ordinal))
        lines.extend(["", "------", ""])
        return lines

    async def render_true_or_false(self, records: list[ProblemRecord]) -> list[str]:
        lines: list[str] = []
        for index, record in enumerate(records, 1):
            description = await self.clean_content(get_description(record.problem))
            stem, rest = first_line_and_rest(description)
            answer = normalize_choice_answer(record.answer)
            suffix = f"({answer})" if answer else "()"
            lines.append(f"{index}. {stem}{suffix}")
            if rest:
                lines.extend(indent_block(rest))
        return lines

    async def render_multiple_choice(self, records: list[ProblemRecord]) -> list[str]:
        lines: list[str] = []
        for index, record in enumerate(records, 1):
            problem = record.problem
            description = await self.clean_content(get_description(problem))
            stem, rest = first_line_and_rest(description)
            answer = normalize_choice_answer(record.answer)
            suffix = f"（{answer}）" if answer else "（ ）"
            lines.append(f"{index}. {stem}{suffix}")
            if rest:
                lines.append("")
                lines.extend(indent_block(rest))
            choices = get_choices(problem)
            for choice_index, choice in enumerate(choices):
                letter = CHOICE_LETTERS[choice_index]
                choice_md = await self.clean_content(choice)
                option_lines = choice_md.splitlines() or [""]
                option_head = f"{letter}. {option_lines[0]}".rstrip()
                if answer and letter in answer:
                    option_head = f"**{option_head}**"
                lines.append("")
                lines.append(f"   {option_head}")
                if len(option_lines) > 1:
                    lines.append("")
                    lines.extend(indent_block("\n".join(option_lines[1:])))
            lines.append("")
        return lines

    async def render_fill_blanks(self, records: list[ProblemRecord], ordinal: int) -> list[str]:
        lines: list[str] = []
        for index, record in enumerate(records, 1):
            description = await self.clean_content(
                description_with_blank_comments(record.problem, record.answer, ordinal)
            )
            title = get_problem_title(record.problem, index)
            if len(records) > 1:
                lines.append(f"{index}.{title}")
                lines.append("")
            description = suppress_duplicate_body_title(record.problem, description)
            description = flatten_inner_headings(description)
            if description:
                lines.extend(description.splitlines())
                lines.append("")
        return lines

    async def render_coding_or_subjective(self, records: list[ProblemRecord], ordinal: int) -> list[str]:
        lines: list[str] = []
        for index, record in enumerate(records, 1):
            problem = record.problem
            title = get_problem_title(problem, index)
            lines.append(f"##### {index}.{title}")
            lines.append("")

            description = await self.clean_content(get_description(problem))
            description = suppress_duplicate_body_title(problem, description)
            description = flatten_inner_headings(description)
            if description:
                lines.extend(description.splitlines())
                lines.append("")

            if "输入样例" not in description and "输出样例" not in description:
                examples = example_test_datas(problem)
                for example_index, example in enumerate(examples, 1):
                    suffix = f" {example_index}" if len(examples) > 1 else ""
                    if example.get("input") is not None:
                        lines.append(f"**输入样例{suffix}:**")
                        lines.append("")
                        lines.extend(fenced_block("in", example.get("input")))
                        lines.append("")
                    if example.get("output") is not None:
                        lines.append(f"**输出样例{suffix}:**")
                        lines.append("")
                        lines.extend(fenced_block("out", example.get("output")))
                        lines.append("")

            code = record.answer if isinstance(record.answer, str) else ""
            if code.strip():
                language = "c++"
                if str(problem.get("compiler") or "").upper() in {"GCC", "MODERN_GCC", "CLANG"}:
                    language = "c"
                lines.extend(["**code:**", ""])
                lines.extend(fenced_block(language, code))
                lines.append("")
            elif ordinal == 8:
                answer_lines = self.render_answer_list(record.answer)
                if answer_lines:
                    lines.extend(["**answer:**", ""])
                    lines.extend(answer_lines)
                    lines.append("")
        return lines

    def render_answer_list(self, answer: Any) -> list[str]:
        if answer in (None, "", []):
            return []
        if isinstance(answer, list):
            output: list[str] = []
            for index, item in enumerate(answer, 1):
                item_text = normalize_markdown(item)
                if "\n" in item_text:
                    output.append(f"{index}.")
                    output.extend(fenced_block("", item_text))
                else:
                    output.append(f"{index}. {item_text}")
            return output
        answer_text = normalize_markdown(answer)
        if "\n" in answer_text:
            return fenced_block("", answer_text)
        return [answer_text]

    async def clean_content(self, text: str) -> str:
        text = normalize_markdown(text)
        text = await self.asset_store.rewrite_markdown_images(text)
        return text.strip()


def save_raw(result: CrawlResult, merge_existing: bool = False) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output = RAW_DIR / f"{slug_for_target(result.target.path)}.json"
    payload = result.raw
    if merge_existing and output.exists():
        try:
            existing = json.loads(output.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if isinstance(existing, dict):
            sections = existing.setdefault("sections", {})
            if isinstance(sections, dict):
                sections.update(payload.get("sections") or {})
            for key in ("exams", "problem_set"):
                if payload.get(key) not in (None, {}, []):
                    existing[key] = payload[key]
            payload = existing
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def merge_markdown_sections(existing_markdown: str, section_blocks: dict[int, str]) -> str:
    merged = existing_markdown.rstrip() + "\n"
    for ordinal in SECTION_ORDER:
        block = section_blocks.get(ordinal)
        if not block:
            continue
        _, section_name = TYPE_BY_ORDINAL[ordinal]
        pattern = re.compile(
            rf"(?ms)^####\s*{re.escape(section_name)}\s*\n.*?^------\s*(?:\n|$)"
        )
        replacement = block.rstrip() + "\n\n"
        if pattern.search(merged):
            merged = pattern.sub(replacement, merged, count=1)
        else:
            merged = merged.rstrip() + "\n\n" + replacement
    return merged.rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl Pintia homework pages into local Markdown files.")
    parser.add_argument(
        "--targets",
        nargs="*",
        help="Markdown target files. Defaults to homework 上机2 through 上机5.",
    )
    parser.add_argument(
        "--types",
        "--type",
        nargs="*",
        dest="types",
        help="Problem type ordinals or names to fetch/render, for example: --types 5 or --types 4,5.",
    )
    parser.add_argument(
        "--manual-answers",
        help=f"JSON fallback answer file. Defaults to {DEFAULT_MANUAL_ANSWERS.relative_to(ROOT)} if it exists.",
    )
    parser.add_argument(
        "--from-raw",
        action="store_true",
        help="Render Markdown from homework/pintia_raw without opening Chrome or calling Pintia.",
    )
    parser.add_argument("--no-write", action="store_true", help="Fetch and save raw JSON without rewriting Markdown.")
    parser.add_argument("--no-raw", action="store_true", help="Do not save raw API JSON.")
    return parser.parse_args()


async def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    load_dotenv(ROOT / ".env.local")
    args = parse_args()
    targets = [normalize_path(item) for item in args.targets] if args.targets else default_targets()
    target_files = [parse_target_file(path) for path in targets]
    type_ordinals = parse_type_ordinals(args.types)
    full_type_selection = is_full_type_selection(type_ordinals)
    manual_answers_path = normalize_path(args.manual_answers) if args.manual_answers else DEFAULT_MANUAL_ANSWERS
    manual_answers = load_manual_answers(manual_answers_path)

    started = time.time()
    if args.from_raw:
        for target in target_files:
            type_text = ",".join(str(item) for item in type_ordinals)
            print(f"[info] rendering {target.path.name} from raw; types={type_text}")
            result = build_result_from_raw(target, type_ordinals, manual_answers)
            if not args.no_write and env_bool("PINTIA_OVERWRITE_MARKDOWN", True):
                renderer = MarkdownRenderer(result, None, type_ordinals)
                if full_type_selection:
                    markdown = await renderer.render()
                else:
                    section_blocks = await renderer.render_sections()
                    markdown = merge_markdown_sections(target.path.read_text(encoding="utf-8"), section_blocks)
                target.path.write_text(markdown, encoding="utf-8")
                print(f"[info] wrote {target.path}")
            else:
                print(f"[info] skipped Markdown write for {target.path.name}")
        elapsed = time.time() - started
        print(f"[done] finished in {elapsed:.1f}s")
        return 0

    async with PintiaClient() as client:
        for target in target_files:
            type_text = ",".join(str(item) for item in type_ordinals)
            print(f"[info] crawling {target.path.name}; types={type_text}")
            result = await crawl_target(client, target, type_ordinals, manual_answers)
            if env_bool("PINTIA_SAVE_RAW", True) and not args.no_raw:
                save_raw(result, merge_existing=not full_type_selection)
            if not args.no_write and env_bool("PINTIA_OVERWRITE_MARKDOWN", True):
                renderer = MarkdownRenderer(result, client, type_ordinals)
                if full_type_selection:
                    markdown = await renderer.render()
                else:
                    section_blocks = await renderer.render_sections()
                    markdown = merge_markdown_sections(target.path.read_text(encoding="utf-8"), section_blocks)
                target.path.write_text(markdown, encoding="utf-8")
                print(f"[info] wrote {target.path}")
            else:
                print(f"[info] skipped Markdown write for {target.path.name}")

    elapsed = time.time() - started
    print(f"[done] finished in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except PintiaError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)
