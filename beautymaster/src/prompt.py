
#1.This is a prompt to describe clothes.
clothes_prompt="""{
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
            "value": "请问这件衣服是什么类型？T恤、衬衣、礼服、婚纱、或者其他？"
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
    
# #1.1.this template is for vlm describe the body shape
# ##1.1.1 Describe the body shape from the following dimensions
# upper_shape=["衣服适合什么季节穿","衣服的风格怎么样", "衣服衣袖长度如何", "衣服的衣领是什么形状", "衣服是什么类型", "衣服是什么颜色", "衣服的面料是什么", "衣服是什么版型", "衣服适合什么性别穿"]
# ##1.1.2 Describe the body shape output format
# upper_out_format = """{"items": ["春、秋", "休闲", "中袖", "V领", "T恤", "黑色", "纯棉", "宽松", "男性"], "category":"上衣"}"""
# ##1.1.3 this template is for vlm describe the body shape 
# vlm_prompt_upper_template = """你是一位时尚搭配大师，你需要为我搭配服装，但是做这个之前你需要仔细观察提供的{category}，请从{upper_shape}这几个维度分析,分析{feature}并生成包含以下字段的 JSON 输出："items"。
#                     items 字段应该是图片中的{feature}的各个维度的特征，与upper_shape中字段一一对应。
#                     upper_shape中的部分字段可选范围如下：
#                     这件衣服适合什么季节穿，应该在[春、夏、秋、冬]中选择一个或者多个；衣服的风格怎么样，在[休闲、正装、运动、或者其他]中选；衣服衣袖长度如何, 在[长袖、中袖、短袖、无袖、或者其他]中选；衣服的衣领是什么形状，在[高领、圆领、V领、或者其他]中选；
#                     衣服是什么类型，在[T恤、衬衣、礼服、婚纱、或者其他]中选；衣服的面料是什么，在[纯棉、化纤、尼龙、或者其他]中选；衣服是什么版型，在[宽松、修身、或者其他]中选；衣服适合什么性别穿, 在[男性、女性、男女均可]中选；
#                     禁止出现图片中包含物品的描述, 图片只能用来分析{feature}特征。不要在输出中包含 ```json ``` 标签。
#                     示例输出: {upper_out_format}。"""    
#2.This is a prompt to describe dresses.    
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
#3.This is a prompt to describe trousers.        
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
            "value": "请问这条裤子是什么版型？宽松、修身、直筒、喇叭、或者其他？"
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
            "value": "<answer7>"
            }
        ]    
    }"""

#4.This is a prompt to describe model.  
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
#5.This template is the original template for using VLM for recommendation
# vlm_prompt_template = "你是一个专业的服装搭配大师，现在需要你根据输入的图片，为客户设计一套穿搭，包括：衣服，裤子或者单选裙子，其中第{}张图片为客户的全身照，第{}张为候选的衣服，第{}张为候选的裤子，第{}张为候选的裙子，注意：当前处在{}， 气温{}， 客户去{}，请在候选的图片中为客户设计三个合适的穿搭方案，方案包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。如果是衣服和裤子的搭配，最后输出的格式如下：搭配方案号{}+候选衣服中的第{}件衣服+候选裤子中的第{}条裤子+打分+简明扼要的理由；如果是单裙子的搭配，最后输出的格式如下：搭配方案号{}+候选裙子中的第{}条裙子+打分+简明扼要的理由。"
# vlm_prompt_template = "你是一个专业的服装搭配大师，请你仔细分析前面输入的{}张图片，其中输入的图片第{}张图片为客户的全身照，第{}张为候选的衣服，第{}张为候选的裤子，第{}张为候选的裙子，注意：当前处在{}， 气温{}， 客户去{}。请结合当前的天气，和气温，重点考虑客户的目的，根据客户全身照，在候选的衣服、候选裤子、候选裙子中为客户设计三套最合适的穿搭方案，方案内容可以包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。最后输出三个搭配的格式请参照：{}。"
vlm_prompt_template = "前面一共提供了2张图片,第一张是全身照,第二张衣服, 请仔细分析并分别描述每一张图片的内容。"

#6.this template is for vlm describe the body shape
##6.1 Describe the body shape from the following dimensions
body_shape=["头发的颜色","头发的长度", "发型风格", "皮肤颜色", "胖瘦状况", "身高状况", "腰部粗细", "腿部长度", "腿部形状", "体型如何"]
##6.2 Describe the body shape output format
body_out_format = """{"items": ["金色", "长发", "大波浪", "黄色皮肤", "匀称身材", "身高偏高", "腰部纤细", "腿部偏长", "O型腿", "细沙漏型体型" ], "gender": "女性"}"""
##6.3 this template is for vlm describe the body shape 
vlm_prompt_body_template = """你是一位时尚搭配大师，你需要为我搭配服装，但是做这个之前你需要仔细观察并描述我的体型特征，请从{shape}这几个维度分析,分析{feature}并生成包含以下字段的 JSON 输出："items"和"gender"。
                    items 字段应该是图片中的我的体型特征，与shape中字段一一对应。注意：禁止出现图片中包含物品的描述, 图片只能用来分析我的体型特征。不要在输出中包含 ```json ``` 标签。
                    gender 字段必须根据图片内容判别图中人物的性别，在此列表中的性别之间进行选择：[男性、女性、男孩、女孩、无性别]。
                    示例输入：代表皮肤白皙的女生的图像。
                    示例输出: {body_out_format}。"""
                    
#7.This template is based on body shape characteristics, using LLM to make preliminary recommendations                   
llm_prompt_template_4o = """您是一位时尚搭配大师，当前处在{season}， 气温{weather}， 我是{gender}，要去{determine}，我的体型特征如下:{shape}，仔细分析并生成包含以下字段的 JSON， 输出："items"、"feature"、"reason"、"category"和"gender"。
                    items 字段应该是与shape中描述的我的体型特征相搭配的衣物列表。每件物品都应代表一件衣服的标题，其中包含物品的款式、颜色和适合的性别，注意：利用您对时尚趋势、风格和性别偏好的理解，根据shape字段中描述的我的体型特征，重点结合当前的季节，气温，和我的出行目的，冬季还需要考虑御寒，夏季需要清凉，{additional_requirements}，为我搭配服装提供准确且相关的建议并写入item字段。
                    category需要在{available_types}，这几个服装类型之间进行选择，且和items字段中搭配的服装类型一一对应。
                    gender您必须在[男性、女性、男孩、女孩、无性别]，这几个性别之间进行选择，可以从{gender}中直接获取。
                    feature 字段是分析的我的体型特征,可以从{shape}中直接获取。
                    reason 字段是选择item字段中搭配的简明理由概述。
                    不要在输出中包含 ```json ``` 的文字。
                 
                    以下是示例输出: {recommend_format}，请严格遵循此格式输出。
                    """                    
#8.This template is the original template for using LLM for recommendation
match_prompt_template = "你是一位时尚搭配大师，当前处在{}， 气温{}， 我要去{}，我体型的基本情况描述如下{}，请从以下（ABC）大类中选出三套最合适的搭配：A：上衣：1.{}、2.{}、3.{}、4.{}、5.{};B：裤子：1.{}、2.{}、3.{}、4.{}、5.{};C：裙子：1.{}、2.{}、3.{}、4.{}、5.{};请结合当前的天气，和气温，重点考虑我的目的，根据我的体型，在候选的上衣、候选裤子、候选裙子中为我设计三套最合适的穿搭方案，方案内容可以包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间。最后输出三个搭配。"


#9.This template is used after the rag module is completed, and the results of rag are input into llm for refined recommendation
##9.1 this is recommend format
upper_lower_format="""{"match_content":[{"id": "1", "category": ["上衣","裤子"], "match_id": ["idx", "idx"], "match_caption":["这件上衣则亮色或印花款式，增加整体的活力感", "这条裤子简洁大方，穿搭效果好"], "score": 95.5, "reason": "" },
                       {"id": "2", "category": ["上衣","半身裙"], "match_id": ["idx", "idx"], "match_caption":["这件上衣轻薄透气的，可以保持凉爽舒适", "这条A字型半身裙，既能够凸显您的腰部线条，又能够适应空调房内的温度"], "score": 85.5, "reason": ""},
                       {"id": "3", "category": ["连衣裙"], "match_id": ["idx"], "match_caption":["这条连衣裙可以展现你的沙漏型身材，突出腰部和腿部的优势"], "score": 75.5, "reason": ""}]}"""   
##9.2 this is template
match_prompt_template_raged = """你是一位时尚搭配大师，当前处在{season}， 气温{weather}， 我的性别是{gender}, 要去{determine}，我体型的基本情况描述如下:{shape}。
                                候选的上衣：[{upper}] 
                                候选裤子：[{lower}]
                                候选半身裙: [{skirt}]
                                候选连衣裙：[{dresses}]
                                请结合当前的天气，和气温，重点考虑我的目的，根据我的体型，在前面的：候选的上衣、候选裤子、候选半身裙、候选连衣裙中为我组合出三套合适的穿搭方案，{additional_requirements}，搭配方案可选组合：1.上衣和一条裤子；2.单选一条连衣裙；3.上衣和一条半身裙;4.外套和一条连衣裙。生成包含以下字段的 JSON 输出："id"、"category"、"match_id"、"score"、"reason"
                                其中id 字段是表示当前的搭配方案是第几个，请在[1, 2, 3]列表中选；match_id 是当前搭配方案中的的服装的idx，需要分别在前面列出的候选的上衣、候选裤子、候选半身裙、候选连衣裙列表中选，并且将选中服装的相应的的idx填进去；category是当前搭配方案的服装类别组成的列表，需要[外套、上衣、裤子、半身裙、连衣裙]之间选择，是match_id字段中选择的服装category字段；match_caption是当前搭配方案中服装的描述，需要分别在前面列出的候选的上衣、候选裤子、候选半身裙、候选连衣裙列表，相应的的content中选；score 字段是对当前搭配方案的一个功能+美学的评分，在0~100中选择；reason 字段是选择当前搭配方案原因的简要概述。
                                示例输出: {upper_lower_format}。输出要求如下：1.请遵循此格式输出三个方案；2.示例输出只是一个格式的参考，禁止按照示例输出中的内容，原样输出；3.不需要其余多余的的解释性内容，不要在输出中包含 ```json ``` 标签"""

#10. This template is used to parse the json generated by vlm                    
parsing_prompt_template = "将{}中conversations部分的内容整理为一句{}的描述，语句言简意赅， 输出内容只包含这一句描述的内容,不要有其他多余的话。"  


#11.The following prompt words are completely based on the prompt words used in gpt-4o. Input the model picture and the output is the matching.
##11.1 the english prompt template
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

##11.2 the output format of recommend
recommend_format = """{"items": ["女士白色衬衣", "女士黑色紧身牛仔裤", "女士绿色长裙"], "category": ["上衣","裤子","连衣裙"], feature:"H型身材，腰细，腿长且直， 皮肤白皙",reason:"春季，10-15度，天气微凉，白色衬衣加黑色牛仔裤，经典搭配，或者单独搭配一套长裙加小开衫也是可以的", "gender": "女性"}"""

##11.3 the chinese prompt template
vlm_prompt_template_4o = """您是一位时尚搭配大师，当前处在{season}，气温{weather}，我要去{determine}，给定一张{feature}的图片，分析{feature}并生成包含以下字段的 JSON 输出："items"、"feature"、"reason"、"category"和"gender"。
                
                    items 字段应该是与图片中的我的体型特征相搭配的衣物列表。每件物品都应代表一件衣服的标题，其中包含物品的款式、颜色和适合的性别，注意：禁止按照图片中的穿搭内容输出，图片只能用来分析我的体型特征，利用您对时尚趋势、风格和性别偏好的理解，根据图片分析我的体型特征，重点结合当前的季节，气温，和我的出行目的，冬季还需要考虑御寒，夏季需要清凉，{order}，为我搭配服装提供准确且相关的建议并写入item字段。
                    category需要在此列表中的类型之间进行选择：[外套、上衣、裤子、半身裙、连衣裙]之间选择，且和items字段中搭配的类型一一对应。
                    gender您必须在此列表中的性别之间进行选择：[男性、女性、男孩、女孩、无性别]
                    feature 字段是从提供图片上分析的我的体型特征。
                    reason 字段是选择item字段中搭配的简明理由概述。
                    禁止出现图片中包含物品的描述, 图片只能用来分析我的体型特征。不要在输出中包含 ```json ``` 标签。

                    示例输入：代表皮肤白皙的女生的图像。

                    示例输出: {recommend_format}。
                    """

#TODO
#12.this template is for vlm describe the body shape
##12.1 Describe the body shape from the following dimensions
upper_shape=["上衣适合穿着的季节","上衣的风格", "上衣衣袖长度", "上衣衣领的形状", "上衣的类型", "上衣的颜色", "上衣的面料", "上衣的版型", "上衣适合穿着的性别"]
##12.2 Describe the body shape output format
upper_out_format = """{"items": ["春季、秋季", "休闲风格", "中袖", "V领", "T恤", "黑色", "纯棉", "宽松", "男性"], "category":"上衣"}"""

upper_choice_list="""items 字段是图片中的上衣的各个维度的特征，与{upper_shape}中字段一一对应， 其中有部分字段是可选的，请直接在可选列表中选取即可。部分字段可选范围如下：上衣适合穿着的季节，应该在[春季、夏季、秋季、冬季]中选择一个或者多个；上衣的风格，在[休闲、正装、运动、其他]中选；上衣衣袖长度, 在[长袖、中袖、短袖、无袖、其他]中选；上衣衣领的形状，在[高领、圆领、V领、其他]中选；
                    上衣的类型，在[T恤、衬衣、礼服、婚纱、其他]中选；上衣的面料，在[纯棉、化纤、尼龙、其他]中选；上衣的版型，在[宽松、修身、其他]中选；上衣适合穿着的性别, 在[男性、女性、男女均可]中选。"""

lower_shape=["裤子适合穿着的季节","裤子的风格", "裤子的长度", "裤子的版型", "裤子的颜色", "裤子的面料", "裤子适合穿着的性别"]
##12.3 Describe the body shape output format
lower_out_format = """{"items": ["春季", "休闲裤", "长裤", "喇叭", "纯棉", "黑色", "男性"], "category":"裤子"}"""
lower_choice_list = """items 字段是图片中的裤子的各个维度的特征，与{lower_shape}中字段一一对应， 其中有部分字段是内容可选的，请直接在可选列表中选取即可。部分字段可选范围如下：裤子适合穿着的季节，应该在[春季、夏季、秋季、冬季]中选择一个或者多个；裤子的风格，在[牛仔裤、休闲裤、正装、运动裤、其他]中选；裤子的长度, 在[长裤、短裤、超短裤、其他]中选；裤子的版型，在[宽松、修身、直筒、喇叭、其他]中选；
                    裤子的面料，在[纯棉、化纤、尼龙、其他]中选；裤子适合穿着的性别, 在[男性、女性、男女均可]中选。"""

dresses_shape=["连衣裙适合穿着的季节", "连衣裙下摆的长度", "连衣裙衣袖长度", "连衣裙衣领形状", "连衣裙的风格", "连衣裙表面特殊的log", "连衣裙的颜色", "连衣裙的版型"]
##12.4 Describe the body shape output format
dresses_out_format = """{"items": ["冬季", "中长未过膝", "长袖", "低胸露背领", "休闲风格", "小碎花", "黄色", "宽松"], "category":"连衣裙"}"""
dresses_choice_list = """items 字段是图片中的连衣裙的各个维度的特征，与{dresses_shape}中字段一一对应， 其中有部分字段是可选的，请直接在可选列表中选取即可。部分字段可选范围如下：连衣裙适合穿着的季节，应该在[春季、夏季、秋季、冬季]中选择一个或者多个；连衣裙下摆的长度，在[超短裙、中长未过膝、长裙]中选；连衣裙衣袖长度, 在[长袖、中袖、短袖、无袖、或者其他]中选；连衣裙的衣领形状，在[高领、圆领、V领、抹胸、低胸露背、吊带、其他]中选；
                    连衣裙的风格，在[晚礼服、休闲风格、职业装、旗袍、其他]中选；连衣裙表面特殊的log，在[纯色、小碎花、印花、中文文字、英文字母、其他]中选；连衣裙的版型，在[宽松、修身、其他]中选。"""

skirt_shape=["半身裙适合穿着的季节", "半身裙下摆的长度", "半身裙的风格", "半身裙表面特殊的log", "半身裙的颜色", "半身裙的版型"]
##12.5 Describe the body shape output format
skirt_out_format = """{"items": ["冬季", "中长未过膝", "长袖", "低胸露背领", "休闲风格", "小碎花", "黄色", "宽松"], "category":"半身裙"}"""
skirt_choice_list = """items 字段是图片中的半身裙的各个维度的特征，与{skirt_shape}中字段一一对应， 其中有部分字段是可选的，请直接在可选列表中选取即可。部分字段可选范围如下：半身裙适合穿着的季节，应该在[春季、夏季、秋季、冬季]中选择一个或者多个；半身裙下摆的长度，在[超短裙、中长未过膝、长裙]中选；
                    半身裙的风格，在[晚礼服、休闲风格、职业装、旗袍、其他]中选；半身裙表面特殊的log，在[纯色、小碎花、印花、中文文字、英文字母、其他]中选；半身裙的版型，在[宽松、修身、其他]中选。"""



##12.6 this template is for vlm describe the all clothes 
vlm_prompt_caption_template = """你是一位时尚搭配大师，你需要为我搭配服装，但是做这个之前你需要仔细观察提供的图片，请先判断输入图片中服装的类型,请在{available_types}中选服装类型，
                            如果判断输入图片中服装的类型是上衣，请从{upper_shape}这几个维度分析,分析并生成包含以下字段的 JSON 输出："items", "category"。
                            {upper_choice_list}， category字段需要填"上衣";
                            上衣的示例输出: {upper_out_format}
                            如果判断输入图片中服装的类型是裤子，请从{lower_shape}这几个维度分析,分析并生成包含以下字段的 JSON 输出："items", "category"。
                            {lower_choice_list}， category字段需要填"裤子";
                            裤子的示例输出: {lower_out_format}
                            如果判断输入图片中服装的类型是半身裙，请从{skirt_shape}这几个维度分析,分析并生成包含以下字段的 JSON 输出："items", "category"。
                            {skirt_choice_list}， category字段需要填"半身裙";
                            半身裙的示例输出: {skirt_out_format}
                            如果判断输入图片中服装的类型是连衣裙，请从{dresses_shape}这几个维度分析,分析并生成包含以下字段的 JSON 输出："items", "category"。
                            {dresses_choice_list}， category字段需要填"连衣裙";
                            半身裙的示例输出: {dresses_out_format}
                            
                            禁止出现图片中包含物品的描述。不要在输出中包含 ```json ``` 标签。每张图片只包含一种类型的服装，必须准确判断服装的类型，然后按照相应的类型示例输出，输出json"""
                 
#13 This template is used to generate a caption in json format based on the specified data in the image.
vlm_caption_prompt_origin = f"按照以下格式创建数据集:\n {clothes_prompt} \n根据提供的图片按json_string的格式生成问题和答案对。答案必须精简，后面有选项的在选项中选即可。答案必须严格来自图像内容，如果根据图像内容无法确定答案，请回答不知道。最后只输出生成好的json_string部分即可。注意gpt字段的value，<answer>部分是hunman字段value部分问题相对应的回答,不要原样输出。"