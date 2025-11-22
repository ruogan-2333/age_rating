F:.
├─get_question_json
│  │  csv_loader.py            加载 CSV 文件
│  │  exam.py                  验证 LLM 生成的 JSON 与 CSV 字段对应关系
│  │  fear.json                LLM 生成的 fear 问卷 JSON 文件
│  │  fear_mapping.csv         本地 fear 问卷填写数据
│  │  json_loader.py           加载 JSON 文件
│  │
│  ├─games                     游戏类问卷填写数据
│  ├─others                    其他类问卷填写数据
│  └─social_apps               社交类问卷填写数据
│
├─gpt_fill
│  │  analyze_answer.py        使用 LLM 分析截图填写问卷，输出 JSON
│  │  answer-rating.json       选项到年龄评级的映射规则（解析 GPT 输出用）
│  │  gpt_get_answer.py        分析 GPT 输出的 JSON 填写结果
│  │  merged.csv               APP 元数据及评论统计信息
│  │
│  ├─all_screenshot            APP 截图（按包名划分）
│  ├─gpt_output                GPT 输出的问卷 JSON 结果
│  │      com.brainy.prankster.puzzle_analyzed.json
│  │
│  └─question                  问卷定义文件
│          fear.json
│          violence.json
│
└─rules_generate
    │  answer-rating.json          游戏问卷规则映射（选项→年龄评级）
    │  get_answer-rating.py        生成 answer-rating.json 的脚本
    │  get_summary-rating.py       生成 ALL_RATING_RULES.json 的脚本
    │  PART1_ALL_RATING_RULES.json 汇总规则示例（暂未使用）
    │  PART1_选项树状结构图_North_America.txt 北美问卷选项树结构
    │  rating.py                   获取各地区年龄评级工具代码
    │
    ├─questionnaire                问卷数据
    └─region_ratings               各地区评级结果

---

如果需要，我也可以直接导出到 Markdown 文件给你使用。要不要我顺便补上一级标题或项目简介？
