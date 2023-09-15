from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import BSHTMLLoader, PyPDFLoader 

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import os
import tqdm 

class DB_FAISS():
    def __init__(self,data_path:str,db_faiss_path:str):
        """
        Given all the HTML pages that were saved from the scrapping operation,
        the class creates a vector store using FAISS and HuggingFace embeddings.
        Args:
            data_path (str): path to the folder where html pages have been saved.
            db_faiss_path (str): path to the folder where the vector store will be saved.
        """
        self.data_path=data_path
        self.db_faiss_path=db_faiss_path
        
        # Create a folder to save our vector store.
        if not os.path.isdir(self.db_faiss_path):
            os.makedirs(self.db_faiss_path,exist_ok=False)
            
        # Each HTML page is going to be split into chunks of 500 characters with an overlap of 50 characters.
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
        # Each chunk of text is going to be embedded using the MiniLM model.
        self.embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                              model_kwargs={'device':'cpu'}
                                            )
        
    def load_documents(self):
        self.documents=[]
        processed_htmls=0
        all_htmls = os.listdir(self.data_path)
        for f in tqdm.tqdm(all_htmls):
            if f.endswith(".html"):
                html_path = os.path.join(self.data_path,f)
                loader = BSHTMLLoader(html_path)
                self.documents.extend(loader.load())
                processed_htmls+=1
            # [You could add a pdf loader here.]
            else:
                continue
        print(f"Processed {processed_htmls}html files")
        
    def create_vector_db(self):
        texts=self.text_splitter.split_documents(self.documents)
    
        # Create a vector store.
        db=FAISS.from_documents(texts,self.embeddings)
        
        # Save your DB. 
        db.save_local(self.db_faiss_path)
    
if __name__ =='__main__':
    db_faiss=DB_FAISS(data_path = "web_data/go_sellsy_com/",
                      db_faiss_path = "vectorstores/db_faiss/")
    db_faiss.load_documents()
    db_faiss.create_vector_db()
    