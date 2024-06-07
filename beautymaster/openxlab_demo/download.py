from huggingface_hub import snapshot_download
# snapshot_download(repo_id="liuhaotian/llava-v1.6-vicuna-7b", local_dir="/data0/tc_workspace/internlm/model/llava-v1.6-vicuna-7b", resume_download=True)
snapshot_download(repo_id="internlm/internlm2-chat-20b-4bits", local_dir="./workspace/internlm2-chat-20b-4bits/", resume_download=True)

snapshot_download(repo_id="OpenGVLab/InternVL-Chat-V1-5-AWQ", local_dir="./workspace/InternVL-Chat-V1-5-AWQ/", resume_download=True)

