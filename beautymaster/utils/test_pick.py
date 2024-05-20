import os
import random

main_dir = "/root/data/fullbody_cleaned_yolo_vl1_5"

for subdir in os.listdir(main_dir):
  subdir_path = os.path.join(main_dir, subdir)

  if not os.path.isdir(subdir_path):
    continue
  
  images_list = []

  for folder in ["images"]:
    folder_path = os.path.join(subdir_path, folder)

    if not os.path.exists(folder_path):
      continue
    
    for filename in os.listdir(folder_path):
      file_path = os.path.join(folder_path, filename)
      
      if not filename.lower().endswith((".jpg", ".json")):
        continue
      
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


