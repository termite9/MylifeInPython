import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="터마이트의 3쿠션 기록관", page_icon="🎱")
st.title("🎱 3쿠션 인터넷 기록소")

# 구글 시트 연결 설정
# (실제 배포 시에는 구글 시트 주소를 secrets.toml에 넣어야 하지만, 테스트용으로 직접 넣는 법을 알려드릴게요)
url = "https://docs.google.com/spreadsheets/d/1w8iNPwWpQC-QGbdNgANtJKETTQlsN-bTe640rPZUKwU/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기
df = conn.read(spreadsheet=url, worksheet="Sheet1")

# 입력 화면
with st.form("entry_form"):
    date = st.date_input("경기 날짜", datetime.date.today())
    winner = st.selectbox("오늘의 승자는?", ["터마이트", "친구1", "친구2", "친구3", "친구4"])
    avg = st.number_input("나의 에버리지", min_value=0.0, max_value=2.0, value=0.4, step=0.01)
    submit = st.form_submit_button("구글 시트에 저장하기")

    if submit:
        # 새로운 데이터 행 생성
        new_row = pd.DataFrame([{"날짜": str(date), "승자": winner, "에버리지": avg}])
        # 기존 데이터에 추가
        updated_df = pd.concat([df, new_row], ignore_index=True)
        # 구글 시트에 업데이트
        conn.update(spreadsheet=url, data=updated_df)
        st.success("구글 시트에 안전하게 기록되었습니다!")
        st.balloons()

# 저장된 기록 보여주기
st.divider()
st.subheader("📊 누적 경기 기록")
st.dataframe(df)

#####실행할때는 터미널에서 streamlit run MyLifeKcs.py 와 같이 실행해야됨