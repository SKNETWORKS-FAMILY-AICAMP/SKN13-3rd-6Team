import chainlit as cl
from langchain_core.messages import HumanMessage
from Legend_Chain import final_graph

# =================== Chainlit ===================
@cl.on_chat_start
async def on_chat_start():
    user_id = cl.user_session.get("user_id") or "default"
    cl.user_session.set("thread_id", f"session-{user_id}")
    await cl.Message(content="안녕하세요! 무엇을 도와드릴까요?").send()


@cl.on_message
async def on_message(message: cl.Message):
    init_state = {"messages": [HumanMessage(content=message.content)]}
    thread_id = cl.user_session.get("thread_id")
    
    result = await final_graph.ainvoke(init_state, config={"configurable": {"thread_id": thread_id}})
    
    answer = result.get("final_answer", "").strip()
    source = result.get("source", "llm")
    
    if not answer or "죄송합니다. 관련 정보를 찾지 못했습니다.".lower() in answer.lower(): 
        answer = "죄송합니다. 관련 정보를 찾지 못했습니다."
        source = "llm" 
    
    await cl.Message(content=f"{answer}\n\n[출처: {source}]").send()

# pip install chainlit langchain langchain_openai langchain_chroma pydantic chromadb openai