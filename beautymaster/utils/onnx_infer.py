import argparse
import os
import sys
import time
import math
from pathlib import Path
import cv2
import numpy as np
import onnxruntime
from tqdm import tqdm
import torch


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
	sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

def make_divisible(x, divisor):
    # Returns x evenly divisible by divisor
    return math.ceil(x / divisor) * divisor

def check_img_size(imgsz, s=32, floor=0):
    # Verify image size is a multiple of stride s in each dimension
    if isinstance(imgsz, int):  # integer i.e. img_size=640
        new_size = max(make_divisible(imgsz, int(s)), floor)
    else:  # list i.e. img_size=[640, 480]
        new_size = [max(make_divisible(x, int(s)), floor) for x in imgsz]
    if new_size != imgsz:
        print(f'WARNING: --img-size {imgsz} must be multiple of max stride {s}, updating to {new_size}')
    return new_size

def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None):
	# Rescale coords (xyxy) from img1_shape to img0_shape
	if ratio_pad is None:  # calculate from img0_shape
		gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
		pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
	else:
		gain = ratio_pad[0][0]
		pad = ratio_pad[1]

	coords[:, [0, 2]] -= pad[0]  # x padding
	coords[:, [1, 3]] -= pad[1]  # y padding
	coords[:, :4] /= gain
	clip_coords(coords, img0_shape)
	return coords

def clip_coords(boxes, shape):
	# Clip bounding xyxy bounding boxes to image shape (height, width)
	boxes[:, [0, 2]] = boxes[:, [0, 2]].clip(0, shape[1])  # x1, x2
	boxes[:, [1, 3]] = boxes[:, [1, 3]].clip(0, shape[0])  # y1, y2
		
def xywh2xyxy(x):
	# Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
	y = np.copy(x)
	y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
	y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
	y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
	y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
	return y

def box_iou(box1, box2, ismin):
	# https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
	"""
	Return intersection-over-union (Jaccard index) of boxes.
	Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
	Arguments:
		box1 (Tensor[N, 4])
		box2 (Tensor[M, 4])
	Returns:
		iou (Tensor[N, M]): the NxM matrix containing the pairwise
			IoU values for every element in boxes1 and boxes2
	"""

	def box_area(box):
		# box = 4xn
		return (box[2] - box[0]) * (box[3] - box[1])

	area1 = box_area(box1.T)
	area2 = box_area(box2.T)

	# inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
	inter = (torch.min(box1[:, None, 2:], box2[:, 2:]) - torch.max(box1[:, None, :2], box2[:, :2])).clamp(0).prod(2)
	# return inter / (area1[:, None] + area2 - inter)  # iou = inter / (area1 + area2 - inter)

	if ismin:
		iou = inter / torch.min(area1[:, None], area2)
	else:
		iou = inter / (area1[:, None] + area2 - inter)
	return iou  # iou = inter / (area1 + area2 - inter)

