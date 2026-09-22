# 필요한 라이브러리 임포트
import streamlit as st
import pymysql

# 1. 웹 화면 제목 설정
st.title("world DB 한국 주요 도시 현황")

# 2. PyMySQL을 이용하여 DB 데이터 조회 함수 정의
def get_korea_cities():
    conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='1234',
        db='world', 
        charset='utf8mb4', 
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with conn.cursor() as cursor:
        sql = "SELECT Name AS 도시명, District AS 시도, Population AS 인구수 FROM city WHERE CountryCode = 'KOR' LIMIT 10;"
        cursor.execute(sql)
	# list[dict] 반환
        return cursor.fetchall() 
    
    conn.close()

# 3. 데이터 로드 및 Streamlit 표출 
data = get_korea_cities()

st.subheader("한국 상위 10개 도시 목록")

st.divider()

# list[dict] 데이터를 깔끔한 표 형태로 웹에 출력
st.table(data) 