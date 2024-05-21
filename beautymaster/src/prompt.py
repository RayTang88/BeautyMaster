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

vlm_prompt_template = "你是一个专业的服装搭配大师，现在需要你根据输入的图片，为客户设计一套穿搭，包括：衣服，裤子或者单选裙子，其中第{}张图片为客户的全身照，第{}张为候选的衣服，第{}张为候选的裤子，第{}张为候选的裙子，注意：当前处在{}， 气温{}， 客户去{}，请根据以上内容为客户设计三个合适的穿搭方案，方案包括一件衣服和一条裤子或者单选一条裙子，并对每个方案打分，分值在0~100之间，并简明扼要的说明理由。"