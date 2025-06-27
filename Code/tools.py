# tools.py

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from langchain_tavily import TavilySearch

# --- Instagram ---
@tool
def instagram_copyright_help(query: str) -> str:
    """인스타 저작권 관련 도움말(https://help.instagram.com/535503073130320/)"""
    url = "https://help.instagram.com/535503073130320/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "Instagram 저작권 도움말 페이지에 접근할 수 없습니다."

@tool
def instagram_general_help(query: str) -> str:
    """인스타 도움말(https://help.instagram.com/126382350847838/)"""
    url = "https://help.instagram.com/126382350847838/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "Instagram 일반 도움말 페이지에 접근할 수 없습니다."

# --- YouTube ---
@tool
def youtube_copyright_help(query: str) -> str:
    """유튜브 저작권 정책 도움말(https://support.google.com/youtube/answer/2797466)"""
    url = "https://support.google.com/youtube/answer/2797466?hl=ko&ref_topic=2778546"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "YouTube 저작권 정책 도움말 페이지에 접근할 수 없습니다."

@tool
def youtube_general_help(query: str) -> str:
    """유튜브 일반 정책 도움말(https://support.google.com/youtube/answer/9245819)"""
    url = "https://support.google.com/youtube/answer/9245819?hl=ko&ref_topic=9282364"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "YouTube 일반 정책 도움말 페이지에 접근할 수 없습니다."

# --- Kakao ---
@tool
def kakao_terms_help(query: str) -> str:
    """카카오 서비스 약관(https://www.kakao.com/policy/terms?type=ts&lang=ko#useterms03_09)"""
    url = "https://www.kakao.com/policy/terms?type=ts&lang=ko#useterms03_09"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "카카오 서비스 약관 페이지에 접근할 수 없습니다."

@tool
def kakao_rights_help(query: str) -> str:
    """카카오 권리 정책(https://www.kakao.com/policy/right)"""
    url = "https://www.kakao.com/policy/right"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "카카오 권리 정책 페이지에 접근할 수 없습니다."

@tool
def kakaopage_publishing_help(query: str) -> str:
    """카카오페이지 퍼블리싱 정책(https://biz.kakaopage.com/publishingcenter/popupfooter/policy)"""
    url = "https://biz.kakaopage.com/publishingcenter/popupfooter/policy"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:2000]
    except Exception:
        return "카카오페이지 퍼블리싱 정책 페이지에 접근할 수 없습니다."

# --- Tavily Web Search ---
@tool
def search_web(query: str, max_results: int = 3, time_range: str = "month") -> dict:
    """최신 정보가 필요할 때 인터넷 검색을 하는 Tool입니다."""
    tavily_search = TavilySearch(max_results=max_results, time_range=time_range)
    search_result = tavily_search.invoke(query)["results"]
    if search_result:
        return {"result": search_result}
    else:
        return {"result": "검색결과가 없습니다."}

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
