# tools.py (수정)
from langchain.tools import tool
from langchain_tavily import TavilySearch
import requests
from bs4 import BeautifulSoup
import json # json 모듈 추가
# --- Instagram ---
@tool
def instagram_copyright_help(query: str) -> str:
    """인스타 저작권 관련 도움말(https://help.instagram.com/535503073130320/) 내용을 검색합니다.""" # description 명확화
    url = "https://help.instagram.com/535503073130320/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text # LLM이 요약하도록 여기서 자르지 않음
    except Exception:
        return "Instagram 저작권 도움말 페이지에 접근할 수 없습니다."

@tool
def instagram_general_help(query: str) -> str:
    """인스타 일반 도움말(https://help.instagram.com/126382350847838/) 내용을 검색합니다.""" # description 명확화
    url = "https://help.instagram.com/126382350847838/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "Instagram 일반 도움말 페이지에 접근할 수 없습니다."

# --- YouTube ---
@tool
def youtube_copyright_help(query: str) -> str:
    """유튜브 저작권 정책(https://support.google.com/youtube/answer/2797466)에 대한 도움말을 검색합니다.""" # description 명확화
    url = "https://support.google.com/youtube/answer/2797466?hl=ko&ref_topic=2778546"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "YouTube 저작권 정책 도움말 페이지에 접근할 수 없습니다."

@tool
def youtube_general_help(query: str) -> str:
    """유튜브 일반 정책 및 저작권에 대한 도움말(https://support.google.com/youtube/answer/9245819)을 검색합니다.""" # description 명확화
    url = "https://support.google.com/youtube/answer/9245819?hl=ko&ref_topic=9282364"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "YouTube 일반 정책 도움말 페이지에 접근할 수 없습니다."

# --- Kakao ---
@tool
def kakao_terms_help(query: str) -> str:
    """카카오 서비스 약관(https://www.kakao.com/policy/terms?type=ts&lang=ko#useterms03_09) 내용을 검색합니다.""" # description 명확화
    url = "https://www.kakao.com/policy/terms?type=ts&lang=ko#useterms03_09"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "카카오 서비스 약관 페이지에 접근할 수 없습니다."

@tool
def kakao_rights_help(query: str) -> str:
    """카카오의 권리 정책 및 저작권 침해 신고 절차(https://www.kakao.com/policy/right)에 대한 도움말을 검색합니다.""" # description 명확화
    url = "https://www.kakao.com/policy/right"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "카카오 권리 정책 페이지에 접근할 수 없습니다."

@tool
def kakaopage_publishing_help(query: str) -> str:
    """카카오페이지의 퍼블리싱 정책(https://biz.kakaopage.com/publishingcenter/popupfooter/policy) 내용을 검색합니다.""" # description 명확화
    url = "https://biz.kakaopage.com/publishingcenter/popupfooter/policy"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text
    except Exception:
        return "카카오페이지 퍼블리싱 정책 페이지에 접근할 수 없습니다."

# --- Tavily Web Search ---
@tool
def search_web(query: str, max_results: int = 3, time_range: str = "month") -> str: # 반환 타입을 dict에서 str로 변경
    """최신 정보가 필요할 때 인터넷 검색을 하는 Tool입니다. 예를 들어 '네이버 블로그 저작권'과 같은 질문에 사용합니다.""" # description 명확화
    tavily_search = TavilySearch(max_results=max_results, time_range=time_range)
    search_result = tavily_search.invoke(query)["results"]
    if search_result:
        # 딕셔너리 리스트를 JSON 문자열로 직렬화하여 반환
        return json.dumps({"results": search_result}, ensure_ascii=False) # 한글 깨짐 방지
    else:
        return json.dumps({"results": []}) # 검색 결과가 없을 때 빈 리스트 반환

# --- 모든 툴 리스트 ---
TOOLS = [
    instagram_copyright_help,
    instagram_general_help,
    youtube_copyright_help,
    youtube_general_help,
    kakao_terms_help,
    kakao_rights_help,
    kakaopage_publishing_help,
    search_web,
]