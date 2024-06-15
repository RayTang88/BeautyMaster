import sys
import os
from PIL import Image
import gradio as gr

vlm_weight_name = '/InternVL-Chat-V1-5-AWQ/'
llm_weight_name = '/internlm2-chat-20b-4bits/'

if os.environ.get('openxlab'):

    base_path = os.environ.get('CODE_ROOT')+"BeautyMaster/"
    os.system(f'git clone --recursive -b openxlab-demo https://github.com/RayTang88/BeautyMaster.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')

    package_path = os.environ.get('CODE_ROOT') + "BeautyMaster/beautymaster/openxlab_demo/lmdeploy-0.4.2-cp310-cp310-manylinux2014_x86_64.whl"
    os.system(f"pip install {package_path} --force-reinstall -i https://pypi.tuna.tsinghua.edu.cn/simple")
    # os.system(f'cd ./BeautyMaster && python beautymaster/openxlab_demo/download.py')
    # os.system(f"cd ..")
    # os.system('apt install git')
    # os.system('apt install git-lfs')
    base_path = os.environ.get('MODEL_ROOT')+"Qwen2-7B-Instruct-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/Qwen2-7B-Instruct-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"MiniCPM-Llama3-V-2_5-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/MiniCPM-Llama3-V-2_5-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"bce-embedding-base_v1/"
    os.system(f'git clone https://www.modelscope.cn/maidalun/bce-embedding-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')

    base_path = os.environ.get('MODEL_ROOT')+"bce-reranker-base_v1/"
    os.system(f'git clone https://www.modelscope.cn/maidalun/bce-reranker-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    vlm_weight_name = '/MiniCPM-Llama3-V-2_5-AWQ/'
    llm_weight_name = '/Qwen2-7B-Instruct-AWQ/'


sys.path.append(os.environ.get('CODE_ROOT')+'BeautyMaster/')
from beautymaster.demo.infer import Interface, parse_opt

example_path = os.environ.get('DATA_ROOT')

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


def cc(image):
    if image.mode in ('RGBA', 'LA'):
        image = image.convert('RGB')
    return image
opt = parse_opt(vlm_weight_name, llm_weight_name)
interface = Interface(**vars(opt))
def run_local(weather, season, determine, additional_requirements, full_body_image_path):

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
    
    full_body_image_path = cc(full_body_image_path["composite"])
    
    match_reslult, _ = interface.match(weather,
    season,
    determine,
    full_body_image_path,
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

    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason   

def run_local_match(weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func):
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
    
    if "Match" == func:
        # match_reslult = interface.match(weather,
        # season,
        # determine,
        # full_body_image_path,
        # additional_requirements)
        planA = clothes_path
        planB = clothes_path
        planC = clothes_path

    elif "RAG" == func:
        # interface.rag(weather,
        #     season,
        #     determine,
        #     full_body_image_path,
        #     additional_requirements)
        pass

    elif "Caption" == func:
        # interface.caption(clothes_path)
                pass

    elif  "TryOn"== func:
        pass

    # def ss(image, save_path):
    #     if image.mode in ('RGBA', 'LA'):
    #         image = image.convert('RGB')
    #     image.save(save_path)    

    # ss(full_body_image_path["background"], "/root/code/test/b.jpg")
    # ss(full_body_image_path["layers"][0], "/root/code/test/l.jpg")
    # ss(full_body_image_path["composite"], "/root/code/test/p.jpg")
    
    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason


def run_local_wardrobe(weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func):
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    planA = Image.new("RGB", (500, 300), 'white')
    planB = Image.new("RGB", (500, 300), 'white')
    planC = Image.new("RGB", (500, 300), 'white')
    rag = ""
    caption = ""
    
    # upper_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # upper_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in upper_list]

    # lower_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # lower_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in lower_list]

    # dresses_list = os.listdir(os.path.join(example_path,"DressCode/upper_body/images/"))
    # dresses_list_path = [os.path.join(example_path,"DressCode/upper_body/images/",garm) for garm in dresses_list]
    #1.get caption
    caption_json, caption_string = interface.caption(clothes_path)
    
    category = caption_json["category"]
    
    #2.write database
    
    
    return category, caption_string


def is_upload():
    global interactive_
    interactive_ = True
    return interactive_


image_blocks = gr.Blocks().queue()
with image_blocks as Match:
    gr.Markdown("## 🌟👗💄 BeautyMaster 💄👗🌟")
    gr.Markdown("Beauty Master make you beautiful every day. Check out the [source codes](https://github.com/RayTang88/BeautyMaster)")
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
            additional_requirements = gr.Textbox(placeholder="描述您对搭配的特殊需求 ex) 简洁大方，美丽动人", show_label=True, elem_id="prompt")

            example = gr.Examples(
                inputs=fullbody_img,
                examples_per_page=10,
                examples=human_list_path
            )

        with gr.Column():
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("Plan A")
                planA_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planA_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planA_match_reason = gr.Textbox(placeholder="Reasons for recommending PlanA", label="match_reason", show_label=True, elem_id="planA_match_reason")
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("Plan B")
                planB_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planB_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planB_match_reason = gr.Textbox(placeholder="Reasons for recommending PlanB", label="match_reason", show_label=True, elem_id="planB_match_reason")
            with gr.Row():
                with gr.Column(elem_id="prompt-container"):
                    gr.Markdown("Plan C")
                planC_clothes_img_A = gr.Image(label="clothes", sources='upload', type="pil", height=300)
                planC_clothes_img_B = gr.Image(label="clothes", sources='upload', type="pil", height=300)      
                with gr.Row(elem_id="prompt-container"):
                    with gr.Row():
                        planC_match_reason = gr.Textbox(placeholder="Reasons for recommending PlanC", label="match_reason", show_label=True, elem_id="planC_match_reason")
                        
        with gr.Column():
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planA = gr.Image(label="Try on output A", elem_id="Mach_output_A",show_share_button=False, height=300)
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planB = gr.Image(label="Try on output B", elem_id="Mach_output_B",show_share_button=False, height=300)
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planC = gr.Image(label="Try on output C", elem_id="Mach_output_C",show_share_button=False, height=300)

    with gr.Row():
        with gr.Row():

            match_button = gr.Button(value="Match", interactive=True)
            tryon_button = gr.Button(value="TryOn(coming soon...)", interactive=True)
        # with gr.Accordion(label="Advanced Settings", open=False):
        #     with gr.Row():
        #         denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
        #         seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)
    match_button.click(run_local, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason], api_name='Match')
    # match_button.click(run_local_match, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason], api_name='Match')
    # tryon_button.click(run_local_tryon, inputs=[fullbody_img, clothes_img, body_desc, cloth_caption], outputs=[planA, planB, planC], api_name='TryOn')
image_blocks = gr.Blocks().queue()
with image_blocks as Wardrobe:
    with gr.Row():
        with gr.Column():
            fullbody_img = gr.ImageEditor(sources='upload', type="pil", label='Human. Mask with pen or use auto-masking', interactive=True)
            with gr.Column():
                with gr.Column():
                    is_checked = gr.Checkbox(label="Yes", info="Use auto-generated mask (Takes 5 seconds)",value=True)
                with gr.Column():
                    is_checked_crop = gr.Checkbox(label="Yes", info="Use auto-crop & resizing",value=False)
                example = gr.Examples(
                inputs=fullbody_img,
                examples_per_page=10,
                examples=human_list_path
            )
        with gr.Column():        
            clothes_img = gr.Image(label="clothes", sources='upload', type="pil")
            with gr.Row(elem_id="prompt-container"):
                with gr.Row():
                    prompt = gr.Textbox(placeholder="Description of garment ex) Short Sleeve Round Neck T-shirts", label="", show_label=False, elem_id="prompt")
            # example = gr.Examples(
            #     inputs=clothes_img,
            #     examples_per_page=8,
            #     examples=upper_list_path)
            
    with gr.Column():
        wardrobe_button = gr.Button(value="Put it in matching wardrobe")
        with gr.Accordion(label="Advanced Settings", open=False):
            with gr.Row():
                denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
                seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)

    wardrobe_button.click(run_local_wardrobe, inputs=[weather, season, determine, additional_requirements, fullbody_img, clothes_img], outputs=[planA, planB, planC, rag, caption], api_name='run')


app = gr.TabbedInterface([Match, Wardrobe], ["Match", "Wardrobe"])
app.launch()
