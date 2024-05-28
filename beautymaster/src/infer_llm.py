from .ready_prompt import ready_prompt_func
from .prompt import match_prompt_template
from lmdeploy import pipeline, TurbomindEngineConfig

def llm_parsing_json(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list):
  
    parsed_list = []
    prompt_list = ready_prompt_func(model_candidate_clothes_jsons, get_num_list, meaning_list)

    responses = pipe(prompt_list)
    
    for response in responses:
        parsed_list.append(response.text)
        
    return parsed_list

#This function is the main interface for llm to make recommendations.
def infer_llm_recommend(weights_path, weight_name, season, weather, determine, model_candidate_clothes_jsons, get_num_list, meaning_list):
    
    # # decrease the ratio of the k/v cache occupation to 20%
    backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, session_len=8190)
    pipe = pipeline(weights_path + weight_name, backend_config=backend_config)  
    
    parsed_list = llm_parsing_json(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list) 
    
    total = sum(a for a in get_num_list)
        
    assert total == len(parsed_list)
    
    match_prompt = match_prompt_template.format(season, weather, determine, parsed_list[0], parsed_list[1], parsed_list[2],parsed_list[3], 
                        parsed_list[4], parsed_list[5], parsed_list[6], parsed_list[7], parsed_list[8], parsed_list[9], 
                        parsed_list[10], parsed_list[11], parsed_list[12], parsed_list[13], parsed_list[14], parsed_list[15])
    
    responses = pipe([match_prompt])
    
    return responses[0].text