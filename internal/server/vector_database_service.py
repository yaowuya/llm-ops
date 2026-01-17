import os

from injector import inject
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings


@inject
class VectorDatabaseService:
    """向量数据库服务（基于本地FAISS）"""

    vector_store: FAISS
    _embeddings: OpenAIEmbeddings
    _index_path: str

    def __init__(self):
        """构造函数，完成FAISS向量数据库实例的创建或加载"""
        self._embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._index_path = os.environ.get("FAISS_INDEX_PATH", "./storage/faiss_index")

        # 尝试加载已有索引，若不存在则创建空索引
        if os.path.exists(self._index_path):
            self.vector_store = FAISS.load_local(
                self._index_path,
                self._embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            # 创建空的FAISS索引
            self.vector_store = FAISS.from_texts([""], self._embeddings)

    def add_documents(self, documents: list[Document]) -> None:
        """添加文档到向量数据库"""
        self.vector_store.add_documents(documents)
        self._save_index()

    def _save_index(self) -> None:
        """保存索引到本地"""
        self.vector_store.save_local(self._index_path)

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        """将对应的文档列表使用换行符进行合并"""
        return "\n\n".join([document.page_content for document in documents])
