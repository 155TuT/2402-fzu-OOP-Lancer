// these are for the ai api
#define CPPHTTPLIB_OPENSSL_SUPPORT
#include "httplib.h"
#include "json.hpp"
#include <windows.h>
#include <wincrypt.h>

//these are for the yaml process
#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <string>
#include <iterator>
#include <vector>
#include <algorithm>
#include <cctype>
#include <regex>
#include <ctime>
#include <iomanip>
#include <chrono>
#include <limits>

using namespace std;
using json = nlohmann::json;

bool vaildinput_yon(){
    char p;
    do {
        cin >> p;
        p = toupper(p);
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (cin.fail()) {
            cin.clear();
            cerr << "input stream error!" << endl;
        } else if (p != 'Y' && p != 'N') {
               cerr << "invalid choice, please enter y or n." << endl;
        }
    } while (p != 'Y' && p != 'N');
    return p == 'Y';
}

string loadapi() {
    try {
        ifstream config_file("config.json");
        if (!config_file.is_open()) {
            cerr << "error: can't open config.json" << endl;
            return "";
        }
        json config = json::parse(config_file);
        return config["api"]["deepseek"]["key"].get<string>();
    } catch (const exception& e) {
        cerr << "configuration read error: " << e.what() << endl;
        return "";
    }
}

string call_deepseek_api(const string& input) {
    const string api_key = loadapi();
    const string endpoint = "/v1/chat/completions";
    const string host = "api.deepseek.com";
    httplib::SSLClient client(host, 443); // https
    // 设置请求prompt
    string prompt = "I'm going to give you an article, and you need to summarize it as succinctly as possible in Chinese, in no more than 30 words, using only pure string formatting, without any emoticons:\n" + input;
    // 构造请求JSON
    json request_body = {
        {"model", "deepseek-chat"},
        {"messages", {
            {
                {"role", "user"},
                {"content", prompt}
            }
        }},
        {"temperature", 0.7},
        {"max_tokens", 2048}
    };
    // 设置请求头
    httplib::Headers headers = {
        {"Content-Type", "application/json"},
        {"Authorization", "Bearer " + api_key}
    };
    // 发送POST请求
    auto res = client.Post(
        endpoint.c_str(),
        headers,
        request_body.dump(),
        "application/json"
    );
    // 处理响应
    if (res && res->status == 200) {
        try {
            json response_json = json::parse(res->body);
            return response_json["choices"][0]["message"]["content"].get<string>();
        } catch (const std::exception& e) {
            cerr << "JSON parsing error: " << e.what() << endl;
            return "";
        }
    } else {
        if (res) cerr << "API request failed with status code: " << res->status << ", echo: " << res->body << endl;
        else cerr << "work request failed" << endl;
        return "";
    }
}

class DefaultData {
private:
    vector<string> articleTagslist;
    string articletitle;
    string filename;
    string excerpt;
    string sysdate, articledate;
    string systime, articletime;

    // 检查标签是否存在
    bool isTagExists(const json& tags, const string& new_tag) {
        auto it = find_if(tags.begin(), tags.end(), 
            [&new_tag](const json& tag) { return tag.get<string>() == new_tag; });
        return it != tags.end();
    }
public:
    DefaultData(const string& title, const string & file, const string& date, const string& time)
        : articletitle(title), filename(file), articledate(date), articletime(time) {
            if (!initTime()) cerr << "failed in loading the system time" << endl;
            else cout << "load the system time successfully" << endl;
            if (!initexcerpt()) cerr << "failed in loading the excerpt file" << endl;
            else cout << "load the generated excerpt successfully" << endl;
        } 
    ~DefaultData() {
        delete this;
    }

    /**
     * 设置文件名
     * @return 文件名
     */
    string fileName() {
        cout << "would you like to change the file name? (y/n)" << endl << "the default file name now is : " << filename << endl;
        if (vaildinput_yon()) {
            cout << "please input the file name behind :" << endl << "(file name can only consist of English or hyphen'-')" << endl;
            getline(cin, filename);
            cout << "changed the file name successfully " << endl;
        }
        return filename;
    }

