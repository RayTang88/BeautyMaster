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
  source="/root/code/BeautyMaster/beautymaster/openxlab_demo/simple_data/"

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
                            
                            if "fullbody" == category:
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
                            data_dict["idx"] = idx
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

  df_right.to_csv(right_csv_name, index=False)
  df_error.to_csv(error_csv_name, index=False)
  
  print("data right number", len(data_right))
  print("data error number", len(data_error))
                    

def main():
  right_csv_name = "/group_share/data_org/DressCode/right_sample_style_sup_rett.csv"
  error_csv_name = "/group_share/data_org/DressCode/error_sample_style_sup_rett.csv"
  
#   right_csv_name = "/root/code/BeautyMaster/beautymaster/openxlab_demo/simple_data/right_sample_style.csv"
#   error_csv_name = "/root/code/BeautyMaster/beautymaster/openxlab_demo/simple_data/error_sample_style.csv"
  creat_database(right_csv_name, error_csv_name)


if __name__ == "__main__":
  main()

