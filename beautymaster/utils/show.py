from PIL import Image

def show_func(match_results, save_path):
    for match_result in match_results:
        image = match_result["image"]
        id = match_result["id"]

        image.save(save_path+"/new_%s.jpg"%(id))

        # image.show()

