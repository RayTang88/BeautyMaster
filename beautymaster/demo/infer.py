import os
import time
import torch
import argparse
import warnings
warnings.filterwarnings('ignore')

from beautymaster.src.infer_rag_recommend import RagAndRecommend
from beautymaster.src.try_on_cat import TryOnInterface
# from beautymaster.utils.show import show_func

os.environ["CUDA_VISIBLE_DEVICES"]="0"

class Interface:
    def __init__(self,
                 weights_path, # model.pt path(s),
                 code_root_path,
                 embedding_model_name,
                 reranker_model_name,
                 vlm_weight_name,
                 llm_weight_name,
                 save_path,
                 get_num_list,
                 meaning_list,
                 csv_data_path,
                 available_types,
                 bce_top_n,
                 content,
                 only_use_vlm,
                 openxlab,
                 recommend_top_n,
                 ) -> None:
        """
        Args:
            weights_path: model.pt path(s)
            embedding_model_name:
            reranker_model_name:
            top_n:
            vlm_weight_name:
            llm_weight_name:
            full_body_image_path:
            save_path: save results to project/name
            get_num_list: model and number of cloth candidates
            meaning_list:
            csv_data_path:
            available_types:
            bce_top_n:
            content:
            only_use_vlm:
            openxlab:
            recommend_top_n:

        Returns:
            None
        
        Raises:
            None
        
        """
        quantstrings = ["awq", "AWQ", "4bits"]
        matches_vlm = [s for s in quantstrings if s in vlm_weight_name]
        matches_llm = [s for s in quantstrings if s in llm_weight_name]
        vlm_awq=True if matches_vlm else False
        llm_awq=True if matches_llm else False
        
        self.ragandrecommend = RagAndRecommend(weights_path, embedding_model_name, reranker_model_name, bce_top_n, recommend_top_n, csv_data_path, vlm_weight_name, vlm_awq, llm_weight_name, llm_awq, available_types, only_use_vlm, openxlab)
        self.save_path = save_path 
        
        self.try_on_class = TryOnInterface(weights_path, code_root_path)
        
        self.total=1
        
    def match_interface(self,
            weather="",
            season="",
            determine="",
            full_body_image_path="",
            additional_requirements=""
            ):
        
        # Infinite loop until the code executes successfully
        Cycles=0
        while Cycles<self.total:
            try:
                with torch.no_grad():
                    #1 use llm after rag 4o like
        
                    llm_recommended, body_shape_descs = self.ragandrecommend.infer_llm_raged_recommend_interface(full_body_image_path, season, weather, determine, additional_requirements)
                    
                    #2.Virtual Try-on according the suggestions
                    # match_result = self.tryon.try_on_func(llm_recommended, full_body_image_path, body_shape_descs)
                    match_result = self.ragandrecommend.match_only_result_func(llm_recommended)
                    # print(match_result)
                    #3.Visualize the results of the suggestions to the user
                    # show_func(match_result, self.save_path)

                    return match_result, body_shape_descs
            except Exception as e:
                Cycles+=1
                print(f"Cycles: {Cycles}/{self.total}, error: {e}, try again...")
                time.sleep(1)  # wait 1 minute
                
    def try_on_interface(self,
        weather="",
        season="",
        determine="",
        full_body_image_path="",
        additional_requirements=""
        ):
        # Infinite loop until the code executes successfully
        Cycles=0
        while Cycles<self.total:
            try:
                with torch.no_grad():
                    #1 use llm after rag 4o like
        
                    llm_recommended, body_shape_descs = self.ragandrecommend.infer_llm_raged_recommend_interface(full_body_image_path, season, weather, determine, additional_requirements)
                    
                    #2.Virtual Try-on according the suggestions
                    match_result = self.try_on_class.try_on_func_all(llm_recommended, full_body_image_path, body_shape_descs)
                    # match_result = self.ragandrecommend.match_only_result_func(llm_recommended)
                    # print(match_result)
                    #3.Visualize the results of the suggestions to the user
                    # show_func(match_result, self.save_path)

                    return match_result, body_shape_descs
            except Exception as e:
                Cycles+=1
                print(f"Cycles: {Cycles}/{self.total}, error: {e}, try again...")
                time.sleep(1)
    
    def try_on_only_interface(self,
        match_result,
        full_body_image_path="",
        body_shape_descs="",
        num_inference_steps=20,
        guidance_scale=2.5,
        seed=1024,
        show_type="result only",
        ):
        # Infinite loop until the code executes successfully

        cycle=0
        while cycle<self.total:

            try:
                with torch.no_grad():
                    #1 use llm after rag 4o like
                    # ragandrecommend = RagAndRecommend(self.weights_path, self.embedding_model_name, self.reranker_model_name, self.top_n, self.csv_data_path, self.vlm_weight_name, self.vlm_awq, self.llm_weight_name, self.llm_awq, self.available_types, self.only_use_vlm, self.openxlab)    
                    # self.llm_recommended, self.body_shape_descs = ragandrecommend.infer_llm_raged_recommend_interface(full_body_image_path, season, weather, determine, additional_requirements)
                    
                    # torch.cuda.synchronize()
                    # torch.cuda.empty_cache()

                    #2.Virtual Try-on according the suggestions

                    try_on_result = self.try_on_class.try_on_func_form_match_result(match_result, full_body_image_path, body_shape_descs, num_inference_steps, guidance_scale, seed, show_type)
                    # torch.cuda.synchronize()
                    # torch.cuda.empty_cache()
                    # match_result = self.ragandrecommend.match_only_result_func(llm_recommended)
                    # print(match_result)
                    #3.Visualize the results of the suggestions to the user
                    # show_func(match_result, self.save_path).

                    return try_on_result
            except Exception as e:
                cycle+=1
                print(f"Cycles: {cycle}/{self.total}, error: {e}, try again...")
                time.sleep(1)  # wait 1 minute
                    
    def rag(self,
            weather="",
            season="",
            determine="",
            full_body_image_path="",
            additional_requirements=""
            ):
        
        rag_4o_like_recommended, _, _ = self.ragandrecommend.infer_rag_4o_like_func(full_body_image_path, season, weather, determine, additional_requirements)
        print("rag_4o_like_recommended" , rag_4o_like_recommended)
        
        return rag_4o_like_recommended
        
    def caption_interface(self,
            clothes_path="",
            ):
        
        # Infinite loop until the code executes successfully
        Cycles=0
        while Cycles<self.total:
            try:
        
                #1. get clothes caption
                caption_json, caption_string = self.ragandrecommend.infer_vlm_caption(clothes_path)
                
                # print("caption", caption_string)
                #2. write database
                return caption_json, caption_string
            except Exception as e:
                Cycles+=1
                print(f"Cycles: {Cycles}/{self.total}, error: {e}, try again...")
                time.sleep(1)  # wait 1 minute

