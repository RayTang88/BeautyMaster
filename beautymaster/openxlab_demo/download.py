import os
from huggingface_hub import snapshot_download

snapshot_download(repo_id="internlm/internlm2-chat-20b-4bits", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-20b-4bits/", resume_download=True)

snapshot_download(repo_id="OpenGVLab/InternVL-Chat-V1-5-AWQ", local_dir=os.environ.get('MODEL_ROOT')+"/InternVL-Chat-V1-5-AWQ/", resume_download=True)

# snapshot_download(repo_id="yisol/IDM-VTON", local_dir=os.environ.get('MODEL_ROOT')+"/IDM-VTON/", resume_download=True)

