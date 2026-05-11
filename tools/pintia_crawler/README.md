# Pintia 作业爬虫与 Markdown 清洗

这个目录保存 Pintia 作业抓取脚本。脚本有两种工作方式：

- 在线抓取：打开 Chrome，访问 Markdown YAML front matter 中的 `link`，抓取题目、答案、图片和原始接口数据。
- 离线清洗：只读取已经保存到 `homework/pintia_raw/` 的 JSON，重新格式化并写回 Markdown，不打开浏览器、不访问 Pintia。

## 题型映射

| `x/type` | Pintia 类型 | 本仓库章节 |
| --- | --- | --- |
| `1` | `TRUE_OR_FALSE` | 判断题 |
| `2` | `MULTIPLE_CHOICE` | 单选题 |
| `3` | 暂无 | 跳过 |
| `4` | `FILL_IN_THE_BLANK` | 填空题 |
| `5` | `FILL_IN_THE_BLANK_FOR_PROGRAMMING` | 程序填空题 |
| `6` | `CODE_COMPLETION` | 函数题 |
| `7` | `PROGRAMMING` | 编程题 |
| `8` | `SUBJECTIVE` | 主观题 |

`x=6` 到 `x=8` 会进入对应 type 页面，再按 `problemSetProblemId` 补抓题目详情。

## 安装

在仓库根目录执行：

```powershell
python -m pip install -r requirements.txt
python -m playwright install chrome
```

脚本默认使用 Chrome，不使用 Edge。`.env.local` 的常用配置：

```text
PINTIA_BROWSER_CHANNEL=chrome
PINTIA_CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
PINTIA_HEADLESS=false
PINTIA_USER_DATA_DIR=.playwright-chrome-profile
PINTIA_PAUSE_FOR_LOGIN=true
PINTIA_LOGIN_WAIT_SECONDS=300
PINTIA_PAGE_SETTLE_SECONDS=3
PINTIA_NAVIGATE_EACH_TYPE=true
```

注意：`.playwright-chrome-profile` 是脚本专用 Chrome 用户数据目录。你平时打开的 Chrome 已登录，不等于脚本窗口已登录。

## 在线抓取

抓取上机2到上机5并重写 Markdown：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py
```

只抓某一份文件：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --targets "homework\2402 - OOP - 上机2 - Lancer.md"
```

只抓指定题型：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --types 5
python tools\pintia_crawler\crawl_pintia_homework.py --types 4,5
```

按文件和按题型可以组合：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --targets "homework\2402 - OOP - 上机5 - Lancer.md" --types 5
```

只抓接口数据、不写 Markdown：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --no-write
```

## 离线清洗

如果 `homework/pintia_raw/` 已经有 JSON，可以不登录、不打开浏览器，直接用 raw 数据重新格式化 Markdown：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --from-raw --types 5
```

只清洗某一份文件的程序填空题：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --from-raw --targets "homework\2402 - OOP - 上机3 - Lancer.md" --types 5
```

只指定部分 type 时，脚本只替换对应章节，保留同一 Markdown 文件中的其他章节。

## 填空格式

填空题和程序填空题会按 Pintia `blanks[index]` 位置插入注释：

```cpp
/*（答案）（2分）*/
```

答案来源优先级：

1. 页面接口返回的标准答案。
2. 题目判题配置中的答案。
3. 整题正确的最后一次提交答案。
4. `tools/pintia_crawler/manual_answers.json` 中的手动兜底答案。

仍然找不到答案时，空白会写成：

```cpp
/*（待补）（?分）*/
```

手动答案文件按 `problemSetProblemId` 配置：

```json
{
  "answers": {
    "1917909441704636437": {
      "answers": ["<class T>", "T& ARRAY<T>"]
    }
  }
}
```

也可以指定其他答案文件：

```powershell
python tools\pintia_crawler\crawl_pintia_homework.py --manual-answers path\to\answers.json
```

## 输出

- Markdown 会保留原 YAML front matter。
- 图片会下载到 `homework/image/<文档名去空格>/`，正文使用相对路径引用。
- 原始接口数据保存到 `homework/pintia_raw/`。
- 只抓部分 type 时，raw JSON 会合并保存，避免覆盖未重新抓取的章节。
- `--from-raw` 不会下载缺失图片；如果图片文件已经在本地，则会继续改写为本地相对路径。
