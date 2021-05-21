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
#alt.themes.enable('quartz')  
# to run this:
# streamlit run streamlit\milestone_app.py


st.title("MADS 592 - NYC Taxis and Precipitation")
st.header("Oleg N and Cory B")
st.subheader("Interactive and supplementary visualizations")

st.info(
    "This page is best viewed with a light colored theme, which can be set in under Settings in the hanburger menu in the top right corner.")



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


st.info(
    "The following two charts show the range of pickups and dropoffs throughout New York City, topping out at over 6 million for the year in some regions!")


HtmlFile = open("streamlit/data/total_pickups.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

HtmlFile = open("streamlit/data/dropoffs.html", 'r')
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
).configure(background='#D9E9F0').interactive()

st.altair_chart(rides)


st.info(
    "Our goal was to show a causal relationship between rain and taxi ridership by counting the number of pickups. After we \
        started we found that this had actually been studied already, by [Kamga et al](https://www.researchgate.net/publication/255982467_Hailing_in_the_Rain_Temporal_and_Weather-Related_Variations_in_Taxi_Ridership_and_Taxi_Demand-Supply_Equilibrium), \
        [Sun et al](https://www.hindawi.com/journals/jat/2020/7081628/), and [Chen et al](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0183574). \
        [Braei et al](https://arxiv.org/pdf/2004.00433.pdf) mentions that rain does increase ridership. Looking at the weather \
        data and finding when rain started, we found that there was a visible increase in ridership after rain had started, \
        as shown in the chart below for January 17th. The increase can be seen in the yellow line, with rain having started at 11:51am. We will study this day further.")



df_single_12hrs = pd.read_csv('streamlit/data/single20100117.csv')
df_single_12hrs['b_ts'] = pd.to_datetime(df_single_12hrs['b_ts'], format='%Y-%m-%d %H:%M:%S')
df_single_12hrs['pickup_datetime_1min'] = pd.to_datetime(df_single_12hrs['pickup_datetime_1min'], format='%Y-%m-%d %H:%M:%S')
df_single_12hrs['pickup_datetime_same_time'] = pd.to_datetime(df_single_12hrs['pickup_datetime_same_time'], format='%Y-%m-%d %H:%M:%S')

b = pd.to_datetime(df_single_12hrs['b_ts'].iloc[0])


line = alt.Chart(pd.DataFrame({'x': [str(b)]})).mark_rule().encode(x=alt.X('x:T', title='') )    

# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_single_12hrs, title='B_ID: ' + str(df_single_12hrs.iloc[0]['b_id']) + " - Rides around " + str(b.strftime('%A')) + ' - ' + str(b)+ '(12 hour window)').mark_line().encode(
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



st.info(
    "Here we show the percent chage in ridership before and after the rain started. The largest increase is in Little Italy.")

HtmlFile = open("streamlit/data/specific_day.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)


st.info(
    "We split January 17th into two 2-hour time segments, before and after the rain started, in order to do a simple difference in differences calculation \
        using the means of each segment. The result was an increase in ridership by 87 rides per minute for this day.")
# make two hour windows before and after boundary
ts_before = b + timedelta(hours=-2)
ts_after = b + timedelta(hours=2)

# get all three weeks in plus/minus 2 hour window
df_sing_3w_4hrs = df_single_12hrs[(df_single_12hrs['pickup_datetime_same_time']>= ts_before) & (df_single_12hrs['pickup_datetime_same_time'] <= ts_after)] 
# current week
df_sing_3w_cw = df_sing_3w_4hrs[df_sing_3w_4hrs['which_week']=='Current week']
# other weeks
df_sing_3w_ow = df_sing_3w_4hrs[df_sing_3w_4hrs['which_week']!='Current week']

lstDictsBID = []
treatment_pre = df_sing_3w_cw[df_sing_3w_cw['pickup_datetime_same_time']< b]['rides_per_minute'].mean()
# https://stackoverflow.com/questions/2853683/what-is-the-preferred-syntax-for-initializing-a-dict-curly-brace-literals-or
lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'treatment', 'timestamp': b + timedelta(hours=-1), 'rides_per_min': treatment_pre})
treatment_post = df_sing_3w_cw[df_sing_3w_cw['pickup_datetime_same_time']>= b]['rides_per_minute'].mean()
lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'treatment', 'timestamp': b + timedelta(hours=1), 'rides_per_min': treatment_post})

lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'counter-factual', 'timestamp': b + timedelta(hours=-1), 'rides_per_min': treatment_pre})

control_ow_pre = df_sing_3w_ow[df_sing_3w_ow['pickup_datetime_same_time']< b]['rides_per_minute'].mean()
lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'control', 'timestamp': b + timedelta(hours=-1), 'rides_per_min': control_ow_pre})
control_ow_post = df_sing_3w_ow[df_sing_3w_ow['pickup_datetime_same_time']>= b]['rides_per_minute'].mean()
lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'control', 'timestamp': b + timedelta(hours=1), 'rides_per_min': control_ow_post})

