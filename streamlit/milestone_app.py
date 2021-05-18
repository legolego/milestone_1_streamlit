import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import numpy as np
import statsmodels.formula.api as smf
from datetime import timedelta
import datetime as dt

alt.data_transformers.disable_max_rows()  
# to run this:
# streamlit run streamlit\milestone_app.py


st.title("MADS 592 - NYC Taxis and Precipitation")
st.header("Oleg N and Cory B")
st.subheader("Interactive and supplementary visualizations")


st.info(
    "We will first start with samples of the original data we used. Below is a few rows of the New York City taxi ride data.\
        ([Source](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)) ")


# https://docs.streamlit.io/en/0.65.0/advanced_concepts.html
df_taxi_sample = pd.read_csv("streamlit/data/yellow_tripdata_2010_sample.csv")
st.dataframe(df_taxi_sample)

st.info(
    "Next is the hourly weather data we used. This is from NOAA, using Central Park as the collection point.\
        To get it, go ([NOAA](https://www.ncdc.noaa.gov/data-access))  --> Data Access --> Quick Links --> US Local -->\
             Local Climatological Data (LCD) --> Choose your location(Add to Cart) --> Go to cart at top --> \
                 LCD CSV, date range --> Continue and give them your email, they'll send it quickly. The documentation is \
                     [here](https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/LCD_documentation.pdf). ")

# https://docs.streamlit.io/en/0.65.0/advanced_concepts.html
df_taxi_sample = pd.read_csv("streamlit/data/hourly-2020-sample.csv")
st.dataframe(df_taxi_sample)


