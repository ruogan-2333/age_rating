import pandas as pd
import os
import re
from collections import defaultdict

# 修改路径（和之前一样）
data_dir = "./region_ratings"
modules = ['controlled', 'crude', 'digital', 'fear', 'gambling', 'language', 'misc', 'sexuality', 'violence']


def extract_age(rating_str):
    if pd.isna(rating_str):
        return None
    s = str(rating_str).strip()
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    lower = s.lower()
    if any(k in lower for k in ["teen", "mature", "pg-13", "t "]):
        return 13
    if any(k in lower for k in ["restricted", "18", "adult", "ao", "18+"]):
        return 18
    if "everyone 10" in lower or "10+" in lower:
        return 10
    return None


# 用来收集：地区 → {原始评级文本 : 出现次数}
region_ratings = defaultdict(lambda: defaultdict(int))

print("正在扫描所有评级文件...\n")

for module in modules:
    r_file = os.path.join(data_dir, f"region_ratings_1_{module}.csv")
    if not os.path.exists(r_file):
        continue

    try:
        df = pd.read_csv(r_file, encoding='gbk')  # 中文 CSV 用 gbk
    except:
        df = pd.read_csv(r_file, encoding='utf-8')

    for _, row in df.iterrows():
        info = str(row['rating_info'])
        lines = info.split('\n')
        if not lines:
            continue
        region = lines[0].strip() or "未知地区"

        rating = "未知分级"
        for line in lines:
            if line.strip().startswith("Rating:"):
                rating = line.split("Rating:", 1)[1].strip()
                break

        if rating and rating != "未知分级":
            region_ratings[region][rating] += 1

# 输出结果（按地区排序）
output = {}
for region in sorted(region_ratings.keys()):
    ratings_list = []
    for rating_text, count in sorted(region_ratings[region].items(), key=lambda x: x[1], reverse=True):
        age = extract_age(rating_text)
        ratings_list.append({
            "rating": rating_text,
            "count": count,
            "parsed_age": age
        })
    output[region] = ratings_list

# 控制台漂亮打印
print("=" * 80)
print("所有地区及其出现过的评级（带解析年龄）")
print("=" * 80)
for region, ratings in output.items():
    print(f"\n【{region}】 共出现 {sum(r['count'] for r in ratings)} 次")
    for item in ratings:
        age_str = f"{item['parsed_age']}岁" if item['parsed_age'] is not None else "无法解析"
        print(f"   → {item['rating']:<30} (出现 {item['count']:>3} 次) → {age_str}")

# 同时保存为 JSON 方便以后查
import json

with open(os.path.join(data_dir, "ALL_REGIONS_RATING_LIST.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n\n已保存详细列表到：ALL_REGIONS_RATING_LIST.json")
print("=" * 80)