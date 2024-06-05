import os
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

# 根据自己代码位置修改
sys.path.append("/root/code/BeautyMaster")
# sys.path.append('/root/BeautyMaster-dev/beautymaster')

from beautymaster.src.infer_vlm import VLM
from beautymaster.src.infer_rag_recommend import RagAndRecommend
from beautymaster.src.bce_langchain import BceEmbeddingRetriever
from beautymaster.src.infer_llm import LLM
from beautymaster.src.try_on import TryOnInterface
from beautymaster.utils.show import show_func

os.environ["CUDA_VISIBLE_DEVICES"]="0"

class Interface:
    def __init__(self,
                 weights_path, # model.pt path(s)
                 embedding_model_name,
                 reranker_model_name,
                 vlm_weight_name,
                 llm_weight_name,
                 save_path,
                 get_num_list,
                 meaning_list,
                 csv_data_path,
                 available_types,
                 top_n,
                 content,
                 only_use_vlm
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
            top_n:
            content:
            only_use_vlm:

        Returns:
            None
        
        Raises:
            None
        
        """
        
        self.ragandrecommend = RagAndRecommend(weights_path, embedding_model_name, reranker_model_name, top_n, csv_data_path, vlm_weight_name, llm_weight_name, available_types, only_use_vlm)
        self.save_path = save_path 
        
        self.tryon = TryOnInterface()
           
    def match(self,
            weather="",
            season="",
            determine="",
            full_body_image_path="",
            additional_requirements=""
            ):
        
        #1 use llm after rag 4o like
        llm_recommended, body_shape_descs = self.ragandrecommend.infer_llm_raged_recommend_interface(full_body_image_path, season, weather, determine, additional_requirements)
        
        #2.Virtual Try-on according the suggestions
        match_result = self.tryon.try_on_func(llm_recommended, full_body_image_path, body_shape_descs)
        # print(match_result)
        #3.Visualize the results of the suggestions to the user
        show_func(match_result, self.save_path)
        
        return match_result
        
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
        
    def caption(self,
            clothes_path="",
            ):
        

        #1. get clothes caption
        caption = self.ragandrecommend.infer_vlm_caption(clothes_path)
        
        print("caption", caption)
        #2. write database
        
        
        return caption
        

def parse_opt():
	parser = argparse.ArgumentParser()
	parser.add_argument('--weights-path', nargs='+', type=str, default='/group_share/model', help='model path(s)')
	parser.add_argument('--vlm-weight-name', nargs='+', type=str, default='/InternVL-Chat-V1-5-AWQ/', help='')
	parser.add_argument('--llm-weight-name', nargs='+', type=str, default='/internlm2-chat-20b-4bits/', help='')
	parser.add_argument('--embedding-model-name', nargs='+', type=str, default='/bce-embedding-base_v1', help='')
	parser.add_argument('--reranker-model-name', nargs='+', type=str, default='/bce-reranker-base_v1', help='')
	parser.add_argument('--save-path', type=str, default='/group_share/data_org/try_on_data/middle/', help='save results to project/name')
	parser.add_argument('--get-num-list', nargs='+', type=int, default=[1, 1, 0, 0], help='model and number of cloth candidates')
	parser.add_argument('--meaning-list', nargs='+', type=str, default=["我的形象特征", "上衣", "裤子", "裙子"], help='The meaning of each item in num_list')
	# parser.add_argument('--weather', type=str, default='30~35摄氏度', help='weather')
	# parser.add_argument('--season', type=str, default='夏季', help='season')
	# parser.add_argument('--determine', type=str, default='约会', help='determine')
	parser.add_argument('--content', type=str, default='images', help='content')
	parser.add_argument('--top-n', type=int, default=5, help='rag num')
	parser.add_argument('--csv-data-path', type=str, default='/group_share/data_org/test_data/sample_style.csv', help='content')
	# parser.add_argument('--full-body-image-path', type=str, default='/group_share/data_org/test_data/fullbody/real_image/v2-637c977c47e7794caa8cc80e12f1a369_r.jpg', help='content')
	parser.add_argument('--available-types', nargs='+', type=str, default=["上衣", "裤子", "裙子"], help='available types')
	parser.add_argument('--only-use-vlm', nargs='+', type=bool, default=False, help='available types')
	# parser.add_argument('--additional-requirements', type=str, default='搭配简单大方', help='additional requirements')
	opt = parser.parse_args()

	return opt

def main(interface, weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func="match"):
    # weather = "30~35摄氏度"
    # season = "夏季"
    # determine = "约会"
    # additional_requirements = "搭配简单大方"
    # full_body_image_path = "/group_share/data_org/test_data/fullbody/real_image/b17ab66100f34037b1a83e4c9e7c97a4_th.jpg" 
    # clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg" 
    
    if "match" == func:
        interface.match(weather,
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
    
    opt = parse_opt()
    interface = Interface(**vars(opt))
    weather = "30~35摄氏度"
    season = "夏季"
    determine = "约会"
    additional_requirements = "搭配简单大方"
    full_body_image_path = "/group_share/data_org/test_data/fullbody/real_image/b17ab66100f34037b1a83e4c9e7c97a4_th.jpg" 
    clothes_path = "/group_share/data_org/test_data/dresses/images/024193_1.jpg" 
    main(interface, weather, season, determine, additional_requirements, full_body_image_path, clothes_path, func="match")
