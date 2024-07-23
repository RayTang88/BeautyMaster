import sys
import os
import torch
from PIL import Image
import gradio as gr

vlm_weight_name = '/InternVL-Chat-V1-5-AWQ/'
llm_weight_name = '/internlm2-chat-20b-4bits/'
vlm_weight_name = '/Mini-InternVL-Chat-2B-V1-5-AWQ/'
vlm_weight_name = '/MiniCPM-Llama3-V-2_5-AWQ/'
llm_weight_name = '/Qwen2-7B-Instruct-AWQ/'

vlm_weight_name = 'InternVL2-2B/'
# llm_weight_name = 'internlm2_5-7b-chat/'
# llm_weight_name = '/Qwen2-7B-Instruct/'
llm_weight_name = "Yi-1.5-6B-Chat"

if os.environ.get('openxlab'):

    base_path = os.environ.get('CODE_ROOT')+"BeautyMaster/"
    os.system(f'git clone --recursive -b openxlab-demo https://github.com/RayTang88/BeautyMaster.git {base_path}')
              
    base_path = os.environ.get('MODEL_ROOT')+"lmdeploy_0-4-2_cpm_v2-5/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/lmdeploy_0-4-2_cpm_v2-5.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    package_path = base_path + "lmdeploy-0.4.2-cp310-cp310-manylinux2014_x86_64.whl"
    os.system(f"pip install {package_path} -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"Qwen2-7B-Instruct-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/Qwen2-7B-Instruct-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"MiniCPM-Llama3-V-2_5-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/MiniCPM-Llama3-V-2_5-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")
    
    base_path = os.environ.get('MODEL_ROOT')+"Mini-InternVL-Chat-2B-V1-5-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/Mini-InternVL-Chat-2B-V1-5-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"bce-embedding-base_v1/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/bce-embedding-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')

    base_path = os.environ.get('MODEL_ROOT')+"bce-reranker-base_v1/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/bce-reranker-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    # vlm_weight_name = '/Mini-InternVL-Chat-2B-V1-5-AWQ/'
    vlm_weight_name = '/MiniCPM-Llama3-V-2_5-AWQ/'
    llm_weight_name = '/Qwen2-7B-Instruct-AWQ/'


sys.path.append(os.environ.get('CODE_ROOT')+'BeautyMaster/')
from beautymaster.openxlab_demo.infer import Interface, parse_opt

example_path = os.environ.get('DATA_ROOT')

upper_body = os.listdir(os.path.join(example_path,"upper_body/images/"))[:7]
upper_body_path = [os.path.join(example_path,"upper_body/images/",human) for human in upper_body]
human_list = os.listdir(os.path.join(example_path,"fullbody_cleaned/images/"))
human_list_path = [os.path.join(example_path,"fullbody_cleaned/images/",human) for human in human_list]



def set_image(match_reslult, idx):
    clothes_img_A = Image.new("RGB", (500, 300), 'white')
    clothes_img_B = Image.new("RGB", (500, 300), 'white')
    match_reason = ""
    if(len(match_reslult[idx]["images"])==1):
        clothes_img_A = match_reslult[idx]["images"][0]
    elif(len(match_reslult[idx]["images"])==2):
        clothes_img_A = match_reslult[idx]["images"][0]
        clothes_img_B = match_reslult[idx]["images"][1]
    match_reason = match_reslult[idx]["match_reason"]

    return clothes_img_A, clothes_img_B, match_reason

def set_image_try_on(match_reslult, idx):
    clothes_img_A = Image.new("RGB", (500, 300), 'white')
    clothes_img_B = Image.new("RGB", (500, 300), 'white')
    match_reason = ""
    if(len(match_reslult[idx]["images"])==1):
        clothes_img_A = match_reslult[idx]["images"][0]
    elif(len(match_reslult[idx]["images"])==2):
        clothes_img_A = match_reslult[idx]["images"][0]
        clothes_img_B = match_reslult[idx]["images"][1]
    match_reason = match_reslult[idx]["match_reason"]
    try_on_img = match_reslult[idx]["tryon_image"]
    return clothes_img_A, clothes_img_B, match_reason, try_on_img


def cc(image):
    if image.mode in ('RGBA', 'LA'):
        image = image.convert('RGB')
    elif image.mode in ('RGB'):
        image = image
    else:
        print("unkown mode", image.mode)   
    return image
