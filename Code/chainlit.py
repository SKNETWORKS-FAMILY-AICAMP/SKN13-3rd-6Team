import chainlit as cl
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from typing import List, Literal, Annotated
from datetime import date
import json 

# tools.py 파일에서 TOOLS를 임포트
from tools import TOOLS

# =================== Embedding & VectorStore ===================
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    embedding_function=embedding_model,
    collection_name="rag_chatbot",
    persist_directory="vector_store/chroma/rag_chatbot"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# =================== Prompt Chains ===================
hyde_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4.1", streaming=True),
    prompt=ChatPromptTemplate.from_template("""#Instruction:
다음 질문에 대해서 완전하고 상세한 답변으로 실제 사실에 기반해서 작성해주세요.
질문과 관련된 내용만으로 작성합니다.
답변과 직접적인 연관성이 없는 내용은 답변에 포함시키지 않습니다.

# 질문:
{query}
""")
)

llm_check_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4.1", streaming=True),
    prompt=ChatPromptTemplate.from_template("""
다음 Context는 사용자의 질문에 대해 충분한 정보를 제공하고 있는가?
질문: {query}
Context: {context}

위 Context만으로 정확하고 신뢰할 수 있는 답변이 가능한 경우 'Y',
불충분하다면 'N',
관련 없는 경우 'llm_message'로 답해주세요.

정확하게 하나의 문자만 출력하세요.
""")
)

# LLM이 도구 결과 요약 및 사용자 정보 기반 답변 생성을 위한 새로운 체인
response_synthesis_llm = ChatOpenAI(model_name="gpt-4.1", streaming=True)
response_synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""
    당신은 사용자에게 친절하고 정확하게 답변하는 AI 어시스턴트입니다.
    오늘 날짜는 {date.today().strftime('%Y년 %m월 %d일')}입니다.
    사용자의 질문과, 제공된 정보 또는 대화 기록을 바탕으로 답변을 완성하세요.
    사용자 이름이 주어졌다면 답변에 친근하게 활용하세요.
    
    # 사용자 정보:
    이름: {{user_name}}
    
    # 대화 기록:
    {{chat_history}}
    
    # 제공된 정보 (도구 실행 결과 또는 RAG 컨텍스트):
    {{context}}
    
    # 답변:
    """),
    ("human", "{query}")
])
response_synthesis_chain = response_synthesis_prompt | response_synthesis_llm


# 엔티티 추출을 위한 LLM 체인
entity_extraction_llm = ChatOpenAI(model_name="gpt-4.1-mini")
entity_extraction_prompt = ChatPromptTemplate.from_template("""
주어진 대화에서 사용자의 이름을 정확히 추출해주세요. 이름만 추출하며, "이름:", "내 이름은"과 같은 접두사는 포함하지 마세요.
이름을 찾을 수 없다면 "None"이라고 답변하세요.

예시:
대화: 안녕 나 강감찬이야
이름: 강감찬

대화: 안녕하세요
이름: None

대화: 내 이름은 김철수야
이름: 김철수

