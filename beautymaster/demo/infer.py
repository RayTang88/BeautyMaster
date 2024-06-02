import os
import sys
import argparse
# 根据自己代码位置修改
sys.path.append("/root/code/BeautyMaster")

# sys.path.append('/root/BeautyMaster-dev/beautymaster')

from beautymaster.src.infer_vlm import infer_vlm_func, infer_vlm_4o_like_func
from beautymaster.src.infer_rag import infer_rag_func, infer_rag_4o_like_func
from beautymaster.src.infer_llm import infer_llm_recommend, infer_llm_recommend_raged
from beautymaster.src.try_on import try_on_func


os.environ["CUDA_VISIBLE_DEVICES"]="0, 1"

def run(weights_path="",  # model.pt path(s)
        vlm_weight_name="", # model name
        llm_weight_name="", # model name
        embedding_model_name="",
		source="",  # file/dir/URL/glob, 0 for webcam
		save_path="",  # save results to project/name
        get_num_list = [], # model and number of cloth candidates
        meaning_list=[],  
		weather="",
        season="",
        determine="",
        content="",
        top_n=5,
        csv_data_path="",
        full_body_image_path="",
        available_types=[],
		additional_requirements=""
        ):
    
    #1.Load caption and template to form prompt
    
    #2.Trained VLM give suggestions
    
    #2.1 only use vlm
    # model_candidate_clothes_list = infer_rag_func(source, get_num_list, content) #for test, now get list randomly.
    # response_string = infer_vlm_func(weights_path, weight_name, model_candidate_clothes_list, season, weather, determine)
    
    #2.2 4o like
    rag_4o_like_recommended, body_shape_descs, gender = infer_rag_4o_like_func(weights_path, vlm_weight_name, llm_weight_name, embedding_model_name, top_n, csv_data_path, full_body_image_path, season, weather, determine, available_types, additional_requirements, False)
    
    #2.3 Because VLM is not effective, LLM is used instead.
    # model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, content) #for test, now get list randomly.
    # response_string = infer_llm_recommend(weights_path, llm_weight_name, season, weather, determine, rag_4o_like_recommended, get_num_list, meaning_list)
    
    #2.4 use llm after rag 4o like
    llm_recommended = infer_llm_recommend_raged(weights_path, llm_weight_name, season, weather, determine, rag_4o_like_recommended, body_shape_descs, gender, get_num_list, meaning_list)
    
    # print(rag_4o_like_recommended)
    # print("----------------------------------------")
    # print(response_string)
    #3.Virtual Try-on according the suggestions
	
    match_result = try_on_func(llm_recommended, full_body_image_path, body_shape_descs)
    print(match_result)
    #4.Visualize the results of the suggestions to the user


def parse_opt():
	parser = argparse.ArgumentParser()
	parser.add_argument('--weights-path', nargs='+', type=str, default='/group_share/model', help='model path(s)')
	parser.add_argument('--vlm-weight-name', nargs='+', type=str, default='/InternVL-Chat-V1-5/', help='')
	parser.add_argument('--llm-weight-name', nargs='+', type=str, default='/internlm2-chat-20b_TurboMind/', help='')
	parser.add_argument('--embedding-model-name', nargs='+', type=str, default='/bce-embedding-base_v1', help='')
	parser.add_argument('--source', type=str, default='/group_share/data_org/test_data/', help='')
	parser.add_argument('--save-path', type=str, default='./save_data/', help='save results to project/name')
	parser.add_argument('--get-num-list', nargs='+', type=int, default=[1, 1, 0, 0], help='model and number of cloth candidates')
	parser.add_argument('--meaning-list', nargs='+', type=str, default=["我的形象特征", "上衣", "裤子", "裙子"], help='The meaning of each item in num_list')
	parser.add_argument('--weather', type=str, default='30~35摄氏度', help='weather')
	parser.add_argument('--season', type=str, default='夏季', help='season')
	parser.add_argument('--determine', type=str, default='约会', help='determine')
	parser.add_argument('--content', type=str, default='images', help='content')
	parser.add_argument('--top-n', type=int, default=5, help='rag num')
	parser.add_argument('--csv-data-path', type=str, default='/group_share/data_org/test_data/sample_style.csv', help='content')
	parser.add_argument('--full-body-image-path', type=str, default='/group_share/data_org/test_data/fullbody/real_image/v2-637c977c47e7794caa8cc80e12f1a369_r.jpg', help='content')
	parser.add_argument('--available-types', nargs='+', type=str, default=["上衣", "裤子", "裙子"], help='available types')
	parser.add_argument('--additional-requirements', type=str, default='搭配简单大方', help='additional requirements')
	opt = parser.parse_args()

	return opt

def main(opt):
	run(**vars(opt))

if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
