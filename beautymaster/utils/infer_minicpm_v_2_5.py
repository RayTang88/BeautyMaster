# test.py
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

def infer_minicpm():

    model = AutoModel.from_pretrained('/root/model/MiniCPM-Llama3-V-2_5/', trust_remote_code=True, torch_dtype=torch.float16)
    model = model.to(device='cuda')

    tokenizer = AutoTokenizer.from_pretrained('/root/model/MiniCPM-Llama3-V-2_5/', trust_remote_code=True)
    model.eval()

    image = Image.open('/root/data/fullbody_cleaned_yolo/1_1_F_Bing_pic.jpg').convert('RGB')
    question = 'What is in the image?'
    msgs = [{'role': 'user', 'content': question}]

    res = model.chat(
        image=image,
        msgs=msgs,
        tokenizer=tokenizer,
        sampling=True,
        temperature=0.7
    )
    print(res)