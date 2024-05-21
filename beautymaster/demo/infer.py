import argparse
import torch
import sys

sys.path.append("/data0/tc_workspace/internlm/code/project/BeautyMaster/beautymaster")

from src.infer_vlm import infer_vlm_func
from src.infer_rag import infer_rag_func

def run(weights='',  # model.pt path(s)
		source='',  # file/dir/URL/glob, 0 for webcam
		save_path='',  # save results to project/name
        get_num_list = [],
        imgsz=640,  # inference size (pixels)
		conf_thres=0.25,  # confidence threshold
        ):
    
    weather = "35~40摄氏度"
    season = "夏季"
    determine = "逛街"
    #1.Load caption and template to form prompt
    
    #2.Trained VLM give suggestions
    model_candidate_clothes_list = infer_rag_func(source, get_num_list) #for test, now get list randomly.
    response_string = infer_vlm_func(weights, model_candidate_clothes_list, season, weather, determine)

    #3.Virtual Try-on according the suggestions

    #4.Visualize the results of the suggestions to the user
    pass

def parse_opt():
	parser = argparse.ArgumentParser()
 
	parser.add_argument('--weights', nargs='+', type=str, default='/data0/tc_workspace/internlm/model/', help='model path(s)')
	parser.add_argument('--source', type=str, default='/data0/tc_workspace/data/vton/test_data/', help='')
 
	parser.add_argument('--save-path', type=str, default='/data0/tc_workspace/internlm/code/project/py_child/data/save_data/', help='save results to project/name')

	parser.add_argument('--get-num-list', nargs='+', type=int, default=[1, 5, 5, 5], help='model and clothes number')
	parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640, 480], help='inference size h,w')
	parser.add_argument('--conf-thres', type=float, default=0.3, help='confidence threshold')

	opt = parser.parse_args()
	opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
	return opt

def main(opt):
	run(**vars(opt))

if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