HtmlFile = open("streamlit/data/total_pickups.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

HtmlFile = open("streamlit/data/dropoffs.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/credit_card_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/cash_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/specific_day.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/single_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/double_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title(" ")
st.title(" ")
st.title("Predict New Image")
HtmlFile = open("streamlit/data/multi_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)



st.info(
    "Here rides throughtout the year are visible, binned by maximum distance and grouped by morning(9am-noon) \
    or afternoon(noon-3pm). It's interesting to see the dips around Christmas, February and March, with a \
    large spike in September.")

df_rides = pd.read_csv("streamlit/data/afternoon_treatment_dist_bins_2010_dow.csv")
df_rides['pickup_date'] = pd.to_datetime(df_rides['pickup_date'])


# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_rides, title='Rides all year').mark_line().encode(
    x=alt.X('pickup_date:T', title='Date/time', 
            axis=alt.Axis( tickCount=18, )
            ),     
    y=alt.Y('RidesCount:Q', title='Rides per time block'),
    color=alt.Color('comp_dist_bins:N', title='Ride distance') ,
    strokeDash=alt.StrokeDash('post_treatment_time_dummy:O', title='Afternoon Dummy')  
).properties(
width=1000,
    height=600
).interactive()

st.altair_chart(rides)


df_weather = pd.read_csv('streamlit/data/cb_weather_to_join.csv')
df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
df_weather_rides = pd.merge(df_weather, df_rides,  how='left', left_on=['DATE','afternoon_dummy'], right_on = ['pickup_date','post_treatment_time_dummy'])
df_reg = df_weather_rides.groupby(['DATE', 'afternoon_dummy', 'HourlyPrecipitation',
       'HourlyDryBulbTemperature', 'treatment', 'pickup_date',
       'post_treatment_time_dummy',
       'pickup_day_of_week', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
       'Friday', 'Saturday', 'Sunday'])['RidesCount'].sum().reset_index()


st.info(
    "Our goal was to try to show causation between rain and ridership. We tried to set up an experiment using the hours of 9am-noon and \
        noon-3pm as a morning/afternoon boundary using differences in differences. Our control group was days with both dry mornings \
            and afternoons, and our treatment group was days with dry morning and wet afternoons.")

df_ols = df_reg
# reg = smf.ols(formula = 'rides_per_minute/total rides in 4 hour window ~ sunday, monmday. tuesday... (6days) + (post)afternoon_dummy + (treatment)norain morinign and rain_afternoon_dummy + interaction(post and treatment)', data = df_ols).fit()
#reg = smf.ols(formula = 'RidesCount ~ treatment + afternoon_dummy + treatment:afternoon_dummy', data = df_ols).fit()
# CB removed hourly precipiation
with st.echo():
    reg = smf.ols(formula = 'RidesCount ~ Tuesday + Wednesday + Thursday + Friday + Saturday + Sunday +  HourlyDryBulbTemperature + treatment + afternoon_dummy + treatment:afternoon_dummy', data = df_ols).fit()
    ols_robust2_1 = reg.get_robustcov_results(cov_type= 'HC1') 
    ols_robust2_1.summary()

df_coeffs = pd.DataFrame(reg.params).reset_index()
df_95errs = pd.DataFrame(ols_robust2_1.conf_int())
df_err_bars = pd.concat([df_coeffs, df_95errs], axis=1).iloc[1:]
df_err_bars.columns = ['Covariate', 'Coeff', 'conf_int0', 'conf_int1']


# https://github.com/altair-viz/altair/issues/1331
base = alt.Chart(df_err_bars, width=800, height=200)
sortCol = 'Coeff'

points = base.mark_point(filled=True).encode(
    x=alt.X(
        'Coeff',
        #scale=alt.Scale(zero=False),
        axis=alt.Axis(title='Coefficient and 95% confidence bars'),
    ),
    y=alt.Y('Covariate:N',
            sort=alt.EncodingSortField(field=sortCol, order='descending')
    ),
    color=alt.value('black')
)
error_bars = base.mark_bar(size=2).encode(
    x=alt.X('conf_int0:Q',
        ),
    x2='conf_int1:Q',
    y=alt.Y('Covariate:N',            
            sort=alt.EncodingSortField(field=sortCol, order='descending'),
    ),
)
rule = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='red').encode(
    x='x',
    size=alt.value(2)
)

st.info(
    "Visual results of the regression with 95% confidence bars.")
st.altair_chart((error_bars + points + rule).interactive())



df_single = pd.read_csv('streamlit/data/single20100117.csv')
df_single['b_ts'] = pd.to_datetime(df_single['b_ts'], format='%Y-%m-%d %H:%M:%S')
df_single['pickup_datetime_1min'] = pd.to_datetime(df_single['pickup_datetime_1min'], format='%Y-%m-%d %H:%M:%S')
df_single['pickup_datetime_same_time'] = pd.to_datetime(df_single['pickup_datetime_same_time'], format='%Y-%m-%d %H:%M:%S')

b = pd.to_datetime(df_single['b_ts'].iloc[0])


line = alt.Chart(pd.DataFrame({'x': [str(b)]})).mark_rule().encode(x=alt.X('x:T', title='') )    

# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_single, title='B_ID: ' + str(df_single.iloc[0]['b_id']) + " - Rides around " + str(b.strftime('%A')) + ' - ' + str(b)).mark_line().encode(
    #x=alt.X('hoursminutes(pickup_datetime_1min):Q', title='Date/time', 
    #x=alt.X('utchoursminutes(pickup_datetime_1min_str):T', title='Date/time', 
    x=alt.X('pickup_datetime_same_time:T', title='Date/time', 
            axis=alt.Axis(
                        tickCount=18,
                    )
            ), 
    #x=alt.X('sequence:Q', axis=None, title='Date/time' ),     
    y=alt.Y('rides_per_minute:Q', title='Rides per minute'),
    color=alt.Color('which_week:N', title='Which week', scale=alt.Scale(
                                            domain=['Week before', 'Current week', 'Week after'],
                                            range=['#DB9EA6 ', '#FFE303', '#adc0d8']))
).properties(
width=700,
    height=250
).interactive()


st.altair_chart(rides+line)

