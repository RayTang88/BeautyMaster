import sys
import importlib
sys.path.append("/root/code/BeautyMaster/beautymaster/third_party/IDM-VTON")

tryon = importlib.import_module("beautymaster.third_party.IDM-VTON.tryon")


def try_on_func(llm_recommended, full_body_image_path, body_shape_descs):
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

          image = tryon.tryon_func(full_body_image_path, clothes_path, body_shape_descs, match_caption, int(id))

          match_dict["id"] = match["id"]
          match_dict["score"] = match["score"]
          match_dict["category"] = match_category_list
          match_dict["match_reason"] = match_reason
          match_dict["image"] = image
          
          match_result.append(match_dict)

  return match_result        

          
