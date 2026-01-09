import streamlit as st

st.title(" 터마이트의  ")

# 입력창
dish = st.text_input("오늘 만든 요리", "닭백숙")
ingredients = st.multiselect("사용한 재료", ["닭", "마늘", "대추", "인삼", "찹쌀"])

# 버튼 클릭 시 반응
if st.button("요리 기록 저장"):
    st.success(f"오늘의 {dish} 기록 완료!")
    st.balloons() # 화면에 축하 풍선이 날아다님
    
# 건강 가이드 (고지혈증 고려)
st.info("💡 팁: 국물보다는 살코기 위주로 드시면 건강 관리에 더 좋습니다.")

