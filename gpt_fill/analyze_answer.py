import json

with open("answer-rating.json", encoding="utf-8") as f:
    RATING_TABLE = json.load(f)
def print_question_ratings(data: dict,do_print=0):
    """
    功能：
    1. 打印每个问题的答案 + 理由 + North America 评级（已优化）
    2. 自动统计 North America 最高年龄
    3. 返回所有导致这个最高年龄的「问题 + 选项」列表
    """
    if do_print:
        print("=" * 90)
        print("North America 评级分析".center(80))
        print("=" * 90)

    max_age = 0
    culprits = []  # 记录所有导致最高年龄的选项

    for qid, info in data["answers"].items():
        answer = info["answer"]
        reason = info.get("reason", "(无理由)")
        if do_print:
            print(f"\n{qid}")
            print(f"   答案: {answer}")
            print(f"   理由: {reason}")

        if answer is None:
            if do_print:
                print("   → 条件跳转，未显示，无影响")
            continue

        found = False
        for category in RATING_TABLE:
            if qid in RATING_TABLE[category]:
                table = RATING_TABLE[category][qid]

                current_q_max = 0
                current_culprits = []

                # 单选题
                if isinstance(answer, str):
                    if answer in table:
                        age = table[answer]["regions"]["North America"]
                        if do_print:
                            print(f"       North America : {age}+")
                        current_q_max = age
                        current_culprits = [answer]
                    else:
                        if do_print:
                            print(f"   → 错误：单选答案 '{answer}' 未匹配！")
                        continue

                # 多选题
                elif isinstance(answer, list):
                    if not answer:
                        if do_print:
                            print("   → 多选但未勾选 → 无影响")
                        continue
                    if do_print:
                        print(f"   → 多选题（{len(answer)}项）：")
                    for opt in answer:
                        if opt in table:
                            age = table[opt]["regions"]["North America"]
                            if do_print:
                                print(f"       {opt} → North America: {age}+")
                            if age > current_q_max:
                                current_q_max = age
                                current_culprits = [opt]
                            elif age == current_q_max:
                                current_culprits.append(opt)
                        else:
                            print(f"       ✗ 错误：选项 '{opt}' 未匹配！")

                found = True

                # 更新全局最高年龄和罪魁祸首
                if current_q_max > max_age:
                    max_age = current_q_max
                    culprits = [(qid, culprit) for culprit in current_culprits]
                elif current_q_max == max_age:
                    culprits.extend((qid, culprit) for culprit in current_culprits)

                break

        if not found:
            print(f"   警告：问题ID '{qid}' 在 answer-rating.json 中找不到！")

    # ========= 最终结果输出 =========
    print("\n" + "=" * 90)
    if max_age == 0:
        print("恭喜！North America 可评 0+（Everyone）".center(80))
    else:
        print(f"North America 最终评级：{max_age}+".center(80))
        print(f"导致该评级的选项共有 {len(culprits)} 个：".center(80))
        for i, (qid, option) in enumerate(culprits, 1):
            print(f"   {i}. {qid} → {option}")
    print("=" * 90)

    # 返回所有导致最高评级的 (问题ID, 选项) 元组列表
    return max_age, culprits



app_names=['com.brainy.prankster.puzzle', 'com.gtsy.annoying.punch.game', 'com.money.run.hypercasual3d', 'com.playflix.kick.breakragdoll.games',  'com.uc.minigame.relax', 'com.rhythmdance.taptile.dancingcats', 'io.gartic.Gartic']
# app_name="com.playflix.kick.breakragdoll.games"
app_name=app_names[3]
print(app_name)
with open(f"./gpt_output/{app_name}_analyzed.json", "r", encoding="utf-8") as f:
    data = json.load(f)
final_age, reasons = print_question_ratings(data)

import pandas as pd


df = pd.read_csv("merged.csv", encoding="utf-8")
result = df[df["app_Id"] == app_name]
if not result.empty:
    rating = result.iloc[0]["contentRating"]              # 比如 ESRB: Teen
    desc   = result.iloc[0]["contentRatingDescription"]   # 描述文字
    print(f"google play 中的rating与summary:")
    print(f"评级: {rating}")
    print(f"描述: {desc}")
else:
    print(f"没找到APP: {app_name}")

