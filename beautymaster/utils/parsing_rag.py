import os
from langchain_core.documents.base import Document

def parsing_rag_func(rag_4o_like_recommended):
    upper=[]
    lower=[]
    dresses=[]
    
    for category, recommends in rag_4o_like_recommended.items():
        
        for recommend_ in recommends:
            # TODO
            recommend = Document(recommend_)
            if category == "上衣":
                upper.append("%s, %s；"%(recommend.id, recommend.content))
            if category == "裤子":
                lower.append("%s, %s；"%(recommend.id, recommend.content))
            if category == "裙子":
                dresses.append("%s, %s；"%(recommend.id, recommend.content))
                
    return "上衣："+upper, "裤子："+lower, "裙子"+dresses
    