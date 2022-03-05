import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import plotly.express as px


@st.cache(show_spinner=False)
def get_exoplanet_data_by_astroquery():
    parameters = 'hostname,pl_name,pl_orbper,pl_orbsmax,pl_bmasse,pl_rade'
    exoplanet_data = NasaExoplanetArchive.query_criteria(table='pscomppars', select=parameters)
    exoplanet_data = exoplanet_data.to_pandas()
    exoplanet_data = exoplanet_data.sort_values(
        by=['hostname'], ignore_index=True
    )
    renamed_columns_dict = {
        'hostname': '母恆星名稱',
        'pl_name': '行星名稱',
        'pl_orbper': '行星軌道週期',
        'pl_orbsmax': '行星軌道半長軸',
        'pl_bmasse': '行星質量',
        'pl_rade': '行星半徑',
    }
    exoplanet_data = exoplanet_data.rename(columns=renamed_columns_dict) #放入字典rename

    return exoplanet_data


def plot_Keplers_3rd_law(selected_exoplanets):
    selected_exoplanets['行星軌道週期平方'] = selected_exoplanets['行星軌道週期'] ** 2
    selected_exoplanets['行星軌道半長軸立方'] = selected_exoplanets['行星軌道週期'] ** 3
    fig = px.scatter(
        selected_exoplanets, x='行星軌道半長軸立方', y='行星軌道週期平方', symbol='行星名稱'
    )

    return st.plotly_chart(fig, use_container_width=True)


st.set_page_config(layout="wide") #設定網站資訊
st.title('用[NASA太陽系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)的資料驗證[克卜勒第三定律](https://zh.wikipedia.org/zh-tw/%E5%BC%80%E6%99%AE%E5%8B%92%E5%AE%9A%E5%BE%8B#%E5%BC%80%E6%99%AE%E5%8B%92%E7%AC%AC%E4%B8%89%E5%AE%9A%E5%BE%8B)')#標題
st.info('克卜勒第三定律為各個行星繞其母恆星公轉週期的平方及其橢圓軌道的半長軸的立方成正比，本教材以NASA太陽系外行星資料庫的資料來驗證此定律。') #藍底

with st.spinner('從[NASA太陽系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)載入資料中，請稍候...'): #資料載入提示文
    exoplanet_data = get_exoplanet_data_by_astroquery() #取得系外行星資料
    hostname_list = list(exoplanet_data['母恆星名稱'].unique())
    st.header('太陽系外行星資料表')#呈現標題
    st.dataframe(exoplanet_data)#呈現表格

hostname = st.sidebar.text_input('輸入母恆星名稱', hostname_list[0]) #輸入框、提示字、預設值

if hostname in hostname_list:
    selected_exoplanets = exoplanet_data[
        exoplanet_data['母恆星名稱'] == hostname].reset_index(drop=True)#存成表格

    st.header(f'{hostname}系統中的行星') #表格標題
    st.table(selected_exoplanets) #顯示表格

    pl_name_list = selected_exoplanets['行星名稱'].tolist()
    period_list = selected_exoplanets['行星軌道週期'].tolist()
    semi_major_axis_list = selected_exoplanets['行星軌道半長軸'].tolist()

    for index, pl_name in enumerate(pl_name_list): #資料計算
        period = period_list[index]
        semi_major_axis = semi_major_axis_list[index]
        k = period ** 2 / semi_major_axis ** 3
        st.success(f"行星{pl_name}的「軌道週期平方除以軌道半長軸的立方」為{k}") #顯示綠底文字

    plot_Keplers_3rd_law(selected_exoplanets) #畫出圖表，用plotly

else:
    st.error('輸入的母恆星名稱並沒有在資料庫中') #再列表，顯示錯誤

