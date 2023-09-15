from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

import torch 

### INITIALIZING LAMINI MODEL
checkpoint = "./model/"

### INITIALIZING PIPELINE CHAIN WITH LANGCHAIN
llm = HuggingFacePipeline.from_model_id(model_id=checkpoint,
                                        task = 'text2text-generation',
                                        model_kwargs={"temperature":0.45,"min_length":30, "max_length":350, "repetition_penalty": 5.0,"do_sample":True})


template = """{text}"""
prompt = PromptTemplate(template=template, input_variables=["text"])
chat = LLMChain(prompt=prompt, llm=llm)

yourprompt = "What's the impact of AI on the future of work?"
reply = chat.run(yourprompt)
print(reply)