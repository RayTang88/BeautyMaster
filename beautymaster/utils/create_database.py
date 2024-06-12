import os
import random
import sys
import argparse
import pandas as pd
import json
from tqdm import tqdm

sys.path.append("/root/code/BeautyMaster")
from beautymaster.demo.infer import Interface, parse_opt

def creat_database(right_csv_name, error_csv_name):
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
  data_right = []
  data_error = []
  i = 0
  for root, dirs, names in tqdm(os.walk(source)):
        for name in tqdm(names):
              i+=1
              try:
                if name[-5:] == "1.jpg":
                      # Interface.caption(root+name)
                      if root.split("/")[-1] == "images":
                            image_path = os.path.join(root, name)
                            
                            category = root.split("/")[-2]
                            
                            if "lower_body" != category:
                                  continue
                            
                            caption_json, caption_string = interface.caption(image_path)
                            print("idx:%d %s %s"%(i, image_path, caption_string))
                            flag = False
                            if category == "upper_body" and caption_json["category"] == "上衣":
                                  flag = True
                            if category == "lower_body" and caption_json["category"] == "裤子":
                                  flag = True
                            if category == "lower_body" and caption_json["category"] == "半身裙":
                                  flag = True
                            if category == "dresses" and caption_json["category"] == "连衣裙":
                                  flag = True      
                            data_dict = {}
                            idx = os.path.basename(image_path).replace(".jpg", "")
                            data_dict["id"] = idx
                            data_dict["category"] = category
                            data_dict["content"] = caption_string
                            if flag:          
                              data_right.append(data_dict)
                            else:
                              print(image_path, category, caption_json["category"])
                              data_error.append(data_dict)
              except Exception as e:
                print("Exception:", str(e))
  df_right = pd.DataFrame(data_right)
  df_error = pd.DataFrame(data_error)

  df_right.to_csv(right_csv_name)
  df_error.to_csv(error_csv_name)
  
  print("data right number", len(data_right))
  print("data error number", len(data_error))
                    

def main():
  right_csv_name = "/group_share/data_org/DressCode/right_sample_style_sup.csv"
  error_csv_name = "/group_share/data_org/DressCode/error_sample_style_sup.csv"
  creat_database(right_csv_name, error_csv_name)
      


if __name__ == "__main__":
  main()