    /**
     * 修改tagList并存入config.json文件
     * @param path 文件路径
     */
    void addTag(const string& new_tag, json& data) {
        if (isTagExists(data["tags"], new_tag))
            cerr << "error: '" << new_tag << "' already exists!" << endl;
        else {
            data["tags"].push_back(new_tag);
            cout << "added '" << new_tag << "' to the list." << endl;
        }
        ofstream file("config.json");
        file << data.dump(4);  // 缩进4空格
        file.close();
        return;
    }

    /**
     * 设置文章标签
     * @return 文章标签列表
     */
    vector<string>& articleTags() {
        ifstream file("config.json");
        if (!file.is_open()) {
            cerr << "failed in loading the default tags config" << endl;
            return articleTagslist;
        }
        json data = json::parse(file);
        showconfigTags(data);
        cout << "would you like to add any tag to the config? (y/n)" << endl;
        if (vaildinput_yon()) {
            cout << "please input the tag you want to add :" << endl << "(input 0 to end the adding)" << endl;
            string tag;
            while (cin >> tag && tag != "0") {
                addTag(tag, data);
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }
            showconfigTags(data);
        }
    
        cout << "which tags do you want to choose for your article?" << endl << "enter one number of the tag per line and input 0 to end the choosing" << endl;
        int i;
        while (true) {
            cin >> i;
            if (cin.fail()) {
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                cerr << "invalid input type, please enter a number." << endl;
                continue;
            }
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            if (i == 0) break;
            if (i < 1 || i > data["tags"].size()) {
                cerr << "number out of range. Valid range: 1-" 
                     << data["tags"].size() << endl;
            } else {
                articleTagslist.push_back(data["tags"][i - 1].get<string>());
                cout << "added the tag: " << data["tags"][i - 1].get<string>() << " to the article" << endl;
            }
        }
    
        return articleTagslist;
    }

    void showconfigTags(json& data) const {
        cout << "the taglist now is:" << endl;
        for (size_t i = 0; i < data["tags"].size(); i++) {
            cout << i + 1 << ". " << data["tags"][i].get<string>() << endl;
        }
        cout << "which contains " << data["tags"].size() << " tags" << endl;
    }

    /**
     * 加载预设摘要
     * @param path 文件路径
     * @return 是否加载成功
     */
    bool initexcerpt(const string& path = "excerpt.txt") {
        ifstream file(path);
        if (!file.is_open()) {
            return false;
        }
        string line;
        while (getline(file, line)) excerpt += line;
        file.close();
        return !excerpt.empty();
    }

    /**
     * 设置文章摘要
     * @note 如选择使用AI生成摘要，则调用DeepSeek API进行生成，如选择手动输入摘要，则直接使用用户输入的内容
     * @param content 文章内容
     * @return 文章摘要
     */
    string articaleExcerpt(const string& content) {
        cout << "would you like to add the excerpt? (y/n)" << endl;
        if(!vaildinput_yon()) return "";
        cout << "the default excerpt now is :" << endl << excerpt << endl << "would you like to change the excerpt? (y/n)" << endl;
        if (vaildinput_yon()) {
            cout << "then would you like to use ai to generate a new one? (y/n)" << endl;
            if (vaildinput_yon()) {
            ai:
                cout << "please wait a moment..." << endl;
                string temp = call_deepseek_api(content);
                if(temp.empty()) {
                    cerr << "failed in generating the excerpt" << endl << "would you like to try again? (y/n)" << endl;
                    if(vaildinput_yon()) {
                        goto ai;
                    } else {
                        cout << "then ";
                        goto end;
                    }
                } else {
                    cout << "generated the excerpt successfully: " << endl << temp << endl;
                    cout << "would you like to use this one? (y/n)" << endl;
                    if(vaildinput_yon()) {
                        excerpt = temp;
                        return excerpt;
                    } else {
                        cout << "then ";
                        goto end;
                    }
                }
            }
        end:
            cout << "please input the excerpt you want to change in one line:" << endl;
            getline(cin, excerpt);
            cout << "changed the excerpt successfully " << endl;
        }
        return excerpt;
    }

    /**
     * 设置文章标题
     * @return 文章标题
     */
    string articleTitle() {
        cout << "would you like to change the article title? (y/n)" << endl << "the default title now is : " << articletitle << endl;
        if (vaildinput_yon()) {
            cout << "please input the title behind :" << endl;
            getline(cin, articletitle);
            cout << "changed the title successfully " << endl;
        }
        return articletitle;
    }

