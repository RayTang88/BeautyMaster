import os
from huggingface_hub import snapshot_download

# snapshot_download(repo_id="internlm/internlm2-chat-20b-4bits", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-20b-4bits/", resume_download=True)

# snapshot_download(repo_id="OpenGVLab/InternVL-Chat-V1-5-AWQ", local_dir=os.environ.get('MODEL_ROOT')+"/InternVL-Chat-V1-5-AWQ/", resume_download=True)

# snapshot_download(repo_id="internlm/internlm2-chat-1_8b", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-1_8b/", resume_download=True)
snapshot_download(repo_id="maidalun1020/bce-embedding-base_v1", local_dir=os.environ.get('MODEL_ROOT')+"/bce-embedding-base_v1/", resume_download=True)
snapshot_download(repo_id="maidalun1020/bce-reranker-base_v1", local_dir=os.environ.get('MODEL_ROOT')+"/bce-reranker-base_v1/", resume_download=True)
# snapshot_download(repo_id="OpenGVLab/Mini-InternVL-Chat-2B-V1-5", local_dir=os.environ.get('MODEL_ROOT')+"/Mini-InternVL-Chat-2B-V1-5/", resume_download=True)
# snapshot_download(repo_id="internlm/internlm2-chat-1_8b", local_dir=os.environ.get('MODEL_ROOT')+"/internlm2-chat-1_8b/", resume_download=True)

# snapshot_download(repo_id="OpenGVLab/Mini-InternVL-Chat-2B-V1-5", local_dir=os.environ.get('MODEL_ROOT')+"/Mini-InternVL-Chat-2B-V1-5/", resume_download=True)

# snapshot_download(repo_id="yisol/IDM-VTON", local_dir=os.environ.get('MODEL_ROOT')+"/IDM-VTON/", resume_download=True)

# from openxlab.model import download

# download(model_repo='raytang88/Qwen2-7B-Instruct-AWQ', model_name='Qwen2-7B-Instruct-AWQ', output=os.environ.get('MODEL_ROOT')+"/Qwen2-7B-Instruct-local-AWQ/")
# download(model_repo='raytang88/MiniCPM-Llama3-V-2_5-AWQ', model_name='MiniCPM-Llama3-V-2_5-AWQ', output=os.environ.get('MODEL_ROOT')+"/MiniCPM-Llama3-V-2_5-local-AWQ/")
