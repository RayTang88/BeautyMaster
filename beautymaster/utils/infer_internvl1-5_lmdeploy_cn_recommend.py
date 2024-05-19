import os
os.chdir('/root/')

import nest_asyncio
nest_asyncio.apply()

from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image

backend_config = TurbomindEngineConfig(session_len=8192, cache_max_entry_count=0.2) # 图片分辨率较高时请调高session_len

pipe = pipeline('/root/share/new_models/OpenGVLab/InternVL-Chat-V1-5', backend_config=backend_config)  # 56099MiB / 81920MiB

image_urls=[
    "/root/IDM-VTON/Dataset/zalando/train/cloth/00000_00.jpg",
    "/root/IDM-VTON/Dataset/zalando/train/cloth/00001_00.jpg",  #  # 60647MiB / 81920MiB
    "/root/IDM-VTON/Dataset/zalando/train/cloth/00002_00.jpg",
    "/root/IDM-VTON/Dataset/zalando/train/cloth/00003_00.jpg",  # 63865MiB / 81920MiB  response.text 为空
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00014_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00005_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00016_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00007_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00018_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00009_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00010_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00011_00.jpg",
    # "/root/IDM-VTON/Dataset/zalando/train/cloth/00012_00.jpg"
]

# 多张图片测试失败
images = [load_image(img_url) for img_url in image_urls]
response = pipe(('这些图片里,每张图片中都含有一件衣服中,可能是上身，下身或者女士长裙，请推荐合适的衣服，用于一位女士在秋天打高尔夫球，并说明理由', images))

# print(response)  # Response(text='', generate_token_len=0, input_token_len=10046, session_id=0, finish_reason='length', token_ids=[], logprobs=None)
print(response.text)

# 两张图片测试成功
# response = pipe(('这两张图片里的衣服哪个更适合下雨天穿？哪个更适合38度的室外活动？理由是什么？', images))  # 60647MiB / 81920MiB     # 56099MiB / 81920MiB
# print(response.text)
# # 对于雨天，黑色T恤似乎更合适，因为它有长袖，可以提供一些防雨保护。此外，材料看起来是棉质的，可能不太防水，但比白色T恤吸收水分的能力更好，白色T恤可能会看起来更湿。
# # 对于38度的户外活动，白色T恤更合适。它有短袖，比黑色T恤的袖子更透气，可以提供更好的通风和冷却。白色颜色也可能在高温下反射更多阳光，比黑色吸收热量更有效。
