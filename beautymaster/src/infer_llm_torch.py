import os
import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from json_repair import repair_json

# from ready_prompt import ready_prompt_func
from .prompt import match_prompt_template, match_prompt_template_raged, body_out_format, llm_prompt_template_4o, recommend_format, upper_lower_format
sys.path.append(os.environ.get('CODE_ROOT')+'BeautyMaster/')
from beautymaster.utils.parsing_rag import parsing_rag_func

class LLM():
    def __init__(self, weights_path, weight_name, awq, openxlab=False):
        # decrease the ratio of the k/v cache occupation to 20%

        # backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1,
        #                                 session_len=2048 if not os.getenv("LLM_SESSION_LEN") else os.getenv("LLM_SESSION_LEN"))
        
        # self.gen_config = GenerationConfig(top_p=0.8,
        #                 top_k=40,
        #                 temperature=0,
        #                 max_new_tokens=512)
        
        
        # if awq:
        #     backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1,
        #                                        model_format='awq',
        #                                        session_len=2048 if not os.getenv("LLM_SESSION_LEN") else os.getenv("LLM_SESSION_LEN"))
        # elif openxlab:
        #     backend_config = PytorchEngineConfig(session_len=2048 if not os.getenv("VLM_SESSION_LEN") else os.getenv("VLM_SESSION_LEN"),  # 图片分辨率较高时请调高session_len
        #                                 cache_max_entry_count=0.05, 
        #                                 tp=1,
        #                                 # quant_policy=0,
        #                                 )  # 两个显卡

        
        # self.pipe = pipeline(weights_path + weight_name, backend_config=backend_config, log_level='INFO')
        
        self.tokenizer = AutoTokenizer.from_pretrained(weights_path + weight_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(weights_path + weight_name, torch_dtype=torch.float16, trust_remote_code=True).cuda()
        self.model = model.eval()

    # def llm_parsing_json(self, model_candidate_clothes_jsons, get_num_list, meaning_list):
    
    #     parsed_list = []
    #     prompt_list = ready_prompt_func(model_candidate_clothes_jsons, get_num_list, meaning_list)

    #     # responses = self.pipe(prompt_list, gen_config=self.gen_config)
    #     responses, _ = self.model.chat(self.tokenizer, prompt_list, history=[])
        
    #     for response in responses:
    #         parsed_list.append(response.text)
            
    #     return parsed_list

    #This function is the main interface for llm to make recommendations, Need to use llm to parse json.
    
    def chat(self, prompt, llm_model_type="yi"):
        
        if "qwen" == llm_model_type:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to("cuda")

            generated_ids = self.model.generate(
                model_inputs.input_ids,
                max_new_tokens=512
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            responses = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        elif "yi" == llm_model_type:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            input_ids = self.tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
            output_ids = self.model.generate(input_ids.to('cuda'), eos_token_id=self.tokenizer.eos_token_id)
            responses = self.tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)
                
        else:
            responses, _ = self.model.chat(self.tokenizer, prompt, history=[])
        
        return responses    
        
    
    def infer_llm_recommend(self, season, weather, determine, model_candidate_clothes_jsons, get_num_list, meaning_list):
        
        
        parsed_list = self.llm_parsing_json(model_candidate_clothes_jsons, get_num_list, meaning_list) 
        
        total = sum(a for a in get_num_list)
            
        assert total == len(parsed_list)
        
        match_prompt = match_prompt_template.format(season, weather, determine, parsed_list[0], parsed_list[1], parsed_list[2],parsed_list[3], 
                            parsed_list[4], parsed_list[5], parsed_list[6], parsed_list[7], parsed_list[8], parsed_list[9], 
                            parsed_list[10], parsed_list[11], parsed_list[12], parsed_list[13], parsed_list[14], parsed_list[15])
        
        # responses = self.pipe([match_prompt])
        responses, _ = self.chat(match_prompt)
        
        return responses[0].text

    #This function is the main interface for llm to make recommendations.
    def infer_llm_single_recommend(self, season, weather, determine, body_shape_response, additional_requirements, available_types):
        
        good_json_obj = repair_json(body_shape_response, return_objects=True)
        print("good_json_obj vlm discribe", good_json_obj)
        item_descs = good_json_obj["items"]
        gender = good_json_obj["gender"]
        
        body_shape_descs = '、'.join(item_descs)
        
        data = {"season":season, "weather":weather, "gender": gender, "determine": determine, "shape":body_shape_descs, "available_types": available_types, "additional_requirements":additional_requirements, "recommend_format": recommend_format}
        match_prompt = llm_prompt_template_4o.format(**data)
        
        # responses = self.pipe([match_prompt])
        responses = self.chat(match_prompt, "qwen")
        
        return responses, body_shape_descs, gender

    #This function is the main interface for llm to make recommendations, after rag, we have get content from database of used in rag.
    def infer_llm_recommend_raged(self, season, weather, determine, additional_requirements, rag_4o_like_recommended, body_shape_descs, gender):
        
        upper, lower, skirt, dresses = parsing_rag_func(rag_4o_like_recommended)
        
        data = {"season":season, "weather":weather, "gender": gender, "determine": determine, "shape":body_shape_descs,"upper":upper, "lower":lower, "skirt":skirt, "dresses":dresses, "additional_requirements":additional_requirements, "upper_lower_format": upper_lower_format}

        match_prompt = match_prompt_template_raged.format(**data)
        
        # responses = self.pipe([match_prompt])
        responses = self.chat(match_prompt, "qwen")

        good_json_obj = repair_json(responses, return_objects=True)
        
        return good_json_obj
    

if __name__ == "__main__":
    weights_path="/group_share/model/"
    vlm_weight_name='internlm2_5-7b-chat/'
    llm_awq=False
    openxlab=True
    llm = LLM(weights_path, vlm_weight_name, llm_awq, openxlab)
    
    
    weather = "30~35摄氏度"
    season = "夏季"
    determine = "约会"
    additional_requirements = "搭配简单大方"
    
    body_shape_response = {"items": ["黑色短发", "短发", "简洁发型", "白皙皮肤", "匀称身材", "身高偏高", "腰部纤细", "腿部偏长", "O型腿", "细沙漏型体型"], "gender": "男性"}
    body_shape_response = json.dumps(body_shape_response)
    
    available_types= ["上衣", "裤子", "半身裙", "连衣裙"]
    match_text, body_shape_descs, gender = llm.infer_llm_single_recommend(season, weather, determine, body_shape_response, additional_requirements, available_types)
    print("response:",match_text)