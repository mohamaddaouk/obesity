# Author    : Mohamad Kheir EL Daouk
# Created on: Sun Sep 25 19:18:27 2022

import hydralit_components as hc
from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
import plotly.offline as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import init_notebook_mode
init_notebook_mode(connected = True)
import cufflinks as cf
cf.go_offline()

st.set_page_config(layout = 'wide')


@st.cache
def load_data():
    df_data = pd.read_csv("data/data.csv")
    df_obesity = pd.read_csv("data/obesity.csv")
    df_obesityByContinent = pd.read_csv("data/obesityByContinent.csv")
    return df_data,df_obesity,df_obesityByContinent

# Load the Data
data,obesity,obesityByContinent = load_data()


def calculate_bmi(weight_kg, height_cm):
    bmi = weight_kg/((height_cm/100)**2)
    if bmi < 16:
        bmi_category = "Severe Thinness"
    elif (bmi >=16) &  (bmi <17):
        bmi_category = "Moderate Thinness"
    elif (bmi >=17) &  (bmi <18.5):
        bmi_category = "Mild Thinness"  
    elif (bmi >=18.5) &  (bmi <25):       
        bmi_category = "Normal"
    elif (bmi >=25) &  (bmi <30):       
       bmi_category = "Overweight"       
    elif (bmi >=30) &  (bmi <35):
        bmi_category = "Obese Class I"  
    elif (bmi >=35) &  (bmi <40):       
        bmi_category = "Obese Class II"
    elif (bmi >=40):       
       bmi_category = "Obese Class III"
    return bmi, bmi_category

# Function to load animations
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
# 
#----------------------------------------------------------------------------------------------------#
# Main page
st.title("Obesity: An Epidemic")

# Menu bar
selected = option_menu(
    menu_title = None,
    options = ["Home", "Global Obesity", "Top 20 Countries", "Obesity by Subregion", "Obesity by Gender", "BMI Calculator"],
    menu_icon = "cast",
    icons = ['house', 'globe', 'bar-chart', 'gear', 'pie-chart', 'calculator'],
    default_index = 0,
    orientation = "horizontal",
    styles = {"nav-link-selected":{"background-color":"#636EFA"}}
)

#----------------------------------------------------------------------------------------------------#
# Page 1: Home
if selected == "Home":
# Insert the facts here
    col1, col2, col3, col4 = st.columns(4)
    
    theme_override = {'bgcolor': '#d6eaff','title_color': '#636EFA', 'content_color': '000000', 'icon': 'bi bi-key', 'icon_color': 'blue'}
    with col1:
        hc.info_card(title = 'Key Fact 1', content = 'Since 1975 obesity has nearly tripled Worldwide', theme_override=theme_override)

    with col2:
        hc.info_card(title = 'Key Fact 2', content = 'In 2016, over 1.9 billion adults were overweight. Of these over 650 million were obese', theme_override=theme_override)

    with col3:
        hc.info_card(title = 'Key Fact 3', content = 'In 2016, more than 340 million children and adolescents aged 5-19 were overweight or obese', theme_override=theme_override)

    with col4:
        hc.info_card(title = 'Key Fact 4', content = 'Obesity is preventable', theme_override=theme_override)

    col1, col2 = st.columns([2,2])
    
    with col1:
        st.header(" What is obesity?")
        st.info("""Obesity is defined as having too much body mass. In general the Body Mass Index (BMI) indicates whether a person has a healthy body weight for his/her height. A BMI of 30 or higher is associated  with obesity.
        According to The Global Burden of Disease (GBD) over 4 million people died as a result of being overweight or obese in 2017.
        """)
        
        st.header("Complications")
        st.error("""
                 - Type 2 diabetes
                 - Heart disease
                 - High blood pressure
                 - Stroke
                 - High cholesterol
                 - Sleep apnea and other breathing problems
                 """)
        
        st.header("Prevention")
        st.success("""
                   - Reducing the number of calories consumed from fats and sugars
                   - Healthy diet
                   - Engaging in regular physical activity (60 minutes per day for children and 150 minutes per week for adults). 
        """)
    with col2:
        animation = load_lottiefile("pushups.json") 
        st_lottie(animation,
        speed = 1,
        reverse = False,
        loop = True,
        quality = 'high',
        height = 500,
        width = 500,
        key = None
        )
#----------------------------------------------------------------------------------------------------#
# Page 2: Global Obesity
if selected == "Global Obesity":
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        #Visualization no. 1
        # Global Obesity Visualization
        st.subheader("Obesity Prevalence among adults by country, 1975-2016")
        fig = px.choropleth(obesity, locations ="ISO3", color="Obesity", hover_name="Country", 
                    animation_frame="Year", color_continuous_scale=px.colors.sequential.Rainbow,
                    range_color=[0,45], 
                    hover_data=["Year", "ISO3", "Obesity", "Population", "Obesity_count"],
                    height=600, width=750,
                    labels={'Obesity':'Obesity rate'},
                    projection="natural earth")
        st.write(fig)
    
    with col2:
        #Visualization no. 2
        st.subheader("Obesity Prevalence Among Adults by Continent, 1975-2016")
        fig = px.line(obesityByContinent, x="Year", y="WeightedObesity", color='Continent',
                    range_x = [1975,2016], range_y=[0,45]) 

        fig.update_layout(
            yaxis_title="Obesity Prevalence (%)",
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)")

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.write(fig)
        st.info("**We notice that obesity and overweight prevalence rates continue to grow.**")
        
