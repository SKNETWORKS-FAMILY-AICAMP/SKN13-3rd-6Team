# import chainlit as cl
# from langchain_core.messages import HumanMessage
# from Legend_Chain import final_graph
## 한번에 응답 - 실시간 streaming X
# # =================== Chainlit ===================
# @cl.on_chat_start
# async def on_chat_start():
#     user_id = cl.user_session.get("user_id") or "default"
#     cl.user_session.set("thread_id", f"session-{user_id}")
#     await cl.Message(content="안녕하세요! 무엇을 도와드릴까요?").send()


# @cl.on_message
# async def on_message(message: cl.Message):
#     init_state = {"messages": [HumanMessage(content=message.content)]}
#     thread_id = cl.user_session.get("thread_id")
    
#     result = await final_graph.ainvoke(init_state, config={"configurable": {"thread_id": thread_id}})
    
#     answer = result.get("final_answer", "").strip()
#     source = result.get("source", "llm")
    
#     if not answer or "죄송합니다. 관련 정보를 찾지 못했습니다.".lower() in answer.lower(): 
#         answer = "죄송합니다. 관련 정보를 찾지 못했습니다."
#         source = "llm" 
    
#     await cl.Message(content=f"{answer}\n\n[출처: {source}]").send()

# # pip install chainlit langchain langchain_openai langchain_chroma pydantic chromadb openai


## final_graph에서 준비된 정보를 받아 직접 실시간 스트리밍 LLM 호출

import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage
from Legend_Chain import final_graph, response_synthesis_chain # response_synthesis_chain 임포트 추가

from dotenv import load_dotenv
load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    user_id = cl.user_session.get("user_id") or "default"
    cl.user_session.set("thread_id", f"session-{user_id}")
    cl.user_session.set("message_history", [])
    await cl.Message(content="안녕하세요! 무엇을 도와드릴까요?").send()

@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    current_human_message = HumanMessage(content=message.content)
    message_history.append(current_human_message)

    init_state = {
        "messages": message_history,
        "query": message.content
    }
    thread_id = cl.user_session.get("thread_id")

    msg = cl.Message(content="")
    await msg.send()

    final_answer_text_streamed = ""
    final_source = "llm" # 기본값

    # LangGraph를 실행하여 최종 답변 생성에 필요한 정보를 모두 수집

    result_state = await final_graph.ainvoke(init_state, config={"configurable": {"thread_id": thread_id}})

    # synthesize_response 노드에서 반환된 정보 추출
    # (여기서는 'synthesize_response' 노드의 최종 출력이 딕셔너리로 가정)
    # result_state는 전체 그래프의 최종 상태를 담고 있습니다.
    # 따라서 synthesize_response 노드가 반환한 정보는 result_state에 직접 있을 수 있습니다.
    # GraphState에 'final_answer_context', 'final_answer_user_name', 'final_answer_chat_history', 'final_source' 필드를 추가해야 함.
    # 만약 GraphState를 변경하지 않았다면, synthesize_response가 반환한 값은 'final_answer', 'source' 키로 바로 있을 것입니다.
    # 하지만 위에서 synthesize_response를 '준비 역할'로 바꾸는 경우, GraphState에 새로운 필드를 추가해야 합니다.
    # 이를 피하기 위해, synthesize_response의 반환 값을 result_state에서 직접 추출하거나,
    # 아니면 GraphState에 해당 필드를 추가해야 합니다.

    # 임시로 result_state에서 필요한 정보 추출 (GraphState에 추가했다는 가정 하에)
    context_to_synthesize = result_state.get("final_answer_context", result_state.get("context_str", ""))
    user_name = result_state.get("final_answer_user_name", result_state.get("user_name", ""))
    chat_history_for_llm = result_state.get("final_answer_chat_history", result_state.get("messages", [])[:-1])
    # GraphState에 final_source를 추가했다면 result_state.get("final_source")
    # 아니면 source_for_output = state.source 였던 부분을 직접 가져와야 함.
    final_source = result_state.get("source", "llm") # GraphState에 source 필드가 있다면 바로 가져옴

    # 이제 response_synthesis_chain을 직접 스트리밍으로 호출
    print("DEBUG (Chainlit): Directly calling response_synthesis_chain.astream for final answer...")
    async for chunk in response_synthesis_chain.astream({
        "query": message.content, # 현재 쿼리 사용
        "context": context_to_synthesize,
        "user_name": user_name,
        "chat_history": chat_history_for_llm
    }):
        if chunk.content:
            await msg.stream_token(chunk.content)
            final_answer_text_streamed += chunk.content

    print("DEBUG (Chainlit): Direct LLM astream finished.")

    if not final_answer_text_streamed or "죄송합니다. 관련 정보를 찾지 못했습니다.".lower() in final_answer_text_streamed.lower():
        final_answer_text_streamed = "죄송합니다. 관련 정보를 찾지 못했습니다."
        final_source = "llm"

    msg.content = f"{final_answer_text_streamed}\n\n[출처: {final_source}]"
    await msg.update()

    message_history.append(AIMessage(content=final_answer_text_streamed))
    cl.user_session.set("message_history", message_history)