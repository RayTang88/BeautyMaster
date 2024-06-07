import os
import random
import sys
import argparse
import pandas as pd
import json


sys.path.append('/root/code/BeautyMaster/beautymaster/demo')
from infer import Interface, parse_opt

# from src.prompt import parsing_prompt_template, match_prompt_template, vlm_prompt_template_4o


from lmdeploy import pipeline, TurbomindEngineConfig

def creat_database(csv_name):
  opt = parse_opt()
  interface = Interface(**vars(opt))
  source="/group_share/data_org/DressCode/"

  # model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, flag) #for test, now get list randomly.

  
  # # decrease the ratio of the k/v cache occupation to 20%
  # backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, session_len=8190)
  # pipe = pipeline('/group_share/model/internlm2-chat-20b_TurboMind/',
  #                 backend_config=backend_config)

  # parsed_list = llm_recommand(pipe, model_candidate_clothes_jsons, get_num_list, meaning_list)
  
  # print(describe)
  data = []
  for root, dirs, names in os.walk(source):
        for name in names:
              if name[-5:] == "1.jpg":
                    # Interface.caption(root+name)
                    if root.split("/")[-1] == "images":
                          image_path = os.path.join(root, name)

                          caption_json, caption_string = interface.caption(image_path)
                          
                          data_dict = {}
                          idx = os.path.basename(image_path).replace(".jpg", "")
                          data_dict["id"] = idx
                          data_dict["content"] = caption_string

                          data.append(data_dict)
  df = pd.DataFrame(data)

  df.to_csv(csv_name)
                    
                  
                   





    





def main():
  csv_name = "/root/data_org/test_data/sample_style.csv"
  creat_database(csv_name)
      


if __name__ == "__main__":
  main()

