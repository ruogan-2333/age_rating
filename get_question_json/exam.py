import json
import pandas as pd  # 强烈推荐安装 pandas，后面会用
import ast

# 比较csv数据里的问题以及选项是否能和生成的json文件匹配。

modules = ['controlled', 'crude', 'digital', 'fear', 'gambling', 'language', 'misc', 'sexuality', 'violence']
name="sexuality"
# df = pd.read_csv(f'{name}_mapping.csv')
# df = pd.read_csv(f'{name}_mapping.csv', encoding="gbk",keep_default_na=False)
df = pd.read_csv(f'{name}_mapping.csv', encoding="utf-8-sig", keep_default_na=False)



columns = df.columns.tolist()
remove_cols = ['combo_id','summary', 'country', 'rating']
columns = [col for col in columns if col not in remove_cols]
print(f"csv中{len(columns)}个问题")
with open(f'{name}.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)
print(f"json中{len(questions)} 个问题字段\n")
print(columns)
# unique_values = df["blood_gore_level_associated"].dropna().replace("", None).dropna() .unique().tolist()
# print(unique_values)



# for column in columns:
#     q=questions[column]
#     option_list = [opt["value"] for opt in q["options"]]
#     unique_values = df[column].dropna().replace("", None).dropna().unique().tolist()
#     # 转成 set 用来比较
#     json_set = set(option_list)
#     csv_set = set(unique_values)
#
#     if json_set == csv_set:
#         # print(f"✔ {column} 完全匹配")
#         continue
#     else:
#
#         print(f"❌ {column} 不匹配")
#
#         print("  - CSV 多出来的：", csv_set - json_set)
#         print("  - JSON 多出来的：", json_set - csv_set)



for column in columns:
    q = questions[column]
    option_list = [opt["value"] for opt in q["options"]]

    # --- 关键：收集所有单个选项 ---
    csv_single_values = set()

    for cell in df[column].dropna():
        cell = cell.strip()
        if cell == "":
            continue

        # 如果是列表字符串，例如 "['A','B']"
        if cell.startswith("[") and cell.endswith("]"):
            try:
                parsed_list = ast.literal_eval(cell)  # 解析成真实列表
                for item in parsed_list:
                    csv_single_values.add(item)
            except Exception:
                # 解析失败就当成普通字符串处理
                csv_single_values.add(cell)
        else:
            # 单选题，直接存
            csv_single_values.add(cell)

    # -------------------------------
    json_set = set(option_list)
    csv_set = csv_single_values
    # -------------------------------

    if json_set == csv_set:
        continue
    else:
        print(f"❌ {column} 不匹配")
        print("  - CSV 多出来的：", csv_set - json_set)
        print("  - JSON 多出来的：", json_set - csv_set)