def non_max_suppression(prediction, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False, multi_label=False, labels=(), max_det=300):
	"""Runs Non-Maximum Suppression (NMS) on inference results

	Returns:
		 list of detections, on (n,6) tensor per image [xyxy, conf, cls]
	"""

	nc = prediction.shape[2] - 5  # number of classes
	xc = prediction[..., 4] > conf_thres  # candidates

	# Checks
	assert 0 <= conf_thres <= 1, f'Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0'
	assert 0 <= iou_thres <= 1, f'Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0'

	# Settings
	min_wh, max_wh = 2, 4096  # (pixels) minimum and maximum box width and height
	max_nms = 30000  # maximum number of boxes into torchvision.ops.nms()
	time_limit = 10.0  # seconds to quit after
	redundant = True  # require redundant detections
	multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)

	t = time.time()
	output = [np.zeros((0, 6))] * prediction.shape[0]
	for xi, x in enumerate(prediction):  # image index, image inference
		# Apply constraints
		# x[((x[..., 2:4] < min_wh) | (x[..., 2:4] > max_wh)).any(1), 4] = 0  # width-height
		x = x[xc[xi]]  # confidence

		# Cat apriori labels if autolabelling
		if labels and len(labels[xi]):
			l = labels[xi]
			v = np.zeros((len(l), nc + 5))
			v[:, :4] = l[:, 1:5]  # box
			v[:, 4] = 1.0  # conf
			v[range(len(l)), l[:, 0].long() + 5] = 1.0  # cls
			x = np.concatenate((x, v), 0)

		# If none remain process next image
		if not x.shape[0]:
			continue

		# Compute conf
		x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf

		# Box (center x, center y, width, height) to (x1, y1, x2, y2)
		box = xywh2xyxy(x[:, :4])
		conf = x[:, 5:].max(-1).reshape(-1, 1)
		j = x[:, 5:].argmax(-1).reshape(-1, 1)
		
		x = np.concatenate((box, conf, j), 1)[conf.reshape(-1) > conf_thres]

		# Check shape
		n = x.shape[0]  # number of boxes
		if not n:  # no boxes
			continue
		elif n > max_nms:  # excess boxes
			x = x[x[:, 4].argsort(descending=True)[:max_nms]]  # sort by confidence

		# Batched NMS
		c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
		boxes, scores = x[:, :4] + c, x[:, 4]  # boxes (offset by class), scores
		# i = torchvision.ops.nms(boxes, scores, iou_thres)  # NMS
		i = cv2.dnn.NMSBoxes(boxes, scores, conf_thres, iou_thres)
		if i.shape[0] > max_det:  # limit detections
			i = i[:max_det]

		output[xi] = x[i]
		if (time.time() - t) > time_limit:
			print(f'WARNING: NMS time limit {time_limit}s exceeded')
			break  # time limit exceeded

	return output

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
	# Resize and pad image while meeting stride-multiple constraints
	shape = im.shape[:2]  # current shape [height, width]
	if isinstance(new_shape, int):
		new_shape = (new_shape, new_shape)

	# Scale ratio (new / old)
	r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
	if not scaleup:  # only scale down, do not scale up (for better val mAP)
		r = min(r, 1.0)

	# Compute padding
	ratio = r, r  # width, height ratios
	new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
	dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
	if auto:  # minimum rectangle
		dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
	elif scaleFill:  # stretch
		dw, dh = 0.0, 0.0
		new_unpad = (new_shape[1], new_shape[0])
		ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

	dw /= 2  # divide padding into 2 sides
	dh /= 2

	if shape[::-1] != new_unpad:  # resize
		im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
	top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
	left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
	im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
	return im, ratio, (dw, dh)

def run(weights=ROOT / 'best.onnx',  # model.pt path(s)
		source='',  # file/dir/URL/glob, 0 for webcam
		imgsz=640,  # inference size (pixels)
		conf_thres=0.25,  # confidence threshold
		iou_thres=0.45,  # NMS IOU threshold
		max_det=1000,  # maximum detections per image
		classes=None,  # filter by class: --class 0, or --class 0 2 3
		agnostic_nms=False,  # class-agnostic NMS
		save_path=ROOT / 'runs/detect',  # save results to project/name
		end_with=0,
		):
	source = str(source)

	# Directories
	save_dir = Path(save_path)  # increment run
	if not os.path.exists(save_dir):
		os.makedirs(save_dir)

	# Load model
	w = str(weights[0] if isinstance(weights, list) else weights)
	stride = 32

