import os
import sys
import argparse

sys.path.append("/root/code/BeautyMaster/beautymaster")
from src.infer_vlm import infer_vlm_func
from src.infer_rag import infer_rag_func
from src.infer_llm import infer_llm_recommend

os.environ["CUDA_VISIBLE_DEVICES"]="0, 1"

def run(weights_path="",  # model.pt path(s)
        weight_name="", # model name
		source="",  # file/dir/URL/glob, 0 for webcam
		save_path="",  # save results to project/name
        get_num_list = [], # model and number of cloth candidates
        meaning_list=[],  
		weather="",  # confidence threshold
        season="",
        determine="",
        content=""
        ):
    
    #1.Load caption and template to form prompt
    
    #2.Trained VLM give suggestions
    
    # model_candidate_clothes_list = infer_rag_func(source, get_num_list) #for test, now get list randomly.
    # response_string = infer_vlm_func(weights_path, weight_name, model_candidate_clothes_list, season, weather, determine)
    
    # Because VLM is not effective, LLM is used instead.
    model_candidate_clothes_jsons = infer_rag_func(source, get_num_list, content) #for test, now get list randomly.
    response_string = infer_llm_recommend(weights_path, weight_name, season, weather, determine, model_candidate_clothes_jsons, get_num_list, meaning_list)
    
    print(response_string)

    #3.Virtual Try-on according the suggestions

    #4.Visualize the results of the suggestions to the user


def parse_opt():
	parser = argparse.ArgumentParser()
 
	parser.add_argument('--weights-path', nargs='+', type=str, default='/group_share/model/', help='model path(s)')
	parser.add_argument('--weight-name', nargs='+', type=str, default='internlm2-chat-20b_TurboMind/', help='')
	parser.add_argument('--source', type=str, default='/group_share/data_org/test_data/', help='')
	parser.add_argument('--save-path', type=str, default='./save_data/', help='save results to project/name')
	parser.add_argument('--get-num-list', nargs='+', type=int, default=[1, 5, 5, 5], help='model and number of cloth candidates')
	parser.add_argument('--meaning-list', nargs='+', type=int, default=["我的形象特征", "上衣", "裤子", "裙子"], help='The meaning of each item in num_list')
	parser.add_argument('--weather', type=str, default='10~15摄氏度', help='weather')
	parser.add_argument('--season', type=str, default='春季', help='season')
	parser.add_argument('--determine', type=str, default='逛街', help='determine')
	parser.add_argument('--content', type=str, default='json', help='content')


	opt = parser.parse_args()

	return opt

def main(opt):
	run(**vars(opt))

if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
