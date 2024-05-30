clothes_prompt="""{
        "version": "0.0.1",
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n请问这件衣服适合什么季节穿？春、夏、秋、冬？."
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "请问这件衣服的风格怎么样？休闲、正装、运动、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": "请问这件衣服衣袖长度如何？长袖、中袖、短袖、无袖、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "请问这件衣服的衣领是什么形状？高领、圆领、V领、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            {
            "from": "human",
            "value": "请问这件衣服是什么风格？T恤、衬衣、礼服、婚纱、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer5>"
            },
            {
            "from": "human",
            "value": "请问这件衣服是什么颜色？"
            },
            {
            "from": "gpt",
            "value": "<answer6>"
            },
            {
            "from": "human",
            "value": "请问这件衣服的面料是什么？纯棉、化纤、尼龙、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer7>"
            },
            {
            "from": "human",
            "value": "请问这件衣服是什么版型？宽松、修身、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer8>"
            },
            {
            "from": "human",
            "value": "请问这件衣服适合什么性别穿？男性、女性、男女均可？"
            },
            {
            "from": "gpt",
            "value": "<answer9>"
            }
        ]    
    }"""
    
dresses_prompt="""{
        "conversations": [
            {
                "from": "human",
                "value": "图中这条裙子适合什么季节穿？春、夏、秋、冬？."
            },
            {
                "from": "gpt",
                "value": "<answer1>"
            },
            {
                "from": "human",
                "value": "图中这条裙子下摆的长度如何？超短裙、中长未过膝、长裙？"
            },
            {
                "from": "gpt",
                "value": "<answer2>"
            },
            {
                "from": "human",
                "value": "图中这条裙子衣袖长度如何？长袖、中袖、短袖、无袖？"
            },
            {
                "from": "gpt",
                "value": "<answer3>"
            },
            {
                "from": "human",
                "value": "图中这条裙子的衣领是什么形状？高领、圆领、V领、抹胸、低胸露背、吊带、其他？"
            },
            {
                "from": "gpt",
                "value": "<answer3>"
            },
            {
                "from": "human",
                "value": "图中这条裙子是什么风格？晚礼服、休闲风、职业装、旗袍、其他？"
            },
            {
                "from": "gpt",
                "value": "<answer5>"
            },
            {
                "from": "human",
                "value": "图中这条裙子表面有什么特殊的log？纯色、小碎花、印花、中文文字、英文字母、其他？"
            },
            {
                "from": "gpt",
                "value": "<answer6>"
            },
            {
                "from": "human",
                "value": "图中这条裙子是什么颜色？"
            },
            {
                "from": "gpt",
                "value": "<answer7>"
            },
            {
                "from": "human",
                "value": "图中这条裙子是什么版型？宽松、修身、其他？"
            },
            {
                "from": "gpt",
                "value": "<answer8>"
            }
        ]
    }"""
    
trousers_prompt="""{
        "conversations":[
            {
            "from": "human",
            "value": "<image>\n请问这条裤子适合什么季节穿？春、夏、秋、冬？."
            },
            {
            "from": "gpt",
            "value": "<answer1>"
            },
            {
            "from": "human",
            "value": "请问这条裤子的风格怎么样？牛仔裤、休闲裤、正装、运动裤、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer2>"
            },
            {
            "from": "human",
            "value": "请问这条裤子长度如何？长裤、短裤、超短裤、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer3>"
            },
            {
            "from": "human",
            "value": "请问这条裤子是什么版型？宽松、修身、直通、喇叭、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer4>"
            },
            "from": "human",
            "value": "请问这条裤子是什么颜色？"
            },
            {
            "from": "gpt",
            "value": "<answer5>"
            },
            "from": "human",
            "value": "请问这条裤子的面料是什么？纯棉、化纤、尼龙、或者其他？"
            },
            {
            "from": "gpt",
            "value": "<answer6>"
            },
            {
            "from": "human",
            "value": "请问这条裤子适合什么性别穿？男性、女性、男女均可？"
            },
            {
            "from": "gpt",
            "value": "<answer9>"
            }
        ]    
    }"""

model_prompt="""{
    "conversations":[
        {
        "from": "human",
        "value": "<image>\n图中人物的头发是什么颜色？"
        },
        {
        "from": "gpt",
        "value": "<answer1>"
        },
        {
        "from": "human",
        "value": "图中人物的头发长度如何？长发、短发、中长、寸头、秃头？"
        },
        {
        "from": "gpt",
        "value": "<answer2>"
        },
        {
        "from": "human",
        "value": "图中人物的头发的发型是什么风格？卷发、直发、大波浪、齐刘海、妹妹头？"
        },
        {
        "from": "gpt",
        "value": "<answer3>"
        },
        {
        "from": "human",
        "value": "图中人物的体型胖瘦状况如何？肥胖、适中、清瘦？"
        },
        {
        "from": "gpt",
        "value": "<answer4>"
        },
        {
        "from": "human",
        "value": "图中人物的身高状况如何？高大、中等、矮小？"
        },
        {
        "from": "gpt",
        "value": "<answer5>"
        },
        {
        "from": "human",
        "value": "图中人物的腰部粗细如何？水桶腰、正常腰、小蛮腰？"
        },
        {
        "from": "gpt",
        "value": "<answer6>"
        },
        {
        "from": "human",
        "value": "图中人物的脸型如何？圆脸、锥子脸、国字方脸？"
        },
        {
        "from": "gpt",
        "value": "<answer7>"
        },
        {
        "from": "human",
        "value": "图中人物的腿部长度如何？长腿、中等腿、短腿？"
        },
        {
        "from": "gpt",
        "value": "<answer8>"
        },
        {
        "from": "human",
        "value": "图中人物的腿部形状如何？直腿、弯腿、O形腿？"
        },
        {
        "from": "gpt",
        "value": "<answer9>"
        }
    ]    
}"""     


