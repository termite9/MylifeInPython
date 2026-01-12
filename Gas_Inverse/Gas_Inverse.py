import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

st.set_page_config(page_title="터마이트의 3쿠션 기록관", page_icon="🎱")
st.title("🎱 3쿠션 인터넷 기록소")

# 구글 시트 URL (시트 ID 뒤에 /edit까지 포함하는 것이 안정적입니다)
url = "https://docs.google.com/spreadsheets/d/1w8iNPwWpQC-QGbdNgANtJKETTQlsN-bTe640rPZUKwU/edit#gid=0"

# 커넥션 생성
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. 데이터 불러오기 함수 (캐시 방지를 위해 ttl=0 설정)
def load_data():
    try:
        # worksheet 이름이 시트 하단 탭 이름과 정확히 일치해야 합니다.
        return conn.read(spreadsheet=url, worksheet="Sheet2", ttl=0)
    except Exception:
        # 시트가 비어있거나 읽기에 실패할 경우 기본 프레임 반환
        return pd.DataFrame(columns=["날짜", "승자", "에버리지"])

df = load_data()

# 입력 화면
with st.form("entry_form"):
    date = st.date_input("경기 날짜", datetime.date.today())
    winner = st.selectbox("오늘의 승자는?", ["터마이트", "친구1", "친구2", "친구3", "친구4"])
    avg = st.number_input("나의 에버리지", min_value=0.0, max_value=2.0, value=0.4, step=0.01)
    submit = st.form_submit_button("구글 시트에 저장하기")

    if submit:
        # 새 데이터 행 생성
        new_row = pd.DataFrame([{"날짜": str(date), "승자": winner, "에버리지": avg}])
        
        # 2. 기존 데이터와 새 데이터 합치기 (비어있는 경우 처리)
        if df.empty:
            updated_df = new_row
        else:
            updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # 3. 구글 시트에 업데이트
        try:
            conn.update(spreadsheet=url, worksheet="Sheet2",data=updated_df)
            st.success("구글 시트에 안전하게 기록되었습니다!")
            st.balloons()
            
            # 중요: 저장 성공 후 즉시 캐시를 비우고 앱을 재실행하여 최신 데이터를 불러옴
            st.cache_data.clear() 
            st.rerun() 
        except Exception as e:
            st.error(f"저장 중 오류가 발생했습니다: {e}")

# 저장된 기록 보여주기
st.divider()
st.subheader("📊 누적 경기 기록")

# 데이터가 있을 때만 테이블 표시
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("아직 저장된 기록이 없습니다. 첫 경기를 입력해보세요!")

#####실행할때는 터미널에서 streamlit run Gas_Inverse.py 와 같이 실행해야됨  billiard-bot@mylifepython.iam.gserviceaccount.com