#----------------------------------------------------------------------------------------------------#
# Page 3: Top 20 Countries
if selected == "Top 20 Countries":
    #Visualization no. 4
    st.subheader(f"Top 20 Countries by Mean Obesity Prevalence Among Adults")
    sel_col, disp_col = st.columns([1,4], gap="large")
    with sel_col:
        sel_year = st.slider("Select a year", min_value = 1976, max_value = 2016, value=2016, step=1)
    with disp_col:
        obesity_for_selected_year = obesity.query("Year=="+str(sel_year)).sort_values(by='Obesity', ascending=False).head(20)
        fig = go.Figure(go.Bar(
                    y=obesity_for_selected_year.Country,
                    x=obesity_for_selected_year.Obesity,
                    orientation='h'))

        fig.update_layout(
            title='Top 20 Countries by Mean Obesity Prevalence Among Adults in ' + str(sel_year), 
            yaxis_title="Obesity Prevalence (%)",
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", 
            width=800, height=500)

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.write(fig)
    
#----------------------------------------------------------------------------------------------------#
# Page 4: Obesity by Subregion
if selected == "Obesity by Subregion":
    
    sel_col, dummy_col = st.columns(2, gap="large")
    with sel_col:
        sel_year2 = 2016
        sel_year2 = st.number_input('Select a year',min_value=1975, max_value=2016, value=2016, step=1)

    col1, col2 = st.columns(2, gap="large") 
    with col1:      
        #Visualization no. 5
        #st.subheader("Obesity Prevalence Among Adults in 2016 for the MENA Region")
        st.subheader("Obesity Prevalence Among Adults in the MENA Region")
                      
        MENAData = data.query("Country in ['Algeria', 'Bahrain', 'Egypt', 'Iran', 'Iran (Islamic Republic of)', 'Iraq', 'Israel', 'Jordan', 'Kuwait', 'Lebanon','Libya', 'Morocco', 'Oman', 'Qatar', 'Saudi Arabia', 'Syria', 'Syrian Arab Republic', 'Tunisia', 'United Arab Emirates', 'Yemen']")
        tempdf = MENAData.query("Year=="+str(sel_year2))

        fig = px.line_polar(tempdf, r='Obesity', theta='Country', color='Sex', line_close=True, 
                            line_shape='spline', range_r=[0,47])
        st.write(fig)

        if sel_year2 == 2016:
            st.info("**We noticed that the female obesity prevalence rate is significantly higher than that of male with the exception of occupied Palestine. In addition, the highest rates are noticed in Kuwait, Qatar, and Saudi Arabia.**")

    with col2:
        # Visualization no. 3
        st.subheader("Obesity Prevalence Among Adults by Continent, 1975-2016")
        fig = px.bar(obesityByContinent, x="Continent", y="WeightedObesity", color="Continent",
                    animation_frame="Year", animation_group="Continent", range_y=[0,45])

        fig.update_layout(
            yaxis_title="Obesity Prevalence (%)",
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)")

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.write(fig)

#----------------------------------------------------------------------------------------------------#
# Page 5: Obesity by Gender

if selected == "Obesity by Gender":
    
    #Visualization no. 5
    st.subheader("Distribution of Mean Obesity Prevalence Among Adults by Gender")
    data1975_2015 = data.query("Year in[1975, 1995, 2016 ]")
    #data1975_2015 = data.query("Year in[1995, 2016 ]")

    fig = px.violin(data1975_2015, y="Obesity", x="Year", color="Sex",  box=True, points="all")

    fig.update_layout(
        #title = "Distribution of Mean Obesity Prevalence Among Adults by Gender",
        xaxis_title="Year",
        yaxis_title="Obesity Prevalence (%)",
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        width=900, height=500)
      
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    st.write(fig)
    st.info("**Obesity prevalence rate among the total population (both sexes) has increased from 1975 till 2015. We noticed that the rate of obesity among females remained higher than that of males.**")

#----------------------------------------------------------------------------------------------------#
# Page 6: BMI Calculator
if selected == "BMI Calculator":
    left_col, info_col, sel_col, disp_col, right_col = st.columns([.5,3,3,3,1], gap='large')
    #info_col, sel_col, disp_col = st.columns(3)
    
    with info_col:
        st.header("Obesity Categories")
        st.markdown(""" 
            |Category|BMI range - kg/m2|
            |:-------|:-------------|
            |Severe Thinness|< 16|
            |Moderate Thinness|16 - 17|
            |Mild Thinness|17 - 18.5|
            |Normal|18.5 - 25| 
            |Overweight|25 - 30|
            |Obese Class I|30 - 35|
            |Obese Class II|35 - 40|
            |Obese Class III|> 40|
            """)
        
    with disp_col:
        st.header("Results")
        BMI_result = st.empty()
        msg = st.empty()
        
    with sel_col:
        st.header("BMI Calculator")     
        BMI_value = 0 
        height_cm = st.text_input('Height in cm')
        weight_kg = st.text_input("Weight in kg")
        if st.button("Calculate"):
            try:
                if (float(height_cm) <= 50):
                    raise Exception("Height must be over 50")
                height_cm = float(height_cm)
                weight_kg = float(weight_kg)
                BMI_value, bmi_category = calculate_bmi(weight_kg, height_cm)
                BMI_result.text_input('Your BMI Result', str(round(BMI_value,2))+' kg/m2')
                if bmi_category == "Normal":
                    msg.success(bmi_category)
                elif bmi_category in ["Moderate Thinness", "Overweight"] :
                    msg.warning(bmi_category)
                elif  bmi_category in ["Severe Thinness", "Obese Class I", "Obese Class II", "Obese Class III"]:
                    msg.error(bmi_category)
                else:
                    msg.write(bmi_category)
 
            except ZeroDivisionError:
                st.error("You can't divide by zero!")
            except ValueError:
                st.error('Height and weight must be numberic')
            except Exception as e:
                st.error(e)
            
# End of code