a_format="""{
    "搭配方案":[
        {
            "方案号": "<1>",
            "方案": "<候选衣服中的第几件衣服>+<候选裤子中的第几条裤子>",
            "得分":"<0~100>",
            "理由": "<简明扼要的理由>"
        },
            "方案号": "<2>",
            "方案": "<候选裙子中的第几裙子>",
            "得分":"<0~100>",
            "理由": "<简明扼要的理由>"
        }
    ]    
}"""       


# vlm_prompt_template = "你是一个专业的服装搭配大师，现在需要你根据输入的图片，为客户设计一套穿搭，包括：衣服，裤子或者单选裙子，其中第{}张图片为客户的全身照，第{}张为候选的衣服，第{}张为候选的裤子，第{}张为候选的裙子，注意：当前处在{}， 气温{}， 客户去{}，请在候选的图片中为客户设计三个合适的穿搭方案，方案包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。如果是衣服和裤子的搭配，最后输出的格式如下：搭配方案号{}+候选衣服中的第{}件衣服+候选裤子中的第{}条裤子+打分+简明扼要的理由；如果是单裙子的搭配，最后输出的格式如下：搭配方案号{}+候选裙子中的第{}条裙子+打分+简明扼要的理由。"
# vlm_prompt_template = "你是一个专业的服装搭配大师，请你仔细分析前面输入的{}张图片，其中输入的图片第{}张图片为客户的全身照，第{}张为候选的衣服，第{}张为候选的裤子，第{}张为候选的裙子，注意：当前处在{}， 气温{}， 客户去{}。请结合当前的天气，和气温，重点考虑客户的目的，根据客户全身照，在候选的衣服、候选裤子、候选裙子中为客户设计三套最合适的穿搭方案，方案内容可以包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。最后输出三个搭配的格式请参照：{}。"
vlm_prompt_template = "前面一共提供了2张图片,第一张是全身照,第二张衣服, 请仔细分析并分别描述每一张图片的内容。"

match_prompt_template = "你是一位时尚搭配大师，当前处在{}， 气温{}， 我要去{}，我体型的基本情况描述如下{}，请从以下（ABC）大类中选出三套最合适的搭配：A：上衣：1.{}、2.{}、3.{}、4.{}、5.{};B：裤子：1.{}、2.{}、3.{}、4.{}、5.{};C：裙子：1.{}、2.{}、3.{}、4.{}、5.{};请结合当前的天气，和气温，重点考虑我的目的，根据我的体型，在候选的上衣、候选裤子、候选裙子中为我设计三套最合适的穿搭方案，方案内容可以包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。最后输出三个搭配。"
  
parsing_prompt_template = "将{}中conversations部分的内容整理为一句{}的描述，语句言简意赅， 输出内容只包含这一句描述的内容,不要有其他多余的话"  

vlm_prompt_template_4o_en = """[
    {
    "role": "user",
    "content": [
        {
        "type": "text",
        "text": \"""Given an image of an item of clothing, analyze the item and generate a JSON output with the following fields: "items", "category", and "gender". 
                    Use your understanding of fashion trends, styles, and gender preferences to provide accurate and relevant suggestions for how to complete the outfit.
                    The items field should be a list of items that would go well with the item in the picture. Each item should represent a title of an item of clothing that contains the style, color, and gender of the item.
                    The category needs to be chosen between the types in this list: [upper_boddy, lower_body, dresses].
                    You have to choose between the genders in this list: [Men, Women, Boys, Girls, Unisex]
                    Do not include the description of the item in the picture. Do not include the ```json ``` tag in the output.
                    
                    Example Input: An image representing a black leather jacket.

                    Example Output: {"items": ["Fitted White Women's T-shirt", "White Canvas Sneakers", "Women's Black Skinny Jeans"], "category": "Jackets", "gender": "Women"}
                    \""",
        }
    ],
    }
]"""

out_format = """{"items": ["白色衬衣", "绿色针织小开衫", "黑色紧身牛仔裤"], feature:"H型身材，腰细，腿长且直， 皮肤白皙",reason:"春季，10-15度，天气微凉，白色衬衣加黑色牛仔裤，经典搭配，加绿色小开衫，可以保暖而不失活泼", "category": "夹克", "gender": "Women"}"""

vlm_prompt_template_4o = """您是一位时尚搭配大师，当前处在{season}， 气温{weather}， 我要去{determine}，给定一张{feature}的图片，分析{feature}并生成包含以下字段的 JSON 输出："items"、"category"和"gender"。
                
                    items 字段应该是与图片中的我的体型特征相搭配的衣物列表。每件物品都应代表一件衣服的标题，其中包含物品的款式、颜色和性别，注意：你可以参考图片中的穿搭也可以不参考，但不要全部按照图片中的穿搭内容输出，图片只是提供了我的体型特征，利用您对时尚趋势、风格和性别偏好的理解，根据图片分析我的体型特征，结合当前的季节，气温，和我的出行目的，{order}，为我搭配服装提供准确且相关的建议并写入item字段。
                    category需要在此列表中的类型之间进行选择：[full_body、upper_boddy、lower_body、dresses]。
                    gender您必须在此列表中的性别之间进行选择：[Men、Women、Boys、Girls、Unisex]
                    feature 字段是从提供图片上分析的我的体型特征。
                    reason 字段是选择item字段中搭配的简明理由概述。
                    不要出现图片中包含物品的描述, 图片只是提供了我的体型特征参考。不要在输出中包含 ```json ``` 标签。

                    示例输入：代表皮肤白皙胖胖的女生的图像。

                    示例输出: {out_format}。
                    """
