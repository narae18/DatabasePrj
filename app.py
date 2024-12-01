import mysql.connector
import pandas as pd
import streamlit as st

# MySQL 연결
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='chlskfo18',  # MySQL 비밀번호
        database='park_db'
    )

# CSV 파일 읽기 (인코딩 처리)
def load_csv_data():
    try:
        # utf-8-sig 인코딩 시도
        data = pd.read_csv(r'C:\Users\narae\OneDrive\바탕 화면\mapo\서울특별시 마포구 공원 내 체육시설 현황.csv', encoding='utf-8-sig')
    except UnicodeDecodeError:
        # utf-8-sig에서 실패할 경우 CP949 인코딩 시도
        data = pd.read_csv(r'C:\Users\narae\OneDrive\바탕 화면\mapo\서울특별시 마포구 공원 내 체육시설 현황.csv', encoding='CP949')
    
    return data

# MySQL에 CSV 데이터를 삽입하는 함수
def insert_data_to_mysql(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    for index, row in data.iterrows():
        cursor.execute("""
        INSERT INTO park_equipment (park_name, 허리돌리기, 온몸들어올리기, 등허리지압기, 파도타기, 윗몸일으키기, 온몸노젓기)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row['공원명'], row['허리돌리기'], row['온몸들어올리기'], row['등허리지압기'], row['파도타기'], row['윗몸일으키기'], row['온몸노젓기']))

    connection.commit()
    cursor.close()
    connection.close()

# Streamlit 웹 대시보드
st.title('공원 운동기구 현황 대시보드')

# CSV 데이터 로드 후 MySQL에 삽입
data = load_csv_data()  # CSV 파일을 로드
insert_data_to_mysql(data)  # MySQL에 데이터 삽입

# MySQL에서 데이터 조회
def get_parks_data():
    connection = get_db_connection()
    query = "SELECT * FROM park_equipment"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# 데이터 조회 후 Streamlit 대시보드에 표시
parks_data = get_parks_data()
st.write(parks_data)