treat_counter_fact = control_ow_post - control_ow_pre + treatment_pre
lstDictsBID.append({'b_id': 0, 'b':b, 'which': 'counter-factual', 'timestamp': b + timedelta(hours=1), 'rides_per_min': treat_counter_fact})

df_did = pd.DataFrame(lstDictsBID)

boundary_line = alt.Chart(pd.DataFrame({'x': [str(b)]})).mark_rule().encode(x=alt.X('x:T', title='') ) 

# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_sing_3w_4hrs, title='B_ID: ' + str(df_single_12hrs.iloc[0]['b_id']) + " - Rides around " + str(b.strftime('%A')) + ' - ' + str(b), height=120).mark_line().encode(
    #x=alt.X('hoursminutes(pickup_datetime_1min):Q', title='Date/time', 
    #x=alt.X('utchoursminutes(pickup_datetime_1min_str):T', title='Date/time', 
    x=alt.X('pickup_datetime_same_time:T', title='Date/time', 
            axis=alt.Axis(
                        tickCount=18,
                    )
            ),     
    y=alt.Y('rides_per_minute:Q', title='Rides per minute', scale=alt.Scale(domain=[0, 700])),
    color=alt.Color('which_week:N', title='Which week', scale=alt.Scale(
                                            domain=['Week before', 'Current week', 'Week after'],
                                            range=['#DB9EA6 ', '#FFE303', '#adc0d8']))
).properties(
width=700,
    height=250
)

did_points = alt.Chart(df_did).mark_circle(size=100).encode(
                    x=alt.X('timestamp:T', title=''),
                    y=alt.Y('rides_per_min:Q', title=''),
                    color=alt.Color('which:N', title='Rides per minute means',
                     scale=alt.Scale(domain=['control', 'treatment', 'counter-factual'], 
                     range=['red','blue', 'blue']),
                     legend=None),                                     
                    )



did_lines = alt.Chart(df_did).mark_line().encode(
                    x=alt.X('timestamp:T', title=''),
                    y=alt.Y('rides_per_min:Q', title=''),
                    color=alt.Color('which:N', title='Rides per minute means', scale=alt.Scale(domain=['control', 'treatment'], range=['red', 'blue'])),                                     
                    )

count_fact_line = alt.Chart(df_did[df_did['which'] == 'counter-factual']).mark_line(strokeWidth=1).encode(
                    x=alt.X('timestamp:T', title=''),
                    y=alt.Y('rides_per_min:Q', title=''),
                    color=alt.Color('which:N', scale=alt.Scale(domain=['counter-factual'], range=['blue']), legend=None), 
                    strokeDash=alt.StrokeDash('which:N', scale=alt.Scale(domain=['counter-factual'], range=[[2,2]]), legend=alt.Legend(title='' ))                              
                    )
diff = round(treatment_post - treat_counter_fact, 1)
dftext = pd.DataFrame({
 'text': [str(diff) + ' more mean rides per minute', 'in post-treatment period'],
 'tx' : [str(df_did['timestamp'].max()), str(df_did['timestamp'].max())],
 'ty': [450, 400]})


text = alt.Chart(dftext).mark_text(color='black', align='left', dx=-100, dy=-50, fontSize=15).encode(
 x='tx:T',
 y=alt.Y('ty:Q'
 ),
 text='text'
)


# https://github.com/altair-viz/altair/issues/1694
alt_did_chart = (rides + boundary_line + did_points + did_lines + count_fact_line + text).resolve_scale(color='independent')

st.altair_chart(alt_did_chart)




st.info(
    "We did try to set up an experiment using the hours of 9am-noon and \
        noon-3pm as a morning/afternoon boundary for a differences in differences. Our control group was days with both dry mornings \
            and afternoons, and our treatment group was days with dry morning and wet afternoons.")


df_weather = pd.read_csv('streamlit/data/cb_weather_to_join.csv')
df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
df_weather_rides = pd.merge(df_weather, df_rides,  how='left', left_on=['DATE','afternoon_dummy'], right_on = ['pickup_date','post_treatment_time_dummy'])
df_reg = df_weather_rides.groupby(['DATE', 'afternoon_dummy', 'HourlyPrecipitation',
       'HourlyDryBulbTemperature', 'treatment', 'pickup_date',
       'post_treatment_time_dummy',
       'pickup_day_of_week', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
       'Friday', 'Saturday', 'Sunday'])['RidesCount'].sum().reset_index()


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


st.title("Predict New Image")
HtmlFile = open("streamlit/data/credit_card_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Image")
HtmlFile = open("streamlit/data/cash_tips.html", 'r')
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


st.title("Predict New Image")
HtmlFile = open("streamlit/data/multi_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)


st.title("Predict New Image")
HtmlFile = open("streamlit/data/kepler_test6.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 900, width=900,)


st.info(
    "Further analysis is needed for this time series, with some hints given by [Moraffah et al](https://arxiv.org/pdf/2102.05829v1.pdf)")













