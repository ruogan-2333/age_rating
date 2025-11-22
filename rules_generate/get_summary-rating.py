import pandas as pd
import os
import re
import json   # ← 新增这行
# 根据summary生成年龄评级规则对照的代码
# 根据实际情况修改 data_dir 路径
data_dir1 = os.path.abspath("../data/questionnaire")
data_dir = os.path.abspath("../data")
data_dir2 = os.path.abspath("../data/region_ratings")
modules = ['controlled', 'crude', 'digital', 'fear', 'gambling', 'language', 'misc', 'sexuality', 'violence']

def extract_numeric(rating_str):
    match = re.search(r'(\d+)', rating_str)
    if match:
        return int(match.group(1))
    lower = rating_str.lower()
    if "mature" in lower or "teen" in lower:
        return 13
    elif "restricted" in lower:
        return 18
    return 0

def rating_sort_key(rating):
    num = extract_numeric(rating)
    if num != 0:
        return (0, num)
    else:
        return (1, rating)

def parse_rating_info(rating_info):
    lines = rating_info.split('\n')
    region = lines[0].strip() if lines and lines[0].strip() else "未知地区"
    rating_level = "未知分级"
    organization = "未知机构"
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("Rating:"):
            rating_text = line_strip.split("Rating:", 1)[1].strip()
            num_match = re.search(r'(\d+\+?)', rating_text)
            if num_match:
                rating_level = num_match.group(1)
            else:
                rating_level = rating_text if rating_text != "" else "未知分级"
        elif line_strip.startswith("Rating authority:"):
            org_text = line_strip.split("Rating authority:", 1)[1].strip()
            organization = org_text if org_text != "" else "未知机构"
    return region, rating_level, organization

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# 我们只改这个函数：原来是画图，现在改成返回结构化数据 + 最后统一保存JSON
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
def generate_rules_json(module_name):
    print(f"[DEBUG] 正在处理模块：{module_name} ...")
    
    question_csv = os.path.join(data_dir1, f"questionnaire_results_1_{module_name}.csv")
    ratings_csv = os.path.join(data_dir2, f"region_ratings_1_{module_name}.csv")
    
    if not os.path.exists(question_csv):
        print(f"[DEBUG] 找不到文件: {question_csv}")
        return None
    if not os.path.exists(ratings_csv):
        print(f"[DEBUG] 找不到文件: {ratings_csv}")
        return None
    
    try:
        df_question = pd.read_csv(question_csv)
        df_ratings = pd.read_csv(ratings_csv)
    except Exception as e:
        print(f"[ERROR] 读取数据失败：{e}")
        return None
    
    df_question = df_question[df_question['summary'] != '提取失败']
    if df_question.empty:
        print(f"[DEBUG] 模块 {module_name} 无有效问卷数据。")
        return None
    
    df_merged = pd.merge(df_question, df_ratings, on='combo_id', how='inner')
    if df_merged.empty:
        print(f"[DEBUG] 模块 {module_name} 合并后无数据。")
        return None
    
    # ↓↓↓ 下面这整段逻辑和你原来完全一样 ↓↓↓
    mapping = {}
    organizations = {}
    exclude_factor = "App has ratings-relevant content as part of the downloaded app package"
    for _, row in df_merged.iterrows():
        try:
            rating_info = str(row['rating_info'])
            region, rating_level, organization = parse_rating_info(rating_info)
            key = (region, rating_level)
            factors = set([fact.strip() for fact in str(row['summary']).split('|') 
                           if fact.strip() and fact.strip() != exclude_factor])
            mapping[key] = mapping.get(key, set()).union(factors)
            if region not in organizations:
                organizations[region] = organization
        except Exception as e:
            print(f"[WARNING] 解析 rating_info 出错: {e}")
            continue

    region_dict = {}
    for (region, rating_level), factors in mapping.items():
        region_dict.setdefault(region, {})
        region_dict[region][rating_level] = region_dict[region].get(rating_level, set()).union(factors)
    
    # ===== 计算每个评级真正的“独特触发因素”（和原来画图一模一样）=====
    final_result_for_this_module = {}
    
    for region, ratings in region_dict.items():
        org = organizations.get(region, "未知机构")
        sorted_ratings = sorted(ratings.items(), key=lambda x: rating_sort_key(x[0]))
        
        union_lower = set()
        processed_ratings = {}
        
        for rating, fac_set in sorted_ratings:
            unique = fac_set - union_lower
            if unique:  # 只有独特因素才记录
                processed_ratings[rating] = {
                    "age": extract_numeric(rating),
                    "unique_factors": sorted(list(unique))
                }
            union_lower = union_lower.union(fac_set)
        
        if processed_ratings:
            final_result_for_this_module[region] = {
                "institution": org,
                "ratings": processed_ratings
            }
    
    return final_result_for_this_module
    # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

# ==================== 主程序：合并所有模块的结果并保存为一个大JSON ====================
all_data = {}

for module in modules:
    question_csv = os.path.join(data_dir1, f"questionnaire_results_1_{module}.csv")
    if not os.path.exists(question_csv):
        print(f"[DEBUG] 模块 {module} 的问卷 CSV 文件不存在: {question_csv}")
        continue
    
    module_result = generate_rules_json(module)
    if not module_result:
        continue
    
    print(f"模块 {module} 处理完成，包含 {len(module_result)} 个地区")
    
    # 合并到总结果（相同地区会自动合并评级）
    for region, data in module_result.items():
        if region not in all_data:
            all_data[region] = {
                "institution": data["institution"],
                "ratings": {}
            }
        # 合并 ratings（如果同地区同评级出现，会自动取并集，后续会再去重计算独特因素）
        for rating_level, info in data["ratings"].items():
            if rating_level not in all_data[region]["ratings"]:
                all_data[region]["ratings"][rating_level] = {"age": info["age"], "all_factors": set()}
            all_data[region]["ratings"][rating_level]["all_factors"].update(info["unique_factors"])

# 最后再次计算“真正独特因素”（跨所有模块后的最终版）
final_output = {}
for region, data in all_data.items():
    sorted_items = sorted(data["ratings"].items(), key=lambda x: rating_sort_key(x[0]))
    lower_union = set()
    clean_ratings = {}
    
    for rating, info in sorted_items:
        current = info["all_factors"]
        unique = current - lower_union
        if unique:
            clean_ratings[rating] = {
                "age": info["age"],
                "unique_factors": sorted(list(unique))
            }
        lower_union.update(current)
    
    if clean_ratings:
        final_output[region] = {
            "institution": data["institution"],
            "ratings": clean_ratings
        }

# 保存为 JSON 文件
output_path = os.path.join(data_dir, "PART1_ALL_RATING_RULES.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_output, f, ensure_ascii=False, indent=2, sort_keys=True)

print("\n" + "="*60)
print("全部完成！")
print(f"最终评级规则已保存为：{output_path}")
print(f"共包含 {len(final_output)} 个国家/地区")
for region in sorted(final_output.keys()):
    print(f"  • {region} ({final_output[region]['institution']}) → {len(final_output[region]['ratings'])} 个评级")
print("="*60)