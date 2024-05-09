from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import os
import json


def save_json(data, json_name):
    with open(json_name, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
        # data：字典的数据
        # fp：保存的文本
        # encoding="utf-8"：使中文能够显示出来，不至于乱码
        # ensure_ascii：保证了 “篮球” 能正确的写入，而不是字节形式
        # indent=4：为了美观，不然会保存成一行

if __name__ == "__main__":
    root_dir = "/root/data/zalando/train/"
    images = os.listdir(root_dir + "/cloth/")

    # 要嵌入的JSON数据
    const_prompt="""{
        "version": "0.0.1",
        "conversations":[
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
            "value": "请问这件衣服是什么风格？T恤、衬衣、礼服、婚纱、或者其他？"
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
            "value": "<answer7>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式为我创建一个数据集:\n {json_string} \n要求：根据提供的图片,按json_string的格式生成问题和答案对。答案要必须精简，不要啰嗦废话，后面有选项的在选项中选即可。保证答案正确，不能瞎编，必须严格来源于图像内容中，如果图像没有，请回答不知道即可。最后只需要输出生成的json_string部分即可，不需要其他多余的部分。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=10240))

    for image in images:
        prompts = [('%s'%prompt, load_image(root_dir + "/cloth/" + image))]
        response = pipe(prompts)

        # print(response[0].text[7:-3])
        try:
            json_obj = json.loads(response[0].text[7:-3])
            json_name =  root_dir + "/json/"  + image[:-4]+".json"
            save_json(json_obj, json_name)
        except json.decoder.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))    