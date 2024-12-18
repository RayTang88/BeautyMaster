import pandas as pd
import mysql.connector
import pymysql
from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
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

    # documents2 = CSVLoader(
    #     '/group_share/data_org/DressCode/right_sample_style_correct_sup_removed.csv', metadata_columns = ["id", "idx"]
    # ).load()
    
    documents2 = CSVLoader(
        '/group_share/data_org/DressCode/right_sample_style_correct_sup_removed.csv', metadata_columns = ["idx", "category"]
    ).load()

    selected_fields = ["content"]

    # documents = CSVLoader(csv_data_path, metadata_columns = ["idx"]).load()

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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=640,
                                                chunk_overlap=0)
    # text_splitter = ChineseTextSplitter(chunk_size=640,
    #                                             chunk_overlap=0)
     
    texts = text_splitter.split_documents(documents2)

    # example 1. retrieval with embedding and reranker
    vb_retriever = VectorStore.from_documents(
        texts, embed_model,
        distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT).as_retriever(
            search_type='similarity',
            search_kwargs={
                'score_threshold': 0.3,
                'k': 10
            })
        
        
    bm25retriever = BM25Retriever.from_documents(documents=texts)
    bm25retriever.k = 10 
    
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25retriever, vb_retriever], weights=[0.4, 0.6]) 

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=ensemble_retriever)

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


class MyDatabases():

    def __init__(self, db_config):
        self.conn = mysql.connector.connect(**db_config)
    def close(self):
        self.conn.close()    

    def create_table(self, table_name):

        cursor = self.conn.cursor()

        # 使用预处理语句创建表
        sql = """CREATE TABLE IF NOT EXISTS {0} (
                idx VARCHAR(16),
                category VARCHAR(16),
                content VARCHAR(256),  
                embedding FLOAT )""".format(table_name)
        
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()

    def delete_table(self, table_name):
        
        cursor = self.conn.cursor()

        # 使用预处理语句创建表
        sql = "DROP TABLE IF EXISTS {0}".format(table_name)
        
        cursor.execute(sql)
        self.conn.commit()
        cursor.close()    


    # 读取 CSV 文件并插入数据
    def import_csv_to_table(self, csv_file_path, table_name):
        data = pd.read_csv(csv_file_path)
        cursor = self.conn.cursor()
        for _, row in data.iterrows():
            sql = "INSERT INTO {0} (idx, category, content) VALUES (%s, %s, %s)".format(table_name)
            cursor.execute(sql, tuple(row))
        self.conn.commit()
        cursor.close()

    # 插入数据
    def insert_data_table(self, data):
        cursor = self.conn.cursor()
        sql = "INSERT INTO data_table (column1, column2, columnN) VALUES (%s, %s, %s)"
        cursor.execute(sql, data)
        self.conn.commit()
        cursor.close()

    # 查询数据
    def query_data_table(self, table_name):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM {0}".format(table_name)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.close()

    # 更新数据
    def update_data(self, data, record_id):
        cursor = self.conn.cursor()
        sql = "UPDATE data_table SET column1 = %s, column2 = %s WHERE idx = %s"
        cursor.execute(sql, (*data, record_id))
        self.conn.commit()
        cursor.close()

    # 删除数据
    def delete_data(self, record_id):
        cursor = self.conn.cursor()
        sql = "DELETE FROM data_table WHERE idx = %s"
        cursor.execute(sql, (record_id,))
        self.conn.commit()
        cursor.close()
        
def search():
    # from langchain import OpenAI, SQLDatabase
    from langchain_community.utilities import SQLDatabase
    from langchain.chains import create_sql_query_chain
    from langchain_core.runnables import RunnablePassthrough
    from operator import itemgetter
    import sys, os
    
    sys.path.append(os.environ.get('CODE_ROOT')+"/BeautyMaster/beautymaster")
    sys.path.append(os.environ.get('CODE_ROOT')+"/BeautyMaster")
    from src.infer_llm import LLM
    weights_path=os.environ.get('MODEL_ROOT')
    llm_weight_name="/Qwen2-7B-Instruct-AWQ/"
    llm_awq=True
    llm = LLM(weights_path, llm_weight_name, llm_awq)

    db_user = "ray"
    db_password = "123"
    db_host = "localhost"
    db_name = "Wardrobe"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    query_chain = create_sql_query_chain(llm, db)
    # 将"question"键转换为当前table_chain所需的"input"键。
    table_chain = {"input": itemgetter("question")} | table_chain
    # 使用table_chain设置table_names_to_use。
    full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain
    
    query = full_chain.invoke(
    {"question": "Alanis Morisette的全部类型是什么"}
    )
    print(query)


if __name__ == "__main__":

    # MySQL 配置
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'Wardrobe'
    }

    table_name="sample"

    # 示例调用
    # db = MyDatabases(db_config)
    # # db.create_table(table_name=table_name)
    # # db.delete_table(table_name=table_name)

    # # csv_file_path = '/root/code/BeautyMaster/beautymaster/openxlab_demo/simple_data/right_sample_style_correct_sup_removed.csv'
    # # db.import_csv_to_table(csv_file_path=csv_file_path, table_name=table_name)
    # # db.insert_data(('new_value1', 'new_value2', 'new_valueN'))
    # db.query_data_table(table_name=table_name)
    # # db.update_data(('updated_value1', 'updated_value2'), 1)
    # # db.delete_data(2)

    # # 关闭连接
    # db.close()
    # search()
    test_bce()

