import argparse
import torch
import sys

print(sys.path.append("./"))

from src.infer_vlm import infer_vlm_func

def run(weights='',  # model.pt path(s)
		source='',  # file/dir/URL/glob, 0 for webcam
		imgsz=640,  # inference size (pixels)
		conf_thres=0.25,  # confidence threshold
		save_path='',  # save results to project/name
        ):
    
    weather = "35~40摄氏度"
    season = "夏季"
    determine = "逛街"
    #1.Load caption and template to form prompt
    model_candidate_clothes_list = rag_func()
    #2.Trained VLM give suggestions
    response_string = infer_vlm_func(weights, model_candidate_clothes_list, season, weather, determine)

    #3.Virtual Try-on according the suggestions

    #4.Visualize the results of the suggestions to the user
    pass

def parse_opt():
	parser = argparse.ArgumentParser()
	parser.add_argument('--weights', nargs='+', type=str, default='', help='model path(s)')
	parser.add_argument('--source', type=str, default='/data0/tc_workspace/data/vton/pic/pic/', help='')
	parser.add_argument('--save_path', default='/data0/tc_workspace/internlm/code/project/py_child/data/save_data/', help='save results to project/name')
	parser.add_argument('--imgsz', '--img', '--img-size', nargs='+',
						type=int, default=[640, 480], help='inference size h,w')
	parser.add_argument('--conf-thres', type=float,
						default=0.3, help='confidence threshold')

	opt = parser.parse_args()
	opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
	return opt

def main(opt):
	run(**vars(opt))


if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
