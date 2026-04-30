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
    exit(1)

print("✅ API 키 확인됨\n")

genai.configure(api_key=GEMINI_API_KEY)

# ============================================
# 2단계: 뷰티 뉴스 수집
# ============================================

print("📰 뷰티 뉴스 수집 중...")

def fetch_articles():
    """뷰티 관련 뉴스 기사 수집"""
    articles = []
    
    try:
        url = "https://www.beautynuri.co.kr/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"⚠️ 접속 실패")
            return articles
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for link in soup.find_all('a', limit=20):
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            if title and href and len(title) > 10:
                if not href.startswith('http'):
                    href = url + href
                
                articles.append({
                    'title': title,
                    'url': href
                })
        
        articles = articles[:3]
        
        if articles:
            print(f"✅ {len(articles)}개 기사 수집 완료\n")
        else:
            print("⚠️ 기사를 찾을 수 없습니다\n")
    
    except Exception as e:
        print(f"❌ 오류: {e}\n")
    
    return articles

articles = fetch_articles()

# ============================================
# 3단계: Gemini로 기사 요약
# ============================================

print("🤖 Gemini AI로 기사 요약 중...\n")

def summarize_articles(articles):
    """Gemini를 사용해 기사 요약"""
    
    if not articles:
        return "수집된 기사가 없습니다."
    
    try:
        articles_text = "\n\n".join([
            f"제목: {article['title']}\n링크: {article['url']}"
            for article in articles
        ])
        
        prompt = f"""당신은 화장품 및 뷰티 산업 분석가입니다.

다음 뷰티/화장품 뉴스 기사들을 읽고, 각 기사를 2-3줄의 간단한 한글 요약으로 정리해주세요.

기사 목록:
{articles_text}

형식:
📌 기사 1
요약: (2-3줄)

📌 기사 2
요약: (2-3줄)

📌 기사 3
요약: (2-3줄)
"""
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        print(f"❌ 요약 생성 실패: {e}")
        return "요약 생성 실패"

summary = summarize_articles(articles)

# ============================================
# 4단계: 최종 메시지 생성
# ============================================

today = datetime.now().strftime('%Y년 %m월 %d일')
time_now = datetime.now().strftime('%H:%M')

final_message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 뷰티 뉴스 자동 요약
📅 {today} {time_now}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ GitHub Actions 자동생성
"""

# ============================================
# 5단계: 결과 저장
# ============================================

output_file = "beauty_news_summary.txt"

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_message)
    
    print(f"✅ 저장 완료: {output_file}\n")
    print("=" * 60)
    print(final_message)
    print("=" * 60)

except Exception as e:
    print(f"❌ 저장 실패: {e}")

print("\n✅ 모든 작업 완료!")
