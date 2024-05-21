import os
import json


def convert_model_prompt(json_obj):
    model_lists = json_obj["conversations"]

    for model_list in model_lists:
        for key,value in model_list.items():

        

            pass
    

def convert_colthes_prompt(json_obj):
    pass

def convert_trouser_prompt(json_obj):
    pass

def convert_dresses_prompt(json_obj):
    pass


def convert(json_obj, prompt_option):

    const_prompt = ""
    if ("clothes" == prompt_option):
        const_prompt = convert_colthes_prompt(json_obj)
    elif("trousers" == prompt_option) :
        const_prompt = convert_trouser_prompt(json_obj)
    elif("dresses" == prompt_option) :
        const_prompt = convert_dresses_prompt(json_obj)
    elif("model" == prompt_option) :  
        const_prompt = convert_model_prompt(json_obj)

    return const_prompt    

if __name__ == "__main__":
    dress_json_name = "/root/data/test_data/dresses/020730_0.json"
    upper_json_name = "/root/data/test_data/upper/000004_0.json"
    lower_json_name = "/root/data/test_data/lower/013574_0.json"
    model_json_name = "/root/data/test_data/model/1_1_F_Bing_pic.json"

    with open(model_json_name, 'r') as f:
        json_obj = json.load(f)
        convert(json_obj, "model")   
    f.close()     
