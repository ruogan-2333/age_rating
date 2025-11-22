## age_rating

####  get_question_json

- 获取json格式问卷

| 文件/目录          | 功能说明                                 |
| ------------------ | ---------------------------------------- |
| `csv_loader.py`    | 加载 CSV 数据文件                        |
| `json_loader.py`   | 加载 JSON 问卷文件                       |
| `exam.py`          | 验证 LLM 生成的 JSON 是否与 CSV 字段一致 |
| `fear.json`        | LLM 生成的 fear 问卷 JSON 结构           |
| `fear_mapping.csv` | fear 问卷对应的本地填写样本数据          |
| `games/`           | 游戏类问卷填写数据                       |
| `others/`          | 其他类型问卷填写数据                     |
| `social_apps/`     | 社交类问卷填写数据                       |

#### gpt_fill

- 利用 LLM 分析应用截图填写问卷，并解析输出。

| 文件/目录            | 功能说明                               |
| -------------------- | -------------------------------------- |
| `analyze_answer.py`  | 解析截图内容并生成问卷 JSON            |
| `gpt_get_answer.py`  | 处理 GPT 输出的问卷结果 JSON           |
| `answer-rating.json` | 选项到年龄评级映射规则（解析用）       |
| `merged.csv`         | APP 元数据（含评论数量等信息）         |
| `all_screenshot/`    | APP 使用截图，按包名分类存放           |
| `gpt_output/`        | GPT 自动填写问卷输出结果 JSON          |
| `question/`          | 问卷定义文件（如 fear、violence 问卷） |

#### rules_generate

- 根据填写结果生成年龄评级规则

| 文件/目录                                | 功能说明                          |
| ---------------------------------------- | --------------------------------- |
| `answer-rating.json`                     | 游戏问卷选项→年龄评级规则数据     |
| `get_answer-rating.py`                   | 生成 answer-rating.json 的脚本    |
| `get_summary-rating.py`                  | 生成 ALL_RATING_RULES.json 的脚本 |
| `PART1_ALL_RATING_RULES.json`            | 汇总规则示例（暂未使用）          |
| `PART1_选项树状结构图_North_America.txt` | 北美问卷选项结构示意              |
| `rating.py`                              | 获取不同地区年龄评级的工具脚本    |
| `questionnaire/`                         | 问卷源数据                        |
| `region_ratings/`                        | 多地区评级结果数据                |

