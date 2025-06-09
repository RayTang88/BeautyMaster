import sys
import os
import torch
import asyncio
from PIL import Image
import gradio as gr




vlm_weight_name = '/InternVL-Chat-V1-5-AWQ/'
llm_weight_name = '/internlm2-chat-20b-4bits/'
vlm_weight_name = '/Mini-InternVL-Chat-2B-V1-5-AWQ/'
vlm_weight_name = '/MiniCPM-Llama3-V-2_5-AWQ/'
llm_weight_name = '/Qwen2.5-7B-Instruct-AWQ/'

vlm_weight_name = 'InternVL2-8B-AWQ/'
# vlm_weight_name = "Janus-Pro-7B"
llm_weight_name = 'internlm3-8b-instruct-awq/'
# llm_weight_name = 'internlm2_5-7b-chat-4bit'
# llm_weight_name = "Yi-6B-Chat-4bits/"

if os.environ.get('openxlab'):

    base_path = os.environ.get('CODE_ROOT')+"BeautyMaster/"
    os.system(f'git clone --recursive -b openxlab-demo https://github.com/RayTang88/BeautyMaster.git {base_path}')

    #densepose
    os.system(f'pip install git+https://github.com/facebookresearch/detectron2@main#subdirectory=projects/DensePose')        
    
    # base_path = os.environ.get('MODEL_ROOT')+"lmdeploy_0-4-2_cpm_v2-5/"
    # os.system(f'git clone https://code.openxlab.org.cn/raytang88/lmdeploy_0-4-2_cpm_v2-5.git {base_path}')
    # os.system(f'cd {base_path} && git lfs pull')
    # package_path = base_path + "lmdeploy-0.4.2-cp310-cp310-manylinux2014_x86_64.whl"
    # os.system(f"pip install {package_path} -i https://pypi.tuna.tsinghua.edu.cn/simple")
    # os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"Qwen2-7B-Instruct-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/Qwen2-7B-Instruct-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"MiniCPM-Llama3-V-2_5-AWQ/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/MiniCPM-Llama3-V-2_5-AWQ.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")
    
    # base_path = os.environ.get('MODEL_ROOT')+"InternVL2-2B-AWQ/"
    # os.system(f'git clone https://code.openxlab.org.cn/raytang88/InternVL2-2B-AWQ.git {base_path}')
    # os.system(f'cd {base_path} && git lfs pull')
    # os.system(f"cd {os.environ.get('CODE_ROOT')}")

    base_path = os.environ.get('MODEL_ROOT')+"bce-embedding-base_v1/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/bce-embedding-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')

    base_path = os.environ.get('MODEL_ROOT')+"bce-reranker-base_v1/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/bce-reranker-base_v1.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")
    
    base_path = os.environ.get('MODEL_ROOT')+"CatVTON/"
    os.system(f'git clone https://code.openxlab.org.cn/raytang88/CatVTON.git {base_path}')
    os.system(f'cd {base_path} && git lfs pull')
    os.system(f"cd {os.environ.get('CODE_ROOT')}")

    # base_path = os.environ.get('MODEL_ROOT')+"CatVTON/"
    # os.system(f'git clone https://code.openxlab.org.cn/raytang88/CatVTON.git {base_path}')
    # os.system(f'cd {base_path} && git lfs pull')
    # os.system(f"cd {os.environ.get('CODE_ROOT')}")
    
    
    # vlm_weight_name = '/Mini-InternVL-Chat-2B-V1-5-AWQ/'
    vlm_weight_name = '/MiniCPM-Llama3-V-2_5-AWQ/'
    llm_weight_name = '/Qwen2-7B-Instruct-AWQ/'
    
    # vlm_weight_name = 'InternVL2-2B-AWQ/'
    # llm_weight_name = 'internlm2_5-7b-chat-4bit'



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

# def set_image_try_on(match_reslult, idx):
    
#     try_on_img = match_reslult[idx]["tryon_image"]
    
#     return try_on_img


def cc(image):
    if image.mode in ('RGBA', 'LA'):
        image = image.convert('RGB')
    elif image.mode in ('RGB'):
        image = image
    else:
        print("unkown mode", image.mode)   
    return image

# async def reset_local_func(instruction_txtbox: gr.Textbox,
#                            state_chatbot: Sequence, session_id: int):
#     """reset the session.

#     Args:
#         instruction_txtbox (str): user's prompt
#         state_chatbot (Sequence): the chatting history
#         session_id (int): the session id
#     """
#     with interface.lock:
#         interface.global_session_id += 1
#     session_id = interface.global_session_id
#     await asyncio.sleep(0)
#     return (state_chatbot, state_chatbot, instruction_txtbox, session_id)

