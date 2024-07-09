

import os
import sys
import importlib
import numpy as np
from PIL import Image

sys.path.append(os.environ.get('CODE_ROOT')+"/BeautyMaster/beautymaster/third_party/IDM-VTON")
from preprocess.openpose.run_openpose import OpenPose
from preprocess.humanparsing.run_parsing import Parsing
from my_get_maks import get_img_agnostic, get_img_agnostic2, get_img_agnostic3
from my_get_pose import InferenceAction
try_on_module = importlib.import_module("beautymaster.third_party.IDM-VTON.tryon")
from beautymaster.utils.onnx_infer import letterbox_keep_new_shape


class TryOnInterface():
      
  def __init__(self,
               weight_path,
               code_root_path
               ):
    
    body_model_path = weight_path+"/IDM-VTON/openpose/ckpts"
    config_path = code_root_path+"/BeautyMaster/beautymaster/third_party/IDM-VTON"
    densepose_model_path = weight_path+"/IDM-VTON/densepose"
    try_on_model_path = weight_path+"/IDM-VTON/"
    human_parsing_model_path = weight_path+"/IDM-VTON/humanparsing"
    
    self.dense_pose = InferenceAction(config_path, densepose_model_path)
    self.body_model = OpenPose(gpu_id=0, body_model_path=body_model_path)
    self.parsing_mask = Parsing(gpu_id=0, human_parsing_model_path=human_parsing_model_path)
    self.try_on = try_on_module.TryOn(try_on_model_path)
    
  #Try the results recommended by the large model on the model
  def get_try_on_result(self, full_body_path, clothes_path_list, full_body_caption, clothes_caption_list, category_list, match_id):
    
    if isinstance(full_body_path, Image.Image):
      img_o=full_body_path
    elif isinstance(full_body_path, np.ndarray):
      print("Image is OpenCV format")
    else:    
      img_o = Image.open(full_body_path)
      
    np_image = np.array(img_o)  
    np_image, _, _ = letterbox_keep_new_shape(np_image, new_shape=(1024, 768)) #hw
    # Converting a NumPy array  to a PIL image
    img_o = Image.fromarray(np_image)
    
    # model = OpenPose(gpu_id=0, body_model_path=body_model_path)
    # keypoints=model('/root/kj_work/IDM-VTON/my_pre_data/img/img1.jpg')
    keypoints=self.body_model(img_o.copy())
    # print(keypoints)

    # img, mask,parsed = p('/root/kj_work/IDM-VTON/my_pre_data/img')
    parsed = self.parsing_mask(img_o.copy())
    # print(parsed.shape)

    # img = Image.open('my_pre_data/img/img1.jpg')
    pose_data = np.array(keypoints['pose_keypoints_2d'])
    # pose_data = pose_data.reshape((1, -1))[0]
    # print(pose_data)
    # exit()
    # pose_data = pose_data.reshape((-1, 2))
    # print(pose_data)
    # exit()
    
    pose = self.dense_pose.execute(img_o.copy())
    pose = Image.fromarray(pose)
    
    tryon_result = img_o.copy()

    for i in range(len(clothes_path_list)):
      category = category_list[i]
      clothes_caption = clothes_caption_list[i]
      clothes_path = clothes_path_list[i]

      agnostic = None
      if "上衣" == category:
        agnostic = get_img_agnostic(img_o.copy(), parsed, pose_data)
        # agnostic.save('/root/data/try_on_data/middle/mask_%d.jpg'%(0))

      elif "裤子" == category or "半身裙" == category:
        agnostic = get_img_agnostic2(img_o.copy(), parsed, pose_data)
        # agnostic.save('/root/data/try_on_data/middle/mask_%d.jpg'%(1))

      elif "连衣裙" == category:
        agnostic = get_img_agnostic3(img_o.copy(), parsed, pose_data)
        # agnostic.save('/root/data/try_on_data/middle/mask_%d.jpg'%(2))


      # print('1'*100)
      # model_path = "/group_share/model/IDM-VTON/"
      # TO = tryon.TryOn(model_path)
      # print(2)
      p1 = [full_body_caption]# 衣服的种类，由LLM或者数据库给出
      p2 = [clothes_caption]# 衣服的种类，由LLM或者数据库给出
      
      # img = Image.open('my_pre_data/img/img1.jpg')
      if isinstance(clothes_path, Image.Image):
        cloth=clothes_path
      elif isinstance(clothes_path, np.ndarray):
        print("Image is OpenCV format")
      else:    
        cloth = Image.open(clothes_path)
      # cloth = Image.open(clothes_path)
      # mask = Image.open('/root/kj_work/IDM-VTON_old/my_tryon_test_data/mask.png')

      # pose = Image.open('/root/kj_work/IDM-VTON_old/my_tryon_test_data/pose.jpg')
      
      tryon_result = self.try_on.tryon(p1, p2, pose,  cloth, tryon_result, agnostic)
      tryon_result.save('/root/data/try_on_data/middle/tryon_result_%s.jpg'%(match_id))
    
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
            #The position of the clothes in the list
            idx = match_category_list.index("上衣")
            match_id =match_id_list[idx]
            match_caption =match_caption_list[idx]

            clothes_path = "/group_share/data_org/DressCode/upper_body/images/" + match_id.split('_')[0]+"_1.jpg"

            image = self.get_try_on_result(full_body_image_path, clothes_path, body_shape_descs, match_caption, int(idx))

            match_dict["id"] = match["id"]
            match_dict["score"] = match["score"]
            match_dict["category"] = match_category_list
            match_dict["match_reason"] = match_reason
            match_dict["image"] = image
            
            match_result.append(match_dict)

    return match_result
  
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
  

  def try_on_func_all(self, llm_recommended, full_body_image_path, body_shape_descs):
      print("llm_recommended[match_content]", llm_recommended)    
      assert len(llm_recommended["match_content"]) > 0
      match_result = []
      if isinstance(llm_recommended, list):
            llm_recommended = llm_recommended[0]
      assert isinstance(llm_recommended, dict)
      print("type--- llm_recommended2", type(llm_recommended))
      match_result = []
      assert len(llm_recommended["match_content"]) > 0
      for match in llm_recommended["match_content"]:
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
            
          assert len(match_category_list) == len(match_id_list)
          assert len(match_caption_list) == len(match_id_list)
          # print("here222222")
          match_dict["id"] = match["id"]
          match_dict["score"] = match["score"]
          match_dict["category"] = match_category_list
          match_dict["match_reason"] = match_reason
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
              # print(os.path.exists(clothes_path), clothes_path)  
              if not os.path.exists(clothes_path):
                  continue
                
              image = Image.open(clothes_path)
              images.append(image)
 
          tryon_image = self.get_try_on_result(full_body_image_path, images, body_shape_descs, match_caption_list, match_category_list, match["id"])
          # tryon_image.save('/root/data/try_on_data/middle/tryon_image_%s.jpg'%(match["id"]))
          match_dict["id"] = match["id"]
          match_dict["score"] = match["score"]
          match_dict["category"] = match_category_list
          match_dict["match_reason"] = match_reason
          match_dict["images"] = images
          match_dict["tryon_image"] = tryon_image

            
          match_result.append(match_dict)

      return match_result

  
  def try_on_simple_func(self, clothes_path, full_body_image_path, body_shape_descs, match_caption):
        
    id =0
    image = self.get_try_on_result(full_body_image_path, clothes_path, body_shape_descs, match_caption, int(id))

    return image  

