from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import os
import json
from tqdm import tqdm 


def save_json(data, json_name):
    with open(json_name, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
        # data：字典的数据
        # fp：保存的文本
        # encoding="utf-8"：使中文能够显示出来，不至于乱码
        # ensure_ascii：保证了 “篮球” 能正确的写入，而不是字节形式
        # indent=4：为了美观，不然会保存成一行
def clean_write(save_txt, error_txt, cleaned_yolo, cleaned_yolo_vl1_5):

    prompt = f"""你是一位专业的数据筛选工程师，本次数据筛选的目标是找到出那些只有一个完整人的全身照,你需要做的工作是将需要的图片筛选选出来，请仔细分析我们提供给你的图片，需要的图片必须满足以下5个特征：1.全身照的人有完整的脸部信息；2.全身照的人呈现站立的姿势；3.必须是全身照，从头人到脚的是一个完整的人，可以清楚的看到人物头和脚；4.一张图片里面只包含1个人；5.图片必须清晰，人的高度超过图片的一半高。以上是需要的图片的特征，如果完全满足以上5个特征中请输出五个特征对应的项置为0，格式：0, 0, 0, 0, 0;如果有其中任何一项不满足请将其中不满足的项置为1，例如第一项不满足的时候，输出格式为1, 0, 0, 0, 0，例如第二项不满足的时候，输出格式为0, 1, 0, 0, 0，例如第三项不满足的时候，输出格式为0, 0, 1, 0, 0，例如第四项不满足的时候，输出格式为0, 0, 0, 1, 0，例如第五项不满足的时候，输出格式为0, 0, 0, 0, 1。再简明扼要的说明原因。"""

    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))
    fe = open(error_txt, "w") 
    index=0
    n = 0                
    with open(save_txt, "w") as f:

        for root, dirs, files in tqdm(os.walk(cleaned_yolo)):

            for image in files:
                try:
                    if image[-3:] == "jpg":
                        print("idx:%d %s"%(index, root +"/"+ image))
                        
        
                        prompts = [('%s'%prompt, load_image(root +"/"+ image))]
                        response = pipe(prompts)

                        f.write("%s %s\n"%(root+"/"+image , response[0].text))
                        f.flush()
                        index+=1
        
                except Exception as e:
                    print("exception at:%d"%(n))
                    fe.write("%d\n"%n)
                    fe.flush()
                    n+=1
        
    f.close()
    fe.close()

def test_single(image_path):
    prompt = f"你是一位火眼金晶的数据筛选工程师，我们的目标是找到出那些只有一个完整人的全身照，你需要做的工作是将不需要的图片意义删选出来，并给出0或1，请仔细分析我们提供给你的图片，不需要的图片包含以下几个特征：1.没有完整的脸；2.不是站立的姿势；3.不是全身照，没有从头人到脚的是一个完整的人；4.一张图片里面包含多个人；5.图片模糊不清，人的占比很小；6.没有人出现；。以上是不需要的图片的特征，如果图片含有以上5个特征中的一个请输出1，如果没有请输出0，请简要的说明理由。"

    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=8190))

    index=0
    n = 0                



    print("idx:%d %s"%(index, image_path))
    
    prompts = [('%s'%prompt, load_image(image_path))]
    response = pipe(prompts)
    print(response[0].text)


prompt = f"""你是一位火眼金晶的数据筛选工程师，本次数据筛选的目标是找到出那些只有一个完整人的全身照,你需要做的工作是将需要的图片筛选选出来，请仔细分析我们提供给你的图片，需要的图片必须满足以下5个特征：
    1.全身照的人有完整的脸部信息；2.全身照的人呈现站立的姿势；3.必须是全身照，从头人到脚的是一个完整的人，可以清楚的看到人物头和脚；4.一张图片里面只包含1个人；5.图片必须清晰，人的高度超过图片的一半高。
    以上是需要的图片的特征，如果完全满足以上5个特征中请先输出0，如果有其中任何一项不满足请先输出1，再简明扼要说明原因。"""    

def label_clothes():
    # 要嵌入的JSON数据
    const_prompt="""{
        "version": "0.0.1",
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n全身照的人是否有完整的脸部信息？."
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "全身照的人是否呈现站立的姿势？？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": 是否是全身照，并且从头人到脚的是一个完整的人，可以清楚的看到人物头和脚？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "一张图片里面只包含1个人？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            {
            "from": "human",
            "value": "图片是否清晰，人的高度超过图片的一半高？"
            },
            {
            "from": "gpt",
            "value": "<answer5>"
            }
        ]    
    }"""

    # 将JSON数据转换为字符串，并转义双引号和花括号
    # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
    json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
    
    # 将转义后的JSON字符串嵌入提示中
    prompt = f"按照以下格式为我创建一个数据集:\n {json_string} \n要求：根据提供的图片,按json_string的格式生成问题和答案对。答案要必须精简，不要啰嗦废话，后面有选项的在选项中选即可。保证答案正确，不能瞎编，必须严格来源于图像内容中，如果图像没有，请回答不知道即可。最后只需要输出生成的json_string部分即可，不需要其他多余的部分。"


    pipe = pipeline('/root/model/InternVL-Chat-V1-5/',
                    backend_config=TurbomindEngineConfig(session_len=12288))
        
      
def move_picture(save_txt, error_txt, cleaned_folder, clean_aligned_txt):
    aligned_txt = open(clean_aligned_txt, 'w')
    fe = open(error_txt, "a") 
    index=0
    n = 0 
    with open(save_txt, 'r') as f:
     
        lines = f.readlines()
        for line in lines:
            try:
                infos = line.strip().split()
                if len(infos) != 6:
                    continue

                if "jpg" not in infos[0]:
                    continue    

                if infos[0][-3:] != "jpg":
                    continue

                # labels = infos[1].split(", ")
                total=0

                a = infos[1][0]
                b = infos[2][0]
                c = infos[3][0]
                d = infos[4][0]
                e = infos[5][0]

                total += int(a) + int(b) + int(c) + int(d) + int(e)

                if total > 0:
                    continue    
                    
                pre_cleaned_picture_path = infos[0]
                pre_cleaned_picture_name = pre_cleaned_picture_path.split('/')[-1]
                cleaned_picture_path = cleaned_folder + pre_cleaned_picture_name

                os.system("cp %s %s"%(pre_cleaned_picture_path, cleaned_picture_path))
                aligned_txt.write("%s %s %d\n"%(cleaned_picture_path, pre_cleaned_picture_path, total))
                aligned_txt.flush()
                index+=1
            except Exception as e:
                print("exception at:%d"%(index))
                fe.write("%d\n"%n)
                fe.flush()
                n+=1          


    f.close()
    aligned_txt.close()
    fe.close()


if __name__ == "__main__":
    root_dir = "/root/data/fullbody/"
    save_txt = "/root/data/cleaned_yolo_vl1.5.txt"
    error_txt = "/root/data/error.txt"
    cleaned_yolo= "/root/data/fullbody_cleaned_yolo/"
    cleaned_yolo_vl1_5= "/root/data/fullbody_cleaned_yolo_vl1_5/"

    # clean_write(save_txt, error_txt, cleaned_yolo, cleaned_yolo_vl1_5)
    clean_aligned_txt = "/root/data/clean_align.txt"

    move_picture(save_txt, error_txt, cleaned_yolo_vl1_5, clean_aligned_txt)
    # image_path = "/root/data/fullbody_cleaned/1839_F_Baidu_Female_workplace_pic2.jpg"
    # test_single(image_path)
    
   
