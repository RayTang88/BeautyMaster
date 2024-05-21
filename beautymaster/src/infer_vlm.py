import os

from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image
from . import prompt

# os.environ["CUDA_VISIBLE_DEVICES"]="0,1"


def infer_vlm_func(weight, model_candidate_clothes_list, season, weather, determine):


    backend_config = TurbomindEngineConfig(session_len=163840,  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.2, 
                                        tp=1,
                                        # quant_policy=0,
                                        )  # 两个显卡

    # pipe = pipeline(weight+"/Mini-InternVL-Chat-2B-V1-5/", backend_config=backend_config, ) 
    # pipe = pipeline(weight+"/InternVL-Chat-V1-5/", backend_config=backend_config, ) 
    # pipe = pipeline(weight+"/internlm-xcomposer2-vl-7b/", backend_config=backend_config, )
    pipe = pipeline(weight+"/internlm-xcomposer2-vl-1_8b/", backend_config=backend_config, )
    pipe = pipeline(weight+"/Qwen-VL-Chat/", backend_config=backend_config) 

    images = [load_image(model_candidate_clothes) for model_candidate_clothes in model_candidate_clothes_list]
    
    # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
    vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine)
    response = pipe((vlm_prompt, images))

    # print(response.text)
    
    return response.text