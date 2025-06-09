# test.py
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

def infer_minicpm_25():

    model = AutoModel.from_pretrained('/data0/tc_workspace/internlm/model/MiniCPM-Llama3-V-2_5/', trust_remote_code=True, torch_dtype=torch.bfloat16)
    model = model.to(device='cuda')

    tokenizer = AutoTokenizer.from_pretrained('/data0/tc_workspace/internlm/model/MiniCPM-Llama3-V-2_5/', trust_remote_code=True)
    model.eval()

    image = Image.open('/data0/tc_workspace/internlm/code/MiniCPM-o/assets/minicpmo2_6/show_demo.jpg').convert('RGB')
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

def infer_minicpm_26_o():
    
    torch.manual_seed(100)

    model = AutoModel.from_pretrained('/data0/tc_workspace/internlm/model/MiniCPM-o-2_6', trust_remote_code=True) # sdpa or flash_attention_2, no eager

    tokenizer = AutoTokenizer.from_pretrained('/data0/tc_workspace/internlm/model/MiniCPM-o-2_6', trust_remote_code=True)
    model.to(torch.bfloat16).cuda().eval()

    image = Image.open("/data0/tc_workspace/internlm/code/MiniCPM-o/assets/minicpmo2_6/show_demo.jpg").convert('RGB')

    # First round chat 
    question = "What is the landform in the picture?"
    msgs = [{'role': 'user', 'content': [image, question]}]

    answer1 = model.chat(
        msgs=msgs,
        tokenizer=tokenizer
    )
    print(answer1)

    # Second round chat, pass history context of multi-turn conversation
    msgs.append({"role": "assistant", "content": [answer1]})
    msgs.append({"role": "user", "content": ["What should I pay attention to when traveling here?"]})

    answer2 = model.chat(
        msgs=msgs,
        tokenizer=tokenizer
    )
    print(answer2) 
    
    
def infer_minicpm_26_o_vllm():
    from transformers import AutoTokenizer
    from PIL import Image
    from vllm import LLM, SamplingParams

    MODEL_NAME = "/data0/tc_workspace/internlm/model/MiniCPM-Llama3-V-2_5-AWQ"
    # Also available for previous models
    # MODEL_NAME = "openbmb/MiniCPM-Llama3-V-2_5"
    # MODEL_NAME = "HwwwH/MiniCPM-V-2"

    image = Image.open("/data0/tc_workspace/internlm/code/MiniCPM-o/assets/minicpmo2_6/show_demo.jpg").convert('RGB')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    llm = LLM(
        model= MODEL_NAME, 
        max_model_len=2048,
        # max_num_seqs=2,
        trust_remote_code=True,
        disable_mm_preprocessor_cache=True,
        limit_mm_per_prompt={"image": 5}
    )
    messages = [{
        "role":
        "user",
        "content":
        # Number of images
        "(<image>./</image>)" + \
        "\nWhat is the content of this image?" 
    }]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Single Inference
    inputs = {
        "prompt": prompt,
        "multi_modal_data": {
            "image": image
            # Multi images, the number of images should be equal to that of `(<image>./</image>)`
            # "image": [image, image] 
        },
    }
    # Batch Inference
    # inputs = [{
    #     "prompt": prompt,
    #     "multi_modal_data": {
    #         "image": image
    #     },
    # } for _ in 2]

    # 2.6
    stop_tokens = ['<|im_end|>', '<|endoftext|>']
    stop_token_ids = [tokenizer.convert_tokens_to_ids(i) for i in stop_tokens]
    # 2.0
    # stop_token_ids = [tokenizer.eos_id]
    # 2.5
    # stop_token_ids = [tokenizer.eos_id, tokenizer.eot_id]

    sampling_params = SamplingParams(
        stop_token_ids=stop_token_ids, 
        #use_beam_search=True,
        temperature=0.7,
        top_p=0.7,
        max_tokens=1024
    )

    outputs = llm.generate(inputs, sampling_params=sampling_params)

    print(outputs[0].outputs[0].text)
    
if __name__ == "__main__":
    infer_minicpm_26_o_vllm()       