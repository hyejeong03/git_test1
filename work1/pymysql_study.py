# 필요한 라이브러리 임포트
import pymysql

# 1. MySQL 데이터베이스 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='world',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor # 조회 결과를 dict 형태로 받기 설정
)

# with 구문을 통해 커서 생성 및 사용 후 자동 반납 (cursor.close())
with conn.cursor() as cursor:
    # 2. SQL 쿼리 실행 (한국 도시 5개 조회)
    sql = "SELECT Name, District, Population FROM city WHERE CountryCode = 'KOR' LIMIT 5;"
    cursor.execute(sql)
    
    # 3. 전체 데이터 수신 (list of dicts)
    cities = cursor.fetchall()
    
    print("조회된 데이터 (파이썬 list[dict] 구조):")
    print(cities)
    
    print("-"*80)
    print("파이썬 for문 및 dict 키 추출을 이용한 데이터 출력:")
    for city in cities:
        name = city['Name']
        district = city['District']
        pop = city['Population']
        print(f"- 도시명: {name} | 지역: {district} | 인구수: {pop:,}명")

# 4. DB 연결 종료
conn.close() 