def parse_opt(vlm_weight_name, llm_weight_name):
	parser = argparse.ArgumentParser()
	parser.add_argument('--weights-path', nargs='+', type=str, default=os.environ.get('MODEL_ROOT'), help='model path(s)')
	parser.add_argument('--code-root-path', nargs='+', type=str, default=os.environ.get('CODE_ROOT'), help='model path(s)')
	parser.add_argument('--vlm-weight-name', nargs='+', type=str, default=vlm_weight_name, help='MiniCPM-Llama3-V-2_5/MiniCPM-Llama3-V-2_5-AWQ/InternVL-Chat-V1-5-AWQ')
	parser.add_argument('--llm-weight-name', nargs='+', type=str, default=llm_weight_name, help='internlm2-chat-7b/internlm2-chat-20b-4bits')
	parser.add_argument('--embedding-model-name', nargs='+', type=str, default='/bce-embedding-base_v1/', help='')
	parser.add_argument('--reranker-model-name', nargs='+', type=str, default='/bce-reranker-base_v1/', help='')
	parser.add_argument('--save-path', type=str, default=os.environ.get('DATA_ROOT'), help='save results to project/name')
	parser.add_argument('--get-num-list', nargs='+', type=int, default=[1, 1, 0, 0], help='model and number of cloth candidates')
	parser.add_argument('--meaning-list', nargs='+', type=str, default=["我的形象特征", "上衣", "裤子", "半身裙", "连衣裙"], help='The meaning of each item in num_list')
	# parser.add_argument('--weather', type=str, default='30~35摄氏度', help='weather')
	# parser.add_argument('--season', type=str, default='夏季', help='season')
	# parser.add_argument('--determine', type=str, default='约会', help='determine')
	parser.add_argument('--content', type=str, default='images', help='content')
	parser.add_argument('--bce-top-n', type=int, default=5, help='rag num')
	parser.add_argument('--csv-data-path', type=str, default=os.environ.get('DATA_ROOT')+"/right_sample_style_correct_sup_removed.csv", help='content')
	# parser.add_argument('--full-body-image-path', type=str, default='/group_share/data_org/test_data/fullbody/real_image/v2-637c977c47e7794caa8cc80e12f1a369_r.jpg', help='content')
	parser.add_argument('--available-types', nargs='+', type=str, default=["上衣", "裤子", "半身裙", "连衣裙"], help='available types')
	parser.add_argument('--only-use-vlm', nargs='+', type=bool, default=False, help='only use vlm')
	parser.add_argument('--openxlab', nargs='+', type=bool, default=True, help='only use vlm')
	parser.add_argument('--recommend_top_n', nargs='+', type=int, default=2, help='schema num') 
	# parser.add_argument('--additional-requirements', type=str, default='搭配简单大方', help='additional requirements')
	opt = parser.parse_args()

	return opt

def run(weather, season, determine, additional_requirements, full_body_image_path, clothes_path, interface, func="match"):

    if "match" == func:
        match_reslult = interface.match(weather,
        season,
        determine,
        full_body_image_path,
        additional_requirements)
    elif "rag" == func:
        interface.rag(weather,
            season,
            determine,
            full_body_image_path,
            additional_requirements)
    elif "caption" == func:
        interface.caption(clothes_path)
    elif  "tryon"== func:
        pass    

if __name__ == "__main__":
    
    opt = parse_opt('/MiniCPM-Llama3-V-2_5-AWQ/', '/Qwen2-7B-Instruct-AWQ/')
    interface = Interface(**vars(opt))
    weather = "30~35摄氏度"
    season = "夏季"
    determine = "约会"
    additional_requirements = "搭配简单大方"
    full_body_image_path = "/group_share/data_org/test_data/fullbody/real_image/b17ab66100f34037b1a83e4c9e7c97a4_th.jpg" 
    clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg" 
    interface.run(interface, weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func="match")
