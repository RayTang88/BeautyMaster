import os
import random

def random_get(images_path, num):
    images_list = []
    images = os.listdir(images_path)
    
    while len(images_list) < num:
        random.shuffle(images)
        candidates = random.sample(images, num)
        for candidate in candidates:
            image_path = os.path.join(images_path, candidate)
            json_path = image_path.replace("_1.jpg", '_0.json').replace("images", 'json').replace(".jpg", '.json')
            
            if os.path.exists(image_path) and os.path.exists(json_path):
                images_list.append(image_path)
    return images_list        
            
        
def random_pick(model_candidate_clothes_path, get_num_list):
    model_candidate_clothes_dict = {}
    for root, dirs, filenames in os.walk(model_candidate_clothes_path):
        for dir_ in dirs:
            images_path = os.path.join(root, dir_, "images")
            if "fullbody" == dir_:
                
                images_list = random_get(images_path, get_num_list[0]) 
                model_candidate_clothes_dict["full_body"] = images_list
                
            if "upper_body" == dir_:
                
                images_list = random_get(images_path, get_num_list[1]) 
                model_candidate_clothes_dict["upper_body"] = images_list 
            
            if "lower_body" == dir_:
                
                images_list = random_get(images_path, get_num_list[2]) 
                model_candidate_clothes_dict["lower_body"] = images_list   
            
            if "dresses" == dir_:
                
                images_list = random_get(images_path, get_num_list[3]) 
                model_candidate_clothes_dict["dresses"] = images_list  
                     
    return model_candidate_clothes_dict  

def ordered_list(model_candidate_clothes_dict):
    
    model_candidate_clothes_list = []
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["full_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["upper_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["lower_body"])
    model_candidate_clothes_list.extend(model_candidate_clothes_dict["dresses"]) 
    
    return model_candidate_clothes_list                       
            
def infer_rag_func(model_candidate_clothes_path, get_num_list):
    
    model_candidate_clothes_dict = random_pick(model_candidate_clothes_path, get_num_list)
    model_candidate_clothes_list = ordered_list(model_candidate_clothes_dict)
    
    total = sum(a for a in get_num_list)
    
    assert total == len(model_candidate_clothes_list)
    
    return model_candidate_clothes_list