import sys
import importlib
import numpy as np
sys.path.append("./BeautyMaster/beautymaster/third_party/IDM-VTON")
from preprocess.openpose.run_openpose import OpenPose
from preprocess.humanparsing.run_parsing import Parsing
from my_get_maks import get_img_agnostic
from my_get_pose import InferenceAction
from PIL import Image

try_on_module = importlib.import_module("beautymaster.third_party.IDM-VTON.tryon")


class TryOnInterface():
      
  def __init__(self,
               body_model_path,
               human_parsing_model_path,
               try_on_model_path
               ):
    
    body_model_path = "/group_share/model/IDM-VTON/openpose/ckpts"
    config_path = "./beautymaster/third_party/IDM-VTON"
    densepose_model_path = "/group_share/model/IDM-VTON/densepose"
    try_on_model_path = "/group_share/model/IDM-VTON/"
    human_parsing_model_path = "/group_share/model/IDM-VTON/humanparsing"
    
    self.dense_pose = InferenceAction(config_path, densepose_model_path)
    self.body_model = OpenPose(gpu_id=0, body_model_path=body_model_path)
    self.parsing_mask = Parsing(gpu_id=0, human_parsing_model_path=human_parsing_model_path)
    self.try_on = try_on_module.TryOn(try_on_model_path)

  def get_try_on_result(self, full_body_path, clothes_path, full_body_caption, clothes_caption, idx):
    if isinstance(full_body_path, Image.Image):
      img_o=full_body_path
    elif isinstance(full_body_path, np.ndarray):
      print("Image is OpenCV format")
    else:    
      img_o = Image.open(full_body_path)
    size = (768, 1024)
    img_o = img_o.resize(size)
    
    # model = OpenPose(gpu_id=0, body_model_path=body_model_path)
    # keypoints=model('/root/kj_work/IDM-VTON/my_pre_data/img/img1.jpg')
    keypoints=self.body_model(img_o.copy())
    # print(keypoints)

    
    
    # img, mask,parsed = p('/root/kj_work/IDM-VTON/my_pre_data/img')
    img, mask, parsed = self.parsing_mask(img_o.copy())
    # print(parsed.shape)

    
    # img = Image.open('my_pre_data/img/img1.jpg')
    pose_data = np.array(keypoints['pose_keypoints_2d'])
    # pose_data = pose_data.reshape((1, -1))[0]
    # print(pose_data)
    # exit()
    # pose_data = pose_data.reshape((-1, 2))
    # print(pose_data)
    # exit()
    agnostic = get_img_agnostic(img_o.copy(), parsed, pose_data)
    # agnostic.save('my_pre_data/mask.jpg')
    # exit()

    # print('1'*100)
    # model_path = "/group_share/model/IDM-VTON/"
    # TO = tryon.TryOn(model_path)
    # print(2)
    p1 = [full_body_caption]# 衣服的种类，由LLM或者数据库给出
    p2 = [clothes_caption]# 衣服的种类，由LLM或者数据库给出
    
    # img = Image.open('my_pre_data/img/img1.jpg')
    if isinstance(clothes_path, Image.Image):
      cloth=full_body_path
    elif isinstance(clothes_path, np.ndarray):
      print("Image is OpenCV format")
    else:    
      cloth = Image.open(clothes_path)
    # cloth = Image.open(clothes_path)
    # mask = Image.open('/root/kj_work/IDM-VTON_old/my_tryon_test_data/mask.png')

    pose = self.dense_pose.execute(img_o.copy())
    pose = Image.fromarray(pose)
    # pose = Image.open('/root/kj_work/IDM-VTON_old/my_tryon_test_data/pose.jpg')
    
    tryon_result = self.try_on.tryon(p1, p2, pose,  cloth, img_o, agnostic)
    
    return tryon_result    

  def try_on_func(self, llm_recommended, full_body_image_path, body_shape_descs):
    print("llm_recommended[match_content]", llm_recommended)    
    assert len(llm_recommended["match_content"]) > 0
    match_result = []
    for match in llm_recommended["match_content"]:
          match_dict = {}
          id = match["id"]
          match_category_list = match["category"]
          match_id_list = match["match_id"]
          match_caption_list = match["match_caption"]
          match_reason = match["reason"]
          score = match["score"]

          assert len(match_category_list) == len(match_id_list)
          assert len(match_caption_list) == len(match_id_list)

          if "上衣" in match_category_list:

            idx = match_category_list.index("上衣")
            match_id =match_id_list[idx]
            match_caption =match_caption_list[idx]

            clothes_path = "/group_share/data_org/DressCode/upper_body/images/" + match_id.split('_')[0]+"_1.jpg"

            image = self.get_try_on_result(full_body_image_path, clothes_path, body_shape_descs, match_caption, int(id))

            match_dict["id"] = match["id"]
            match_dict["score"] = match["score"]
            match_dict["category"] = match_category_list
            match_dict["match_reason"] = match_reason
            match_dict["image"] = image
            
            match_result.append(match_dict)

    return match_result
  
  def try_on_simple_func(self, clothes_path, full_body_image_path, body_shape_descs, match_caption):
        
    id =0
    image = self.get_try_on_result(full_body_image_path, clothes_path, body_shape_descs, match_caption, int(id))

    return image  

