import openai
import base64
import os
import json
import time
start = time.perf_counter()
def images_analyze(
        image_paths: list[str],
        api_key: str = ?????,
        # model: str = "gpt-4o",
        model: str = "gpt-4o-mini",
        temperature: float = 0.2
) -> str:
    """
    看图说话 + 简要分析：输入任意图片，输出“图片里有什么 + 简要分析”

    参数同上，返回纯文本（中文，简洁清晰，带要点）
    """
    with open(r"F:\文件\年龄分级\相关资料\workplace\gpt_handler\gpt_ex\question\violence.json", encoding="utf-8") as f:
        questionnaire_json = f.read()
    # ============ 全新通用分析 prompt（已调到最优）============
    prompt = f'''
    你是一个极其严谨专业的 App 内容评级审核专家。

    原始问卷（仅用于理解问题含义，不要原样输出）：
    {questionnaire_json}

    任务：
    1. 仔细看完我上传的所有截图,根据截图里面的信息填写问卷。
    2. 严格按下面 JSON 格式输出（必须一字不差）：

    {{
      "answers": {{
        "每个问题ID": {{
          "answer": 答案（单选填字符串，多选用数组，文本填字符串，没答案填null）,
          "confidence": 0.00到1.00（保留两位小数）,
          "reason": "用一句简洁中文说明你为什么这么填（必须写，10-30字）"
        }}
        // 所有问题都要出现
      }},
      "image_analysis": {{
        "文件名1.png": "对这张图内容的简要描述（20-40字中文）",
        "文件名2.png": "对这张图内容的简要描述（20-40字中文）"
        // 每张上传的图片都要分析
      }},
      "image_files": ["实际文件名列表"],
      "overall_confidence": 0.98,
      "comment": "有必要时填中文备注，否则空字符串"
    }}

    规则：
    - reason 字段必须真实填写，不能偷懒写“明显”或“根据图片”
    - image_analysis 里的文件名必须和实际上传的一模一样（包括后缀）
    - overall_confidence = 所有 confidence 的平均值
    - 直接输出纯 JSON，开头是{{ 结尾是}}，不要任何解释、代码块、换行说明

    开始处理图片。
    '''
    # =========================================================

    client = openai.OpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }
    ]

    for path in image_paths:
        base64_image = base64.b64encode(open(path, "rb").read()).decode('utf-8')
        ext = path.lower().split(".")[-1]
        mime_type = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png",
                     "gif": "gif", "webp": "webp"}.get(ext, "jpeg")

        messages[0]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{mime_type};base64,{base64_image}"
            }
        })

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1500,
        temperature=temperature  # 0.2 让语言稍自然一点，但不乱编
    )

    return response.choices[0].message.content.strip()

folder_path=r"F:\文件\年龄分级\相关资料\workplace\gpt_handler\gpt_ex\app_screenshot"

# subfolders = [f for f in os.listdir(folder_path)
#               if os.path.isdir(os.path.join(folder_path, f))]
# print(subfolders)   # 就是所有子文件夹名字的列表

# app_names=['com.brainy.prankster.puzzle', 'com.gtsy.annoying.punch.game', 'com.money.run.hypercasual3d', 'com.playflix.kick.breakragdoll.games',  'com.uc.minigame.relax', 'com.rhythmdance.taptile.dancingcats', 'io.gartic.Gartic']
# app_names=['com.playflix.kick.breakragdoll.games',  'com.uc.minigame.relax', 'com.rhythmdance.taptile.dancingcats', 'io.gartic.Gartic']
app_names=['io.gartic.Gartic' ]
for app_name in app_names:
    path = os.path.join(folder_path, app_name)
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.png')]
    # print(image_paths)
    result = images_analyze(image_paths)
    print(result)
    data = json.loads(result)
    with open(f"{app_name}_analyzed.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# app_name="com.brainy.prankster.puzzle"
# path = os.path.join(folder_path, app_name)
# image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith('.png')]
# # print(image_paths)
# result = images_analyze(image_paths)
# print(result)
# data = json.loads(result)
# with open(f"{app_name}_analyzed.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)
end = time.perf_counter()       # 结束计时
print(f"总耗时：{end - start:.3f} 秒")