# opt = parse_opt(vlm_weight_name, llm_weight_name)
# interface = Interface(**vars(opt))
def run_local_match(weather, season, determine, additional_requirements, full_body_image):
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))
    #RGBA-RGB
    planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    
    planA_match_reason = ""
    planB_match_reason = ""
    planC_match_reason = ""
    
    # print("full_body_image mode-------------", full_body_image["composite"].mode)
    full_body_image = cc(full_body_image["composite"])
    # print("full_body_image mode-------------", full_body_image.mode)
    
    match_reslult, _ = interface.match_interface(weather,
    season,
    determine,
    full_body_image,
    additional_requirements)
    
    if len(match_reslult)==3:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason = set_image(match_reslult, 1)
        planC_clothes_img_A, planC_clothes_img_B, planC_match_reason = set_image(match_reslult, 2)
  
    elif len(match_reslult)==2:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason = set_image(match_reslult, 1)
        
    elif len(match_reslult)==1:
                
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_reslult, 0)
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason   

def run_local_tryon(weather, season, determine, additional_requirements, full_body_image):
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planA_match_reason = ""
    planB_match_reason = ""
    planC_match_reason = ""
    planA_try_on = Image.new("RGB", (500, 300), 'white')
    planB_try_on = Image.new("RGB", (500, 300), 'white')
    planC_try_on = Image.new("RGB", (500, 300), 'white')
    
    
    # print("full_body_image mode-------------", full_body_image["composite"].mode)
    full_body_image = cc(full_body_image["composite"])
    # print("full_body_image mode-------------", full_body_image.mode)
    
    match_reslult, _ = interface.try_on_interface(weather,
    season,
    determine,
    full_body_image,
    additional_requirements)

    if len(match_reslult)==3:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_reslult, 1)
        planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planC_try_on = set_image_try_on(match_reslult, 2)
  
    elif len(match_reslult)==2:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_reslult, 1)
        
    elif len(match_reslult)==1:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planA_try_on, planB_try_on, planC_try_on

def run_local_tryon_only(weather, season, determine, additional_requirements, full_body_image):
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planA_match_reason = ""
    planB_match_reason = ""
    planC_match_reason = ""
    planA_try_on = Image.new("RGB", (500, 300), 'white')
    planB_try_on = Image.new("RGB", (500, 300), 'white')
    planC_try_on = Image.new("RGB", (500, 300), 'white')
    
    
    # print("full_body_image mode-------------", full_body_image["composite"].mode)
    full_body_image = cc(full_body_image["composite"])
    # print("full_body_image mode-------------", full_body_image.mode)
    
    match_reslult, _ = interface.try_on_interface(weather,
    season,
    determine,
    full_body_image,
    additional_requirements)

    if len(match_reslult)==3:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_reslult, 1)
        planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planC_try_on = set_image_try_on(match_reslult, 2)
  
    elif len(match_reslult)==2:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_reslult, 1)
        
    elif len(match_reslult)==1:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_reslult, 0)

    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planA_try_on, planB_try_on, planC_try_on


def run_local_wardrobe(clothes_path, category_input):
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    # planA = Image.new("RGB", (500, 300), 'white')
    # planB = Image.new("RGB", (500, 300), 'white')
    # planC = Image.new("RGB", (500, 300), 'white')
    category = ""
    caption_string = ""
    
    # upper_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # upper_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in upper_list]

    # lower_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # lower_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in lower_list]

    # dresses_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # dresses_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in dresses_list]
    #1.get caption
    caption_json, caption_string = interface.caption_interface(clothes_path)
    
    category = caption_json["category"]
    
    #2.write database
    
    
    return category, caption_string


def is_upload():
    global interactive_
    interactive_ = True
    return interactive_