# 	session = onnxruntime.InferenceSession(w, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
	session = onnxruntime.InferenceSession(w)
	imgsz = check_img_size(imgsz, s=32)  # check image size

	index = 0

	for root, dirs, files in tqdm(os.walk(source)):
		for f in files:
			try:
				if f[-4:] != ".jpg":
					continue
				# if f != "1468_F_Baidu_Female_workplace_pic2.jpg":
				# 	continue
				if root.strip().split("/")[-1] == "Baidu_Female_workplace_pic2":
					continue

				img_path = os.path.join(root, f)
				img0 = cv2.imread(img_path)
				img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB) # BGR to RGB
				if img.shape[0] < 300 or img.shape[1] < 300:
					continue
				# Padded resize
				img = letterbox(img, imgsz, stride=stride, auto=False)[0]

				# Convert
				img = img.transpose((2, 0, 1)) # HWC to CHW, BGR to RGB
				img = np.ascontiguousarray(img)
				img = img.astype('float32')
				img = img / 255.0  # 0 - 255 to 0.0 - 1.0
				if len(img.shape) == 3:
					img = img[None]  # expand for batch dim

				# Inference
				# print(session.get_outputs()[0].name, session.get_outputs()[1].name, session.get_outputs()[2].name)
				pred = session.run([session.get_outputs()[0].name, session.get_outputs()[1].name, session.get_outputs()[2].name], {session.get_inputs()[0].name: img})
				output8 = np.array(pred[0])  #4800
				output16 = np.array(pred[1])  #1200
				output32 = np.array(pred[2])  #300

				# endwithconcat = False
				# endwithreshape = False
				# endwithsqueeze = True

				# print(output8.shape, output16.shape, output32.shape)

				if 0 == end_with: #endwithconcat or endwithsqueeze
					output = np.concatenate([output8, output16, output32], axis=2)
					output = output.reshape(1, -1, 7)

				elif 1 == end_with: #endwithreshape
					output = np.concatenate([output8, output16, output32], axis=1)
					output = output.reshape(1, -1, 7)

				# print(max(output[0, :, 4]))
				# print(max(output[0, :, 5]))
				# print(max(output[0, :, 6]))

				# NMS
				pred = non_max_suppression(output, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
				# Process predictions
				nhead = 0
				nbody = 0
				f = Path(img_path)  # to Path
				save_path = str(save_dir / f.name)  # img.jpg
				nhead = 0
				nbody = 0	
				xyxy_head = []
				xyxy_body = []				
				for i, det in enumerate(pred):  # per image
					# normalization gain whwh
					if len(det):
						# Write results
						det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

						for *xyxy, conf, cls in reversed(det):


							# cv2.rectangle(img0, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
							# cv2.putText(img0, str(int(cls)) + ":" + str(round(conf, 3)), (int(xyxy[0]) + 10, int(xyxy[1])-10), 0, 0.5, (255, 0, 0))

							if(int(cls)==0):
								nbody+=1
								xyxy_body.append(xyxy)
							if(int(cls)==1):
								nhead+=1
								xyxy_head.append(xyxy)
						# cv2.imwrite("/root/data/save_data/a.jpg", img0)
				if ((nhead ==1) and (nbody==1)):
					pre_cleaned_picture_path = img_path
					pre_cleaned_folder = pre_cleaned_picture_path.split('/')[-2]
					pre_cleaned_picture_name = pre_cleaned_picture_path.split('/')[-1]
					cleaned_picture_name = pre_cleaned_picture_name[:-4] + "_F_" + pre_cleaned_folder + pre_cleaned_picture_name[-4:]
					cleaned_picture_path = save_dir / cleaned_picture_name
					# print(cleaned_picture_path)
					iou = box_iou(torch.tensor(xyxy_body), torch.tensor(xyxy_head), True)
					h = xyxy_body[0][3] - xyxy_body[0][1]
					if h > 0.6 * img0.shape[0]:
						if iou > 0.5:
							# cv2.imwrite(save_path, img0)
							os.system("cp %s %s"%(pre_cleaned_picture_path, cleaned_picture_path))	

			except Exception as e:
				print(e)
			

def parse_opt():
	parser = argparse.ArgumentParser()
	parser.add_argument('--weights', nargs='+', type=str, default='/root/model/py_clean/onnx/best_240415_endwithsqueeze.onnx', help='model path(s)')
	parser.add_argument('--source', type=str,
						default='/root/data/fullbody/',
						help='file/dir/URL/glob, 0 for webcam')
	parser.add_argument('--save_path', default='/root/data/fullbody_cleaned_yolo/', help='save results to project/name')
	parser.add_argument('--imgsz', '--img', '--img-size', nargs='+',
						type=int, default=[640, 480], help='inference size h,w')
	parser.add_argument('--conf-thres', type=float,
						default=0.25, help='confidence threshold')
	parser.add_argument('--iou-thres', type=float,
						default=0.5, help='NMS IoU threshold')
	parser.add_argument('--max-det', type=int, default=1000,
						help='maximum detections per image')
	parser.add_argument('--end-with', type=int, default=0,
						help='0:endwithconcat or endwithsqueeze, 1:endwithreshape')

	opt = parser.parse_args()
	opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
	return opt

def main(opt):
	run(**vars(opt))


if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
