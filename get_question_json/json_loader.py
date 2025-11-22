import json

# 读取最完美的 JSON 文件
with open('violence.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)  # 现在 questions 是一个 dict，不是 list！

print(f"共加载了 {len(questions)} 个问题字段\n")
print("=" * 80)

# 1. 直接通过 id 访问（最爽的一点！）
print("【1】直接用 id 取问题")
q = questions["blood_gore_level"]
print(f"问题ID      : {q}")  # 其实 key 就是 id，不用再存一份
print(f"问题内容    : {q['question']}")
print(f"类型        : {q['type']}")
print(f"所有选项    : {[opt['value'] for opt in q['options']]}")
print(f"显示条件    : {q.get('show_if')}")
print()

# 2. 批量打印所有问题（按你想要的顺序）
print("【2】按逻辑顺序打印所有问题（推荐顺序）")
ordered_ids = [
    "Gory_Images",
    "violence_content",
    "violence_setting", "violence_style", "reactions_to_violence",
    "violence_presentation", "blood_gore_level", "war_setting",
    "injury_penalties", "violent_overtones",
    "violence_setting_context", "pixelated_childlike_style",
    "reactions_to_violence_type", "violence_presentation_style",
    "blood_gore_level_associated", "creatures_human_behaviour",
    "violence_against_real_animals", "violent_overtones_present",
    "disturbing_images_explicitness", "blood_unrelated_description"
]

for qid in ordered_ids:
    q = questions[qid]
    opts = [opt['value'] for opt in q['options']]
    triggers = [opt['triggers'] for opt in q['options'] if opt['triggers']]
    trigger_info = f" → 触发: {triggers}" if triggers else ""

    print(f"{qid:35} | {q['type']:8} | {len(opts)} 个选项{trigger_info}")
print()

# 3. 快速查找某个选项会触发哪些问题
print("【3】查看某个选项会触发什么后续问题")
content_opts = questions["violence_content"]["options"]
for opt in content_opts:
    if opt["triggers"]:
        print(f"选择「{opt['value'][:50]:50}」→ 会触发问题组: {opt['triggers']}")

print()

# 4. 检查某个问题是否应该显示（模拟逻辑）
print("【4】模拟：如果用户选了 violence_content 中的第一项，应该显示哪些问题？")
selected_triggers = []
for opt in content_opts:
    if "against humans" in opt["value"]:  # 模拟用户选了这个
        if opt["triggers"]:
            selected_triggers.append(opt["triggers"])

print("触发的问题组:", selected_triggers)

print("这些问题现在应该显示：")
for qid, q in questions.items():
    show_if = q.get("show_if")
    if show_if and "triggered" in show_if:
        if show_if["triggered"] in selected_triggers:
            print(f"   → {qid}: {q['question'][:60]}...")