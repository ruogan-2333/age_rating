# age_rating

文件结构:
F:.
├─get_question_json
│  │  csv_loader.py-->加载csv文件脚本
│  │  exam.py	-->验证json文件(LLM生成)是否能和csv文件逐个字段对应
│  │  fear.json	-->LLM生成的fear部分的json问卷文件
│  │  fear_mapping.csv-->本地的fear部分的问卷填写数据
│  │  json_loader.py	-->加载json文件脚本
│  │
│  ├─games	-->问卷填写数据,游戏部分问卷
│  │
│  ├─others	-->问卷填写数据,其他部分问卷
│  │
│  └─social_apps-->问卷填写数据,社交部分问卷
│
├─gpt_fill
│  │  analyze_answer.py-->使用LLM分析图片填写问卷,结果保存在本地json文件中.
│  │  answer-rating.json-->规则json文件,每个选项映射到年龄评级.在这部分代码中用于分析gpt返回的json
│  │  gpt_get_answer.py-->分析gpt返回的json文件
│  │  merged.csv	-->app以及metadata信息,包含"问题评论"数量
│  │
│  ├─all_screenshot-->文件夹里是app使用截图,用包名做文件夹名字.
│  ├─gpt_output	-->gpt返回的json
│  │      com.brainy.prankster.puzzle_analyzed.json
│  │
│  └─question	-->问卷,暂时就整理出这俩.
│          fear.json
│          violence.json
│
└─rules_generate	-->分析填写的问卷数据,生成规则
    │  answer-rating.json		-->每个问题选项到年龄评级的映射(只包括游戏问卷,不包括社交和其他问卷.)
    │  get_answer-rating.py		-->获取answer-rating的代码
    │  get_summary-rating.py	-->获取ALL_RATING_RULES.json的代码
    │  PART1_ALL_RATING_RULES.json	-->summary规则的映射,暂时没啥用
    │  PART1_选项树状结构图_North_America.txt	
    │  rating.py				-->获取各个地区年龄评级的代码.工具代码
    ├─questionnaire		-->问卷数据
    └─region_ratings		-->问卷的评级结果数据