대화: {dialogue}
이름:
""")
entity_extraction_chain = entity_extraction_prompt | entity_extraction_llm

# =================== GraphState ===================
class GraphState(BaseModel):
    messages: Annotated[List, add_messages]
    query: str = ""
    hyde_answer: str = ""
    context_docs: List = []
    context_str: str = ""
    tool_result: str = ""
    route: Literal["use_rag", "use_tool", "llm_message", "tool_call", "synthesize_response"] = "use_rag" 
    final_answer: str = ""
    source: str = ""
    user_name: str = "" 

# =================== Helper Functions ===================
def format_docs(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def run_hyde(state: GraphState):
    latest_message = state.messages[-1].content
    
    hyde_result = hyde_chain.invoke({"query": latest_message})
    
    if isinstance(hyde_result, dict):
        hyde_answer = hyde_result.get("text", hyde_result.get("answer", str(hyde_result)))
    else:
        hyde_answer = str(hyde_result)
            
    print(f"DEBUG: Hyde Answer: '{hyde_answer}'")
    
    return {
        "query": latest_message, # 현재 턴의 질문을 query로 설정
        "hyde_answer": hyde_answer,
        "messages": state.messages + [AIMessage(content=hyde_answer)],
    }

def run_retriever(state: GraphState):
    docs = retriever.invoke(state.hyde_answer)
    
    if not docs:
        print("DEBUG: No documents found by retriever. Routing to tool or fallback.")
        return {"context_docs": [], "context_str": "", "route": "tool_call"} 
        
    context_str = format_docs(docs)
    print(f"DEBUG: Retrieved Context: '{context_str[:200]}...'")
    return {"context_docs": docs, "context_str": context_str, "route": "synthesize_response"}

def route_decision(state: GraphState):
    llm_check_result = llm_check_chain.invoke({"query": state.query, "context": state.context_str})
    
    decision_raw = ""
    if isinstance(llm_check_result, dict):
        decision_raw = llm_check_result.get("text", llm_check_result.get("answer", str(llm_check_result)))
    else:
        decision_raw = str(llm_check_result)
    
    decision = decision_raw.strip().lower()

    print(f"DEBUG: LLM Check Decision Raw: '{decision_raw}'")
    print(f"DEBUG: LLM Check Decision Processed: '{decision}'")

    if decision == "y":
        return {"route": "use_rag"}
    elif decision == "n":
        return {"route": "tool_call"}
    else:
        # LLM이 직접 답변해야 하는 경우에도 synthesize_response를 거치도록 변경
        # query와 messages를 바탕으로 답변을 생성하게 함
        return {"route": "synthesize_response"} 

# =================== Tool Node Functions ===================
tool_calling_llm = ChatOpenAI(model_name="gpt-4.1-mini", streaming=True).bind_tools(TOOLS)

def call_tool_llm(state: GraphState):
    print(f"DEBUG: Calling tool_calling_llm with query: {state.query}")
    response = tool_calling_llm.invoke(state.query)
    
    if response.tool_calls:
        print(f"DEBUG: Tool Call detected: {response.tool_calls}")
        return {"messages": state.messages + [response]}
    else:
        print(f"DEBUG: No tool call, LLM responded directly: {response.content}")
        # LLM이 직접 답변한 경우에도 synthesize_response로 넘겨서 최종 답변 포맷팅
        return {
            "tool_result": response.content, # LLM의 직접 응답을 tool_result에 저장하여 context로 활용
            "messages": state.messages + [response],
            "source": "llm_tool_fallback",
            "route": "synthesize_response" # synthesize_response로 라우팅
        }

def process_tool_result(state: GraphState):
    tool_message = None
    for msg in reversed(state.messages):
        if isinstance(msg, ToolMessage):
            tool_message = msg
            break

    if tool_message:
        tool_output_raw = tool_message.content
        tool_name = tool_message.name
        tool_id = tool_message.tool_call_id

        print(f"DEBUG: Tool execution result for tool '{tool_name}' (ID: {tool_id}): '{tool_output_raw[:200]}...'")
        
        processed_tool_output = ""
        source = tool_name 

        # search_web 도구의 출력 처리
        if tool_name == "search_web":
            try:
                parsed_output = json.loads(tool_output_raw)
                if isinstance(parsed_output, dict) and "results" in parsed_output:
                    search_results_list = parsed_output["results"]
                    if search_results_list:
                        formatted_results = []
                        for res in search_results_list:
                            content_snippet = res.get("content", "내용 없음")
                            if content_snippet:
                                content_snippet = content_snippet[:500] + "..." if len(content_snippet) > 500 else content_snippet
                            formatted_results.append(
                                f"**제목:** {res.get('title', '제목 없음')}\n"
                                f"**URL:** {res.get('url', 'URL 없음')}\n"
                                f"**내용:** {content_snippet}\n"
                                f"---"
                            )
                        processed_tool_output = "\n\n".join(formatted_results)
                    else:
                        processed_tool_output = "인터넷 검색 결과가 없습니다."
                else:
                    processed_tool_output = "인터넷 검색 결과 형식 오류."
            except json.JSONDecodeError as e:
                processed_tool_output = f"인터넷 검색 결과 JSON 파싱 오류: {e}"
                print(f"ERROR: Search web result JSON parsing failed: {e}")
            except Exception as e:
                processed_tool_output = f"인터넷 검색 결과 처리 중 오류 발생: {e}"
                print(f"ERROR: Search web result processing failed: {e}")
        else:
            processed_tool_output = tool_output_raw # LLM이 요약하도록 원본 전달

        if not processed_tool_output or \
           "접근할 수 없습니다" in processed_tool_output or \
           "검색결과가 없습니다" in processed_tool_output:
            
            return {
                "final_answer": "죄송합니다. 도구에서 관련 정보를 찾지 못했습니다.",
                "source": "llm",
                "tool_result": tool_output_raw 
            }
        
        return {
            "tool_result": processed_tool_output,
            "source": source,
            "route": "synthesize_response"
        }
    else:
        print("DEBUG: process_tool_result called but no recent ToolMessage found.")
        return {"final_answer": "도구 실행 결과를 처리할 수 없습니다.", "source": "llm"}


def synthesize_response(state: GraphState):
    print("DEBUG: Entering synthesize_response node.")
    context_to_synthesize = state.context_str 
    if state.tool_result: # tool_result가 있다면 (도구 호출 또는 LLM 직접 응답)
        context_to_synthesize = state.tool_result
        print(f"DEBUG: Synthesizing with Tool Result (or direct LLM response): {context_to_synthesize[:200]}...")
    elif not context_to_synthesize: # RAG 컨텍스트도 없고 tool_result도 없는 경우
        print("DEBUG: No context or tool result to synthesize with.")
        # 이 경우 LLM이 chat_history만으로 답변 시도
        context_to_synthesize = "" 

    try:
        # chat_history를 프롬프트에 포함하여 LLM이 대화 흐름을 이해하도록 함
        # LangChain의 messages 리스트를 그대로 전달
        final_answer_message = response_synthesis_chain.invoke({
            "query": state.query,
            "context": context_to_synthesize,
            "user_name": state.user_name,
            "chat_history": state.messages[:-1] # 마지막 사용자 메시지 제외 (현재 쿼리이므로)
        })
        final_answer_text = final_answer_message.content
        print(f"DEBUG: Synthesized Final Answer: '{final_answer_text}'")
        
        # LLM_tool_fallback이 synthesize_response로 넘어왔을 때 source를 llm으로 변경
        source_for_output = state.source
        if source_for_output == "llm_tool_fallback":
            source_for_output = "llm"

        return {
            "final_answer": final_answer_text,
            "source": source_for_output
        }
    except Exception as e:
        print(f"ERROR: Response synthesis failed: {e}")
        return {"final_answer": "죄송합니다. 답변을 생성하는 데 실패했습니다.", "source": "llm"}


def extract_user_name(state: GraphState):
    last_human_message_content = ""
    for msg in reversed(state.messages):
        if isinstance(msg, HumanMessage):
            last_human_message_content = msg.content
            break

    if last_human_message_content:
        name_extraction_result = entity_extraction_chain.invoke({"dialogue": last_human_message_content})
        extracted_name_raw = name_extraction_result.content.strip()
        
        # '이름:' 접두사 제거
        if extracted_name_raw.startswith("이름:"):
            extracted_name = extracted_name_raw[len("이름:"):].strip()
        else:
            extracted_name = extracted_name_raw
        
        print(f"DEBUG: Extracted name raw: '{extracted_name_raw}'")
        print(f"DEBUG: Extracted name processed: '{extracted_name}'")
        
        if extracted_name.lower() != "none" and extracted_name:
            print(f"DEBUG: User name extracted: '{extracted_name}'")
            return {"user_name": extracted_name}
    
    print("DEBUG: No user name extracted or 'None'.")
    return {"user_name": state.user_name}

def fallback_node(state: GraphState):
    final_answer = state.final_answer or "죄송합니다. 관련 정보를 찾지 못했습니다."
    print(f"DEBUG: Fallback Answer: '{final_answer}'")
    
    # fallback 시에도 synthesize_response를 거치도록 변경
    # fallback은 일반적으로 최종 답변을 내지 않고, LLM에게 최종 답변을 맡기는 역할
    return {"final_answer": final_answer, "source": "llm"} # 직접 답변하지 않고, synthesize_response로 넘어가야 함

# =================== Graph Setup ===================
checkpointer = MemorySaver()
graph = StateGraph(GraphState)

graph.add_node("extract_name", extract_user_name) 
graph.add_node("hyde", run_hyde)
graph.add_node("retrieve", run_retriever)
graph.add_node("check_route", route_decision)
graph.add_node("call_tool_llm", call_tool_llm)
graph.add_node("process_tool_result", process_tool_result)
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(TOOLS)
graph.add_node("tool_runner", tool_node)
graph.add_node("synthesize_response", synthesize_response)
graph.add_node("fallback", fallback_node) # fallback 노드는 synthesize_response로 연결

graph.set_entry_point("extract_name")

graph.add_edge("extract_name", "hyde")

graph.add_edge("hyde", "check_route")

graph.add_conditional_edges("check_route", lambda state: state.route, {
    "use_rag": "retrieve",
    "tool_call": "call_tool_llm",
    "llm_message": "synthesize_response" # llm_message인 경우 synthesize_response로 바로 이동
})

graph.add_edge("retrieve", "synthesize_response")

graph.add_conditional_edges(
    "call_tool_llm",
    # LLM이 도구 호출을 하지 않고 직접 응답한 경우 바로 synthesize_response로 이동
    lambda state: "tool_runner" if hasattr(state.messages[-1], 'tool_calls') and state.messages[-1].tool_calls else "synthesize_response",
    {
        "tool_runner": "tool_runner",
        "synthesize_response": "synthesize_response" # LLM이 직접 응답한 경우
    }
)

graph.add_edge("tool_runner", "process_tool_result")
graph.add_edge("process_tool_result", "synthesize_response")

graph.add_edge("synthesize_response", END)
graph.add_edge("fallback", END) # fallback은 이제 직접 END로 갈 수 있음. (synthesize_response로 라우팅하는 대신)

final_graph = graph.compile(checkpointer=checkpointer)

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