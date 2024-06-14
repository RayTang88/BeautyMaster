import os
from json_repair import repair_json

def parsing_rag_func(rag_4o_like_recommended):
    upper=""
    lower=""
    skirt=""
    dresses=""
    
    for _, recommends in rag_4o_like_recommended.items():
        
        for recommend in recommends:
            # TODO
            if(len(recommend.page_content.split("\n")))<2:
                continue
            idx = recommend.metadata["idx"]
            category_en = recommend.page_content.split("\n")[0].replace("category: ", "")
            content = recommend.page_content.split("\n")[1].replace("content: ", "")
            category = content.replace("content: ", "").split("、")[0]
            if category == "上衣" and category_en == "upper_body":
                upper+=("idx: %s, content: %s"%(idx, content))
            if category == "裤子" and category_en == "lower_body":
                lower+=("idx: %s, content: %s"%(idx, content))
            if category == "半身裙" and category_en == "lower_body":
                skirt+=("idx: %s, content: %s"%(idx, content))
            if category == "连衣裙" and category_en == "dresses":
                dresses+=("idx: %s, content: %s"%(idx, content))

    return upper, lower, skirt, dresses
    