    /**
     * 加载初始时间
     * @return 是否加载成功
     */
    bool initTime() {
        auto now = chrono::system_clock::now();
        time_t now_time_t = chrono::system_clock::to_time_t(now);

        std::tm* now_tm = std::localtime(&now_time_t);
        if (now_tm == nullptr) return false;

        ostringstream oss;
        oss << put_time(localtime(&now_time_t), "%Y/%m/%d %H:%M:%S");

        string formattedDateTime = oss.str();

        sysdate = formattedDateTime.substr(0, 10);
        systime = formattedDateTime.substr(11);
        return true;
    }

    /**
     * 设置文章日期
     * @return 文章日期
     */
    string articleDate() {
        cout << "would you like to change the article date? (y/n)" << endl << "the default date now is : " << articledate << endl;
        if (vaildinput_yon()) {
            cout << "then how about to use the system date? (y/n)" << endl << "the system date when you open the file is : " << sysdate << endl;
            if (vaildinput_yon()) articledate = sysdate;
            else {
                cout << "please input the date behind: (YYYY/MM/DD)" << endl;
                getline(cin, articledate);
            }
            cout << "changed the date successfully " << endl;
        }
        return articledate;
    }

    /**
     * 设置文章时间
     * @return 文章时间
     */
    string articleTime() {
        cout << "would you like to change the article time? (y/n)" << endl << "the default time now is : " << articletime << endl;
        if (vaildinput_yon()) {
            cout << "then how about to use the system time? (y/n)" << endl << "the system time when you open the file is : " << systime << endl;
            if (vaildinput_yon()) articletime = systime;
            else {
                cout << "please input the time behind: (HH:MM:SS)" << endl;
                getline(cin, articletime);
            }
            cout << "changed the time successfully " << endl;
        }
        return articletime;
    }

    /**
     * 创建封面文件夹
     * @param folder_name 文件夹名称
     */
    void createCoverFolder(const string& folder_name) {
        using namespace filesystem;
        cout << "do you need the corresponding resource folder? (y/n)" << endl;
        if (vaildinput_yon()) {
            try {
                filesystem::path target_path = "../_posts" / filesystem::path(folder_name);
        
                if (filesystem::create_directory(target_path) == 0) {
                    if (filesystem::exists(target_path)) {
                        cerr << "folder already exists : " << target_path << endl;
                        return;
                    } else {
                        cerr << "folder creation failed (Unknown cause) : " << target_path << endl;
                        return;
                    }
                }
            } catch (const exception& e) {
                cerr << "error : " << e.what() << endl;
                return;
            }
            cout << "cover folder created successfully : " << folder_name << endl;
        }
        return;
    }
    
};

class YAMLProcessor {
private:
    string articletitle; // origin title
    string outputFilename; // origin-title.md
    string linkFilename; // origin-title

    string generatedate;
    string generatetime;

    string content;
    string yamlHeader;
    string bodyContent;
    
    vector<string> tags;
    string excerpt;
    string sticky;

    // 字符串清理
    void trim(string &s) {
        s.erase(s.begin(), find_if(s.begin(), s.end(), [](int ch) {
            return !isspace(ch) && ch != '\"';
        }));
        s.erase(find_if(s.rbegin(), s.rend(), [](int ch) {
            return !isspace(ch) && ch != '\"';
        }).base(), s.end());
    }

    // 解析代码块语言
    void parseCodeBlocks() {
        regex codeBlockRegex("```([a-zA-Z+]+)");
        smatch match;
        string temp = bodyContent;

        while (regex_search(temp, match, codeBlockRegex)) {
            string lang = match[1].str();
            transform(lang.begin(), lang.end(), lang.begin(), ::toupper);
            if (lang == "CPP") lang = "C++";
            if (lang != "IN" && lang != "OUT" && lang != "ANS" && find(tags.begin(), tags.end(), lang) == tags.end()) tags.push_back(lang);
            temp = match.suffix().str();
        }
    }

