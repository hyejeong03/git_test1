# 필요한 라이브러리 임포트
import streamlit as st
import pymysql

st.title("대륙 및 인구수 조건별 도시 검색")

st.divider()

# 1. 사이드바 드롭다운 위젯 생성
continent = st.sidebar.selectbox("대륙 선택", ['Asia', 'Europe', 'North America', 'Africa'])

# 2. 입력 폼 생성 (버벅임 방지용 st.form)
with st.form("search_form"):
    min_pop = st.number_input("최소 인구수를 입력하세요", value=1000000, step=500000)
    submitted = st.form_submit_button("DB 검색 실행")

# 3. 버튼 클릭 시 DB 조회 및 결과 표출
if submitted:

    # 파이썬과 MySQL DB 연결 전용 통로 생성
    conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='1234',
        db='world', 
        charset='utf8mb4', 
        cursorclass=pymysql.cursors.DictCursor
    )

    # 파이썬 코드로 MySQL DBMS에 명령을 내리고 결과를 받아오는 핵심 조작 도구 생성
    with conn.cursor() as cursor:
        ##f접두사 대신 사용하는 placeholder %s -> 해킹 등의 악의적 조작을 막아줌
        sql = """
        SELECT C.Name AS 도시명, CO.Name AS 국가명, C.Population AS 인구수
        FROM city C
        INNER JOIN country CO ON C.CountryCode = CO.Code
        WHERE CO.Continent = %s AND C.Population >= %s
        ORDER BY C.Population DESC LIMIT 10;
        """
        # DB 조회 실행
        cursor.execute(sql, (continent, min_pop))
        # 조회 결과 가져오기
        result = cursor.fetchall()
        
        st.success(f"{continent} 대륙 / {min_pop:,}명 이상 도시 검색 완료!")

        # list[dict] 데이터 시각화
        st.table(result)  
    
    conn.close()
