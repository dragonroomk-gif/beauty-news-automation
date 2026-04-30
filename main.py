import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime
import os

print("=" * 60)
print("🚀 뷰티 뉴스 자동 요약 시작")
print("=" * 60)

# ============================================
# 1단계: API 키 확인
# ============================================

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ 오류: GEMINI_API_KEY가 설정되지 않았습니다!")
    print("   GitHub Secrets에서 API 키를 설정해주세요.")
    exit(1)

print("✅ API 키 확인됨\n")

genai.configure(api_key=GEMINI_API_KEY)

# ============================================
# 2단계: 뷰티 뉴스 수집
# ============================================

print("📰 뷰티 뉴스 수집 중...")

def fetch_articles():
    """뷰티 관련 뉴스 기사 수집"""
    
    try:
        # 뷰티누리 웹사이트
        url = "https://www.beautynuri.co.kr/"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"⚠️  접속 실패 (상태코드: {response.status_code})")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 뉴스 제목과 링크 찾기
        articles = []
        
        # HTML에서 링크 추출
        for link in soup.find_all('a', limit=20):
            title = link.get_text(strip=True)
            href = link.get('href', '')
