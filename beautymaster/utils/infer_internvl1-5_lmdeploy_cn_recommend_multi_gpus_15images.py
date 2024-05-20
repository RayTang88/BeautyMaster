import os
os.environ["CUDA_VISIBLE_DEVICES"]="0,1"
os.chdir('/root/')

import nest_asyncio
nest_asyncio.apply()

from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image


backend_config = TurbomindEngineConfig(session_len=163840,  # 图片分辨率较高时请调高session_len
                                       cache_max_entry_count=0.2, 
                                       tp=2)  # 两个显卡

gen_config = GenerationConfig(top_p=0.8,
                              top_k=40,
                              temperature=0.8,
                              max_new_tokens=1024) 

pipe = pipeline('/root/share/new_models/OpenGVLab/InternVL-Chat-V1-5', backend_config=backend_config) 
image_urls=[
    "/root/IDM-VTON/Dataset/zalando/555/003315_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/004798_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/005000_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/016158_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/016315_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/017016_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/017418_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/017462_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/026068_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/027163_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/027655_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/033980_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/041335_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/048453_1.jpg",
    "/root/IDM-VTON/Dataset/zalando/555/049497_1.jpg",
]

images = [load_image(img_url) for img_url in image_urls]
response = pipe(('这些图片里,每张图片中都含有一件衣服中,可能是上衣，下衣或者女士长裙，请推荐一身合适的衣服（"上衣+下衣"或者"长裙"），用于一位女士在秋天打高尔夫球，并说明理由, 输出格式如下，第{n}张{上衣，下衣或者长裙}和第{m}张{上衣，下衣或者长裙}，适合{场景}，因为{理由}，如果候选图片没有下身衣服或者长裙，可以只推荐一个', images))

# print(response)
print(response.text)
