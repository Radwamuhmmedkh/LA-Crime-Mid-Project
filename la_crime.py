
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

la_crime = pd.read_csv('la_crime.csv')
st.set_page_config(layout= 'wide', page_title= 'LA Crime Analysis 2010 - 2025', page_icon= '🔪')
st.markdown("""<h1 style="color:Black;text-align:center;">🔪 LA Crime Analysis 2010 - 2025 </h1>""", unsafe_allow_html= True)
st.image('crime_scene.jpg', width = 2000)

st.markdown("""This Analysis explores crimes patterns in <b>Los Angeles</b> from 2010 till 2025, We will extract meaningful inshigts to uncover several crime patterns.
<br>The Dataset used is:
""", unsafe_allow_html= True)
st.markdown("[Data Part 1️⃣](https://data.lacity.org/Public-Safety/Crime-Data-from-2010-to-2019/63jg-8b9z/about_data)  [Data Part 2️⃣](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data)")
st.text("Let's take a look at the Data set after cleaning:")
st.dataframe(la_crime.head())
st.markdown("""<p> The columns that we are intrested in are: 
<ul>
            <li>📅 DATE_OCC : Actual date when the crime occurred </li>
            <li>🕰️ Vict_Age: Age of the victim</li>
            <li>♀️♂️ Vict_Sex: Gender of the victim</li>
            <li>📊 Vict_Descent: Ethnic descent of the victim</li>
            <li>🔪 Crime: Crime type "derived from Crime code"</li>
            <li>🗺️ Area_Name: Name of the area where the crime occurred</li>
            <li>🗺️ Premis_Desc: Description of the premise where crime occurred</li>
            <li>📍 (LAT, LON): Latitude and Longitude coordinate of the crime location</li>
        </ul> </p>""", unsafe_allow_html= True)
crimes_per_age_group = la_crime[la_crime['Crime'] == 'OTHERS'].groupby(['Age_group', 'Crm_Cd_Desc'])['DR_NO'].count().reset_index()
crimes_per_age_group.rename(columns= {'DR_NO' : 'Count'}, inplace= True)
crimes_per_age_group.sort_values(by = 'Count', inplace = True, ascending= False)
other_crimes_list = list(crimes_per_age_group[crimes_per_age_group['Count'] > 10000].Crm_Cd_Desc.unique())
st.markdown("[📄 Crime Code Document](https://data.lacity.org/api/views/63jg-8b9z/files/fff2caac-94b0-4ae5-9ca5-d235b19e3c44?download=true&filename=UCR-COMPSTAT062618.pdf)")
page = st.sidebar.selectbox('🕵️ Explore Crime by:', ['🚻 Gender', '🎂 Age','🌎 Ethnicity','🕒 Date & Time','📍 Location'])
st.markdown("---")
if(page == '🚻 Gender'):
    st.subheader("🚻 Explore Crime by: Gender")
    st.info("""⚠️ As shown in the following Histogram Victim data indicates an equal distribution between **male** and **female**, but in the following anlysis we will discuss crime types.""")
    st.plotly_chart(px.histogram(data_frame= la_crime, x = 'Vict_Sex', text_auto= True, labels={"Vict_Sex": "Gender"}))
    st.markdown("---")
    st.info("""⚠️ Gender-based analysis reveals that females are more frequently victimized in cases of **Domestic Violence**, **Violence** and **Sexual Assault**, and males are more in cases of **Burgaly** and **General Theft**.""")
    crime_per_gender_type = la_crime.groupby(['Crime' , 'Vict_Sex'])['DR_NO'].count().reset_index()
    crime_per_gender_type.rename(columns= {'DR_NO' : 'Count'}, inplace= True)
    crime_per_gender_type.sort_values(by = 'Count', ascending= False, inplace= True)
    st.plotly_chart(px.bar(data_frame= crime_per_gender_type, x = 'Crime', y = 'Count', color= 'Vict_Sex', barmode= 'group'))
    others_crime = la_crime[la_crime['Crime'] == 'OTHERS'].groupby(['Crm_Cd_Desc', 'Vict_Sex'])['DR_NO'].count().reset_index()
    others_crime.rename(columns= {'DR_NO' : 'Count'}, inplace= True)
    others_crime.sort_values(by = 'Count', inplace = True, ascending= False)
    st.plotly_chart(px.bar(data_frame= others_crime[others_crime['Count'] > 20000], x = 'Crm_Cd_Desc', y = 'Count', color= 'Vict_Sex', barmode= 'group', height= 600, labels={"Crm_Cd_Desc": "Crime"}))

