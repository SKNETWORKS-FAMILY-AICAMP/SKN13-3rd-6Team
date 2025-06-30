# SKN13-3rd-6Team

### 🤖 3차 프로젝트: 콘텐츠 크리에이터들을 위한 저작권 정보제공 챗봇 시스템<br>

**개발기간:** 2025.06.26 ~ 2025.06.30

## 💻 팀 소개
## 팀명: 공구함(00과 99즈)🪛

<!-- | **기원준👨‍💻** | **강지윤👩‍💻** | **최호연👨‍💻** | **이명인👨‍💻** |
|:--------------:|:--------------:|:--------------:|:--------------:|
| @usey10        | @thanGyuPark   | @Hyeseo20      | @pbr2858        | -->


<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/14543590-abc0-4274-81b2-b62166b4f462" width="100"/><br/>기원준👨‍💻
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/a35d2590-93c0-4b86-9145-4ec912ead0b3" width="100"/><br/>강지윤👩‍💻
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/3ab67e76-86ae-4f51-b952-645dbd4c26f1" width="60"/><br/>최호연👨‍💻
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/044c3463-0670-4fa5-ab1e-cba03e4029b5" width="100"/><br/>이명인👨‍💻
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/ki-student"><img src="https://img.shields.io/badge/GitHub-ki--student-1F1F1F?logo=github" alt="기원준 GitHub"/></a>
    </td>
    <td align="center">
      <a href="https://github.com/jiyun-kang12"><img src="https://img.shields.io/badge/GitHub-jiyun--kang12-1F1F1F?logo=github" alt="강지윤 GitHub"/></a>
    </td>    <td align="center">
      <a href="https://github.com/oowixj819"><img src="https://img.shields.io/badge/GitHub-oowixj819-1F1F1F?logo=github" alt="최호연 GitHub"/></a>
    </td>    <td align="center">
      <a href="https://github.com/leemyeongin2416"><img src="https://img.shields.io/badge/GitHub-leemyeongin2416-1F1F1F?logo=github" alt="이명인 GitHub"/></a>
    </td>
</table>



### 📌 1. 프로젝트 개요

#### 1.1. 개발 동기 및 목적  

오늘날 **콘텐츠 크리에이터**라는 직업은 유튜브, 블로그, 쇼츠 등 다양한 플랫폼의 성장과 함께 빠르게 증가

