# 我们在`BCEmbedding`中提供langchain直接集成的接口。
from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS as VectorStore
from langchain_community.vectorstores.utils import DistanceStrategy


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
