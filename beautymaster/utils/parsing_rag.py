import os
from json_repair import repair_json

def parsing_rag_func(rag_4o_like_recommended):
    upper=""
    lower=""
    skirt=""
    dresses=""
    
    for category, recommends in rag_4o_like_recommended.items():
        
        for recommend in recommends:
            # TODO
            if(len(recommend.page_content.split("\n")))<3:
                continue
            
            idx = recommend.page_content.split("\n")[1]
            content = recommend.page_content.split("\n")[2]
            if category == "上衣":
                upper+=("%s, %s"%(idx, content))
            if category == "裤子":
                lower+=("%s, %s"%(idx, content))
            if category == "半身裙":
                skirt+=("%s, %s"%(idx, content))
            if category == "连衣裙":
                dresses+=("%s, %s"%(idx, content))

    return upper, lower, skirt, dresses
    