def run_local_match(weather, season, determine, additional_requirements, full_body_image):
    # opt = parse_opt(vlm_weight_name, llm_weight_name)
    # interface = Interface(**vars(opt))

    #RGBA-RGB
    planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    # planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    # planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    
    planA_match_reason = ""
    planB_match_reason = ""
    # planC_match_reason = ""
    
    # print("full_body_image mode-------------", full_body_image["composite"].mode)
    full_body_image = cc(full_body_image["composite"])
    # print("full_body_image mode-------------", full_body_image.mode)
    
    match_result, body_shape_descs = interface.match_interface(weather,
    season,
    determine,
    full_body_image,
    additional_requirements)
    
    if len(match_result)==3:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_result, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason = set_image(match_result, 1)
        # planC_clothes_img_A, planC_clothes_img_B, planC_match_reason = set_image(match_reslult, 2)
  
    elif len(match_result)==2:
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_result, 0)
        planB_clothes_img_A, planB_clothes_img_B, planB_match_reason = set_image(match_result, 1)
        
    elif len(match_result)==1:
                
        planA_clothes_img_A, planA_clothes_img_B, planA_match_reason = set_image(match_result, 0)
 
    return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, match_result, body_shape_descs  
    # return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason

def run_local_tryon(weather, season, determine, additional_requirements, full_body_image):
   
    try:
        # opt = parse_opt(vlm_weight_name, llm_weight_name)
        # interface = Interface(**vars(opt))
        # opt = parse_opt(vlm_weight_name, llm_weight_name)
        # interface = Interface(**vars(opt))
        # func="match"
        # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
  
        # while Cycles<total:
        
        planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
        planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
        planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
        planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
        # planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
        # planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
        planA_match_reason = ""
        planB_match_reason = ""
        # planC_match_reason = ""
        planA_try_on = Image.new("RGB", (500, 300), 'white')
        planB_try_on = Image.new("RGB", (500, 300), 'white')
        # planC_try_on = Image.new("RGB", (500, 300), 'white')
        
        
        # print("full_body_image mode-------------", full_body_image["composite"].mode)
        full_body_image = cc(full_body_image["composite"])
        # print("full_body_image mode-------------", full_body_image.mode)
        
        match_result, _ = interface.try_on_interface(weather,
        season,
        determine,
        full_body_image,
        additional_requirements)

        if len(match_result)==3:
            planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_result, 0)
            planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_result, 1)
            # planC_clothes_img_A, planC_clothes_img_B, planC_match_reason, planC_try_on = set_image_try_on(match_reslult, 2)

        elif len(match_result)==2:
            planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_result, 0)
            planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planB_try_on = set_image_try_on(match_result, 1)
                    
        elif len(match_result)==1:
            planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planA_try_on = set_image_try_on(match_result, 0)
                # torch.cuda.synchronize()
                # torch.cuda.empty_cache()
        return planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planA_try_on, planB_try_on
    
    except Exception as e:
 
        print(f"error: {e}, try again...")
       
    
def run_local_tryon_only(full_body_image, match_result, body_shape_descs):
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    # planA_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    # planA_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    # planB_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    # planB_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    # planC_clothes_img_A = Image.new("RGB", (500, 300), 'white')
    # planC_clothes_img_B = Image.new("RGB", (500, 300), 'white')
    # planA_match_reason = ""
    # planB_match_reason = ""
    # planC_match_reason = ""
    planA_try_on = Image.new("RGB", (500, 300), 'white')
    planB_try_on = Image.new("RGB", (500, 300), 'white')
    # planC_try_on = Image.new("RGB", (500, 300), 'white')
    
    
    # print("full_body_image mode-------------", full_body_image["composite"].mode)
    full_body_image = cc(full_body_image["composite"])
    # print("full_body_image mode-------------", full_body_image.mode)
    if(len(match_result) < 1):
        return planA_try_on, planB_try_on
        
    try_on_result= interface.try_on_only_interface(match_result, full_body_image, body_shape_descs)

    if len(try_on_result)==3:
        planA_try_on = set_image_try_on(try_on_result, 0)
        planB_try_on = set_image_try_on(try_on_result, 1)
        # planC_try_on = set_image_try_on(try_on_result, 2)
  
    elif len(try_on_result)==2:
        planA_try_on = set_image_try_on(try_on_result, 0)
        planB_try_on = set_image_try_on(try_on_result, 1)
        
    elif len(try_on_result)==1:
        planA_try_on = set_image_try_on(try_on_result, 0)

    return planA_try_on, planB_try_on


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
    
    #2.write database(TODO)
    
    
    return category, caption_string


