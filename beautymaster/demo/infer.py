import os
import sys
import argparse

sys.path.append("/root/code/BeautyMaster/beautymaster")
from src.infer_vlm import infer_vlm_func
from src.infer_rag import infer_rag_func

os.environ["CUDA_VISIBLE_DEVICES"]="0,1"

def run(weights_path='',  # model.pt path(s)
        weight_name='',
		source='',  # file/dir/URL/glob, 0 for webcam
		save_path='',  # save results to project/name
        get_num_list = [],
        imgsz=640,  # inference size (pixels)
		conf_thres=0.25,  # confidence threshold
        ):
    
    weather = "10~15摄氏度"
    season = "春季"
    determine = "逛街"
    #1.Load caption and template to form prompt
    
    #2.Trained VLM give suggestions
    model_candidate_clothes_list = infer_rag_func(source, get_num_list) #for test, now get list randomly.
    response_string = infer_vlm_func(weights_path, weight_name, model_candidate_clothes_list, season, weather, determine)

    
    print(response_string)

    #3.Virtual Try-on according the suggestions

    #4.Visualize the results of the suggestions to the user


def parse_opt():
	parser = argparse.ArgumentParser()
 
	parser.add_argument('--weights-path', nargs='+', type=str, default='/root/model/', help='model path(s)')
	parser.add_argument('--weight-name', nargs='+', type=str, default='InternVL-Chat-V1-5/', help='')
	parser.add_argument('--source', type=str, default='/root/data/test_data/', help='')
	parser.add_argument('--save-path', type=str, default='./save_data/', help='save results to project/name')
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
