# 📁 chainlit.py

import chainlit as cl
from langchain_core.messages import HumanMessage
from chain import final_graph  # ✅ 위에서 만든 모듈 import

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content

    init_state = {
        "messages": [HumanMessage(content=user_input)]
    }
    config = {
        "configurable": {"thread_id": "user-1"}
    }

    result = final_graph.invoke(init_state, config=config)

    await cl.Message(content=result["final_answer"]).send()
