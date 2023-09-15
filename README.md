# Sellsy Personnal ChatBot 🤖
This code will allow you to build a conversationnal chatbot with some additionnal 
knowledge from [Sellsy](https://go.sellsy.com') locally. 


## 1. First steps. 💻
You should first create a virtual environnement to work in. The command: 

``` 
python -m venv .venv
```
should do the trick. 
Your  virtual environnement can be activated through: 
```bash
source .venv/bin/activate
```
From there, install all the required librairies with: 
```bash
pip install -r requirements.txt
```
You can quickly ensure you're good to go by running the command:
```bash
check_main_lib_import.sh
```


## 2. Let's build the SellsyAI bot ! 🎯

### 2.1 Webscrapping 🌎
Since we aim to create a vector database with [Sellsy](https://go.sellsy.com') website content, we need to perform some webscrapping. 
Excecuting: 
```python 
python extract.py
``` 
allow you to do so and saved all retrieved HTML and PDF files in the folder `/web_data`. 

❗️I personnaly do not have huge skills in webscrapping. Feel free to correct the proposed code or point out any mistake I could have made 🙂

### 2.2 Download the LLM model. 🔥

Since we are going to locally run our LLM model, we cannot go with too large model (since they won't fit in your RAM). We get consideration for a model called __LaMini-Flan-T5__. This model is a fine-tuned version of `google/flan-t5-base` on _LaMini-instruction_ dataset that contains 2.58M samples for instruction fine-tuning. Additional information could be found on the [project repository](https://github.com/mbzuai-nlp/lamini-lm). 

```python 
python download.py
```
will automatically download the whole model and some of its config files in the folder `/model` through HuggingFaceHub. 


### 2.3 Create the vector database. 📚

From the HTML files we retrievd, we are going to build up a complete vector database through the extensive use of langchain. 

Launch 
```python 
pyhton ingest.py
```
to build up our vector database. Launching the code will / should take few minutes since we grasped few hundred pages. 


### 2.4 Serve and deploy our model. 🔨

We are going to use a convinient library to locally serve our model through the chainlit library. 
We deploy our model through: 

```python 
chainlit run deploy.py -w
```

Connecting to http://localhost:8000 will give you a local access to your personnal SellsyAIbot. Start chating with it and see how it behaves regarding some specific requests you might have on Seelsy ! 


## 3. To play around and go further

While deploying your chatbot and building the vector database should not give you that much troubles, please find below few adjustments you could do on your own: 

- Add some Sellsy related PDFs you own to rebuild and complete the vector database we initially created. Or even create a new vector database with only a specific type of PDF / .md files and see how your bot behaves.  

- Change the LLM model. You might give a shot to increase the generative abilities of your bot by downloading a larger LMM. You could start through this [one](https://huggingface.co/MBZUAI/LaMini-Flan-T5-77M/tree/main) first or even try Llama2-CPU compliant version. In the later case, only changing the checkpoint path should not be sufficient and some adjustment should be required. 😉 Try to weight the pros & cons of a larger model. Is the time response inscrease worth the gain obtained on responses quality. 

- You current bot version is mostly only looking within the database you've just created. It has for now 
no chat history integration. Using the _ConversationalRetrievalChain_ classes from `langchain.chain` library should help you to designed a better bot  

- Build a cleaner and a better web-scrapping algorithms than the one proposed 📈

