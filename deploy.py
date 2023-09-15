import chainlit as cl
from chatbot import QA_SellsyAIBot

## chainlit here
@cl.on_chat_start
async def start():
 sellsy_aibot =  QA_SellsyAIBot()
 chain=sellsy_aibot.get_bot()
 msg=cl.Message(content="Firing up the company info bot...")
 await msg.send()
 msg.content= "Hi, I'm the SeelsyAIBot ! 🤖 What is your query?"
 await msg.update()
 cl.user_session.set("chain",chain)


@cl.on_message
async def main(message):
 chain=cl.user_session.get("chain")
 cb = cl.AsyncLangchainCallbackHandler(
  stream_final_answer=True, answer_prefix_tokens=["FINAL","ANSWER"]
  )
 cb.ansert_reached=True
 res=await chain.acall(message, callbacks=[cb])
 answer=res["result"]
 sources=res["source_documents"]

 if sources:
  answer+=f"\nSources: "+str(str(sources))
 else:
  answer+=f"\nNo Sources found"

 await cl.Message(content=answer).send() 