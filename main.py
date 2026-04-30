import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import json
import datetime

# ==========================================
# 1. 개인 키 설정 (본인의 키로 변경하세요!)
# ==========================================
GEMINI_API_KEY = "여기에_본인의_GEMINI_API_KEY를_넣으세요"
KAKAO_TOKEN = "여기에_본인의_카카오톡_ACCESS_TOKEN을_넣으세요"

# ==========================================
# 2. 뷰티누리 사이트 크롤링 (최신 기사 제목 수집)
# ==========================================
def get_beautynuri_news():
    url = "https://www.beautynuri.com/news/list/0/0/0" # 뷰티누리 최신뉴스 페이지
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_titles = []
    # 보통 기사 제목은 특정 클래스나 태그 안에 있습니다. (a 태그 위주로 수집)
    # ※ 주의: 사이트 구조가 바뀌면 select 부분을 수정해야 할 수 있습니다.
    articles = soup.select('.news_list .tit a') 
    
    for article in articles[:10]: # 최신 10개만 가져오기
        title = article.text.strip()
        if title:
            news_titles.append(title)
            
    return "\n".join(news_titles)

# ==========================================
# 3. Gemini로 A4 한 장 분량 요약하기
# ==========================================
def summarize_news(news_text):
    genai.configure(api_key=GEMINI_API_KEY)
    # 최신 빠르고 가벼운 모델 사용
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    prompt = f"""
    당신은 화장품 산업 및 뷰티 트렌드 전문가입니다. 
    오늘자 뷰티누리 뉴스의 주요 제목들을 전달해 드릴 테니, 
    이를 바탕으로 A4 용지 1장 분량(약 1000자 내외)의 '오늘의 뷰티 트렌드 브리핑'을 작성해주세요.
    가독성 좋게 글머리 기호를 사용하고, 핵심만 명확하게 짚어주세요.
    
    [오늘의 뉴스 제목]
    {news_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# ==========================================
# 4. 카카오톡 '나에게 보내기' 전송
# ==========================================
def send_kakao_message(text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {KAKAO_TOKEN}"
    }
    
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": "https://www.beautynuri.com",
                "mobile_web_url": "https://www.beautynuri.com"
            },
            "button_title": "뷰티누리 바로가기"
        })
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("✅ 카카오톡 메시지 전송 성공!")
    else:
        print(f"❌ 전송 실패: {response.status_code} - {response.text}")

# ==========================================
# 실행 부분
# ==========================================
print("크롤링을 시작합니다...")
news_data = get_beautynuri_news()

if news_data:
    print("기사 수집 완료! Gemini 요약을 시작합니다...")
    summary = summarize_news(news_data)
    
    print("요약 완료! 카카오톡으로 전송합니다...")
    send_kakao_message(summary)
else:
    print("크롤링된 기사가 없습니다. 사이트 구조를 확인해주세요.")
