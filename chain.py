# 📁 my_chain.py

from datetime import date
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from typing import List, Literal, Annotated
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import YouTubeSearchTool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_tavily import TavilySearch

# =================== Embedding & VectorStore ===================
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    embedding_function=embedding_model,
    collection_name="rag_chatbot",
    persist_directory="vector_store/chroma/rag_chatbot"
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})


# -------------------
# ✅ 슬라이딩 윈도우 설정
# -------------------
MAX_MEMORY_MESSAGES = 3

def get_recent_messages(messages):
    return messages[-MAX_MEMORY_MESSAGES:]

# -------------------
# 1️⃣ HYDE
hyde_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    prompt=PromptTemplate(
        template="당신은 저작권 전문 AI입니다. 다음 질문에 대해 검색하기 좋은 설명을 생성하세요:\n{query}",
        input_variables=["query"]
    )
)

# -------------------
# 2️⃣ 벡터 검색기
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

# -------------------
# 3️⃣ 분기 판단기
llm_check_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4.1"),
    prompt=PromptTemplate(
        template="""
질문: {query}
문맥: {context}

- 관련 정보가 일부라도 포함되어 있다면 Y
- 관련은 있으나 정보가 부족하면 N
- 완전 무관하거나 잡담이면 llm_message

하나만 출력: Y / N / llm_message
""",
        input_variables=["query", "context"]
    )
)

# -------------------
# 4️⃣ 답변 체인
answer_chain = LLMChain(
    llm=ChatOpenAI(model_name="gpt-4.1-mini"),
    prompt=PromptTemplate(
        template="""
# Context:
{context}

# Question:
{query}

- 문맥에 명확한 정보가 있으면 답변하세요.
- 없으면 "정보가 부족해서 답할 수 없습니다."라고 하세요.
""",
        input_variables=["context", "query"]
    )
)

# -------------------
# 5️⃣ 툴 바인딩
youtube_search = YouTubeSearchTool()
tavily_search = TavilySearch(
    max_result=3,
    include_images=True,
)
tool_llm = ChatOpenAI(model_name="gpt-4.1-mini").bind_tools(tools=[tavily_search, youtube_search])

# -------------------
# 6️⃣ 상태 클래스
class GraphState(BaseModel):
    messages: Annotated[List, add_messages]
    query: str = ""
    hyde_answer: str = ""
    context_docs: List[Document] = []
    context_str: str = ""
    tool_result: str = ""
    route: Literal["use_rag", "use_tool", "llm_message"] = "use_rag"
    final_answer: str = ""

# -------------------
# 7️⃣ 노드 정의
def run_hyde(state: GraphState):
    recent_messages = get_recent_messages(state.messages)
    latest = recent_messages[-1].content
    hyde = hyde_chain.run({"query": latest})
    return {
        "query": latest,
        "hyde_answer": hyde,
        "messages": recent_messages + [AIMessage(content=hyde)]
    }

def run_retriever(state: GraphState):
    docs = retriever.invoke(state.hyde_answer)
    return {"context_docs": docs, "context_str": format_docs(docs)}

def route_decision(state: GraphState):
    decision = llm_check_chain.run({"query": state.query, "context": state.context_str}).strip().lower()
    if decision == "y":
        return {"route": "use_rag"}
    elif decision == "n":
        return {"route": "use_tool"}
    else:
        return {"route": "llm_message"}

def run_answer(state: GraphState):
    result = answer_chain.run({"context": state.context_str, "query": state.query})
    return {"final_answer": result}

def run_tool(state: GraphState):
    recent_messages = get_recent_messages(state.messages)

    try:
        tool_response = tool_llm.invoke([HumanMessage(content=state.query)])  # ✅ dict → list[HumanMessage]
        tool_text = tool_response.content.strip() if tool_response.content else ""
    except Exception:
        tool_text = ""

    if not tool_text:
        llm_fallback = ChatOpenAI(model_name="gpt-4.1-mini")
        fallback_text = llm_fallback.invoke(state.query).content
        final_text = fallback_text
    else:
        final_text = tool_text

    return {
        "tool_result": tool_text,
        "final_answer": final_text,
        "messages": recent_messages + [AIMessage(content=final_text)]
    }

def fallback_node(state: GraphState):
    llm = ChatOpenAI(model_name="gpt-4.1-mini")
    reply = llm.invoke(state.query).content
    return {
        "final_answer": reply,
        "messages": state.messages + [AIMessage(content=reply)]
    }

# -------------------
# 8️⃣ LangGraph 구성
# -------------------
graph = StateGraph(GraphState)

graph.add_node("hyde", run_hyde)
graph.add_node("check_route", route_decision)
graph.add_node("retrieve", run_retriever)
graph.add_node("answer", run_answer)
graph.add_node("tool_search", RunnableLambda(run_tool))
graph.add_node("fallback", RunnableLambda(fallback_node))

graph.set_entry_point("hyde")
graph.add_edge("hyde", "check_route")

graph.add_conditional_edges("check_route", lambda state: state.route, {
    "use_rag": "retrieve",
    "use_tool": "tool_search",
    "llm_message": "fallback"
})

graph.add_edge("retrieve", "answer")
graph.add_edge("answer", END)
graph.add_edge("tool_search", END)
graph.add_edge("fallback", END)

checkpointer = MemorySaver()
final_graph = graph.compile(checkpointer=checkpointer)