    // 排除md中的一级标题 (to be improved)
    void processMarkdownTitle() {
        vector<string> h1_matches;
        regex h1_regex(R"(\n?#\s+([^\n]+))");
        
        // 第一步：查找所有一级标题
        auto h1_begin = sregex_iterator(bodyContent.begin(), bodyContent.end(), h1_regex);
        for (auto it = h1_begin; it != sregex_iterator(); it++) h1_matches.push_back((*it)[1].str());
    
        // 没有一级标题
        if (h1_matches.empty()) return;
    
        // 仅有一个一级标题
        if (h1_matches.size() == 1) {
            cout << "here find a title in the content: " << h1_matches[0] << endl;
            cout << "would you like to use this title as the article title? (y/n)" << endl;
            if (vaildinput_yon()) setTitle(h1_matches[0]);
            // 删除该一级标题
            bodyContent = regex_replace(bodyContent, h1_regex, "$1");
            return;
        }
    
        // 多个一级标题时对所有标题降级
        regex header_regex(R"((\n|^)(#{1,6})(\s+)([^\n]+))");
        sregex_iterator begin(bodyContent.begin(), bodyContent.end(), header_regex);
        sregex_iterator end;
        
        string result;
        size_t last_pos = 0;
        
        for (auto it = begin; it != end; it++) {
            // 添加非匹配部分
            result += bodyContent.substr(last_pos, it->position() - last_pos);
            
            // 处理当前匹配
            string prefix = (*it)[2];
            string text = (*it)[4];
            
            if (prefix.length() == 6) {
                result += (*it)[1].str() + "**" + text + "**";
            } else {
                result += (*it)[1].str() + string(prefix.length()+1, '#') + (*it)[3].str() + text;
            }
            
            last_pos = it->position() + it->length();
        }
        
        // 添加剩余内容
        result += bodyContent.substr(last_pos);
        bodyContent = result;
        cout << "too many first-level title were found in the text and have been automatically downgraded for you" << endl;
        return;
    }
    
public:
    YAMLProcessor() {
        system("chcp 65001 > nul"); // 设置控制台编码为UTF-8
        system("cls"); // 清屏
        cout << "welcome to the YAML front matter processor!" << endl;
        cout << "this program will help you to generate the YAML front matter for your markdown file." << endl;
        cout << "the default file to load is \"draft\"." << endl << "would you like to change file to read? (y/n)" << endl;
        setFileName(); // 设置默认文件名为draft.md
        while (vaildinput_yon()) {
            cout << "please input the file name behind:" << endl;
            cout << "notice: file name can only use English" << endl;
            string filename;
            getline(cin, filename); // 防止空格干扰
            if (!loadFile(filename + ".md")) { 
                cerr << "failed in loading this file" << endl << "are you still want to change file to read? (y/n)" << endl;
            } else {
                cout << "load the file: "<< filename << " successfully" << endl;
                setFileName(filename); // 设置文件名
                break;
            }
        }

        if(content.empty()) { // 如果没有加载文件，则使用默认文件
            if (!loadFile()) cerr << "failed in loading the origin file" << endl;
            else cout << "load the origin file successfully" << endl;
        }
        
        if (!parseHeader()) cerr << "failed in reading YAML" << endl;
        else cout << "parsed the YAML successfully" << endl;
    }
    ~YAMLProcessor() {
        delete this;
    }
    /**
     * 加载Markdown文件
     * @param path 文件路径
     * @return 是否加载成功
     */
    bool loadFile(const string &path = "draft.md") {
        ifstream file(path);
        if (!file) return false;

        stringstream buffer;
        buffer << file.rdbuf();
        content = buffer.str();
        return true;
    }

    /**
     * 解析YAML前页内容
     * @return 是否解析成功
     */
    bool parseHeader() {
        size_t first = content.find("---\n");
        size_t second = content.find("---\n", first + 4);
        if (first == string::npos || second == string::npos){
            bodyContent = content;
            return false;
        }

        yamlHeader = content.substr(first + 4, second - first - 4);
        bodyContent = content.substr(second + 4);

        // 解析标题作为输出文件名
        istringstream headerStream(yamlHeader);
        string line;
        while (getline(headerStream, line)) {
            if (line.find("title:") == 0) {
                size_t colonPos = line.find(':');
                string title = line.substr(colonPos+1);
                trim(title);
                setTitle(title);
            }
            if(line.find("date:") == 0) {
                size_t colonPos = line.find(':');
                generatedate = line.substr(colonPos + 2, 10);
                generatetime = line.substr(colonPos + 13, 8);
            }
        }
        return true;
    }

    /**
     * 设置文章标题
     * @param title 文章标题
     */
    void setTitle(const string& title) {
        articletitle = title;
        //processMarkdownTitle();
    }

