# SKN13-3rd-6Team

### 🤖 3차 프로젝트: 콘텐츠 크리에이터들을 위한 저작권 정보제공 챗봇 시스템<br>

**개발기간:** 2025.06.26 ~ 2025.06.30

## 💻 팀 소개

<!-- | **기원준👨‍💻** | **강지윤👩‍💻** | **최호연👨‍💻** | **이명인👨‍💻** |
|:--------------:|:--------------:|:--------------:|:--------------:|
| @usey10        | @thanGyuPark   | @Hyeseo20      | @pbr2858        | -->


<table>
  <tr>
    <td align="center">
      <img src="" width="100"/><br/>기원준👨‍💻
    </td>
    <td align="center">
      <img src="" width="100"/><br/>강지윤👩‍💻
    </td>
    <td align="center">
      <img src="" width="100"/><br/>최호연👨‍💻
    </td>
    <td align="center">
      <img src="" width="100"/><br/>이명인👨‍💻
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

![매일경제](https://github.com/user-attachments/assets/2ac781e2-0cfc-459d-a37c-f60095352244)<br>
(출처: 매일경제 https://www.mk.co.kr/news/culture/10918121)

❗하지만 그에 반해, **저작권에 대한 정보 접근성과 이해도는 여전히 부족한 상황**임

특히 **초보 크리에이터들**은 플랫폼별 정책, 국내외 저작권법, 공정 이용(Fair Use) 기준 등에 대한 **혼란과 어려움**을 겪고 있음

예를 들어, 유튜브와 같은 해외 플랫폼을 활용할 경우, 국내 저작권법을 따라야 하는지, 플랫폼의 정책을 따르는 것이 우선인지, 해외 저작권 기준까지 고려해야 하는지 등이 명확하지 않게 느껴지며, 관련 정보를 일일이 찾아보기 어렵고 복잡하다는 현실적인 문제점이 존재함

![크리에이터 실태조사](https://github.com/user-attachments/assets/2775a996-f914-4018-922e-bb41e7b15369)<br>
(출처: 크리에이터, 대세와 직업 그 사이 <개인 미디어 콘텐츠 크리에이터 실태 조사>   https://www.kocca.kr/trend/vol29/sub/s32.html)


#### 1.2. 본 챗봇의 차별성

한국저작권협회에서는 챗봇 서비스를 제공하고 있긴 하지만, 다음과 같은 한계점 존재❗

![저작권협회 챗봇](https://github.com/user-attachments/assets/d2b869dc-4cf4-4d76-b924-4e0f5df832e3)

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
| 분야                   | 기술 및 라이브러리                                                                                                                                                                                                                                       |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 프로그래밍 언어 & 개발환경 | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white" /> <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=https://gist.githubusercontent.com/yourusername/uniqueid/raw/vscode-logo.svg&logoColor=white" />|
| LLM 체인 및 자연어 처리   |![LangChain](https://img.shields.io/badge/LangChain-005F73?style=for-the-badge&logo=LangChain&logoColor=white)                                                                                                     |
| LLM 모델               | <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=OpenAI&logoColor=white" /> |
| 데이터 수집              | <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=OpenAI&logoColor=white" /> |
| 데이터베이스 및 임베딩     | <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=https://gist.githubusercontent.com/yourusername/uniqueid/raw/chromadb-logo.svg&logoColor=white" />                                                                                                   |
| 환경변수 관리            | <img src="https://img.shields.io/badge/python_dotenv-000000?style=for-the-badge&logo=Python&logoColor=white" />                                                                                                                                      |
| 문서 로딩               | <img src="https://img.shields.io/badge/PyPDFLoader-4B8BBE?style=for-the-badge&logo=PyPDFLoader&logoColor=white" />                                                                                                                                              |
| 협업 및 형상관리        | <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white" /> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white" /> |


### 📦 3. 데이터 수집 및 전처리

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

