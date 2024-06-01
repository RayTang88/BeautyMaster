from BCEmbedding.tools.langchain import BCERerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS as VectorStore
from langchain_community.vectorstores.utils import DistanceStrategy


def bce_retriever(weights_path, embedding_model_name, top_n, csv_data, item_dicts):

    # init embedding model
    embedding_model_name = embedding_model_name
    embedding_model_kwargs = {'device': 'cuda'}
    embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True}

    embed_model = HuggingFaceEmbeddings(model_name=weights_path+embedding_model_name,
                                        model_kwargs=embedding_model_kwargs,
                                        encode_kwargs=embedding_encode_kwargs)

    reranker_args = {
        'model': '/group_share/model/bce-embedding-base_v1',
        'top_n': top_n,
        'device': 'cuda',
        'use_fp16': True
    }
    reranker = BCERerank(**reranker_args)

    # init documents
    documents = CSVLoader(csv_data).load()

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
    
    similar_items = {}
    for category, items in item_dicts.items():
      
      # Generate the embedding for the input item
    #   input_embedding = get_embeddings([desc])
    
    #   # Find the most similar items based on cosine similarity
    #   similar_indices = find_similar_items(input_embedding, embeddings, threshold=0.6)
    #   similar_items += [df_items.iloc[i] for i in similar_indices]
    
        response = compression_retriever.get_relevant_documents(items)
        # similar_items.append(response)
        similar_items[category] = response
    
    return similar_items

    # response = compression_retriever.get_relevant_documents('夏天穿的短袖上衣')
    # print(response)