elif(page == '🎂 Age'):
    st.subheader("🎂 Explore Crime by: Age")
    st.info("⚠️ A significant number of victims fall within the **35** to **54** age range, suggesting that this stage of life may carry heightened risks. The following chart illustrates that this age group is the most affected across nearly all crime categories.")
    st.plotly_chart(px.histogram(data_frame= la_crime, x = 'Age_group', text_auto= True))

    crimes_per_age_group = la_crime.groupby(['Age_group', 'Crime'])['DR_NO'].count().reset_index()
    crimes_per_age_group.rename(columns= {'DR_NO' : 'Count'}, inplace= True)
    crimes_per_age_group.sort_values(by = 'Count', inplace = True, ascending= False)
    st.plotly_chart(px.bar(data_frame= crimes_per_age_group, x = 'Crime', y = 'Count', color = 'Age_group', barmode= 'group'))
   
    crimes_per_age_group = la_crime[la_crime['Crime'] == 'OTHERS'].groupby(['Age_group', 'Crm_Cd_Desc'])['DR_NO'].count().reset_index()
    crimes_per_age_group.rename(columns= {'DR_NO' : 'Count'}, inplace= True)
    crimes_per_age_group.sort_values(by = 'Count', inplace = True, ascending= False)
    st.plotly_chart(px.bar(data_frame= crimes_per_age_group[crimes_per_age_group['Count'] > 10000], x = 'Crm_Cd_Desc', y = 'Count', color= 'Age_group', barmode= 'group', height = 600, labels={"Crm_Cd_Desc": "Crime"}))
    
elif(page == '🌎 Ethnicity'):
    st.subheader("🌎 Explore Crime by: Ethnicity")
    st.markdown("""
    ### 📊 LA Population Breakdown:
    - **Hispanic or Latino (any race):** 47.2%
    - **Non-Hispanic White:** 28.3%
    - **Black or African American:** 8.5%
    - **Asian:** 12.0%
    - **Native American:** 1.2%
    - **Pacific Islander:** 0.1%
    """)

    st.info("🎯 Nearly **1 in 2** residents in Los Angeles identifies as **Hispanic or Latino**, making it the largest ethnic group in the city.")
    st.plotly_chart(px.histogram(data_frame= la_crime, x = 'Vict_Descent', text_auto= True, labels = {"Vict_Descent" : "Ethnicity"}))

    crimesType_per_descents = la_crime.groupby(['Vict_Descent', 'Crime'])['DR_NO'].count().reset_index()
    crimesType_per_descents = crimesType_per_descents.rename(columns={'DR_NO' : 'Count'}).sort_values(by = 'Count', ascending= False)
    st.plotly_chart(px.bar(data_frame= crimesType_per_descents,x = 'Crime', y = 'Count', color = 'Vict_Descent', barmode= 'group', height= 600))

    crimesType_per_descents = la_crime[la_crime['Crm_Cd_Desc'].isin(other_crimes_list)].groupby(['Vict_Descent', 'Crm_Cd_Desc'])['DR_NO'].count().reset_index()
    crimesType_per_descents = crimesType_per_descents.rename(columns={'DR_NO' : 'Count'}).sort_values(by = 'Count', ascending= False)
    st.plotly_chart(px.bar(data_frame= crimesType_per_descents, x = 'Crm_Cd_Desc', y = 'Count', color = 'Vict_Descent', barmode= 'group', height=600))
    st.info("⚠️ **Hispanic and Latino individuals** are the most frequent victims across most crime categories in Los Angeles. ❗ However, some crimes — like **[Burglary - Theft of idenity - other Theft]** — show a different pattern, with other groups more affected.")

