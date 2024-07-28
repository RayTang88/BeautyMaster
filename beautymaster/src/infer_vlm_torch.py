import os
import sys
import numpy as np

import numpy as np
import torch
import torchvision.transforms as T
# from decord import VideoReader, cpu
from PIL import Image
from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer

sys.path.append(os.environ.get('CODE_ROOT')+'BeautyMaster/')
from beautymaster.utils.onnx_infer import letterbox, letterbox_keep_new_shape
from .prompt import vlm_prompt_template_4o_en, vlm_prompt_template_4o, vlm_prompt_template, vlm_prompt_body_template , vlm_prompt_caption_template, upper_shape, upper_choice_list, upper_out_format, lower_shape, lower_choice_list, lower_out_format, dresses_shape, dresses_choice_list, dresses_out_format, skirt_shape, skirt_choice_list, skirt_out_format, body_out_format, body_shape


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)

class VLM():
    
    def __init__(self, weights_path, weight_name, awq, openxlab=False):
        
        # weights_path="/group_share/model/"
        # vlm_weight_name="InternVL2-2B/"
        # vlm_awq=False
        # openxlab=True
    
        model_path = weights_path + weight_name
        
        self.model = AutoModel.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            low_cpu_mem_usage=True,
            trust_remote_code=True
        ).eval().cuda()

        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

        self.generation_config = dict(
        num_beams=1,
        max_new_tokens=1024,
        do_sample=False,
        )    


    def build_transform(self, input_size):
        MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
        transform = T.Compose([
            T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
            T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(mean=MEAN, std=STD)
        ])
        return transform


    def find_closest_aspect_ratio(self, aspect_ratio, target_ratios, width, height, image_size):
        best_ratio_diff = float('inf')
        best_ratio = (1, 1)
        area = width * height
        for ratio in target_ratios:
            target_aspect_ratio = ratio[0] / ratio[1]
            ratio_diff = abs(aspect_ratio - target_aspect_ratio)
            if ratio_diff < best_ratio_diff:
                best_ratio_diff = ratio_diff
                best_ratio = ratio
            elif ratio_diff == best_ratio_diff:
                if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                    best_ratio = ratio
        return best_ratio


    def dynamic_preprocess(self, image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
        orig_width, orig_height = image.size
        aspect_ratio = orig_width / orig_height

        # calculate the existing image aspect ratio
        target_ratios = set(
            (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
            i * j <= max_num and i * j >= min_num)
        target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

        # find the closest aspect ratio to the target
        target_aspect_ratio = self.find_closest_aspect_ratio(
            aspect_ratio, target_ratios, orig_width, orig_height, image_size)

        # calculate the target width and height
        target_width = image_size * target_aspect_ratio[0]
        target_height = image_size * target_aspect_ratio[1]
        blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

        # resize the image
        resized_img = image.resize((target_width, target_height))
        processed_images = []
        for i in range(blocks):
            box = (
                (i % (target_width // image_size)) * image_size,
                (i // (target_width // image_size)) * image_size,
                ((i % (target_width // image_size)) + 1) * image_size,
                ((i // (target_width // image_size)) + 1) * image_size
            )
            # split the image
            split_img = resized_img.crop(box)
            processed_images.append(split_img)
        assert len(processed_images) == blocks
        if use_thumbnail and len(processed_images) != 1:
            thumbnail_img = image.resize((image_size, image_size))
            processed_images.append(thumbnail_img)
        return processed_images


    def load_image(self, image_file, input_size=448, max_num=6):

        if isinstance(image_file, Image.Image):
            image=image_file
        elif isinstance(image_file, np.ndarray):
            print("Image is OpenCV format")
        else:
            image = Image.open(image_file).convert('RGB')

        # Converting a PIL image to a NumPy array 
        # np_image = np.array(image)  
        # np_image, _, _ = letterbox_keep_new_shape(np_image, new_shape=(1920, 1280)) #hw
        # # Converting a NumPy array  to a PIL image
        # image = Image.fromarray(np_image) 

        transform = self.build_transform(input_size=input_size)
        images = self.dynamic_preprocess(image, image_size=input_size, use_thumbnail=True, max_num=max_num)
        pixel_values = [transform(image) for image in images]
        pixel_values = torch.stack(pixel_values)
        return pixel_values


    # def infer_vlm_func(self, weights_path, weight_name, model_candidate_clothes_list, season, weather, determine):

    #     print(model_candidate_clothes_list)

    #     images = [load_image(model_candidate_clothes) for model_candidate_clothes in model_candidate_clothes_list]
        
    #     # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
    #     # vlm_prompt = prompt.vlm_prompt_template.format("16", "1", "2,3,4,5,6", "7,8,9,10,11", "12,13,14,15,16", season, weather, determine, prompt.a_format)
    #     vlm_prompt = vlm_prompt_template
    #     # print(vlm_prompt)
    #     response = self.pipe((vlm_prompt, images), gen_config=self.gen_config)

    #     # print(response.text)
        
    #     return response.text

    # Simple function to take in a list of text objects and return them as a list of embeddings
    def get_embeddings(input):
        pass
        # response = client.embeddings.create(
        #     input=input,
        #     model=EMBEDDING_MODEL
        # ).data
        # return [data.embedding for data in response]

    def analyze_image(self, image_base64, subcategories):
        pass

        # response = client.chat.completions.create(
        #     model=GPT_MODEL,
        #     messages=[
        #         {
        #         "role": "user",
        #         "content": [
        #             {
        #             "type": "text",
        #             "text": """Given an image of an item of clothing, analyze the item and generate a JSON output with the following fields: "items", "category", and "gender". 
        #                        Use your understanding of fashion trends, styles, and gender preferences to provide accurate and relevant suggestions for how to complete the outfit.
        #                        The items field should be a list of items that would go well with the item in the picture. Each item should represent a title of an item of clothing that contains the style, color, and gender of the item.
        #                        The category needs to be chosen between the types in this list: {subcategories}.
        #                        You have to choose between the genders in this list: [Men, Women, Boys, Girls, Unisex]
        #                        Do not include the description of the item in the picture. Do not include the ```json ``` tag in the output.
                            
        #                        Example Input: An image representing a black leather jacket.

        #                        Example Output: {"items": ["Fitted White Women's T-shirt", "White Canvas Sneakers", "Women's Black Skinny Jeans"], "category": "Jackets", "gender": "Women"}
        #                        """,
        #             },
        #             {
        #             "type": "image_url",
        #             "image_url": {
        #                 "url": f"data:image/jpeg;base64,{image_base64}",
        #             },
        #             }
        #         ],
        #         }
        #     ],
        #     max_tokens=300,
        # )
        # # Extract relevant features from the response
        # features = response.choices[0].message.content
        # return features

    def infer_vlm_4o_like_func(self, full_body_image_path, season, weather, determine):
            
        image = self.load_image(full_body_image_path).to(torch.bfloat16).cuda()

        # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
        # vlm_prompt = prompt.vlm_prompt_template.format("16", "1", "2,3,4,5,6", "7,8,9,10,11", "12,13,14,15,16", season, weather, determine, prompt.a_format)

        data = {"season":season, "weather":weather, "determine": determine, "feature":"我的体型特征", "order":"搭配需要大方简洁", "out_format": out_format}

        vlm_prompt = "<image>\n" + vlm_prompt_template_4o.format(**data)
     
        response = self.model.chat(self.tokenizer, image, vlm_prompt, self.generation_config)

        return response

    def infer_vlm_body_shape_func(self, full_body_image_path, body_shape, body_out_format):
        
        data = {"shape": body_shape, "feature":"我的体型特征", "body_out_format":body_out_format}
        vlm_prompt = "<image>\n" + vlm_prompt_body_template.format(**data)
        # print("full_body_image_path:" ,full_body_image_path)
        # full_body_image_path = '/root/data/test_data/pil/boy.jpg'
        image = self.load_image(full_body_image_path).to(torch.bfloat16).cuda()
        print("infer_vlm_body_shape_func  response 0:")
        response = self.model.chat(self.tokenizer, image, vlm_prompt, self.generation_config)
        print("infer_vlm_body_shape_func  response 1:" ,response)
        
        return response
    
    def infer_vlm_clothes_caption_func(self, clothes_image_path, available_types):
            
        data = {"available_types": available_types, "upper_shape": upper_shape, "upper_choice_list":upper_choice_list, "upper_out_format":upper_out_format,
        "lower_shape": lower_shape, "lower_choice_list":lower_choice_list, "lower_out_format":lower_out_format,
        "dresses_shape": dresses_shape, "dresses_choice_list":dresses_choice_list, "dresses_out_format":dresses_out_format,
        "skirt_shape": skirt_shape, "skirt_choice_list":skirt_choice_list, "skirt_out_format":skirt_out_format,
        }
        
        vlm_prompt = "<image>\n" + vlm_prompt_caption_template.format(**data)
    
    
        image = self.load_image(clothes_image_path).to(torch.bfloat16).cuda()
        
        response = self.model.chat(self.tokenizer, image, vlm_prompt, self.generation_config)

        return response
    

if __name__ == "__main__":
    weights_path="/group_share/model/"
    vlm_weight_name="InternVL2-2B/"
    vlm_awq=False
    openxlab=True
    vlm = VLM(weights_path, vlm_weight_name, vlm_awq, openxlab)
    
    image_path = '/root/data/test_data/pil/boy.jpg'
    response = vlm.infer_vlm_body_shape_func(image_path, body_shape, body_out_format)
    print("response:",response)