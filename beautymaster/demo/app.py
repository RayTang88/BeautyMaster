import sys
import os
from PIL import Image
import gradio as gr
sys.path.append('/root/code/BeautyMaster/beautymaster/demo')
from infer import Interface, parse_opt


example_path = os.path.join("/group_share/data_org/", 'test_data/')

upper_list = os.listdir(os.path.join(example_path,"upper_body/images/"))
upperlist_path = [os.path.join(example_path,"upper_body/images/",garm) for garm in upper_list]

lower_list = os.listdir(os.path.join(example_path,"upper_body/images/"))
lower_list_path = [os.path.join(example_path,"upper_body/images/",garm) for garm in lower_list]

dresses_list = os.listdir(os.path.join(example_path,"upper_body/images/"))
dresses_list_path = [os.path.join(example_path,"upper_body/images/",garm) for garm in dresses_list]

human_list = os.listdir(os.path.join(example_path,"fullbody/images/"))
human_list_path = [os.path.join(example_path,"fullbody/images/",human) for human in human_list]

# human_ex_list = []
# for ex_human in human_list_path:
#     ex_dict= {}
#     ex_dict['background'] = ex_human
#     ex_dict['layers'] = None
#     ex_dict['composite'] = None
#     human_ex_list.append(ex_dict)

opt = parse_opt()
interface = Interface(**vars(opt))

def run_local(weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func):
    
    planA = Image.new("RGB", (500, 300), 'white')
    planB = Image.new("RGB", (500, 300), 'white')
    planC = Image.new("RGB", (500, 300), 'white')
    rag = ""
    caption = ""
    
    if "Match" == func:
        match_reslult = interface.match(weather,
        season,
        determine,
        full_body_image_path,
        additional_requirements)
        
        if len(match_reslult)==3:
             
            planA = match_reslult[0]['image']
            planB = match_reslult[1]['image']
            planC = match_reslult[2]['image']
        if len(match_reslult)==2:
            planA = match_reslult[0]['image']
            planB = match_reslult[1]['image']

        if len(match_reslult)==1:
                 
            planA = match_reslult[0]['image']
   
    elif "RAG" == func:
        
        rag_reuslt = interface.rag(weather,
            season,
            determine,
            full_body_image_path,
            additional_requirements)
        rag = rag_reuslt
    
    elif "Caption" == func:
        
        caption_result = interface.caption(clothes_path)
        
        caption = caption_result
        
    elif  "tryon"== func:
        pass
    else :
        print("error function select!")
    
    return planA, planB, planC, rag, caption   

def run_local_test(garm_img, func):
    # func="match"
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg"
    if "Match" == func:
        # match_reslult = interface.match(weather,
        # season,
        # determine,
        # full_body_image_path,
        # additional_requirements)
        return garm_img, garm_img
    elif "RAG" == func:
        # interface.rag(weather,
        #     season,
        #     determine,
        #     full_body_image_path,
        #     additional_requirements)
        return garm_img, garm_img
    elif "Caption" == func:
        # interface.caption(clothes_path)
        return garm_img, garm_img
    elif  "TryOn"== func:
        return garm_img, garm_img 


image_blocks = gr.Blocks().queue()
with image_blocks as demo:
    gr.Markdown("## 🌟👗💄 BeautyMaster 💄👗🌟")
    gr.Markdown("Beauty Master make you beautiful every day. Check out the [source codes](https://github.com/RayTang88/BeautyMaster)")
    with gr.Row():
        with gr.Column():
            # fullbody_img = gr.ImageEditor(sources='upload', type="pil", label='Human. Mask with pen or use auto-masking', interactive=True)
            # with gr.Column():
            #     with gr.Column():
            #         is_checked = gr.Checkbox(label="Yes", info="Use auto-generated mask (Takes 5 seconds)",value=True)
            #     with gr.Column():
            #         is_checked_crop = gr.Checkbox(label="Yes", info="Use auto-crop & resizing",value=False)
            fullbody_img = gr.Image(label="fullbody", sources='upload', type="pil")
            season = gr.Dropdown(choices=["春季","夏季","秋季","冬季"], label="季节", value="春季")
            weather = gr.Dropdown(choices=["零下10摄氏度","0摄氏度","10摄氏度","20摄氏度","30摄氏度"], label="温度", value="零下10摄氏度")
            determine = gr.Dropdown(choices=["约会","逛街","晚宴","工作"], label="目的", value="约会")
            additional_requirements = "简洁大方美丽漂亮"

            example = gr.Examples(
                inputs=fullbody_img,
                examples_per_page=10,
                examples=human_list_path
            )

        with gr.Column():
            clothes_img = gr.Image(label="clothes", sources='upload', type="pil")
            with gr.Row(elem_id="prompt-container"):
                with gr.Row():
                    prompt = gr.Textbox(placeholder="Description of garment ex) Short Sleeve Round Neck T-shirts", show_label=False, elem_id="prompt")
            example = gr.Examples(
                inputs=clothes_img,
                examples_per_page=8,
                examples=upperlist_path)
            func = gr.Dropdown(choices=["Match","RAG","Caption","TryOn"], label="功能", value="Match")
            additional_requirements = gr.Textbox(placeholder="描述您对搭配的特殊需求 ex) 简洁大方，美丽动人", show_label=True, elem_id="prompt")
            rag = gr.Textbox(placeholder="rag output", show_label=False, elem_id="rag")
            caption = gr.Textbox(placeholder="caption", show_label=False, elem_id="caption")        
        with gr.Column():
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planA = gr.Image(label="Mach output A", elem_id="Mach_output_A",show_share_button=False)

            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planB = gr.Image(label="Mach output B", elem_id="Mach_output_B",show_share_button=False)
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            planC = gr.Image(label="Mach output C", elem_id="Mach_output_C",show_share_button=False)


    with gr.Column():
        run_button = gr.Button(value="Run")
        with gr.Accordion(label="Advanced Settings", open=False):
            with gr.Row():
                denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
                seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)

    run_button.click(run_local, inputs=[weather, season, determine, additional_requirements, fullbody_img, clothes_img, func], outputs=[planA, planB, planC, rag, caption], api_name='run')

image_blocks.launch()

