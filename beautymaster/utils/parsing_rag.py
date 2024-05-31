import os
from json_repair import repair_json
from langchain_core.documents.base import Document

def parsing_rag_func(rag_4o_like_recommended):
    upper="上衣"
    lower="裤子"
    dresses="裙子"
    
    for category, recommends in rag_4o_like_recommended.items():
        
        for recommend in recommends:
            # TODO
            # recommend = Document(recommend_)
            if(len(recommend.page_content.split("\n")))<3:
                continue
            if category == "上衣":
                upper+=("%s, %s；"%(recommend.page_content.split("\n")[1] ,recommend.page_content.split("\n")[2]))
            if category == "裤子":
                lower+=("%s, %s；"%(recommend.page_content.split("\n")[1] ,recommend.page_content.split("\n")[2]))
            if category == "裙子":
                dresses+=("%s, %s；"%(recommend.page_content.split("\n")[1] ,recommend.page_content.split("\n")[2]))
                
    return upper, lower, dresses
    