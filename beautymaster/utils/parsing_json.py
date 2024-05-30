import os
import random
import sys
import argparse
import pandas as pd
import json


sys.path.append("/root/code/BeautyMaster/beautymaster")
# from src.infer_vlm import infer_vlm_func
from src.infer_rag import infer_rag_func
from src.prompt import parsing_prompt_template, match_prompt_template


from lmdeploy import pipeline, TurbomindEngineConfig


def ready_prompt(model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  prompt_list=[]
  
  expanded_list = [item for sublist in [[meaning_list[i]] * num for i, num in enumerate(get_num_list)] for item in sublist]
  
  for model_candidate_clothes_json, meaning in zip(model_candidate_clothes_jsons, expanded_list):
    
    try:
        file_descriptor = open(model_candidate_clothes_json, 'rb')
    except OSError:
        pass

    with file_descriptor:
        decoded_object = json.load(file_descriptor)
        
    pasing_prompt = parsing_prompt_template.format(decoded_object, meaning)
    
    file_descriptor.close()
    
    prompt_list.append(pasing_prompt)
    
  return prompt_list  
    

def llm_parsing_json(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  parsed_list = []
  prompt_list = ready_prompt(model_candidate_clothes_jsons, get_num_list, meaning_list)

  responses = pipe(prompt_list)
  
  for response in responses:
    parsed_list.append(response.text)
    
  return parsed_list

def llm_recommand(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list):
  
  weather = "10~15摄氏度"
  season = "春季"
  determine = "逛街"
  parsed_list = llm_parsing_json(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list)    
  
  match_prompt = match_prompt_template.format(season, weather, determine, parsed_list[0], parsed_list[1], parsed_list[2],parsed_list[3], 
                      parsed_list[4], parsed_list[5], parsed_list[6], parsed_list[7], parsed_list[8], parsed_list[9], 
                      parsed_list[10], parsed_list[11], parsed_list[12], parsed_list[13], parsed_list[14], parsed_list[15])
  
  responses = pipe([match_prompt])
  
  return   responses[0].text

  # return parsed_list



def recommand():

  source="/root/data/test_data/"
  get_num_list = [1, 5, 5, 5]
  meaning_list = ["我的形象特征", "上衣", "裤子", "裙子"]
  flag = "json"
  model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, flag) #for test, now get list randomly.
  
  # # decrease the ratio of the k/v cache occupation to 20%
  backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, session_len=8190)
  pipe = pipeline('/group_share/model/internlm2-chat-20b_TurboMind/',
                  backend_config=backend_config)

  describe = llm_recommand(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list)
  
  return describe
  

def creat_database(csv_name):
    
  source="/root/data/test_data/"
  get_num_list = [1, 15, 15, 15]
  meaning_list = ["我的形象特征", "上衣", "裤子", "裙子"]
  flag = "json"
  model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, flag) #for test, now get list randomly.

  
  # # decrease the ratio of the k/v cache occupation to 20%
  backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, session_len=8190)
  pipe = pipeline('/group_share/model/internlm2-chat-20b_TurboMind/',
                  backend_config=backend_config)

  # parsed_list = llm_recommand(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list)
  
  # print(describe)
  parsed_list = llm_parsing_json(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list)


  data = []
  for parsing, json in zip(parsed_list[1:], model_candidate_clothes_jsons[1:]):
        data_dict = {}
        idx = os.path.basename(json).replace(".json", "")
        data_dict["id"] = idx
        data_dict["content"] = parsing

        data.append(data_dict)

    
  df = pd.DataFrame(data)

  df.to_csv(csv_name)

def main():
  csv_name = "/root/data_org/test_data/sample_style.csv"
  creat_database(csv_name)
      


if __name__ == "__main__":
  main()

