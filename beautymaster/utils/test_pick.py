import os
import random

# 主文件夹路径
main_dir = "/root/data/fullbody_cleaned_yolo_vl1_5"

# 遍历所有子文件夹
for subdir in os.listdir(main_dir):
  subdir_path = os.path.join(main_dir, subdir)
  
  # 忽略非文件夹
  if not os.path.isdir(subdir_path):
    continue
  
  images_list = []
  # 遍历 images 和 json 文件夹
  for folder in ["images"]:
    folder_path = os.path.join(subdir_path, folder)
    
    # 忽略不存在的文件夹
    if not os.path.exists(folder_path):
      continue
    
    # 遍历所有文件
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      
      # 忽略非 JPG 和 JSON 文件
      if not filename.lower().endswith((".jpg", ".json")):
        continue
      
      # 检查是否存在对应文件
      corresponding_filename = filename.replace(".jpg", ".json")
      corresponding_file_path = os.path.join(folder_path, corresponding_filename).replace("images", "json")
      
      if os.path.exists(corresponding_file_path):
        images_list.append(file_path)
      

      # print(f"Found a pair: {file_path} and {corresponding_file_path}")

  random.shuffle(images_list)    

  for image_path in images_list[:20]:

    image_test_data_path = image_path.replace("DressCode", "test_data")

    if not os.path.exists(os.path.dirname(image_test_data_path)):
      os.makedirs(os.path.dirname(image_test_data_path))

    # print(image_test_data_path.replace("0.jpg", "1.jpg"))  

    os.system("cp %s %s"%(image_path.replace("0.jpg", "1.jpg"), image_test_data_path.replace("0.jpg", "1.jpg")))

    json_path = image_path.replace("images", "json").replace(".jpg", ".json")

    json_test_data_path = json_path.replace("DressCode", "test_data")

    if not os.path.exists(os.path.dirname(json_test_data_path)):
      os.makedirs(os.path.dirname(json_test_data_path))
    # print(json_test_data_path)  

    os.system("cp %s %s"%(json_path, json_test_data_path))


