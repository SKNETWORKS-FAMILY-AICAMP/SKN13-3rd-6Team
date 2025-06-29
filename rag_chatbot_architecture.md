## Chainlit & LangGraph 기반 챗봇 시스템 요구사항 명세서

---

## 요구사항 명세서

### 기능 요구사항 (Functional Requirements)

| 구분 | 요구사항 ID | 요구사항 명 | 상세 설명 | 관련 코드/기능 |
| :--- | :--- | :--- | :--- | :--- |
| **대화 관리** | FR-C-01 | 사용자 입력 처리 | 시스템은 사용자로부터 텍스트 형식의 질문을 입력받을 수 있어야 한다. | `chainlit @cl.on_message` |
|  | FR-C-02 | 응답 메시지 표시 | 시스템은 생성된 답변을 사용자 인터페이스에 텍스트 형식으로 표시해야 한다. | `@cl.on_message` 내 `cl.Message.send()` |
|  | FR-C-03 | 상태 기반 대화 기억 및 맥락 유지 | 시스템은 각 사용자 세션(`thread_id`)별로 대화 기록을 저장하고 새로운 답변 생성 시 이전 대화 흐름을 반영해야 한다. | `MemorySaver`, `thread_id`, `GraphState.messages`, `response_synthesis_chain` |
| **개인화** | FR-P-01 | 사용자 이름 추출 | 시스템은 대화에서 사용자의 이름을 정확히 추출할 수 있어야 한다. | `extract_name` 노드, `entity_extraction_chain` |
|  | FR-P-02 | 이름 활용 응답 | 추출된 이름을 응답에 포함하여 친근한 표현을 생성해야 한다. | `synthesize_response` 노드, `response_synthesis_chain` |
| **로직 / 라우팅** | FR-L-01 | HyDE 적용 | RAG 검색 최적화를 위해 HyDE 방식으로 가상 응답을 생성해야 한다. | `hyde` 노드, `hyde_chain` |
|  | FR-L-02 | 동적 경로 결정 | 질문에 따라 'RAG', '도구 사용', 'LLM 직접 답변' 중 최적 경로를 선택해야 한다. | `check_route` 노드, `llm_check_chain` |
| **RAG** | FR-R-01 | 관련 문서 검색 | Chroma DB에서 관련 문서를 검색해야 한다. | `retrieve` 노드 |
|  | FR-R-02 | 정보 기반 답변 | 검색된 문서 내용을 기반으로 응답을 생성해야 한다. | `synthesize_response` 노드 |
| **도구 사용** | FR-T-01 | 필요 도구 선택 | 질문에 따라 적절한 도구를 선택할 수 있어야 한다. | `call_tool_llm` 노드, `.bind_tools(TOOLS)` |
|  | FR-T-02 | 도구 실행 | 선택된 도구를 실행하고 결과를 받아야 한다. | `tool_runner` 노드 |
|  | FR-T-03 | 결과 가공/요약 | 도구의 출력 결과를 요약 및 정리하여 사용해야 한다. | `process_tool_result` 노드 |
|  | FR-T-04 | 웹 검색 결과 처리 | 웹 검색 결과를 구조화된 형식으로 가공해야 한다. | `process_tool_result` 내 JSON 파싱 로직 |
| **출력** | FR-O-01 | 최종 답변 합성 | 다양한 컨텍스트를 종합하여 응답을 생성해야 한다. | `synthesize_response` 노드 |
|  | FR-O-02 | 정보 출처 명시 | 응답과 함께 출처 정보를 사용자에게 표시해야 한다. | `@cl.on_message` 내 출력 포맷팅 |

### 비기능 요구사항 (Non-functional Requirements)

| 구분 | 요구사항 ID | 요구사항 명 | 상세 설명 | 관련 코드/기능 |
| :--- | :--- | :--- | :--- | :--- |
| **성능** | NFR-PF-01 | 응답 시간 | 15초 이내에 응답을 제공해야 한다. | 시스템 전반 |
| **보안** | NFR-SC-01 | API 키 관리 | 민감한 키 정보는 환경 변수로 관리되어야 한다. | `dotenv` 사용 |
| **사용성** | NFR-US-01 | 직관적 UI | 별도 학습 없이 UI를 사용할 수 있어야 한다. | `chainlit` 프레임워크 |
| **유지보수성** | NFR-MN-01 | 모듈화 구조 | 노드 단위로 분리되어 있어야 유지보수에 용이하다. | LangGraph 구조 전체 |

