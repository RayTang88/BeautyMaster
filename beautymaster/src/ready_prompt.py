import json
from .prompt import pasing_prompt_template

#This function is to prepare prompts for converting json description into txt description. 
#It is more efficient to use list to ask llm questions.
def ready_prompt_func(model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  prompt_list=[]
  
  expanded_list = [item for sublist in [[meaning_list[i]] * num for i, num in enumerate(get_num_list)] for item in sublist]
  
  for model_candidate_clothes_json, meaning in zip(model_candidate_clothes_jsons, expanded_list):
    
    try:
        file_descriptor = open(model_candidate_clothes_json, 'rb')
    except OSError:
        pass

    with file_descriptor:
        decoded_object = json.load(file_descriptor)
        
    parsing_prompt = parsing_prompt_template.format(decoded_object, meaning)
    
    file_descriptor.close()
    
    prompt_list.append(parsing_prompt)
    
  return prompt_list  