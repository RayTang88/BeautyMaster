import os
import random
from json_repair import repair_json
from PIL import Image
from .infer_vlm import VLM
from .infer_llm import LLM
from .bce_langchain import BceEmbeddingRetriever
from .prompt import vlm_prompt_body_template, body_shape, body_out_format

class RagAndRecommend():
    def __init__(self, 
                 weights_path,
                 embedding_model_name,
                 reranker_model_name,
                 top_n, csv_data_path,
                 vlm_weight_name,
                 llm_weight_name, 
                 available_types, 
                 only_use_vlm):
        
        self.bceEmbeddingRetriever = BceEmbeddingRetriever(weights_path, embedding_model_name, reranker_model_name, top_n, csv_data_path)
                
        self.vlm = VLM(weights_path, vlm_weight_name)
        self.llm = LLM(weights_path, llm_weight_name)
        
        self.available_types = available_types
        self.only_use_vlm = only_use_vlm
 
    def random_get(self, images_path, num, content):
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
                
            
    def random_pick(self, model_candidate_clothes_path, get_num_list, content):
        model_candidate_clothes_dict = {}
        for root, dirs, filenames in os.walk(model_candidate_clothes_path):
            for dir_ in dirs:
                images_path = os.path.join(root, dir_, "images")
                if "fullbody" == dir_:
                    
                    content_list = self.random_get(images_path, get_num_list[0], content) 
                    model_candidate_clothes_dict["full_body"] = content_list
                    
                if "upper_body" == dir_:
                    
                    content_list = self.random_get(images_path, get_num_list[1], content) 
                    model_candidate_clothes_dict["upper_body"] = content_list 
                
                if "lower_body" == dir_:
                    
                    content_list = self.random_get(images_path, get_num_list[2], content) 
                    model_candidate_clothes_dict["lower_body"] = content_list   
                
                if "dresses" == dir_:
                    
                    content_list = self.random_get(images_path, get_num_list[3], content) 
                    model_candidate_clothes_dict["dresses"] = content_list  
                        
        return model_candidate_clothes_dict  


    def ordered_list(self, model_candidate_clothes_dict):
        
        model_candidate_clothes_list = []
        model_candidate_clothes_list.extend(model_candidate_clothes_dict["full_body"])
        model_candidate_clothes_list.extend(model_candidate_clothes_dict["upper_body"])
        model_candidate_clothes_list.extend(model_candidate_clothes_dict["lower_body"])
        model_candidate_clothes_list.extend(model_candidate_clothes_dict["dresses"]) 
        
        return model_candidate_clothes_list   
        
    def infer_rag_func(self, model_candidate_clothes_path, get_num_list, content):
        
        model_candidate_clothes_dict = self.random_pick(model_candidate_clothes_path, get_num_list, content)
        model_candidate_clothes_list = self.ordered_list(model_candidate_clothes_dict)
        
        total = sum(a for a in get_num_list)
        
        assert total == len(model_candidate_clothes_list)
        
        return model_candidate_clothes_list


    def infer_rag_4o_like_func(self, full_body_image_path, season, weather, determine, additional_requirements):
        
        #这个接口完全参照4o，根据全身照，推荐搭配，internvl给出的结果和提供的图片穿着有很大关系,搭配的结果不太理想，未启用状态
        if self.only_use_vlm:
            match_text = self.vlm.infer_vlm_4o_like_func(full_body_image_path, season, weather, determine)
        else: 
        #这个接口1.先根据全身照，描述全身照的身材；2.根据身材llm推荐搭配；3.根据推荐的搭配在数据库里面RAG搜索相似的；4.让他模型在RAG推荐的里面搭配三套，由粗到细。这个接口实现了1,2,3的功能

            body_shape_response = self.vlm.infer_vlm_body_shape_func(full_body_image_path, body_shape, body_out_format)
            match_text, body_shape_descs, gender = self.llm.infer_llm_single_recommend(season, weather, determine, body_shape_response, additional_requirements)
            
        good_json_obj = repair_json(match_text, return_objects=True)
        # print("good_json_obj llm recommend ", good_json_obj)
        item_descs = good_json_obj["items"]
        category_descs = good_json_obj["category"]
        
        #目前需要搭配的类别
        assert len(item_descs) == len(category_descs)
        
        # 创建a和b之间的字典映射
        mapping = dict(zip(category_descs, item_descs))
        
        # 使用字典推导式处理c中的元素，根据映射关系从b中取出对应的元素，并输出为字典
        items = {item: mapping[item] for item in self.available_types if item in mapping}
        
        # print(items)
        
        print("--------------------")
        # 用RAG进行检索和排序
        similar_items = self.bceEmbeddingRetriever.bce_retriever(items)
        
        return similar_items, body_shape_descs, gender
    
    def infer_llm_raged_recommend_interface(self, full_body_image_path, season, weather, determine, additional_requirements):
        
        similar_items, body_shape_descs, gender = self.infer_rag_4o_like_func(full_body_image_path, season, weather, determine, additional_requirements)
        recommended = self.llm.infer_llm_recommend_raged(season, weather, determine, similar_items, body_shape_descs, gender)
        
        return recommended, body_shape_descs
    
    #This interface is used to extract the caption of clothes
    def infer_vlm_caption(self, clothes_image_path):
        
        caption_response = self.vlm.infer_vlm_clothes_caption_func(clothes_image_path, self.available_types)
        
        # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
        # json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
        
        good_json_obj = repair_json(caption_response, return_objects=True)
        
        good_json_obj["items"].insert(0, good_json_obj["category"])
        item_descs = good_json_obj["items"]
        clothes_shape_descs = '、'.join(good_json_obj["items"])
        
        return good_json_obj, clothes_shape_descs
    # Here we only show the matching results without adding tryon results
    def match_only_result_func(self, llm_recommended):
        print("llm_recommended[match_content]", llm_recommended)    
        assert len(llm_recommended["match_content"]) > 0
        match_result = []
        for match in llm_recommended["match_content"]:
            match_dict = {}
            match_category_list = match["category"]
            match_id_list = match["match_id"]
            match_caption_list = match["match_caption"]
            match_reason = match["reason"]
            
            assert len(match_category_list) == len(match_id_list)
            assert len(match_caption_list) == len(match_id_list)
            
            match_dict["id"] = match["id"]
            match_dict["score"] = match["score"]
            match_dict["category"] = match_category_list
            match_dict["match_reason"] = match_reason
            
            images = []
            
            for category, match_id, match_caption in zip(match_category_list, match_id_list, match_caption_list):
                try:
                
                    if "上衣" == category:
                        # idx = match_category_list.index("上衣")
                        # match_id =match_id_list[idx]
                        # match_caption =match_caption_list[idx]
                        clothes_path = "/group_share/data_org/DressCode/upper_body/images/" + match_id.split('_')[0]+"_1.jpg"
                    elif "裤子" == category:
                        clothes_path = "/group_share/data_org/DressCode/lower_body/images/" + match_id.split('_')[0]+"_1.jpg"
                    elif "裙子" == category:
                        clothes_path = "/group_share/data_org/DressCode/dresses/images/" + match_id.split('_')[0]+"_1.jpg"   
                    image = Image.open(clothes_path)
                        
                    images.append(image)
                except FileNotFoundError:
                    continue
                        
            match_dict["images"] = images
            match_result.append(match_dict)

        return match_result

   