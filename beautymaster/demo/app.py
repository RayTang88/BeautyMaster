import sys
import os
sys.path.append('./')
from PIL import Image
import gradio as gr

from .infer import Interface, parse_opt, main


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

image_blocks = gr.Blocks().queue()
with image_blocks as demo:
    gr.Markdown("## BeautyMaster 💄👗🌟")
    gr.Markdown("Beauty Master make you beautiful every day. Check out the [source codes](https://github.com/RayTang88/BeautyMaster)")
    with gr.Row():
        with gr.Column():
            imgs = gr.ImageEditor(sources='upload', type="pil", label='Human. Mask with pen or use auto-masking', interactive=True)
            with gr.Column():
                with gr.Row():
                    is_checked = gr.Checkbox(label="Yes", info="Use auto-generated mask (Takes 5 seconds)",value=True)
                with gr.Row():
                    is_checked_crop = gr.Checkbox(label="Yes", info="Use auto-crop & resizing",value=False)
            season = gr.Dropdown(options=["春季","夏季","秋季","冬季"], label="季节")
            weather = gr.Dropdown(options=["零下10摄氏度","0摄氏度","10摄氏度","20摄氏度","30摄氏度"], label="温度")
            determine = gr.Dropdown(options=["约会","逛街","晚宴","工作"], label="目的")
            additional_requirements = "简洁大方美丽漂亮"

            example = gr.Examples(
                inputs=imgs,
                examples_per_page=10,
                examples=human_list_path
            )

        with gr.Column():
            garm_img = gr.Image(label="Garment", sources='upload', type="pil")
            with gr.Row(elem_id="prompt-container"):
                with gr.Row():
                    prompt = gr.Textbox(placeholder="Description of garment ex) Short Sleeve Round Neck T-shirts", show_label=False, elem_id="prompt")
            example = gr.Examples(
                inputs=garm_img,
                examples_per_page=8,
                examples=upperlist_path)
        with gr.Column():
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            masked_img = gr.Image(label="Masked image output", elem_id="masked-img",show_share_button=False)
        with gr.Column():
            # image_out = gr.Image(label="Output", elem_id="output-img", height=400)
            image_out = gr.Image(label="Output", elem_id="output-img",show_share_button=False)

    with gr.Column():
        match_button = gr.Button(value="Match")
        with gr.Accordion(label="Advanced Settings", open=False):
            with gr.Row():
                denoise_steps = gr.Number(label="Denoising Steps", minimum=20, maximum=40, value=30, step=1)
                seed = gr.Number(label="Seed", minimum=-1, maximum=2147483647, step=1, value=42)

    match_button.click(fn=main, inputs=[interface, weather, season, determine, additional_requirements, imgs, garm_img, "match"], outputs=[image_out,masked_img], api_name='match')

image_blocks.launch()