def run_tec_support(items, err_code):
    need_content_dict = {"错误码":"错误描述", "授权编号":"授权项"}  
    result_dicts = interface.rag_tec_supoort(items, err_code, need_content_dict)
    
    result = ""
    for result_dict in result_dicts["match_content"]:
        match_id = result_dict["match_id"] 
        if type(result_dict["match_id"]) == list:
            match_id = result_dict["match_id"][0]
            
        match_caption = result_dict["match_caption"]  
        if type(result_dict["match_caption"]) == list:
            match_caption = result_dict["match_caption"][0] 
            
        id = result_dict["id"] 
        if type(result_dict["id"]) == list:
            id = result_dict["id"][0]    
     
               
        result += ("%s.%s:%s, %s:%s;\n"% (id, items, match_id, need_content_dict[items], match_caption))

    return result    


def is_upload():
    global interactive_
    interactive_ = True
    return interactive_

if __name__ == '__main__':

    sys.path.append(os.environ.get('CODE_ROOT')+'BeautyMaster/')
    from beautymaster.demo.infer import Interface, parse_opt  
    # save memory commit
    opt = parse_opt(vlm_weight_name, llm_weight_name)
    interface = Interface(**vars(opt))   
    image_blocks = gr.Blocks().queue()
    
    with image_blocks as Match:
        state_session_id = gr.State(0)

        gr.Markdown("## 🌟 牛逼技术支持 🌟")
        gr.Markdown("因为算力的问题，目前上传一个简化版本。如果您想体验完整的功能，请移步Github并持续关注我们的后续工作。Github：[source codes](https://github.com/RayTang88/BeautyMaster), 欢迎star🌟")
        gr.Markdown("如使用过程中出现错误提示，请重复Match，感谢您的使用！")
        
        with gr.Row():
            with gr.Column():
                # with gr.Row():
                #     with gr.Row():
                #         is_checked = gr.Checkbox(label="Yes", info="Use auto-generated mask (Takes 5 seconds)",value=True)
                #     with gr.Row():
                #         is_checked_crop = gr.Checkbox(label="Yes", info="Use auto-crop & resizing",value=False)
                # fullbody_img = gr.Image(label="fullbody", sources='upload', type="pil")
                with gr.Row():
                    with gr.Row():
                        items = gr.Dropdown(choices=["错误码","授权编号"], label="技术支持类型", value="错误码")
                    with gr.Row():
                        # additional_requirements = gr.Dropdown(choices=["复古怀旧","时尚前卫","活力运动","优雅知性"], label="您的个性搭配需求", value="时尚前卫")    
                        err_code = gr.Textbox(placeholder="描述您将输入的信息) -61", show_label=True, label="您想知道的内容", elem_id="prompt")

            with gr.Column():
                with gr.Row():
       
                    match_caption = gr.Textbox(placeholder="", label="技术支持内容", show_label=True, elem_id="planA_match_reason")
                
        with gr.Row():
            with gr.Row():

                # match_button = gr.Button(value="step-1.Match", interactive=True)
                tryon_button = gr.Button(value="Match", interactive=True)
                # reset_button = gr.Button(value="Reset", interactive=True)
            # with gr.Accordion(label="Advanced Settings", open=False):
            #     with gr.Row():
            #         denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
            #         seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)
        # match_button.click(run_local, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, planC_clothes_img_A, planC_clothes_img_B, planC_match_reason], api_name='Match')
        # match_result = gr.State([])
        # body_shape_descs = gr.State('')
        
        # match_button.click(run_local_match, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason, match_result, body_shape_descs], api_name='Match')
        # match_button.click(run_local_match, inputs=[weather, season, determine, additional_requirements, fullbody_img], outputs=[planA_clothes_img_A, planA_clothes_img_B, planA_match_reason, planB_clothes_img_A, planB_clothes_img_B, planB_match_reason], api_name='Match')
        tryon_button.click(run_tec_support, inputs=[items, err_code], outputs=[match_caption], api_name='TryOn')
        # tryon_button.click(run_local_tryon_only, inputs=[fullbody_img, match_result, body_shape_descs], outputs=[planA, planB], api_name='TryOn')
        
    app = gr.TabbedInterface([Match], ["牛逼技术支持"])
    app.launch(server_name='192.168.0.122' ,server_port=7860)
