import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="터마이트의 3쿠션 기록관", page_icon="🎱")
st.title("🎱 3쿠션 인터넷 기록소")

# 1. 주소 수정: 뒤의 /edit 부분을 제거하고 깔끔하게 시트 ID만 남깁니다.
# url = "https://docs.google.com/spreadsheets/d/1w8iNPwWpQC-QGbdNgANtJKETTQlsN-bTe640rPZUKwU"
# 기존 주소 대신 아래처럼 시트 ID 뒤에 'edit'까지만 남겨보세요.
url = "https://docs.google.com/spreadsheets/d/1w8iNPwWpQC-QGbdNgANtJKETTQlsN-bTe640rPZUKwU/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 데이터 불러오기 (ttl=0을 넣어 실시간으로 반영되게 합니다)
try:
    df = conn.read(spreadsheet=url, worksheet="Sheet1", ttl=0)
except Exception as e:
    # 시트에 데이터가 아예 없을 경우를 대비해 빈 데이터프레임 생성
    df = pd.DataFrame(columns=["날짜", "승자", "에버리지"])

# 입력 화면
with st.form("entry_form"):
    date = st.date_input("경기 날짜", datetime.date.today())
    winner = st.selectbox("오늘의 승자는?", ["터마이트", "친구1", "친구2", "친구3", "친구4"])
    avg = st.number_input("나의 에버리지", min_value=0.0, max_value=2.0, value=0.4, step=0.01)
    submit = st.form_submit_button("구글 시트에 저장하기")

    if submit:
        new_row = pd.DataFrame([{"날짜": str(date), "승자": winner, "에버리지": avg}])
        # 기존 데이터와 새 데이터 합치기
        updated_df = pd.concat([df, new_row], ignore_index=True)
        # 구글 시트에 업데이트
        conn.update(spreadsheet=url, data=updated_df)
        st.success("구글 시트에 안전하게 기록되었습니다!")
        st.balloons()
        st.rerun() # 저장 후 화면 갱신

# 저장된 기록 보여주기
st.divider()
st.subheader("📊 누적 경기 기록")
st.dataframe(df)

#####실행할때는 터미널에서 streamlit run MyLifeKcs.py 와 같이 실행해야됨