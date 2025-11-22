import pandas as pd
import os
import json
import re
import ast  # 用于安全的列表字符串解析

#获取每个选项的年龄评级,保存在answer-rating.json文件中

data_dir = os.path.abspath("../data")
questionnaire_dir = './questionnaire'
ratings_dir = './region_ratings'

modules = ['controlled', 'crude', 'digital', 'fear', 'gambling', 'language', 'misc', 'sexuality', 'violence']

def extract_age(rating_str):
    if pd.isna(rating_str) or rating_str == '':
        return None
    s = str(rating_str).strip()
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    lower = s.lower()
    if any(k in lower for k in ["teen", "mature", "pg-13", "t"]):
        return 13
    if any(k in lower for k in ["restricted", "18", "adult", "ao", "18+"]):
        return 18
    if "everyone 10" in lower or "10+" in lower:
        return 10
    return None

def parse_rating_info(rating_info):
    if pd.isna(rating_info):
        return "未知地区", None
    lines = str(rating_info).split('\n')
    region = lines[0].strip() if lines else "未知地区"
    rating = "未知分级"
    for line in lines:
        if line.strip().startswith("Rating:"):
            rating = line.split("Rating:", 1)[1].strip()
            break
    return region, rating

# 最终结果（分层结构）
final_result = {}

print("开始分析各模块问卷选项（已支持多选拆分）...")

for module in modules:
    q_file = os.path.join(questionnaire_dir, f"questionnaire_results_1_{module}.csv")
    r_file = os.path.join(ratings_dir, f"region_ratings_1_{module}.csv")

    if not (os.path.exists(q_file) and os.path.exists(r_file)):
        print(f"跳过 {module}（文件缺失）")
        continue

    print(f"正在处理模块: {module}")
    df_q = pd.read_csv(q_file, encoding="gbk", keep_default_na=False)
    df_r = pd.read_csv(r_file, encoding="gbk", keep_default_na=False)
    df = pd.merge(df_q, df_r, on='combo_id', how='inner')

    module_data = {}
    question_cols = [col for col in df_q.columns if col not in ['combo_id', 'summary']]

    for col in question_cols:
        # 用来收集每个“单个选项”出现时，对应的地区最低年龄
        single_option_to_regions = {}  # "选项文本" → {region: min_age}

        for _, row in df.iterrows():
            cell_value = row[col]
            region, rating = parse_rating_info(row['rating_info'])
            age = extract_age(rating)
            if age is None:
                age = 0

            # ========== 处理多选或单选 ==========
            options_in_this_cell = []

            if pd.isna(cell_value) or cell_value == '':
                continue

            cell_str = str(cell_value).strip()

            # 情况1：是列表字符串，如 "['A', 'B']"
            if cell_str.startswith('[') and cell_str.endswith(']'):
                try:
                    option_list = ast.literal_eval(cell_str)
                    if isinstance(option_list, list):
                        options_in_this_cell = [str(opt).strip() for opt in option_list if str(opt).strip()]
                except:
                    pass  # 解析失败就当普通字符串处理

            # 情况2：不是列表，就当单个选项
            if not options_in_this_cell:
                options_in_this_cell = [cell_str] if cell_str else []

            # ========== 拆分更新 ==========
            for opt in options_in_this_cell:
                if opt not in single_option_to_regions:
                    single_option_to_regions[opt] = {}
                if region not in single_option_to_regions[opt]:
                    single_option_to_regions[opt][region] = age
                else:
                    single_option_to_regions[opt][region] = min(single_option_to_regions[opt][region], age)

        # 转为最终格式
        question_data = {}
        for opt, regions_dict in single_option_to_regions.items():
            if not opt:
                continue
            question_data[opt] = {"regions": regions_dict}

        # 按 North America 年龄排序（从高到低，更严格的排前面）
        if question_data:
            sorted_items = sorted(
                question_data.items(),
                key=lambda x: x[1]["regions"].get("North America", x[1]["regions"].get("United States", 0)),
                reverse=True
            )
            module_data[col] = dict(sorted_items)

    if module_data:
        final_result[module] = module_data

# ==================== 1. 保存完整分层 JSON ====================
json_path = os.path.join(data_dir, "answer-rating.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(final_result, f, ensure_ascii=False, indent=2, sort_keys=True)

# ==================== 2. 生成树状结构图（显示 North America 评级）===================
tree_lines = ["评级触发选项树状结构（North America 评级）", "=" * 80]

for module in sorted(final_result.keys()):
    tree_lines.append(f"\n【{module}】")
    questions = final_result[module]
    for q_idx, (question, options) in enumerate(sorted(questions.items())):
        prefix = "└── " if q_idx == len(questions) - 1 else "├── "
        tree_lines.append(f"{prefix}{question}")
        for opt_idx, (option, data) in enumerate(options.items()):
            opt_prefix = "    └── " if opt_idx == len(options) - 1 else "    ├── "

            # 优先找 North America，其次 United States，最后取第一个
            regions = data["regions"]
            na_age = regions.get("North America") or regions.get("United States")
            if na_age is None and regions:
                na_age = next(iter(regions.values()))

            age_str = f"{na_age}+" if na_age > 0 else "0（Everyone）"
            tree_lines.append(f"{opt_prefix}{option} → North America: {age_str}")

# 输出
print("\n" + "\n".join(tree_lines))

tree_path = os.path.join(data_dir, "PART1_选项树状结构图_North_America.txt")
with open(tree_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(tree_lines))

print("\n" + "="*80)
print("全部完成！多选题已完美拆分处理")
print(f"JSON 保存：{json_path}")
print(f"树状图保存：{tree_path}")
print("="*80)