    /**
     * 获取文章标题
     * @return 文章标题
     */
    string getTitle() const { return articletitle; }

    /**
     * 设置文件名
     * @param filename 文件名
     * @note 文件名会被转换为小写，并替换空格为短横线
     */
    void setFileName(const string &filename = "draft") {
        string sanitized = filename;
        replace(sanitized.begin(), sanitized.end(), ' ', '-');
        sanitized.erase(remove_if(sanitized.begin(), sanitized.end(),
            [](char c){ return !isalnum(c) && c != '_' && c != '-'; }), 
            sanitized.end());
        linkFilename = sanitized;
        outputFilename = sanitized + ".md";
    }

    /**
     * 设置文章日期
     * @param date 生成日期
     */
    void setDate(const string& date) { generatedate = date; }

    /**
     * 获取文章日期
     * @return 文章日期
     */
    string getDate() const { return generatedate; }

    /**
     * 设置文章时间
     * @param time 生成时间
     */
    void setTime(const string& time) { generatetime = time; }

    /**
     * 获取文章时间
     * @return 文章时间
     */
    string getTime() const { return generatetime; }

    /**
     * 获取文件名称
     * @return 文件名称
     */
    string getFileName() const { return linkFilename; }

    /**
     * 获取文章内容
     * @return 文章内容
     */
    string getBodyContent() const { return bodyContent; }

    /**
     * 设置文章摘要
     * @param texts 摘要文本
     */
    void setExcerpts(const string& texts) { excerpt = texts; }

    /**
     * 设置文章标签
     * @param tagList 标签数组
     */
    void setTags(const vector<string>& tagList) {
        parseCodeBlocks(); // 自动解析代码块语言
        tags.insert(tags.end(), tagList.begin(), tagList.end());
    }

    /**
     * 设置置顶等级
     * @param level 置顶等级
     */
    void setsticky(int level) {
        sticky = to_string(level); // to be improved
    }

    /**
     * 生成封面链接
     */
    inline string generateCoverURL(const string & articlename, const string & fliename = "head.webp", const string & sitename = "https://155tut.github.io/") {
        return sitename + generatedate + "/" + articlename + "/" + fliename;
    }

    /**
     * 更新YAML前页
     */
    void updateYAML() {
        stringstream newHeader;
        
        newHeader << "---\n" << "title: " << articletitle << "\n";
        
        // 添加生成时间
        newHeader << "date: " << generatedate;
        if(!generatetime.empty()) newHeader << " " << generatetime;
        newHeader << "\n";

        // 添加自定标签
        if (!tags.empty()) { 
            newHeader << "tags:";
            for (const auto &tag : tags) newHeader << "\n - " << tag;
        }

        // 添加摘要信息
        if (!excerpt.empty()) newHeader << "\nexcerpt: \"" << excerpt << "\"";

        // 添加置顶等级
        if (!sticky.empty()) newHeader << "\nsticky: " << sticky;

        // 添加封面链接
        if (!generatedate.empty()) newHeader << "\ncover: \"" << generateCoverURL(linkFilename) << "\""; 
        
        newHeader << "\n---\n";

        // 更新内容
        content = newHeader.str() + bodyContent;
    }

    /**
     * 保存文件
     */
    void saveFile() {
        using namespace filesystem;
        if (outputFilename.empty()) outputFilename = "../_posts/output.md";
        else outputFilename = "../_posts/" + outputFilename;

        filesystem::path dir = filesystem::path(outputFilename).parent_path();
        if (!dir.empty()) filesystem::create_directories(dir);

        ofstream out(outputFilename);
        out << content;
        cout << "done with: " << outputFilename << endl;
        out.close();
    }
};

int main(int argc, char* argv[]) {
    YAMLProcessor processor;
    DefaultData data(processor.getTitle(),processor.getFileName(), processor.getDate(), processor.getTime());

    processor.setTitle(data.articleTitle());
    processor.setFileName(data.fileName());
    data.createCoverFolder(processor.getFileName());
    
    processor.setDate(data.articleDate());
    processor.setTime(data.articleTime());
    processor.setTags(data.articleTags());
    processor.setExcerpts(data.articaleExcerpt(processor.getBodyContent()));

    processor.updateYAML();
    processor.saveFile();

    return 0;
}