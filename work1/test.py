import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="차량 현황 추세 대시보드", layout="wide")

st.title("📊 월별·지역별·차종별 총계 추세 대시보드")

# 사이드바 - 파일 업로드
st.sidebar.header("📁 데이터 업로드")
uploaded_file = st.sidebar.file_uploader(
    "CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"]
)


@st.cache_data
def load_data(file):
    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    else:
        # 데이터가 없을 때 동작 확인용 샘플 데이터 생성
        import numpy as np

        dates = pd.date_range(
            start="2024-01-01", periods=12, freq="MS"
        ).strftime("%Y-%m")
        regions = [
            "경기도",
            "강원특별자치도",
            "충청북도",
            "충청남도",
            "전북특별자치도",
            "전라남도",
            "경상북도",
            "경상남도",
            "제주특별자치도",
        ]
        car_types = ["승용", "승합", "화물", "특수"]

        data = []
        for d in dates:
            for r in regions:
                for c in car_types:
                    data.append(
                        {
                            "월": d,
                            "지역": r,
                            "차종": c,
                            "총계": np.random.randint(100, 1000),
                        }
                    )
        df = pd.DataFrame(data)
    return df


# 데이터 불러오기
df = load_data(uploaded_file)

# 컬럼 존재 유무 확인을 위한 가이드 메시지 (파일 업로드 시)
expected_cols = {"월", "지역", "차종", "총계"}
if not expected_cols.issubset(df.columns):
    st.error(
        f"데이터에 다음 열(Column)이 포함되어 있는지 확인해주세요: {expected_cols}"
    )
    st.stop()

# -------------------------------------------------------------
# 사이드바 - 관점 선택 및 필터 설정
# -------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🔍 보기 설정")

view_type = st.sidebar.radio(
    "조회 기준 선택", ["1. 전체 월별 총계", "2. 지역별(도 단위) 추세", "3. 차종별 추세"]
)

# -------------------------------------------------------------
# 1) 첫 화면: 전체 월별 총계 추세
# -------------------------------------------------------------
if view_type == "1. 전체 월별 총계":
    st.subheader("📈 전체 월별 총계 추세")

    df_monthly = df.groupby("월", as_index=False)["총계"].sum()

    fig = px.line(
        df_monthly,
        x="월",
        y="총계",
        markers=True,
        title="전체 월별 총계 추세",
        labels={"월": "월", "총계": "총계 (대)"},
        text="총계",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 데이터 테이블 보기"):
        st.dataframe(df_monthly, use_container_width=True)

# -------------------------------------------------------------
# 2) 사이드바 라디오버튼: 지역별(도 단위) 추세
# -------------------------------------------------------------
elif view_type == "2. 지역별(도 단위) 추세":
    st.subheader("🗺️ 지역별(도 단위) 총계 추세")

    region_options = ["전체 도 비교"] + sorted(df["지역"].dropna().unique().tolist())
    selected_region = st.sidebar.radio("지역(도) 선택", region_options)

    if selected_region == "전체 도 비교":
        df_region = df.groupby(["월", "지역"], as_index=False)["총계"].sum()
        fig = px.line(
            df_region,
            x="월",
            y="총계",
            color="지역",
            markers=True,
            title="도별 월별 총계 추세 비교",
            labels={"월": "월", "총계": "총계 (대)", "지역": "지역(도)"},
        )
    else:
        df_region = df[df["지역"] == selected_region]
        df_region_grouped = df_region.groupby("월", as_index=False)[
            "총계"
        ].sum()
        fig = px.line(
            df_region_grouped,
            x="월",
            y="총계",
            markers=True,
            title=f"[{selected_region}] 월별 총계 추세",
            labels={"월": "월", "총계": "총계 (대)"},
            text="총계",
        )
        fig.update_traces(textposition="top center")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 데이터 테이블 보기"):
        st.dataframe(
            df_region if selected_region == "전체 도 비교" else df_region_grouped,
            use_container_width=True,
        )

# -------------------------------------------------------------
# 3) 사이드바 라디오버튼: 차종별 추세
# -------------------------------------------------------------
elif view_type == "3. 차종별 추세":
    st.subheader("🚘 차종별 총계 추세")

    car_options = ["전체 차종 비교"] + sorted(df["차종"].dropna().unique().tolist())
    selected_car = st.sidebar.radio("차종 선택", car_options)

    if selected_car == "전체 차종 비교":
        df_car = df.groupby(["월", "차종"], as_index=False)["총계"].sum()
        fig = px.line(
            df_car,
            x="월",
            y="총계",
            color="차종",
            markers=True,
            title="차종별 월별 총계 추세 비교",
            labels={"월": "월", "총계": "총계 (대)", "차종": "차종"},
        )
    else:
        df_car = df[df["차종"] == selected_car]
        df_car_grouped = df_car.groupby("월", as_index=False)["총계"].sum()
        fig = px.line(
            df_car_grouped,
            x="월",
            y="총계",
            markers=True,
            title=f"[{selected_car}] 월별 총계 추세",
            labels={"월": "월", "총계": "총계 (대)"},
            text="총계",
        )
        fig.update_traces(textposition="top center")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 데이터 테이블 보기"):
        st.dataframe(
            df_car if selected_car == "전체 차종 비교" else df_car_grouped,
            use_container_width=True,
        )