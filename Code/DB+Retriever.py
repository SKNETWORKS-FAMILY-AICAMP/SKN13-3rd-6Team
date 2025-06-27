# 1. 데이터 로드
from langchain_community.document_loaders import PyMuPDFLoader

pdf_paths = [
            "저작권법.pdf", 
            "저작권상담사례집2024.pdf", 
            "인공지능과 저작권 제1-2부.pdf", 
            "최진원_알기 쉬운 저작권 계약 가이드북(제2판)_2024.pdf", 
            "naver.pdf",
            "1인 미디어 창작자를 위한 저작권 안내서(2019).pdf",
            "US_copyright.pdf",
            "wipo_copyright.pdf",
            "공공저작물 저작권 관리 및 이용 지침 해설서(개정20240101업로드용).pdf",
            "네이버 블로그.pdf",
            "카카오 서비스 약관20230109.pdf",
            "하버드)해외 저작권, 공정이용 가이드라인.pdf",
            "생성형AI 저작권 가이드라인.pdf"
            ]

import fitz  # PyMuPDF

# markdown에 넣기
def pdfs_as_markdown_blocks(pdf_paths: list[str]) -> list[dict]:
    all_blocks = []

    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        for page in doc:
            blocks_data = page.get_text("dict")["blocks"]
            for block in blocks_data:
                if "lines" not in block:
                    continue
                text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        text += span["text"]
                text = text.strip()
                if text:
                    # 마크다운 구조 분류
                    if text.startswith("제") and "조" in text:
                        all_blocks.append({"type": "section", "text": f"## {text}"})
                    elif text.endswith("가이드") or len(text) < 20:
                        all_blocks.append({"type": "title", "text": f"# {text}"})
                    else:
                        all_blocks.append({"type": "paragraph", "text": text})
    return all_blocks

all_blocks = pdfs_as_markdown_blocks(pdf_paths)
## 2. Text split
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 1. Markdown header 기반 splitter 정의
header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "title"), ("##", "section")])

# 2. 블록 → Markdown 텍스트로 변환
def blocks_to_markdown_text(blocks):
    return "\n\n".join(b["text"] for b in blocks)

markdown_text = blocks_to_markdown_text(all_blocks)

# 3. Markdown header 기준으로 구조 단위로 분할 (Document 객체 반환됨)
structured_chunks = header_splitter.split_text(markdown_text)

# 4. Recursive splitter 설정
recursive_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

# 5. 구조 단위 chunk들을 다시 세부적으로 쪼개고, metadata 유지
final_split_docs = []
for doc in structured_chunks:
    content = doc.page_content      # ✅ Document 객체로부터 텍스트 추출
    metadata = doc.metadata         # ✅ Document 객체로부터 메타데이터 추출

    small_chunks = recursive_splitter.split_text(content)
    for chunk in small_chunks:
        final_split_docs.append(Document(page_content=chunk, metadata=metadata))

len(final_split_docs)
# 3. metadata 반영
from langchain_core.documents import Document

def assign_metadata(docs: list[Document]) -> list[Document]:
    result = []

    for doc in docs:
        text = doc.page_content.lower()
        metadata = doc.metadata.copy()  # 기존 metadata 보존

        # 1. 플랫폼
        platforms = ["네이버", "카카오", "유튜브", "인스타그램", "naver", "kakao", "youtube", "instagram"]
        matched_platforms = [p for p in platforms if p in text]
        if matched_platforms:
            metadata["platform"] = ", ".join(matched_platforms)  # ✅ 리스트를 문자열로 변환

        # 2. 법 영역 (국내/해외)
        if any(word in text for word in ["fair use", "dmca", "united states", "미국"]):
            metadata["law_scope"] = "해외"
        elif any(word in text for word in ["저작권법", "공공누리", "kogl", "대한민국"]):
            metadata["law_scope"] = "국내"

        # 3. 문서 유형
        if any(word in text for word in ["사례", "faq"]):
            metadata["doc_type"] = "사례집"
        elif any(word in text for word in ["가이드", "guide"]):
            metadata["doc_type"] = "가이드"
        elif any(word in text for word in ["법", "조항", "제"]):
            metadata["doc_type"] = "법령"

        # 4. 출처
        if "저작권법" in text:
            metadata["source"] = "저작권법"
        elif "dmca" in text:
            metadata["source"] = "DMCA"
        elif "공공누리" in text or "kogl" in text:
            metadata["source"] = "KOGL"
        elif "크리에이티브 커먼즈" in text or "creative commons" in text:
            metadata["source"] = "CC"

        # 5. 토픽 자동 태깅
        keyword_to_topic = {
            "음악": "음악사용",
            "배경음악": "음악사용",
            "이미지": "이미지사용",
            "ai": "ai저작권",
            "인공지능": "ai저작권",
            "공정이용": "공정이용",
            "인용": "인용",
            "계약": "저작권계약",
            "저작권료": "저작권계약",
            "공공저작물": "공공저작물"
        }
        topics = {tag for keyword, tag in keyword_to_topic.items() if keyword in text}
        if topics:
            metadata["topic"] = ", ".join(topics)  # ✅ 리스트 → 문자열 변환

        # 문서에 metadata 반영
        doc.metadata = metadata
        result.append(doc)

    return result

result_docs = assign_metadata(final_split_docs)

# 4. embedding 모델 생성 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
load_dotenv()
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
## 5. DB 생성
from langchain_chroma import Chroma
from langchain_core.documents import Document
import math

# 1. Chroma 인스턴스 생성
vector_store = Chroma(
    embedding_function=embedding_model,
    collection_name="rag_chatbot",
    persist_directory="vector_store/chroma/rag_chatbot"
)

# 2. 문서 배치 추가 함수 정의
def batch_add_documents(vector_store, documents: list[Document], batch_size: int = 500):
    total = len(documents)
    num_batches = math.ceil(total / batch_size)

    for i in range(num_batches):
        batch = documents[i * batch_size : (i + 1) * batch_size]
        vector_store.add_documents(batch)
        print(f"✅ Added batch {i+1}/{num_batches} (size: {len(batch)})")

# 문서 추가
batch_add_documents(vector_store, result_docs, batch_size=500)

# # 저장 메시지 출력 (persist 호출 없이)
# print("✅ Vector store saved to disk at:", persist_directory)


# 6. Retriever (MMR + MultiQuery)
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

# LLM 인스턴스 생성 (예: temperature=0, gpt-4.1 등)
llm = ChatOpenAI(model="gpt-4.1", temperature=0)

# Chroma 벡터DB의 기본 retriever 사용
retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm
)