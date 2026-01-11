import streamlit as st
import pandas as pd
import datetime
import os
# st.write(f"현재 파일이 저장되는 위치: {os.getcwd()}")
# 파일 경로 설정
DATA_FILE = "billiard_results.csv"

# 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["날짜", "승자", "에버리지"])

st.set_page_config(page_title="터마이트의 3쿠션 기록관", page_icon="🎱")
st.title("🎱 3쿠션 마스터: 기록 보관소")

# --- 데이터 로드 ---
df_history = load_data()

# 메인 화면: 경기 기록 입력
st.header("📝 오늘의 경기 기록")
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("경기 날짜", datetime.date.today())
    winner = st.selectbox("오늘의 승자는?", ["터마이트", "친구1", "친구2", "친구3", "친구4"])
with col2:
    avg = st.number_input("나의 에버리지", min_value=0.0, max_value=2.0, value=0.4, step=0.01)

if st.button("경기 결과 저장하기"):
    # 새로운 기록 추가
    new_data = pd.DataFrame({"날짜": [str(date)], "승자": [winner], "에버리지": [avg]})
    # 기존 데이터에 합치기
    df_updated = pd.concat([df_history, new_data], ignore_index=True)
    # 파일로 저장
    df_updated.to_csv(DATA_FILE, index=False)
    st.balloons()
    st.success("데이터가 안전하게 저장되었습니다!")
    st.rerun() # 화면 갱신

<<<<<<< HEAD
# --- 검색 및 통계 화면 ---
=======
# 경기a 통계 시각화 (예시 데이터)
>>>>>>> 81cb7f7f4a1b1cf0f4a7c463a1c0d98c1100a222
st.divider()
st.header("🔍 과거 기록 검색")

search_name = st.text_input("검색하고 싶은 사람의 이름을 입력하세요 (예: 터마이트)")
if search_name:
    filtered_df = df_history[df_history['승자'].str.contains(search_name)]
    st.write(f"'{search_name}'님의 승리 기록입니다:")
    st.table(filtered_df)
else:
    st.write("전체 경기 기록:")
    st.table(df_history)


#####실행할때는 터미널에서 streamlit run MyLifeKcs.py 와 같이 실행해야됨