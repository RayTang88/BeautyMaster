import os

from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image
from .prompt import vlm_prompt_template


def infer_vlm_func(weights_path, weight_name, model_candidate_clothes_list, season, weather, determine):

    backend_config = TurbomindEngineConfig(session_len=163840,  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.2, 
                                        tp=2,
                                        # quant_policy=0,
                                        )  # 两个显卡

    pipe = pipeline(weights_path + weight_name, backend_config=backend_config, )
    print(model_candidate_clothes_list)

    images = [load_image(model_candidate_clothes) for model_candidate_clothes in model_candidate_clothes_list]
    
    # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
    # vlm_prompt = prompt.vlm_prompt_template.format("16", "1", "2,3,4,5,6", "7,8,9,10,11", "12,13,14,15,16", season, weather, determine, prompt.a_format)
    vlm_prompt = vlm_prompt_template
    # print(vlm_prompt)
    response = pipe((vlm_prompt, images))

    # print(response.text)
    
    return response.text