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


def mysqlserch():
    import mysql.connector
    import numpy as np
    import faiss

    # 连接到 MySQL 数据库
    conn = mysql.connector.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    cursor = conn.cursor()

    # 创建表来存储向量数据和相关信息
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS embeddings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data BLOB
    )
    ''')

    # 插入示例数据 (嵌入向量)
    def insert_embedding(vector):
        # 将向量转换为二进制格式
        vector_blob = vector.tobytes()
        cursor.execute('INSERT INTO embeddings (data) VALUES (%s)', (vector_blob,))
        conn.commit()

    # 生成一些随机向量并插入数据库
    for _ in range(100):
        vec = np.random.rand(128).astype('float32')
        insert_embedding(vec)

    # 从数据库中检索所有向量
    cursor.execute('SELECT data FROM embeddings')
    rows = cursor.fetchall()

    # 将二进制数据转换回 NumPy 数组
    vectors = [np.frombuffer(row[0], dtype='float32') for row in rows]
    vectors = np.vstack(vectors)

    # 使用 Faiss 构建索引
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    # 执行相似性搜索
    query_vector = np.random.rand(128).astype('float32').reshape(1, -1)
    D, I = index.search(query_vector, k=5)  # 搜索最相似的 5 个向量

    print("Distances:", D)
    print("Indices:", I)

    # 查询原始数据，根据 Faiss 返回的索引从 MySQL 数据库中检索数据
    for idx in I[0]:
        cursor.execute('SELECT * FROM embeddings WHERE id=%s', (idx + 1,))
        print(cursor.fetchone())

    # 关闭数据库连接
    conn.close()

