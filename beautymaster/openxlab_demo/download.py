import os
from huggingface_hub import snapshot_download

# snapshot_download(repo_id="internlm/internlm2-chat-20b-4bits", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-20b-4bits/", resume_download=True)

# snapshot_download(repo_id="OpenGVLab/InternVL-Chat-V1-5-AWQ", local_dir=os.environ.get('MODEL_ROOT')+"/InternVL-Chat-V1-5-AWQ/", resume_download=True)

snapshot_download(repo_id="internlm/internlm2-chat-1_8b", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-1_8b/", resume_download=True)

snapshot_download(repo_id="OpenGVLab/Mini-InternVL-Chat-2B-V1-5", local_dir=os.environ.get('MODEL_ROOT')+"/Mini-InternVL-Chat-2B-V1-5/", resume_download=True)

# snapshot_download(repo_id="yisol/IDM-VTON", local_dir=os.environ.get('MODEL_ROOT')+"/IDM-VTON/", resume_download=True)