elif(page == '🕒 Date & Time'):
    st.subheader("🕒 Explore Crime by: Date & Time")
    selected_time = st.multiselect("🕰️ Select time range: ", options = list(la_crime['Time_of_the_day'].unique()))
    if(len(selected_time) > 0):
        la_crime_filtered = la_crime[la_crime['Time_of_the_day'].isin(selected_time)]
        crime_time_of_the_day = la_crime_filtered[la_crime_filtered['Crime'] != 'OTHERS'].groupby(['Time_of_the_day' , 'Crime'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'}).sort_values(by = 'Count', ascending= False)
        st.plotly_chart(px.bar(data_frame= crime_time_of_the_day, x = 'Time_of_the_day', y = 'Count', color = 'Crime', barmode= 'group'))

        crime_time_of_the_day = la_crime_filtered[la_crime_filtered['Crm_Cd_Desc'].isin(other_crimes_list)].groupby(['Time_of_the_day' , 'Crm_Cd_Desc'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'}).sort_values(by = 'Count', ascending= False)
        st.plotly_chart(px.bar(data_frame= crime_time_of_the_day, x = 'Time_of_the_day', y = 'Count', color = 'Crm_Cd_Desc', barmode= 'group'))
    else:
        crime_time_of_the_day = la_crime[la_crime['Crime'] != 'OTHERS'].groupby(['Time_of_the_day' , 'Crime'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'}).sort_values(by = 'Count', ascending= False)
        st.plotly_chart(px.bar(data_frame= crime_time_of_the_day, x = 'Time_of_the_day', y = 'Count', color = 'Crime', barmode= 'group'))

        crime_time_of_the_day = la_crime[la_crime['Crm_Cd_Desc'].isin(other_crimes_list)].groupby(['Time_of_the_day' , 'Crm_Cd_Desc'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'}).sort_values(by = 'Count', ascending= False)
        st.plotly_chart(px.bar(data_frame= crime_time_of_the_day, x = 'Time_of_the_day', y = 'Count', color = 'Crm_Cd_Desc', barmode= 'group'))
    
    st.info("⚠️ **Burglary theft from vehicle** dominates at night and evening, while **Other Theft** peaks in the afternoon. **Violent crimes** such as **Simple Assault** and **Roberry** occur most frequently during night and evening hours.")
    crime_type_yearly = la_crime.groupby(['Crime', 'Year_OCC'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'})
    st.plotly_chart(px.line(data_frame= crime_type_yearly, x = 'Year_OCC', y = 'Count', color= 'Crime', height= 800))

    crime_type_yearly = la_crime[la_crime['Crm_Cd_Desc'].isin(other_crimes_list)].groupby(['Crm_Cd_Desc', 'Year_OCC'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO':'Count'})
    st.plotly_chart(px.line(data_frame= crime_type_yearly, x = 'Year_OCC', y = 'Count', color= 'Crm_Cd_Desc', height= 800))
    st.info("⚠️ Some crimes have sudden increase in **2022**")

elif(page == '📍 Location'):
    st.subheader("📍 Explore Crime by: Location")
    st.text("⚠️ Places where Crimes happend")
    df = la_crime.groupby(['Premis_Desc'])['DR_NO'].count().reset_index().sort_values(by = 'DR_NO', ascending = False)[:15]
    st.plotly_chart(px.bar(data_frame = df, y = 'DR_NO', x = 'Premis_Desc'))
    st.info("⚠️ Most crimes happend in **single family dwelling** followed by **STREET**")
    crime_per_area = la_crime.groupby(['AREA_NAME'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO': 'Count'})
    crime_per_area.sort_values(by = 'Count', ascending= True, inplace= True, ignore_index= True)
    px.bar(data_frame= crime_per_area, x = 'AREA_NAME', y = 'Count')
    st.info("⚠️ According to the bar chart **Hollenbeck** is the most safe area according the number of crimes while **77th Street** is the most dangerous Area.")
    crime_per_area_per_year = la_crime.groupby(['AREA_NAME', 'Year_OCC'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO': 'Count'})
    st.plotly_chart(px.line(data_frame= crime_per_area_per_year, x = 'Year_OCC', y = 'Count', color= 'AREA_NAME', height= 800))
    st.info("⚠️ According to the bar chart **Central** has the heighest crime rate in **2022**, followed by **77th Street**.")

    st.text("📅 Select Date Range:")
    start_date = st.date_input('Start Date', value= la_crime['DATE_OCC'].min(), min_value= la_crime['DATE_OCC'].min(), max_value= la_crime['DATE_OCC'].max())
    end_date = st.date_input('End Date', value= la_crime['DATE_OCC'].max(), min_value= la_crime['DATE_OCC'].min(), max_value= la_crime['DATE_OCC'].max())
    la_crime['DATE_OCC'] = pd.to_datetime(la_crime['DATE_OCC'], errors='coerce')
    la_crime_filtered = la_crime[(la_crime['DATE_OCC'] >= str(start_date)) & (la_crime['DATE_OCC'] <= str(end_date))]
    crime_per_area_per_year = la_crime_filtered.groupby(['AREA_NAME', 'Year_OCC'])['DR_NO'].count().reset_index().rename(columns= {'DR_NO': 'Count'})
    st.plotly_chart(px.line(data_frame= crime_per_area_per_year, x = 'Year_OCC', y = 'Count', color= 'AREA_NAME', height= 800), key="area_trend_chart")

    st.subheader("🗺️ Explore Crime Location")
    selection = st.selectbox('📍 Choose Area:', list(la_crime.AREA_NAME.unique()))
    la_crime_area = la_crime[la_crime['AREA_NAME'] == selection]

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=la_crime_area['LAT'],
        lon=la_crime_area['LON'],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='Cities',
        text='West Valley'
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=8,
        mapbox_center={"lat": 34.044727, "lon": -118.2426},  # Center on LA
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig)
