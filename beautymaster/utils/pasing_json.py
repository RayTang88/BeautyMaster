import os
import random
import sys
import argparse

sys.path.append("/root/code/BeautyMaster/beautymaster")
# from src.infer_vlm import infer_vlm_func
from src.infer_rag import infer_rag_func
from src.prompt import pasing_prompt
import json_repair

from lmdeploy import pipeline, TurbomindEngineConfig

def ready_prompt(model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  prompt_list=[]
  
  expanded_list = [item for sublist in [[meaning_list[i]] * num for i, num in enumerate(get_num_list)] for item in sublist]
  
  for  model_candidate_clothes_json, meaning in zip(model_candidate_clothes_jsons, expanded_list):
    
    try:
        file_descriptor = open(model_candidate_clothes_json, 'rb')
    except OSError:
        pass

    with file_descriptor:
        decoded_object = json_repair.load(file_descriptor)
        

    
    prompt = pasing_prompt.format(decoded_object, meaning)
    
    file_descriptor.close()
    
    prompt_list.append(prompt)
    
  return prompt_list  
    

def infer_llm(model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  # # decrease the ratio of the k/v cache occupation to 20%
  backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2)
  pipe = pipeline('/root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-20b',
                  backend_config=backend_config)
  
  prompt_list = ready_prompt(model_candidate_clothes_jsons, get_num_list, meaning_list)
  responses = pipe(prompt_list)
  
  for response in responses:
    print(response.text)  
    
  return responses    


def main():

  source="/root/data/test_data/"
  get_num_list = [1, 3, 3, 3]
  meaning_list = ["全身照", "上衣", "裤子", "裙子"]
  flag = "json"
  model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, flag) #for test, now get list randomly.
  

  describe = infer_llm(model_candidate_clothes_jsons, get_num_list, meaning_list)
  


if __name__ == "__main__":
  main()

