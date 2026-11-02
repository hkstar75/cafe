import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="카페 통합 시스템", layout="wide")
st.title("☕ 동네 카페 통합 시스템")

# 2. 데이터 불러오기 및 날짜 데이터 가공  df = data frame   
df = pd.read_excel('cafe_sales_data.xlsx')
df['결제일자'] = pd.to_datetime(df['결제일자']) 
df['월'] = df['결제일자'].dt.month
df['주'] = df['결제일자'].dt.isocalendar().week
df['일'] = df['결제일자'].dt.date

# 3. 탭 구성
tab1, tab2, tab3 = st.tabs(["소개", "메뉴", "대시보드"])

# [탭 1] 카페 소개
with tab1:
    st.header("🏡 카페 소개")
    st.image(r".\image\cafe1.jpg", width=600)
    st.write("**뚱이 내리는 고요하고 맑은 커피.**")
    st.write("매일 아침 직접 로스팅한 원두로 일상의 작은 휴식을 제공합니다.")

# [탭 2] 대표 메뉴
with tab2:
    st.header("📋 대표 메뉴")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("https://images.unsplash.com/photo-1551030173-122aabc4489c?auto=format&fit=crop&w=400", width=250)
        st.subheader("아메리카노")
        st.write("산미 없는 고소하고 다크한 풍미 (4,500원)")
        
    with c2:
        st.image("https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=400", width=250)
        st.subheader("초코케이크")
        st.write("진한 초콜릿의 꾸덕함 (6,500원)")
        
    with c3:
        st.image("https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400", width=250)
        st.subheader("소금빵")
        st.write("고메버터와 짭짤한 펄솔트 (6,000원)")

# [탭 3] 대시보드
with tab3:
    st.header("📊 맞춤형 대시보드")
    
    # 3-1. 조건 필터 (달, 주, 날짜)
    st.write("🔍 **데이터 필터링**")
    f1, f2, f3 = st.columns(3)
    
    with f1:
        month_list = sorted(df['월'].unique())
        sel_month = st.selectbox("달 선택", ["전체"] + list(month_list))
    with f2:
        date_list = sorted(df['일'].unique())
        sel_date = st.selectbox("날짜 선택", ["전체"] + list(date_list))
        
    # 필터 적용
    filtered_df = df.copy()
    if sel_month != "전체":
        filtered_df = filtered_df[filtered_df['월'] == sel_month]
    if sel_date != "전체":
        filtered_df = filtered_df[filtered_df['일'] == sel_date]
        
    # 3-2. i를 활용한 총 매출액 계산 (인덱스 리셋 필수)
    filtered_df = filtered_df.reset_index(drop=True)
    total_revenue = 0
    for i in range(len(filtered_df)):
        total_revenue += filtered_df.loc[i, '총결제금액']
        
    st.subheader(f"💰 선택 기간 총 매출: {total_revenue:,}원")
    
    # 3-3. 조회 기준 선택
    st.write("---")
    view_mode = st.radio(
        "조회 기준 (원하는 항목을 선택하세요)",
        ["전체 데이터 표", "카테고리별 매출", "메뉴별 매출", "단가 기준 (고가/저가)", "결제수단별 매출"],
        horizontal=True
    )
    
    # 3-4. 선택된 기준에 따른 차트/표 출력
    if view_mode == "전체 데이터 표":
        st.dataframe(filtered_df, use_container_width=True)
        
    elif view_mode == "카테고리별 매출":
        st.bar_chart(filtered_df.groupby('카테고리')['총결제금액'].sum())
        
    elif view_mode == "메뉴별 매출":
        st.bar_chart(filtered_df.groupby('메뉴명')['총결제금액'].sum())
        
    elif view_mode == "단가 기준 (고가/저가)":
        # 단가 5000원을 기준으로 고가/저가 분류
        price_df = filtered_df.copy()
        price_df['단가구분'] = price_df['단가'].apply(lambda x: '비싼 메뉴(5000원 초과)' if x > 5000 else '싼 메뉴(5000원 이하)')
        st.bar_chart(price_df.groupby('단가구분')['총결제금액'].sum())
        
    elif view_mode == "결제수단별 매출":
        st.bar_chart(filtered_df.groupby('결제수단')['총결제금액'].sum())