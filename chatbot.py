from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA


from langchain.llms import HuggingFacePipeline


custom_prompt_template='''Use the following pieces of information to answer the users question. 
If you don't know the answer, please just say that you don't know the answer. Don't make up an answer.

Context:{context}
question:{question}

Only returns the helpful anser below and nothing else.
'''

def set_custom_prompt():
 '''
 Prompt template for QA retrieval for each vector store
 '''
 prompt =PromptTemplate(template=custom_prompt_template, input_variables=['context','question'])

 return prompt

class QA_SellsyAIBot():
    def __init__(self):
        self.embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                              model_kwargs={'device':'cpu'})
        
        self.db_faiss_path = "vectorstores/db_faiss/"
        self.model = 'model/'
        
        self.db = FAISS.load_local(self.db_faiss_path,self.embeddings)
        
        self.load_llm()
        self.qa_prompt=set_custom_prompt()
        self.qa = self.retrieval_qa_chain()
    
   
    def load_llm(self):
        self.llm = HuggingFacePipeline.from_model_id(model_id=self.model,
                                                task = 'text2text-generation',
                                                model_kwargs={"temperature":0.45,"min_length":30, "max_length":350, "repetition_penalty": 5.0,"do_sample":True})

    
    def retrieval_qa_chain(self):
        qa_chain=RetrievalQA.from_chain_type(llm=self.llm,
                                             chain_type="stuff",
                                             retriever=self.db.as_retriever(search_type="similarity",search_kwargs={'k':2}),
                                             return_source_documents=True,
                                             chain_type_kwargs={'prompt':self.qa_prompt  }
  )
        return qa_chain
    
    def get_bot(self):
        return self.qa
    