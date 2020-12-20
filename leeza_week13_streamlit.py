#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:27:09 2020

@author: leeza
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt
import altair as alt



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
outpatient_ny = df_outpatient_2[df_outpatient_2['provider_state'] == 'NY']



st.title('Analysis of New York Inpatient and Outpatient Facilities 2015 Medicare Data')

st.subheader('By: Leeza A. Santos')

st.subheader('Last Updated: 12/20/2020')
 
st.header('This dashboard displays reported Medicare data on New York inpatient and outpatient hospital facilities utilizing Python programming language and deployed by Streamlit. ')


CHOICES = {1: "hospitals_ny", 2: "hospitals_ny", 3: "outpatient_ny"}


def format_func(option):
    return CHOICES[option]


option = st.selectbox("Select option", options=list(CHOICES.keys()), format_func=format_func)
st.write(f"You selected option {option} called {format_func(option)}")


st.subheader('Total Discharges and Average Medicare Payments by City')
st.markdown('The scatterplot below displays inpatient hospitals with the highest discharge rates and outpatient facilities with the highest services in NY. To view all counties, please enlarge the graph.')

circle1 = inpatient_ny[['provider_city', 'total_discharges', 'average_medicare_payments']]

c = alt.Chart(circle1).mark_circle().encode(
x='provider_city', y='total_discharges', size='average_medicare_payments', color='average_medicare_payments', tooltip=['provider_city', 'total_discharges', 'average_medicare_payments'])

st.altair_chart(c, use_container_width=True)




st.subheader('Top 10 Highest Discharge Rates and Outpatient Services')
st.markdown('The bar charts below displays inpatient hospitals with the highest discharge rates and outpatient facilities with the highest services in NY.')

df_bar1 = inpatient_ny[['provider_name','total_discharges']]
source1 = df_bar1[2077:2087]
 
bar1 = alt.Chart(source1).mark_bar().encode(
    x='provider_name',
    y='total_discharges'
    )
st.altair_chart(bar1)


df_bar2 = outpatient_ny[['provider_name','outpatient_services']]
source2 = df_bar2[321:331]

bar2 = alt.Chart(source2).mark_bar().encode(
    x='provider_name',
    y='outpatient_services'
    )
st.altair_chart(bar2)





    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  




# Getting column names
hospitals_ny_list = list(hospitals_ny)

# Bar Chart for "efficient_use_of_medical_imaging_national_comparison_footnote" NY average vs Stony Brook
hospitals_ny["efficient_use_of_medical_imaging_national_comparison_footnote"].mean()
# 11.7375
st.subheader('Medical Imaging Efficiency NY vs Elmhurst Hospital Center')
bar3 = pd.DataFrame({
    'NY vs Elmhurst': ['All NY Hospital Average', 'Elmhurst Hospital Center'],
    'Score': [11.7375, 5, ],
})
st.dataframe(bar3)


#Bar Chart
st.subheader('Hospital Type - NY')
bar4 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar4)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')


st.subheader('With a PIE Chart:')
fig = px.pie(bar4, values='hospital_type', names='index')
st.plotly_chart(fig)



st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#Timeliness of Care
st.subheader('NY Hospitals - Timelieness of Care')
bar5 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar5, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')



#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )





##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar6 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar6)
st.header("Hospital - ")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)



# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)