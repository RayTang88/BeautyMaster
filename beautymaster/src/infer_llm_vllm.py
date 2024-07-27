import os
from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig, PytorchEngineConfig
from json_repair import repair_json
from .ready_prompt import ready_prompt_func
from .prompt import match_prompt_template, match_prompt_template_raged, body_out_format, llm_prompt_template_4o, recommend_format, upper_lower_format
from beautymaster.utils.parsing_rag import parsing_rag_func
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

class LLM():
    def __init__(self, weights_path, weight_name, awq, openxlab=False):
        # decrease the ratio of the k/v cache occupation to 20%
        self.weights_path = weights_path
        self.weight_name = weight_name

        backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1,
                                        session_len=2048 if not os.getenv("LLM_SESSION_LEN") else os.getenv("LLM_SESSION_LEN"))
        
        self.gen_config = GenerationConfig(top_p=0.8,
                        top_k=40,
                        temperature=0,
                        max_new_tokens=512)
        
        
        if awq:
            backend_config = TurbomindEngineConfig(cache_max_entry_count=0.1,
                                               model_format='awq',
                                               session_len=2048 if not os.getenv("LLM_SESSION_LEN") else os.getenv("LLM_SESSION_LEN"))
        elif openxlab:
            backend_config = PytorchEngineConfig(session_len=2048 if not os.getenv("VLM_SESSION_LEN") else os.getenv("VLM_SESSION_LEN"),  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.05, 
                                        tp=1,
                                        # quant_policy=0,
                                        )  # 两个显卡

        
        # self.pipe = pipeline(weights_path + weight_name, backend_config=backend_config, log_level='INFO')

        # 2.5
        self.tokenizer = AutoTokenizer.from_pretrained(weights_path + weight_name, trust_remote_code=True)
        self.pipe = LLM(
            model=weights_path + weight_name,
            trust_remote_code=True, quantization="AWQ"
        )
        self.sampling_params = SamplingParams(temperature=0.2, max_tokens=64)


    def llm_parsing_json(self, model_candidate_clothes_jsons, get_num_list, meaning_list):
    
        parsed_list = []
        prompt_list = ready_prompt_func(model_candidate_clothes_jsons, get_num_list, meaning_list)

        responses = self.pipe(prompt_list, gen_config=self.gen_config)
        
        for response in responses:
            parsed_list.append(response.text)
            
        return parsed_list

    #This function is the main interface for llm to make recommendations, Need to use llm to parse json.
    def infer_llm_recommend(self, season, weather, determine, model_candidate_clothes_jsons, get_num_list, meaning_list):
        
        
        parsed_list = self.llm_parsing_json(model_candidate_clothes_jsons, get_num_list, meaning_list) 
        
        total = sum(a for a in get_num_list)
            
        assert total == len(parsed_list)
        
        match_prompt = match_prompt_template.format(season, weather, determine, parsed_list[0], parsed_list[1], parsed_list[2],parsed_list[3], 
                            parsed_list[4], parsed_list[5], parsed_list[6], parsed_list[7], parsed_list[8], parsed_list[9], 
                            parsed_list[10], parsed_list[11], parsed_list[12], parsed_list[13], parsed_list[14], parsed_list[15])
        
        responses = self.pipe([match_prompt])
        
        return responses[0].text

    #This function is the main interface for llm to make recommendations.
    def infer_llm_single_recommend(self, season, weather, determine, body_shape_response, additional_requirements, available_types):
        
        good_json_obj = repair_json(body_shape_response, return_objects=True)
        print("good_json_obj vlm discribe", good_json_obj)
        item_descs = good_json_obj["items"]
        gender = good_json_obj["gender"]
        
        body_shape_descs = '、'.join(item_descs)
        
        data = {"season":season, "weather":weather, "gender": gender, "determine": determine, "shape":body_shape_descs, "available_types": available_types, "additional_requirements":additional_requirements, "recommend_format": recommend_format}
        prompt = llm_prompt_template_4o.format(**data)

        messages = [{
            'role': 'user',
            'content': f'{prompt}'
        }]
        match_prompt = self.tokenizer.apply_chat_template(messages,
                                            tokenize=False,
                                            add_generation_prompt=True) 
        
  
        
        responses = self.pipe.generate(match_prompt, sampling_params=self.sampling_params)
        # responses = self.pipe([match_prompt])
        
        return responses[0].outputs[0].text, body_shape_descs, gender

    #This function is the main interface for llm to make recommendations, after rag, we have get content from database of used in rag.
    def infer_llm_recommend_raged(self, season, weather, determine, additional_requirements, rag_4o_like_recommended, body_shape_descs, gender, recommend_top_n):
        
        upper, lower, skirt, dresses = parsing_rag_func(rag_4o_like_recommended)
        
        data = {"season":season, "weather":weather, "gender": gender, "determine": determine, "shape":body_shape_descs,"upper":upper, "lower":lower, "skirt":skirt, "dresses":dresses, "additional_requirements":additional_requirements, "upper_lower_format": upper_lower_format, "recommend_top_n": recommend_top_n}

        prompt = match_prompt_template_raged.format(**data)

        messages = [{
            'role': 'user',
            'content': f'{prompt}'
        }]
        match_prompt = self.tokenizer.apply_chat_template(messages,
                                            tokenize=False,
                                            add_generation_prompt=True) 
        
  
        
        responses = self.pipe.generate(match_prompt, sampling_params=self.sampling_params)
        
        # responses = self.pipe([match_prompt])

        good_json_obj = repair_json(responses[0].responses[0].text, return_objects=True)
        
        return good_json_obj