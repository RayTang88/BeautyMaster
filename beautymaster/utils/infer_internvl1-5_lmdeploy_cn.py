from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import os
import json
from json_repair import repair_json
import random
from tqdm import tqdm 


def save_json(data, json_name):
    with open(json_name, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
        # data：字典的数据
        # fp：保存的文本
        # encoding="utf-8"：使中文能够显示出来，不至于乱码
        # ensure_ascii：保证了 “篮球” 能正确的写入，而不是字节形式
        # indent=4：为了美观，不然会保存成一行

def label_clothes(root_dir):
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
            "value": "请问这件衣服衣袖长度如何？长袖、中袖、短袖、无袖、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "请问这件衣服的衣领是什么形状？高领、圆领、V领、或者其他？"
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
            {
            "from": "human",
            "value": "请问这件衣服是什么颜色？"
            },
            {
            "from": "gpt",
            "value": "<answer6>"
            },
            {
            "from": "human",
            "value": "请问这件衣服的面料是什么？纯棉、化纤、尼龙、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer7>"
            },
            {
            "from": "human",
            "value": "请问这件衣服是什么版型？宽松、修身、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer8>"
            },
            {
            "from": "human",
            "value": "请问这件衣服适合什么性别穿？男装、女装、男女均可？"
            },
            {
            "from": "gpt",
            "value": "<answer9>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式为我创建一个数据集:\n {json_string} \n要求：根据提供的图片,按json_string的格式生成问题和答案对。答案要必须精简，不要啰嗦废话，后面有选项的在选项中选即可。保证答案正确，不能瞎编，必须严格来源于图像内容中，如果图像没有，请回答不知道即可。最后只需要输出生成的json_string部分即可，不需要其他多余的部分。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))

    images = os.listdir(root_dir + "/images/") 
    index=0
    for image in tqdm(images):
        index+=1  
        if image[-5:] == "1.jpg":
            continue

        if not os.path.exists(root_dir + "/images/" + image):
            continue

        json_path = root_dir + "/json/"
        json_name =  json_path  + image[:-4]+".json"
        if os.path.exists(json_path  + image[:-4]+".json"):
            continue

        try:
            print("index:%d:%s"%(index, root_dir + "/images/" + image))
            prompts = [('%s'%prompt, load_image(root_dir + "/images/" + image))]
            response = pipe(prompts)

            # print(response[0].text[7:-3])

            # json_obj = json.loads(response[0].text[7:-3])
            good_json_obj = repair_json(response[0].text, return_objects=True)

            if not os.path.exists(json_path):
                os.makedirs(json_path)
            
            save_json(good_json_obj, json_name)
        except Exception as e:
            print("Exception:", str(e))            

  

def label_trous(root_dir):
    # 要嵌入的JSON数据
    const_prompt="""{
        "version": "0.0.1",
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n请问这条裤子适合什么季节穿？春、夏、秋、冬？."
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "请问这条裤子的风格怎么样？牛仔裤、休闲裤、正装、运动裤、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": "请问这条裤子长度如何？长裤、短裤、超短裤、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "请问这条裤子是什么版型？宽松、修身、直通、喇叭、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            "from": "human",
            "value": "请问这条裤子是什么颜色？"
            },
            {
            "from": "gpt",
            "value": "<answer5>"
            },
            "from": "human",
            "value": "请问这条裤子的面料是什么？纯棉、化纤、尼龙、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer6>"
            },
            {
            "from": "human",
            "value": "请问这条裤子适合什么性别穿？男装、女装、男女均可？"
            },
            {
            "from": "gpt",
            "value": "<answer9>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式为我创建一个数据集:\n {json_string} \n要求：根据提供的图片,按json_string的格式生成问题和答案对。答案要必须精简，不要啰嗦废话，后面有选项的在选项中选即可。保证答案正确，不能瞎编，必须严格来源于图像内容中，如果图像没有，请回答不知道即可。最后只需要输出生成的json_string部分即可，不需要其他多余的部分。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))

    images = os.listdir(root_dir + "/images/")   
    # random.shuffle(images)

    # iamges = images[:10000]    


    for image in images:
        if image[-5:] == "1.jpg":
            continue

        if not os.path.exists(root_dir + "/images/" + image):
            continue

        json_path = root_dir + "/json/"
        if os.path.exists(json_path  + image[:-4]+".json"):
            continue

        try:
            prompts = [('%s'%prompt, load_image(root_dir + "/images/" + image))]
            response = pipe(prompts)

            # print(response[0].text[7:-3])
        
            # json_obj = json.loads(response[0].text[7:-3])
            good_json_obj = repair_json(response[0].text, return_objects=True)

            if not os.path.exists(json_path):
                os.makedirs(json_path)
            json_name =  json_path  + image[:-4]+".json"
            save_json(good_json_obj, json_name)
        except Exception as e:
            print("Exception:", str(e))            


def label_model(image_path, json_path):
    # 要嵌入的JSON数据
    const_prompt="""{
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n图中人物的头发是什么颜色？"
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "图中人物的头发长度如何？长发、短发、中长、寸头、秃头？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": "图中人物的头发的发型是什么风格？卷发、直发、大波浪、齐刘海、妹妹头？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "图中人物的体型胖瘦状况如何？肥胖、适中、清瘦？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            {
            "from": "human",
            "value": "图中人物的身高状况如何？高大、中等、矮小？"
            },
            {
            "from": "gpt",
            "value": "<answer5>"
            },
            {
            "from": "human",
            "value": "图中人物的腰部粗细如何？水桶腰、正常腰、小蛮腰？"
            },
            {
            "from": "gpt",
            "value": "<answer6>"
            },
            {
            "from": "human",
            "value": "图中人物的脸型如何？圆脸、锥子脸、国字方脸？"
            },
            {
            "from": "gpt",
            "value": "<answer7>"
            },
            {
            "from": "human",
            "value": "图中人物的腿部长度如何？长腿、中长腿、短腿？"
            },
            {
            "from": "gpt",
            "value": "<answer8>"
            },
            {
            "from": "human",
            "value": "图中人物的腿部形状如何？直腿、弯腿、O形腿？"
            },
            {
            "from": "gpt",
            "value": "<answer9>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式创建数据集:\n {json_string} \n根据提供的图片按json_string的格式生成问题和答案对。答案必须精简，后面有选项的在选项中选即可。答案必须严格来自图像内容，如果根据图像内容无法确定答案，请回答不知道。最后只输出生成的json_string部分即可。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))

    images = os.listdir(image_path)

                    

    for image in images:

        if not os.path.exists(root_dir + "/images/" + image):
            continue

        if os.path.exists(json_path  + image[:-4]+".json"):
            continue

        try:
            prompts = [('%s'%prompt, load_image(image_path + image))]
            response = pipe(prompts)

            # print(response[0].text[7:-3])

            # json_obj = json.loads(response[0].text[7:-3])
            good_json_obj = repair_json(response[0].text, return_objects=True)
            
            if not os.path.exists(json_path):
                os.makedirs(json_path)
            json_name =  json_path  + image[:-4]+".json"
            save_json(good_json_obj, json_name)
        except Exception as e:
            print("Exception:", str(e))            

   
def label_model_sup(image_path, json_path):
    # 要嵌入的JSON数据
    const_prompt="""{
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n图中人物的是否穿的裙子？"
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "图中人物是否穿外套？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": "图中人物的上衣包含外套的长度是否超过腰部？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "图中人物的裤子长度是否超过膝盖？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            {
            "from": "human",
            "value": "图中人物是什么性别？男性、女性？"
            },
            {
            "from": "gpt",
            "value": "<answer10>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式创建数据集:\n {json_string} \n根据提供的图片按json_string的格式生成问题和答案对。答案必须精简，后面有选项的在选项中选即可。答案必须严格来自图像内容，如果根据图像内容无法确定答案，请回答不知道。最后只输出生成的json_string部分即可。注意<answer>部分是hunman问题相对应的回答，请在（是、否、不知道）三个答案中选择，不要原样输出。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))

    images = os.listdir(image_path)                

    for image in images:

        if os.path.exists(json_path  + image[:-4]+".json"):
            continue

        prompts = [('%s'%prompt, load_image(image_path + image))]
        response = pipe(prompts)

        # print(response[0].text[7:-3])
        try:
            # json_obj = json.loads(response[0].text[7:-3])
            good_json_obj = repair_json(response[0].text, return_objects=True)

            if not os.path.exists(json_path):
                os.makedirs(json_path)
            json_name =  json_path  + image[:-4]+".json"
            save_json(good_json_obj, json_name)
        except Exception as e:
            print("Exception:", str(e))              


if __name__ == "__main__":
    root_dir = "/root/data/fullbody_cleaned_yolo_vl1_5"
    # images = os.listdir(root_dir + "/cloth/")
    image_path = "/root/data/fullbody_cleaned_yolo_vl1_5/"
    json_path = "/root/data/fullbody_cleaned_yolo_vl1_5_json/"
    json_path_sup = "/root/data/fullbody_cleaned_yolo_vl1_5_json_sup/"

    # label_model_sup(image_path, json_path_sup)

    root_dir = "/root/data/DressCode/lower_body/"

    # label_trous(root_dir)

    root_dir = "/root/data/DressCode/upper_body/"

    label_clothes(root_dir)

    