import os
import numpy as np

from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image
from .prompt import vlm_prompt_template_4o_en, vlm_prompt_template_4o, vlm_prompt_template, vlm_prompt_body_template , vlm_prompt_caption_template, upper_shape, upper_choice_list, upper_out_format, lower_shape, lower_choice_list, lower_out_format, dresses_shape, dresses_choice_list, dresses_out_format, skirt_shape, skirt_choice_list, skirt_out_format
from PIL import Image

class VLM():
    
    def __init__(self, weights_path, weight_name, awq):
        backend_config_awq = TurbomindEngineConfig(session_len=40960,  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.05, 
                                        tp=1,
                                        model_format='awq',
                                        # quant_policy=0,
                                        )  # 两个显卡
        
        backend_config = TurbomindEngineConfig(session_len=40960,  # 图片分辨率较高时请调高session_len
                                        cache_max_entry_count=0.05, 
                                        tp=1,
                                        # quant_policy=0,
                                        )  # 两个显卡

        self.pipe = pipeline(weights_path + weight_name, backend_config=backend_config_awq if awq else backend_config, log_level='INFO')

    def infer_vlm_func(self, weights_path, weight_name, model_candidate_clothes_list, season, weather, determine):

        print(model_candidate_clothes_list)

        images = [load_image(model_candidate_clothes) for model_candidate_clothes in model_candidate_clothes_list]
        
        # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
        # vlm_prompt = prompt.vlm_prompt_template.format("16", "1", "2,3,4,5,6", "7,8,9,10,11", "12,13,14,15,16", season, weather, determine, prompt.a_format)
        vlm_prompt = vlm_prompt_template
        # print(vlm_prompt)
        response = self.pipe((vlm_prompt, images))

        # print(response.text)
        
        return response.text

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
        
        if isinstance(full_body_image_path, Image.Image):
            image=full_body_image_path
        elif isinstance(image, np.ndarray):
            print("Image is OpenCV format")
        else:
            image = load_image(full_body_image_path)
            
        image = load_image(full_body_image_path)

        # vlm_prompt = prompt.vlm_prompt_template.format("1", "2~6", "7~11", "12~16", season, weather, determine, 'n', 'n', 'n', 'n', 'n', 'n')
        # vlm_prompt = prompt.vlm_prompt_template.format("16", "1", "2,3,4,5,6", "7,8,9,10,11", "12,13,14,15,16", season, weather, determine, prompt.a_format)

        data = {"season":season, "weather":weather, "determine": determine, "feature":"我的体型特征", "order":"搭配需要大方简洁", "out_format": out_format}

        vlm_prompt = vlm_prompt_template_4o.format(**data)
     
        response = self.pipe((vlm_prompt, image))

        return response.text

    def infer_vlm_body_shape_func(self, full_body_image_path, body_shape, body_out_format):
        
        data = {"shape": body_shape, "feature":"我的体型特征", "body_out_format":body_out_format}
        vlm_prompt = vlm_prompt_body_template.format(**data)
        # print("full_body_image_path:" ,full_body_image_path)
        
        if isinstance(full_body_image_path, Image.Image):
            image=full_body_image_path
        elif isinstance(full_body_image_path, np.ndarray):
            print("Image is OpenCV format")
        else:
            image = load_image(full_body_image_path)
        response = self.pipe((vlm_prompt, image))

        return response.text
    
    def infer_vlm_clothes_caption_func(self, clothes_image_path, available_types):
            
        data = {"available_types": available_types, "upper_shape": upper_shape, "upper_choice_list":upper_choice_list, "upper_out_format":upper_out_format,
        "lower_shape": lower_shape, "lower_choice_list":lower_choice_list, "lower_out_format":lower_out_format,
        "dresses_shape": dresses_shape, "dresses_choice_list":dresses_choice_list, "dresses_out_format":dresses_out_format,
        "skirt_shape": skirt_shape, "skirt_choice_list":skirt_choice_list, "skirt_out_format":skirt_out_format,
        }
        
        vlm_prompt = vlm_prompt_caption_template.format(**data)
        
        if isinstance(clothes_image_path, Image.Image):
            image=clothes_image_path
        elif isinstance(clothes_image_path, np.ndarray):
            print("Image is OpenCV format")
        else:
            image = load_image(clothes_image_path)
    
        # image = load_image(clothes_image_path)
        
        response = self.pipe((vlm_prompt, image))

        return response.text