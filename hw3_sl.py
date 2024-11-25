# 라이브러리 로드
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.write('C221036 오승은')
st.title("전국 행정구역별 합계출산율 지도")
#### 지도 시각화 ########################################

# 데이터 로드
birth_df = pd.read_csv('합계출산율_행정구역별.csv', header=1, encoding='euc-kr')
birth_df.columns = ['행정구역', '합계출산율']

# '통합창원시'를 '창원시'로 변경
birth_df.loc[birth_df['행정구역'] == '통합창원시', '행정구역'] = '창원시'

gdf_korea = gpd.read_file('gdf_korea_2024.json')


# 기본 지도 생성
city_hall = [37.566345, 126.977893] # 기준 좌표 (서울시청)

kor_map = folium.Map(
    location = city_hall,
    zoom_start = 8,
    tiles = 'cartodbpositron'
)

# Choropleth 레이어 생성
folium.Choropleth(
    geo_data = gdf_korea, #GeoJSON 지도 데이터
    data = birth_df, # 출산율 데이터
    columns = ('행정구역', '합계출산율'),
    key_on = 'feature.properties.NAME',
    fill_color = 'BuPu',
    fill_opacity = 0.7,
    line_opacity = 0.5,
    legend_name = '합계출산율'
).add_to(kor_map)

# 지역 이름 툴팁 추가
folium.GeoJson(
    gdf_korea,
    tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['지역명:']),
    style_function=lambda x: {
        'color': 'transparent',  # 경계선 색상 설정
        'weight': 0  # 경계선 두께 설정
    }
).add_to(kor_map)

# 지도 출력
st_folium(kor_map, width=700, height=500)

# 전체 지역 개수
total = birth_df.shape[0]
st.write(f'전체 지역 개수: {total}개')

# 합계 출산율이 1.0 이하인 지역 개수
under_1 = birth_df[birth_df['합계출산율'] <= 1.0].shape[0]
st.write(f'합계 출산율이 1.0 이하인 지역 개수: {under_1}개')

# 합계 출산율이 1.0 이하인 지역의 비율
under_1_ratio = under_1 / total * 100
st.write(f'합계 출산율이 1.0 이하인 지역의 비율: {under_1_ratio:.2f}%')

##### 합계출산율 히스토그램 ########################################
st.write("## 합계출산율 히스토그램")
fig = px.histogram(
    birth_df,
    x='합계출산율',
    nbins=15,
    title='합계출산율 히스토그램'
)

st.plotly_chart(fig)

st.write("""
- 지역별 합계출산율은 왼쪽으로 치우친 (right-skewed) 분포를 띄고 있다.
- 즉, 합계출산율의 평균이나 중앙값보다 최빈값이 더 낮다.
- 0.7대의 합계출산율을 기록한 지역이 가장 많았다.
         """)
##### 합계출산율 상위 10개 지역 ########################################
birth_df_descend = birth_df.sort_values(by='합계출산율', ascending=False)
st.write("## 합계출산율 상위 10개 지역")
st.write(birth_df_descend.head(10))

st.write("""
- 합계출산율이 높은 10개 지역은 전부 수도권 외의 지역이다.
- 모두 특별시, 특별자치시, 광역시에 해당하지 않는 기초자치단체이며 대부분 농촌지역이거나 인구밀도가 낮은 지역이다.
         """)

#### 합계출산율 하위 10개 지역 ########################################
birth_df_ascend = birth_df.sort_values(by='합계출산율', ascending=True)
st.write("## 합계출산율 하위 10개 지역")
st.write(birth_df_ascend.head(10))

st.write("""
- 합계출산율이 낮은 하위 10개 지역은 모두 광역시 혹은 특별시에 해당하는 지역이다.
- 부산광역시의 중구, 대구광역시의 서구를 제외하면 모두 서울특별시의 지역이다.
         """)
