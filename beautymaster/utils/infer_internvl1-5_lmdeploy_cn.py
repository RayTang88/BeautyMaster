from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import os
import json
 
root_dir = "/root/data/zalando/train/cloth/"
images = os.listdir(root_dir)

# 要嵌入的JSON数据
const_prompt="""{
    "id": "<random_number_string>",
    "image": "test_img/oph.jpg",
    "conversations": [
        {
        "from": "human",
        "value": "<image>\n请问这件衣服适合什么季节穿？春、夏、秋、冬？."
        },
        {
        "from": "gpt",
        "value": "<answer1>"
        },
        {
        "from": "human",
        "value": "请问这件衣服的风格怎么样？休闲、正装、运动、或者其他？"
        },
        {
        "from": "gpt",
        "value": "<answer2>"
        },
        {
        "from": "human",
        "value": "请问这件衣服衣袖长度如何？长袖、短袖、无袖、或者其他？"
        },
        {
        "from": "gpt",
        "value": "<answer3>"
        },
        {
        "from": "human",
        "value": "请问这件衣服的衣领是什么形状？圆领、V领、或者其他？"
        },
        {
        "from": "gpt",
        "value": "<answer4>"
        },
        {
        "from": "human",
        "value": "请问这件衣服是T恤、衬衣、礼服、婚纱、或者其他？"
        },
        {
        "from": "gpt",
        "value": "<answer5>"
        },
        "from": "human",
        "value": "请问这件衣服是什么颜色？"
        },
        {
        "from": "gpt",
        "value": "<answer6>"
        },
        "from": "human",
        "value": "请问这件衣服的面料是什么？纯棉、化纤、尼龙、或者其他？"
        },
        {
        "from": "gpt",
        "value": "<answer6>"
        },
    ]
}"""

# 将JSON数据转换为字符串，并转义双引号和花括号
# json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
 
# 将转义后的JSON字符串嵌入提示中
prompt = f"按照以下格式为我创建一个数据集:\n {json_string} \n要求：根据提供的图片,按json_string的格式生成问题和答案对，答案要尽可能精简正确，不能瞎编，必须严格来源于图像内容中，如果图像没有，请回答不知道即可,最后只需要输出生成的json_string部分即可，不需要其他多余的部分。"


pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                backend_config=TurbomindEngineConfig(session_len=10240))
# pipe = pipeline('/root/model/InternVL-Chat-V1-5-Int8/',
#                 backend_config=TurbomindEngineConfig(session_len=10240))
# pipe = pipeline("/share/new_models/liuhaotian/llava-v1.6-vicuna-7b/",
#                 backend_config=TurbomindEngineConfig(session_len=8192))


for image in images:
    prompts = [('%s'%prompt, load_image(root_dir+image))]
    response = pipe(prompts)
    print(response[0].text)