image_blocks = gr.Blocks().queue()
with image_blocks as Match:
    gr.Markdown("## 🌟👗💄 美妆达人 - 美丽您的每一天 💄👗🌟")
    gr.Markdown("因为算力的问题，目前上传一个简化版本。如果您想体验完整的功能，请移步Github并持续关注我们的后续工作。Github：[source codes](https://github.com/RayTang88/BeautyMaster), 欢迎star🌟")
    gr.Markdown("使用方法：在美妆搭配页面按示例上传一张全身照，点击Match按钮，即可体验，目前我们内置了一个精简的服饰数据库供基础效果展示。")
    gr.Markdown("注意事项：1.如果点击Match一分钟后未有响应，可再次点击Math按钮尝试；2.试穿功能和美丽衣橱暂未开放，请持续关注我们的后续工作。")
    with gr.Row():
        with gr.Column():
            fullbody_img = gr.ImageEditor(sources='upload', type="pil", label='Human. Mask with pen or use auto-masking', interactive=True)
            with gr.Row():
                with gr.Row():
                    is_checked = gr.Checkbox(label="Yes", info="Use auto-generated mask (Takes 5 seconds)",value=True)
                with gr.Row():
                    is_checked_crop = gr.Checkbox(label="Yes", info="Use auto-crop & resizing",value=False)
            # fullbody_img = gr.Image(label="fullbody", sources='upload', type="pil")
            season = gr.Dropdown(choices=["春季","夏季","秋季","冬季"], label="季节", value="夏季")
            weather = gr.Dropdown(choices=["零下10摄氏度左右","0摄氏度左右","10摄氏度左右","20摄氏度左右","30摄氏度左右", "40摄氏度左右"], label="温度", value="40摄氏度左右")
            determine = gr.Dropdown(choices=["约会","逛街","晚宴","工作"], label="目的", value="逛街")
            additional_requirements = gr.Textbox(placeholder="描述您对搭配的特殊需求 ex) 简洁大方，美丽动人", show_label=True, label="您的个性搭配需求", elem_id="prompt")

            example = gr.Examples(
                inputs=fullbody_img,
                examples_per_page=10,
                examples=human_list_path
            )

        with gr.Column():
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("推荐方案 1")
                planA_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planA_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planA_match_reason = gr.Textbox(placeholder="", label="推荐理由", show_label=True, elem_id="planA_match_reason")
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("推荐方案 2")
                planB_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planB_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planB_match_reason = gr.Textbox(placeholder="", label="推荐理由", show_label=True, elem_id="planB_match_reason")
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("推荐方案 3")
                planC_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planC_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)      
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planC_match_reason = gr.Textbox(placeholder="", label="推荐理由", show_label=True, elem_id="planC_match_reason")
                        
        with gr.Column():
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planA = gr.Image(label="试穿展示 1", elem_id="Mach_output_A",show_share_button=False)
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planB = gr.Image(label="试穿展示 2", elem_id="Mach_output_B",show_share_button=False)
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planC = gr.Image(label="试穿展示 3", elem_id="Mach_output_C",show_share_button=False)

    with gr.Row():
        with gr.Row():

            match_button = gr.Button(value="Match", interactive=True)
            tryon_button = gr.Button(value="Try on", interactive=True)
        # with gr.Accordion(label="Advanced Settings", open=False):
        #     with gr.Row():
        #         denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
        #         seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)
    # match_button.click(run_local, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason], api_name='Match')
    match_button.click(run_local_match, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason], api_name='Match')
    tryon_button.click(run_local_tryon, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planA, planB, planC], api_name='TryOn')
image_blocks = gr.Blocks().queue()
with image_blocks as Wardrobe:
    gr.Markdown("这里是您的美丽衣橱，您可以将想要搭配的服饰上传到这里。")
    with gr.Row():
        with gr.Column():        
            clothes_img = gr.Image(label="clothes", sources='upload', type="pil")
            with gr.Row(elem_id="prompt-container"):
                with gr.Row():
                    category_input = gr.Dropdown(choices=["上衣","裤子","半身裙","连衣裙", "其他"], label="类别", value="连衣裙")
                    prompt = gr.Textbox(placeholder="", label="", show_label=False, elem_id="prompt")
                    
            with gr.Row(elem_id="prompt-container"):
                with gr.Row():
                    category = gr.Textbox(placeholder="", label="类别", show_label=True, elem_id="prompt")
                    caption = gr.Textbox(placeholder="", label="文字说明", show_label=True, elem_id="prompt")
         
            example = gr.Examples(
                inputs=clothes_img,
                examples_per_page=8,
                examples=upper_body_path)
  
            
    with gr.Column():
        wardrobe_button = gr.Button(value="Put it in matching wardrobe(coming soon...)")
        # with gr.Accordion(label="Advanced Settings", open=False):
        #     with gr.Row():
        #         denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
        #         seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)

    # wardrobe_button.click(run_local_wardrobe, inputs=[clothes_img, category_input], outputs=[category, caption], api_name='wardrobe')


app = gr.TabbedInterface([Match, Wardrobe], ["美妆搭配", "美丽衣橱"])
app.launch()
