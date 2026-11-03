import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Use a lightweight CPU-friendly embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class LocalSEOKnowledgeBase:
    def __init__(self, db_path="vector_index"):
        self.db_path = db_path
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        self.vector_store = self._init_vector_store()

    def _init_vector_store(self):
        if os.path.exists(self.db_path):
            return FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            # Initialize with default baseline SEO context
            init_docs = [
                Document(page_content="AI Overviews (formerly SGE) heavily favor brands cited with high authority and clear definitions in the top 3 spots."),
                Document(page_content="Brand mention detection looks for exact or fuzzy matches inside Google AI Overview snippets and Bing Copilot blocks.")
            ]
            vector_store = FAISS.from_documents(init_docs, self.embeddings)
            vector_store.save_local(self.db_path)
            return vector_store

    def add_document(self, text, metadata=None):
        doc = Document(page_content=text, metadata=metadata or {})
        self.vector_store.add_documents([doc])
        self.vector_store.save_local(self.db_path)

    def search(self, query, k=2):
        results = self.vector_store.similarity_search(query, k=k)
        return [res.page_content for res in results]