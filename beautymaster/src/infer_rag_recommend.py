import os
import random
from json_repair import repair_json
from PIL import Image
# from .infer_vlm_torch import VLM
# from .infer_llm_torch import LLM
from .infer_vlm import VLM
from .infer_llm import LLM
from .bce_langchain import BceEmbeddingRetriever
from .prompt import vlm_prompt_body_template, body_shape, body_out_format

class RagAndRecommend():
    def __init__(self, 
                 weights_path,
                 embedding_model_name,
                 reranker_model_name,
                 bce_top_n, recommend_top_n,
                 csv_data_path,
                 vlm_weight_name,
                 vlm_awq,
                 llm_weight_name, 
                 llm_awq,
                 available_types, 
                 only_use_vlm,
                 openxlab=False):
        
        self.bceEmbeddingRetriever = BceEmbeddingRetriever(weights_path, embedding_model_name, reranker_model_name, bce_top_n, csv_data_path)
        self.vlm = VLM(weights_path, vlm_weight_name, vlm_awq, openxlab)
        self.llm = LLM(weights_path, llm_weight_name, llm_awq, openxlab)


        
        self.available_types = available_types
        self.only_use_vlm = only_use_vlm
        self.recommend_top_n = recommend_top_n
 
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
        
        #This interface is completely based on 4o. It recommends matching according to the full-body photo. 
        # The result given by internvl is closely related to the clothes in the provided picture. 
        # The matching result is not ideal and is not enabled.
        if self.only_use_vlm:
            match_text = self.vlm.infer_vlm_4o_like_func(full_body_image_path, season, weather, determine)
        else: 
        #This interface 1. first describes the body shape of the full-body photo; 
        # 2. recommends matching according to the body shape; 
        # 3. searches for similar matching in the database RAG based on the recommended matching; 
        # 4. lets the model match three sets of matching in the RAG recommendation, from coarse to fine. 
        # This interface implements the functions of 1, 2, and 3.

            body_shape_response = self.vlm.infer_vlm_body_shape_func(full_body_image_path, body_shape, body_out_format)
            match_text, body_shape_descs, gender = self.llm.infer_llm_single_recommend(season, weather, determine, body_shape_response, additional_requirements, self.available_types)
            
        good_json_obj = repair_json(match_text, return_objects=True)
        print("good_json_obj rough llm recommend ", good_json_obj)
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
    
    
    #This is a  main interface ,used to match in infer.py
    def infer_llm_raged_recommend_interface(self, full_body_image_path, season, weather, determine, additional_requirements):
        #vlm+rag
        similar_items, body_shape_descs, gender = self.infer_rag_4o_like_func(full_body_image_path, season, weather, determine, additional_requirements)
        #llm recomend
        recommended = self.llm.infer_llm_recommend_raged(season, weather, determine, additional_requirements, similar_items, body_shape_descs, gender, self.recommend_top_n)
        # recommended = ""
        
        return recommended, body_shape_descs
    
    #This interface is used to extract the caption of clothes
    def infer_vlm_caption(self, clothes_image_path):
        
        caption_response = self.vlm.infer_vlm_clothes_caption_func(clothes_image_path, self.available_types)
        
        # json_string = json.dumps(const_prompt).replace('"', '\\"').replace('{', '\\{').replace('}', '\\}')
        # json_string = const_prompt.replace('"', '\\"').replace('{', '\\{').replace('}', '\\}').replace('\n', '\\n')
        
        good_json_obj = repair_json(caption_response, return_objects=True)
        
        good_json_obj["items"].insert(0, good_json_obj["category"])
        # item_descs = good_json_obj["items"]
        clothes_shape_descs = '、'.join(good_json_obj["items"])
        
        return good_json_obj, clothes_shape_descs
    
    # Filter out incompatible combinations
    def filter_output(self, comb):
        from itertools import combinations

        # Optional List
        items = ["上衣", "裤子", "半身裙", "连衣裙"]

        # List of unacceptable combinations
        unacceptable_combinations = [
            ["上衣", "连衣裙"],
            ["裤子", "连衣裙"],
            ["裤子"],
            ["半身裙"],
            ["上衣"],
            ["裤子", "半身裙"],
            ["连衣裙", "半身裙"],
        ]

        # Convert unacceptable combinations into sets for easier comparison
        unacceptable_sets = [set(comb) for comb in unacceptable_combinations]

        comb_set = set(comb)
        
        if (comb_set not in unacceptable_sets) and  len(comb_set)<3:
            if "上衣" in comb and "上衣" != comb[0] :
                comb.remove("上衣")
                comb.insert(0, "上衣")
                
            return True, comb
        return False, None
    
    # Here we only show the matching results without adding tryon results
    def match_only_result_func(self, llm_recommended):
        print("llm_recommended[match_content]", llm_recommended)
        print("type--- llm_recommended", type(llm_recommended))     
        print("len--- llm_recommended", len(llm_recommended))  
        
        # becacuse the out of llm may have many style(fuck)
        # ex：0.{'match_content': [{...}]}；1.[{'match_content': [{...}]}]；2.[{'match_content': {...}]；3.[{...}]
        # 0 
        llm_recommended_with_match_content = llm_recommended
        # 1
        if isinstance(llm_recommended, list):
            llm_recommended_with_match_content = llm_recommended[0]
        assert isinstance(llm_recommended_with_match_content, dict)
        print("type--- llm_recommended2", type(llm_recommended_with_match_content))          
        match_result = []
        if "match_content" in llm_recommended_with_match_content:
            llm_recommended_list = llm_recommended_with_match_content["match_content"]
            # 2
            if isinstance(llm_recommended_list, dict):
                llm_recommended_list = [llm_recommended_list]
        # 3
        else:
            llm_recommended_list = llm_recommended    
        assert len(llm_recommended_list) > 0
        for match in llm_recommended_list:
            match_dict = {}
            match_category_list = match["category"]
                        
            #Filter out incompatible combinations
            flag, match_caption_list = self.filter_output(match_category_list)
            if not flag:
                continue
            # print("here1111111")
            match_id_list = match["match_id"]
            match_caption_list = match["match_caption"]
            match_reason = match["reason"]
            
            assert len(match_category_list) == len(match_id_list), f"error: len(match_category_list):%d != len(match_id_list):%d"%(len(match_category_list), len(match_id_list))
            assert len(match_caption_list) == len(match_id_list), f"error: len(match_caption_list):%d != len(match_id_list):%d"%(len(match_caption_list), len(match_id_list))
            # print("here222222")
            match_dict["id"] = match["id"]
            match_dict["score"] = match["score"]
            match_dict["category"] = match_category_list
            match_dict["match_reason"] = match_reason
            match_dict["match_caption"] = match_caption_list
            match_dict["match_id"] = match_id_list
            # print("here333333")
            images = []
            
            for category, match_id, match_caption in zip(match_category_list, match_id_list, match_caption_list):
                # try:
                data_root = os.environ.get('DATA_ROOT')
            
                if "上衣" == category:
                    # idx = match_category_list.index("上衣")
                    # match_id =match_id_list[idx]
                    # match_caption =match_caption_list[idx]
                    # The match_id field is in the form of 'match_id': ['idx: 050040_1', 'idx: 019252_1']
                    clothes_path = data_root + "/upper_body/images/" + match_id.replace("idx:", "").strip().split('_')[0] + "_1.jpg"
                elif "裤子" == category:
                    clothes_path = data_root + "/lower_body/images/" +match_id.replace("idx:", "").strip().split('_')[0] + "_1.jpg"
                elif "半身裙" == category:
                    clothes_path = data_root + "/lower_body/images/" + match_id.replace("idx:", "").strip().split('_')[0] + "_1.jpg"
                elif "连衣裙" == category:
                    clothes_path = data_root + "/dresses/images/" + match_id.replace("idx:", "").strip().split('_')[0] +"_1.jpg"    
                print(os.path.exists(clothes_path), clothes_path)  
                if not os.path.exists(clothes_path):
                    continue
                
                image = Image.open(clothes_path)
                
                    
                images.append(image)
                # except FileNotFoundError:
                #     continue
                        
            match_dict["images"] = images
            match_result.append(match_dict)

        return match_result

   