👉 **디지털 콘텐츠 산업의 경제적 규모**<br>
과학기술정보통신부와 한국전파진흥협회가 발표한 <디지털 크리에이터 미디어 산업 실태조사>에 따르면, 국내 디지털크리에이터미디어 사업체는 총 11,123개, 종사자는 35,375명, 연간 산업 매출은 약 4조 1,254억 원에 달함
<img src="https://github.com/user-attachments/assets/2ac781e2-0cfc-459d-a37c-f60095352244" width="800" height="350" alt="저작권협회 챗봇"> <br>
(출처: 매일경제 https://www.mk.co.kr/news/culture/10918121)

❗하지만 그에 반해, **저작권에 대한 정보 접근성과 이해도는 여전히 부족한 상황**임

특히 **초보 크리에이터들**은 플랫폼별 정책, 국내외 저작권법, 공정 이용(Fair Use) 기준 등에 대한 **혼란과 어려움**을 겪고 있음

예를 들어, 유튜브와 같은 해외 플랫폼을 활용할 경우, 국내 저작권법을 따라야 하는지, 플랫폼의 정책을 따르는 것이 우선인지, 해외 저작권 기준까지 고려해야 하는지 등이 명확하지 않게 느껴지며, 관련 정보를 일일이 찾아보기 어렵고 복잡하다는 현실적인 문제점이 존재함

<img src="https://github.com/user-attachments/assets/0849ba07-766c-4c05-bdb8-59a88f180498" width="800" height="350" alt="저작권 관련 기사"> <br>
(출처: 경기도의회 웹진 <SNS에 공유만 했는데, 저작권법 위반이라니?> https://webzine.ggc.go.kr/?p=38108&utm_source=chatgpt.com)


#### 1.2. 본 챗봇의 차별성

한국저작권협회에서는 챗봇 서비스를 제공하고 있긴 하지만, 다음과 같은 한계점 존재❗

<img src="https://github.com/user-attachments/assets/d2b869dc-4cf4-4d76-b924-4e0f5df832e3" width="500" height="600" alt="저작권협회 챗봇"> <br>


🚫 **사전에 등록된 질문-답변(Q&A) 데이터베이스**를 기반으로 하기 때문에 **사용자의 구체적인 상황이나 맥락을 반영하지 못함**

예를 들어, "배경음악으로 사용해도 되는 곡인가요?"와 같은 질문은 사용자마다 사용하는 **곡 종류, 사용 맥락, 업로드 플랫폼**에 따라 판단 기준이 달라질 수 있음

하지만 기존 챗봇은 이러한 **다양한 조건이나 개별 경험을 반영하지 못한 채** 정해진 답변만을 제공하기 때문에 실질적인 도움을 주기 어려움

👉 따라서 본 프로젝트는 다음과 같은 방향으로 접근:

- **RAG(Retrieval-Augmented Generation)** 구조 활용
- **신뢰성 있는 최신 문서 기반 정보 검색**
- **LLM을 통한 자연스러운 대화와 맞춤형 응답 제공**


#### 1.3. 개발 목표  

**💡 본 프로젝트의 최종 목표:**

**사용자의 개별 맥락과 경험을 반영하고, 최신 정보에 기반한 신뢰도 높은 응답을 제공하는 RAG 기반 지능형 챗봇 어플리케이션**을 개발하는 것

기존의 정형화된 Q&A 챗봇이 가지는 한계를 넘어서,

**사용자 상황에 맞는 맞춤형 답변**과 **최신 문서 기반 정보 제공**이 가능한 챗봇을 구현하고자 함

**💡 본 팀이 설정한 세부 개발 목표:**

- 다양한 플랫폼(예: 유튜브, 네이버 블로그 등)에서 발생 가능한 저작권 이슈를 중심으로 **🔍관련 문서 데이터 수집 및 전처리**
- 수집된 데이터를 바탕으로 💾 **벡터 DB 구축 및 임베딩 처리**
- **🧾 사용자의 질문을 기반으로 적절한 정보를 검색하고 요약해주는 RAG 시스템**
- **🔄 LangGraph 기반 대화 흐름 설계 및 💬사용자 맞춤형 응답 구현**

👉 이러한 목표를 통해 사용자들이 **저작권에 대한 복잡한 법률 정보나 정책을 손쉽게 이해하고, 자신의 콘텐츠 제작에 바로 적용할 수 있는 환경**을 구축하고자 함

---

### 📌 2. 기술 스택
| **분야**              | **기술 및 라이브러리**                                                                                                                                                                                                                            |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🖥️ 프로그래밍 언어 & 개발환경 | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white" /> <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=VisualStudioCode&logoColor=white" />            |
| 🔗 LLM 체인 및 워크플로우   | <img src="https://img.shields.io/badge/LangChain-005F73?style=for-the-badge&logo=LangChain&logoColor=white" /> <img src="https://img.shields.io/badge/LangGraph-000000?style=for-the-badge&logo=LangChain&logoColor=white" />             |
| 🧠 LLM 모델           | <img src="https://img.shields.io/badge/OpenAI%20GPT--4.1-412991?style=for-the-badge&logo=OpenAI&logoColor=white" /> <img src="https://img.shields.io/badge/OpenAI%20Embeddings-10A37F?style=for-the-badge&logo=OpenAI&logoColor=white" /> |
| 📄 문서 로딩 및 전처리      | <img src="https://img.shields.io/badge/PyMuPDF-00599C?style=for-the-badge&logo=AdobeAcrobatReader&logoColor=white" /> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />            |
| 📦 벡터 저장소 및 임베딩     | <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=Chroma&logoColor=white" />                                                                                                                                |
| 🌐 데이터 수집           | <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" /> <img src="https://img.shields.io/badge/requests-7A88CF?style=for-the-badge&logo=Python&logoColor=white" />                   |
| 🤖 챗봇 인터페이스         | <img src="https://img.shields.io/badge/Chainlit-FFCC00?style=for-the-badge&logo=Lightning&logoColor=black" />                                                                                                                             |
| 🔐 환경 변수 및 설정 관리    | <img src="https://img.shields.io/badge/python_dotenv-000000?style=for-the-badge&logo=Python&logoColor=white" />                                                                                                                           |
| 💬 메시지 및 커뮤니케이션     | <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white" />                                                                                                                                |
| 📁 협업 및 형상 관리       | <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white" />                               |

### 📌 3. 파일구조

📁 SKN13-3rd-6Team <br>
├─ 📁 Code/  <br>
│   ├─ 📁 RAG_APP/ <br>
│   │   ├─Legend_Chain.py <br>
│   │   ├─ chainlit.py <br> 
│   │   ├─ tool.spy <br>
│   ├─ 📁 preprocessing/ <br>
│   │   ├─Chromadb.ipynb <br>
├─ 📁 Dataset/<br>
│   ├─ 📁 csv/<br>
│   ├─ ├─kakao_page.csv<br>
│   │   ├─youtube_copyright_tools.csv<br>
│   │   ├─└─ ... <br>
│   ├─ 📁 json/<br>
│   │   ├─instagram_faq_answers.json<br>
│   │   ├─youtube_support_faq.json<br>
│   ├─ 📁 pdf/<br>
│   │   ├─저작권법.pdf<br>
│   │   ├─US_copyright.pdf<br>
│   │   ├─└─ ... <br>
├─ 📁 Document/<br>
│   ├─ 요구사항 명세서.md<br>
├─ 📁 Structure/<br>
│   ├─ 플로우차트.pdf<br>
│   ├─ System Architecture.pdf<br>
├─ README.md

### 📌 4. 데이터 수집 및 전처리

✅ **데이터 내용에 따른 수집 방식 및 형태**

수집한 데이터는 크게 다음 두 가지 형태로 구성:

1.  📁 PDF 형식 문서

정부 기관, 공공기관 등에서 직접 제공하는 저작권 관련 정책/가이드 문서를 다운로드하여 확보
수집 방식: 공식 웹사이트에서 다운로드 → 텍스트 추출 → Markdown 구조 변환 → 문단 단위 Split
| 파일명                                     | 주요 내용              |
| --------------------------------------- | ------------------ |
| 저작권법(법률).pdf                            | 최신 개정 저작권법 전문      |
| 저작권상담사례집2024.pdf                        | 상담 사례 기반 질의응답 사례집  |
| 생성형AI 저작권 가이드라인.pdf                     | 생성형 AI 시대 저작권 가이드  |
| 최진원 계약 가이드북.pdf                         | 콘텐츠 계약 시 유의사항      |
| US\_copyright.pdf / wipo\_copyright.pdf | 해외 저작권 기준          |
| 네이버, 카카오 관련 PDF                         | 주요 플랫폼 약관 및 저작권 정책 |

전처리 방식:
- 각 페이지의 텍스트 블록(`page.get_text("dict")["blocks"]`)을 탐색
- 블록 내 텍스트를 span 단위로 합쳐 문단을 구성
- 텍스트 내용에 따라 `type` 태깅:
    - 조문 형태: `type = "section"` (`## 제3조 내용`)
    - 짧은 제목, 소제목: `type = "title"` (`# 이용 가이드`)
    - 일반 텍스트: `type = "paragraph"`
- 메타데이터: 각 문서에 `source = 파일명`을 태깅하여 출처 추적 가능

2. 🌐 웹 기반 동적 크롤링 데이터 (CSV / JSON)
   
수집 방식: 각 플랫폼 고객센터/FAQ 페이지를 `Selenium` 기반 동적 크롤링

📄 CSV 파일 (카카오, 유튜브 등)
| 파일명                           | 설명               |
| ----------------------------- | ---------------- |
| kakao\_page.csv               | 카카오 고객센터 문서 목록   |
| kakao\_policy\_full\_text.csv | 각 페이지의 전체 본문 텍스트 |
| kakao\_rights\_info.csv       | 콘텐츠 권리 및 신고 가이드  |
| youtube\_copyright\_tools.csv | 유튜브 저작권 도구 소개    |

🧾 JSON 파일 (인스타그램, 유튜브 FAQ)
| 파일명                          | 설명             |
| ---------------------------- | -------------- |
| instagram\_faq\_answers.json | 인스타그램 공식 FAQ   |
| youtube\_support\_faq.json   | 유튜브 저작권 관련 FAQ |

전처리 방식:
- HTML 파싱 후 본문만 추출
- JSON/CSV 각각 문서 단위로 분리 및 구조 정리
- FAQ는 질의응답 형태로 구조화 (질문 → 답변)

🏷️ **메타데이터 태깅 기준**
| 메타데이터 항목        | 태깅 기준 (조건 키워드)                                                                                                                                                     | 예시 값                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------- |
| **`platform`**  | 본문 내 특정 플랫폼명 포함 (`naver`, `kakao`, `youtube`, `instagram`, 등)                                                                                                      | `"카카오", "유튜브"`       |
| **`law_scope`** | - `fair use`, `dmca`, `미국` 등 포함 → `"해외"`<br> - `저작권법`, `공공누리`, `kogl`, `대한민국` 등 포함 → `"국내"`                                                                        | `"국내"` 또는 `"해외"`     |
| **`doc_type`**  | - `"사례"`, `"faq"` 포함 → `"사례집"`<br> - `"가이드"`, `"guide"` 포함 → `"가이드"`<br> - `"법"`, `"조항"`, `"제"` 포함 → `"법령"`                                                        | `"가이드"`, `"법령"` 등    |
| **`source`**    | 특정 키워드 포함 시 수동 분류:<br> - `"저작권법"` → `"저작권법"`<br> - `"dmca"` → `"DMCA"`<br> - `"공공누리"`, `"kogl"` → `"KOGL"`<br> - `"크리에이티브 커먼즈"` → `"CC"`                           | `"KOGL"`, `"DMCA"` 등 |
| **`topic`**     | 사전 정의된 키워드에 따라 분류:<br> - `"음악"`, `"배경음악"` → `"음악사용"`<br> - `"ai"`, `"인공지능"` → `"ai저작권"`<br> - `"인용"` → `"인용"`<br> - `"계약"` → `"저작권계약"`<br> - `"공공저작물"` → `"공공저작물"` | `"음악사용, ai저작권"` 등    |

### 📌 5. RAG 기반 챗봇 구현🤖

🔧**시스템 아키텍처**
![image](https://github.com/user-attachments/assets/47b56c74-dbff-4418-9147-f6bc3aca8f15)

- LangGraph : 상태 기반 대화 흐름 제어
- LangChain : RAG, LLMChain, tool integration
- OpenAI GPT-4.1 : 질의 응답, 분기 판단, 응답 생성
- ChromaDB + OpenAI Embedding : 벡터 검색 (Retrieval)
- Chainlit : 대화형 웹 UI 프론트엔드

🧩 **주요 노드 및 흐름 설명**<br>
<img src="https://github.com/user-attachments/assets/f3036216-f3b0-40ee-ade6-dd2bac03feae" width="500" height="700" alt="langgraph_image"> <br>

| **노드 이름**             | **설명**                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `extract_name`        | 사용자 이름 추출 (예: “나 홍길동이야”) → 맞춤형 응답에 활용                                                                            |
| `hyde`                | HYDE 기법으로 검색에 적합한 문장 생성 (`query → hyde_answer`)                                                                  |
| `check_route`         | HYDE 결과와 context를 바탕으로 라우팅 분기 결정:<br>① `use_rag` (검색 사용)<br>② `tool_call` (도구 호출)<br>③ `llm_message` (LLM 직접 응답) |
| `retrieve`            | RAG 컨텍스트 문서 검색 수행 (`retriever.invoke(hyde_answer)`)                                                              |
| `call_tool_llm`       | 도구 호출이 필요한 경우, LLM이 사용할 툴 판단 (`search_web` 등)                                                                    |
| `tool_runner`         | LLM이 선택한 실제 툴 실행 (예: `ToolNode`)                                                                                 |
| `process_tool_result` | 도구 실행 결과 정제 및 요약, 유효성 검증                                                                                         |
| `synthesize_response` | 최종 응답 생성: 사용자 이름, 대화 이력, RAG/Tool 결과 기반으로 답변 생성                                                                  |
| `fallback`            | 검색/도구 모두 실패 시 기본 메시지 출력 또는 LLM 재질문 시도                                                                            |

**🤖 최종 플로우 차트**
![image](https://github.com/user-attachments/assets/d588e8d8-6d28-4f8d-b9a5-48bdf6c42ad9)

💬 **예시 질의응답 시나리오**
| 사용자 질문                  | 처리 경로                                           | 설명                  |
| ----------------------- | ----------------------------------------------- | ------------------- |
| "유튜브에서 배경음악 써도 돼?"      | HYDE → retrieve → synthesize\_response          | RAG 문서에서 유튜브 가이드 검색 |
| "크리에이티브 커먼즈가 뭐야?"       | HYDE → retrieve → synthesize\_response          | CC 정책 PDF에서 내용 추출   |
| "최근 인공지능 관련 저작권 뉴스 알려줘" | tool\_call → search\_web → synthesize\_response | 외부 검색 툴 호출          |

⏩ **Langgraph 개발 과정 문서**

 ### 📌 6. 챗봇 평가지표(LAGAS)
 

 ### 📌 7. Chainlit 구현 화면

 ### 📌 8. 한줄 회고

 - 기원준:
 - 강지윤:
 - 최호연:
 - 이명인:
