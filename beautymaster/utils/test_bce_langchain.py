# 我们在`BCEmbedding`中提供langchain直接集成的接口。
from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS as VectorStore
from langchain_community.vectorstores.utils import DistanceStrategy



def test_bce():
    # with open('/root/data_org/test_data/sample_style.csv', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in spamreader:
    #         print(', '.join(row))

    # init embedding model

    documents = CSVLoader(
        '/root/data_org/test_data/sample_style2.csv'
    ).load()

    documents2 = CSVLoader(
        '/root/data_org/test_data/sample_style.csv', metadata_columns = ["id", "idx"]
    ).load()

    selected_fields = ["content"]

    # documents1=[]

    # for doc in documents2:
    #     for field in selected_fields:
    #         if field in doc.page_content:
    #             documents1.append(doc.page_content[field])
    # print(documents1)            
    # documents1 = [doc[field] for doc in documents for field in selected_fields if field in doc]

    embedding_model_name = '/root/model/bce-embedding-base_v1/'
    embedding_model_kwargs = {'device': 'cuda'}
    embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True}

    embed_model = HuggingFaceEmbeddings(model_name=embedding_model_name,
                                        model_kwargs=embedding_model_kwargs,
                                        encode_kwargs=embedding_encode_kwargs)

    reranker_args = {
        'model': '/root/model/bce-reranker-base_v1/',
        'top_n': 5,
        'device': 'cuda',
        'use_fp16': True
    }
    reranker = BCERerank(**reranker_args)

    # init documents
    # documents = PyPDFLoader(
    #     '/workspace/GitProjects/BCEmbedding/BCEmbedding/tools/eval_rag/eval_pdfs/Comp_en_llama2.pdf'
    # ).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,
                                                chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # example 1. retrieval with embedding and reranker
    retriever = VectorStore.from_documents(
        texts, embed_model,
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT).as_retriever(
            search_type='similarity',
            search_kwargs={
                'score_threshold': 0.3,
                'k': 10
            })

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=retriever)

    response = compression_retriever.get_relevant_documents('这件上衣适合夏季穿着，风格休闲，长袖V领，材质为纯棉，版型宽松，颜色为白色')
    # response = compression_retriever.invoke('衣适合夏季穿着，风格休闲，长袖V领，材质为纯棉，版型宽松，颜色为白色')
    print(response)


def add():
    # -*- coding: utf-8 -*-
    import math
    import time
    import faiss
    import numpy as np
    
    # 增
    ## 验证新增一个新的id:vector是否能够同步(注：此时的id是之前没有出现过的)
    
    d = 768  # 向量维数
    
    data = [[i] * d for i in range(2000)]
    data = np.array(data).astype('float32')  # 注意，只能插入float32类型的向量 
    ids = np.arange(0, 2000)
    data_length=len(ids)   # 自定义向量的Id
    
    
    nlist = int(4 * math.sqrt(data_length))  # 聚类中心的个数
    time1 = time.time()
    
    quantizer = faiss.IndexFlatL2(d)  # 内部的索引方式依然不变
    index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)  # 倒排索引
    index.train(data)  # 注意，倒排索引一定要进行train
    index.add_with_ids(data,ids)
    print(index.is_trained)
    time2 = time.time()
    print(f'构建索引插入数据的时间为{time2 - time1}')
    
    
    query_vector = np.array([[1] * 768]).astype('float32')
    dis, ind = index.search(query_vector, 1)  # 1代表返回的结果数
    print(f'全1向量的最近的向量id为{ind}')
    print(dis)
    
    
    
    add_data = np.array([[1000] * 768]).astype('float32')
    add_id = np.array([3000])
    index.add_with_ids(add_data, add_id)
    print(f'\n注意插入数据后的样本总数为{index.ntotal}')
    
    query_vector = np.array([[1000] * 768]).astype('float32')
    dis, ind = index.search(query_vector, 1)
    print(f'新插入的全1000向量的最近的向量id为{ind}')
    print(dis)
    
    query_vector = np.array([[1] * 768]).astype('float32')
    dis, ind = index.search(query_vector, 1)
    print(f'\n全1向量的最近的向量id为{ind}')
    print(dis)
 
 
def test_faiss():
    pass
