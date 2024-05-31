import os
import random
from json_repair import repair_json
from .infer_vlm import infer_vlm_4o_like_func, infer_vlm_sigle_func
from .infer_llm import infer_llm_single_recommend
from .bce_langchain import bce_retriever
from .prompt import vlm_prompt_body_template, body_shape, body_out_format



def random_get(images_path, num, content):
    content_list = []
    images = os.listdir(images_path)
    
    while len(content_list) < num:
        random.shuffle(images)
        candidates = random.sample(images, num)
        for candidate in candidates:
            image_path = os.path.join(images_path, candidate)
            json_path = image_path.replace("_1.jpg", '_0.json').replace("images", 'json').replace(".jpg", '.json')
            
            if os.path.exists(image_path) and os.path.exists(json_path):
                if "images" == content:
                    content_list.append(image_path)
                elif "json" == content:   
                    content_list.append(json_path) 
    return content_list        
            
        
def random_pick(model_candidate_clothes_path, get_num_list, content):
    model_candidate_clothes_dict = {}
    for root, dirs, filenames in os.walk(model_candidate_clothes_path):
        for dir_ in dirs:
            images_path = os.path.join(root, dir_, "images")
            if "fullbody" == dir_:
                
                content_list = random_get(images_path, get_num_list[0], content) 
                model_candidate_clothes_dict["full_body"] = content_list
                
            if "upper_body" == dir_:
                
                content_list = random_get(images_path, get_num_list[1], content) 
                model_candidate_clothes_dict["upper_body"] = content_list 
            
            if "lower_body" == dir_:
                
                content_list = random_get(images_path, get_num_list[2], content) 
                model_candidate_clothes_dict["lower_body"] = content_list   
            
            if "dresses" == dir_:
                
                content_list = random_get(images_path, get_num_list[3], content) 
                model_candidate_clothes_dict["dresses"] = content_list  
                     
    return model_candidate_clothes_dict  


def ordered_list(model_candidate_clothes_dict):
    
    model_candidate_clothes_list = []
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["full_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["upper_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["lower_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["dresses"]) 
    
    return model_candidate_clothes_list   
      
def infer_rag_func(model_candidate_clothes_path, get_num_list, content):
    
    model_candidate_clothes_dict = random_pick(model_candidate_clothes_path, get_num_list, content)
    model_candidate_clothes_list = ordered_list(model_candidate_clothes_dict)
    
    total = sum(a for a in get_num_list)
    
    assert total == len(model_candidate_clothes_list)
    
    return model_candidate_clothes_list


def infer_rag_4o_like_func(weights_path, vlm_weight_name, llm_weight_name, embedding_model_name, top_n, csv_data, full_body_image_path, season, weather, determine, available_types, use_vlm):
    
    #目前VLM给出的结果和提供的图片穿着有很大关系,搭配的结果不太理想
    if use_vlm:
        match_text = infer_vlm_4o_like_func(weights_path, vlm_weight_name, full_body_image_path, season, weather, determine)
    else:
        data = {"shape": body_shape, "feature":"我的体型特征", "out_format":body_out_format}
        vlm_prompt_template = vlm_prompt_body_template.format(**data)
        body_shape_response = infer_vlm_sigle_func(weights_path, vlm_weight_name, full_body_image_path, season, weather, determine, vlm_prompt_template)
        match_text, body_shape_descs, gender = infer_llm_single_recommend(weights_path, llm_weight_name, season, weather, determine, body_shape_response)
        
    good_json_obj = repair_json(match_text, return_objects=True)
    item_descs = good_json_obj["items"]
    category_descs = good_json_obj["category"]
    
    #目前需要搭配的类别
    assert len(item_descs) == len(category_descs)
    
    # 创建a和b之间的字典映射
    mapping = dict(zip(category_descs, item_descs))
    
    # 使用字典推导式处理c中的元素，根据映射关系从b中取出对应的元素，并输出为字典
    items = {item: mapping[item] for item in available_types if item in mapping}
    
    print(items)
    
    print("--------------------")
    
    similar_items = bce_retriever(weights_path, embedding_model_name, top_n, csv_data, items)
    
    return similar_items, body_shape_descs, gender