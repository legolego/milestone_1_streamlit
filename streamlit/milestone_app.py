import os
from token import NT_OFFSET
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import altair as alt
import numpy as np
import statsmodels.formula.api as smf
from datetime import timedelta
import datetime as dt
from streamlit.proto.Markdown_pb2 import Markdown

CURRENT_THEME = "light"
alt.data_transformers.disable_max_rows()  
# to run this:
# streamlit run streamlit\milestone_app.py



st.title("MADS 592 - NYC Taxis and Precipitation")
st.header("Cory B and Oleg N")
st.markdown('\n\n')
st.header("Interactive and supplementary visualizations")
st.markdown('\n\n')

st.info('Please note each chart below is interactive.')
st.markdown(
    "We will first start with samples of the original data we used. Below is a few rows of the New York City taxi ride data\
        ([Source](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)).")
st.markdown('\n\n')

# https://docs.streamlit.io/en/0.65.0/advanced_concepts.html
df_taxi_sample = pd.read_csv("streamlit/data/yellow_tripdata_2010_sample.csv")
st.dataframe(df_taxi_sample)
st.markdown('\n\n')
st.markdown(
    "Next is the hourly weather data we used. This is from NOAA, using Central Park as the collection point.\
        To get it, go ([NOAA](https://www.ncdc.noaa.gov/data-access))  --> Data Access --> Quick Links --> US Local -->\
             Local Climatological Data (LCD) --> Choose your location(Add to Cart) --> Go to cart at top --> \
                 LCD CSV, date range --> Continue and give them your email, they'll send it quickly. The documentation is \
                     [here](https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/LCD_documentation.pdf). ")
st.markdown('\n\n')
# https://docs.streamlit.io/en/0.65.0/advanced_concepts.html
df_taxi_sample = pd.read_csv("streamlit/data/hourly-2020-sample.csv")
st.dataframe(df_taxi_sample)

st.title(' ')
st.markdown('''We wanted to get an overall sense of the taxi activity in NYC for pickups and drop-offs, 
so we created heatmaps for each taxi zone aggregated over 2010. It was no surprise to us that Manhattan had by 
far the most pickups and drop-offs, but it was a small surprise to see how many fewer pickups and drop-offs
 occurred in Staten Island. This lack of pickups in other bouroughs is a problem that Green taxis were created to solve
 ([Source](https://www.forbes.com/sites/johngiuffo/2013/09/30/nycs-new-green-taxis-what-you-should-know/?sh=cc6ff1a32a28)).
  Tooltips were included to show different metrics such as money spent on 
 fares, counts, and number of passengers dropped off.''')

HtmlFile = open("streamlit/data/total_pickups.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700)
st.info('Manhattan had by far the most pickups; JFK and LaGuardia airports were comparable to some of the Manhattan zones')

st.title(' ')
HtmlFile = open("streamlit/data/dropoffs.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)
st.info('Manhattan still had the most activity, but you can see the dropoffs radiated out from Manhattan and are more spread out.')

st.title(' ')
st.markdown(
    "Here rides throughtout the year are visible, binned by maximum distance and grouped by morning(9am-noon) \
    or afternoon(noon-3pm). It's interesting to see the dips around Christmas, February and March, with a \
    large spike in September.")
st.markdown('\n\n')
st.markdown('\n\n')
df_rides = pd.read_csv("streamlit/data/afternoon_treatment_dist_bins_2010_dow.csv")
df_rides['pickup_date'] = pd.to_datetime(df_rides['pickup_date'])


# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_rides, title='Rides all year').mark_line().encode(
    x=alt.X('pickup_date:T', title='Date/time', 
            axis=alt.Axis( tickCount=18, )
            ),     
    y=alt.Y('RidesCount:Q', title='Rides per time block'),
    color=alt.Color('comp_dist_bins:N', title='Distance bins (mi)') ,
    strokeDash=alt.StrokeDash('post_treatment_time_dummy:O', title='Afternoon Dummy')  
).properties(
width=875,
    height=475
).interactive()


st.altair_chart(rides)
st.info('This plot is to help illustrate inherent trends for the mornings and afternoons throughout the year. Rides were also binned based on distance.')

st.markdown('\n\n')
st.markdown('\n\n')
st.header('Taxi rides and precipitation inquiry')
st.markdown('\n\n')
st.markdown(
"Our goal was to show a causal relationship between rain and taxi ridership by counting the number of pickups before and after a rain event began. After we \
started we found that this had actually been studied already, by [Kamga et al](https://www.researchgate.net/publication/255982467_Hailing_in_the_Rain_Temporal_and_Weather-Related_Variations_in_Taxi_Ridership_and_Taxi_Demand-Supply_Equilibrium),\
[Sun et al](https://www.hindawi.com/journals/jat/2020/7081628/), and [Chen et al](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0183574). \
[Braei et al](https://arxiv.org/pdf/2004.00433.pdf) mentions that rain does increase ridership.")

st.markdown( "To investigate this relationship between rain and number of taxi rides, we created a script to identify days with rain events, and more specifically, found when these rain events began. \
We found many days throughout 2010 to investigate this relationship, but we wanted to pick a particular day to focus our initial investigation on.") 

st.markdown("We picked January 17th because this day had a rainstorm that started around 12:00 pm, \
and we thought noon was a good symmetrical boundary to split the data on ; this way, we could visualize the difference in rides for the morning \
and the afternoon, and this would represent our pre-rain and post-rain comparison. \
We found that there was a visible increase in ridership after rain had started, \
as shown in the chart below for January 17th. The increase can be seen in the yellow line, with rain having started at 11:51am. We will study this day further.")

st.markdown('\n\n')
st.markdown('\n\n')

df_single_12hrs = pd.read_csv('streamlit/data/single20100117.csv')
df_single_12hrs['b_ts'] = pd.to_datetime(df_single_12hrs['b_ts'], format='%Y-%m-%d %H:%M:%S')
df_single_12hrs['pickup_datetime_1min'] = pd.to_datetime(df_single_12hrs['pickup_datetime_1min'], format='%Y-%m-%d %H:%M:%S')
df_single_12hrs['pickup_datetime_same_time'] = pd.to_datetime(df_single_12hrs['pickup_datetime_same_time'], format='%Y-%m-%d %H:%M:%S')

b = pd.to_datetime(df_single_12hrs['b_ts'].iloc[0])


line = alt.Chart(pd.DataFrame({'x': [str(b)]})).mark_rule().encode(x=alt.X('x:T', title='') )    

# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_single_12hrs, title="Rides around " + str(b.strftime('%A')) + ' - ' + str(b)+ '(12 hour window)').mark_line().encode(
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
width=875,
    height=350
).interactive()
st.altair_chart(rides+line)
st.info('Here you can you see a spike in rides began around 12:30pm that is sustained to around 2:30pm. The previous and following week are overlayed to help illustrate inherent trends')


st.title(' ')
st.markdown(
'We wanted to investigate the taxi ride activity in Manhattan before and after the rainstorm had begun on 01/17. We aggregated the number of taxi pickups for  9am - 12pm and \
12pm - 3pm, and then computed the percent difference in rides. \
\n\n')

st.markdown('\n\n')
st.markdown('On this particular day, you can see a large percentage increase in the number of rides \
for various taxi zones in the afternoon. The choropleth below shows the results obtained. \
The largest increase is in Little Italy with a 248% increase.') 

st.title(' ')
HtmlFile = open("streamlit/data/specific_day.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)
st.info('Taxi pickups broadly increased across Manhattan after the rain event began on 01/17, especially over mid to lower Manhattan with many increasing over 50%')
st.title(' ')
st.markdown(
    "Here are two time lapses of the same day ( January 17th ) from 9am to 3pm. In the first time lapse the taxi rides are visualized via a density heatmap that represents the taxi pickups that occurred during this time range. You can see a jump in rides around 12:30pm that is sustained in the heatmap and in the time lapse time bars.\
    The second time lapse is an arc map where each pickup location is connected to its drop off location via an arc.")
st.title(' ')
HtmlFile = open("streamlit/data/kepler_test6.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 840, width=840,)
st.info('Press the play button on the bottom right to view the time lapse. This plot was generated using kepler.gl')
st.title(' ')

HtmlFile = open("streamlit/data/kepler_test7.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 840, width=840,)
st.info('Here is an arc map of the same time lapse on January 17th; for each taxi ride, the pickup location (in blue) is connected to its drop off location (in yellow) via an arc.')
st.title(' ')
st.header('Applying Differences in Differences')
st.markdown('\n\n')
st.markdown(
    "We split January 17th into two 2-hour time segments, before and after the rain started, in order to do a simple difference in differences calculation \
        using the means of each segment. The result was an increase in ridership by 87 rides per minute for this day.")
st.title(' ')
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

st.title(' ')
# https://altair-viz.github.io/user_guide/times_and_dates.html
rides = alt.Chart(df_sing_3w_4hrs, title="Rides in two-hour period before and after " + str(b.strftime('%A')) + ' - ' + str(b), height=120).mark_line().encode(
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
width=875,
    height=350
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
                    strokeDash=alt.StrokeDash('which:N', scale=alt.Scale(domain=['counter-factual'], range=[[2,2]]), legend=alt.Legend(title='Diff-in-Diff' ))                              
                    )
diff = round(treatment_post - treat_counter_fact, 1)

c_pre = round(control_ow_pre, 1)
c_post = round(control_ow_post, 1)
t_pre = round(treatment_pre, 1)
t_post = round(treatment_post, 1)
t_cf = round(treat_counter_fact, 1)

x_pre = str(df_did['timestamp'].min())
x_post = str(df_did['timestamp'].max())

dftext_res = pd.DataFrame({
 'text': [str(diff) + ' more mean rides per minute', 'in post-treatment period'],
 'tx' : [x_post, x_post],
 'ty': [450, 400]})

text_res = alt.Chart(dftext_res).mark_text(color='black', align='left', dx=-100, dy=-80, fontSize=15).encode(
 x='tx:T',
 y=alt.Y('ty:Q'
 ),
 text='text'
)

dftext_pre = pd.DataFrame({
 'text': [t_pre, c_pre],
 'tx' : [x_pre, x_pre ],
 'ty': [280, 315]})

text_pre = alt.Chart(dftext_pre).mark_text(color='black', align='left', dx=-45, dy=0, fontSize=15, fontWeight=700).encode(
 x='tx:T',
 y=alt.Y('ty:Q'
 ),
 text='text'
)

dftext_post = pd.DataFrame({
 'text': [t_cf, c_post, t_post],
 'tx' : [x_post, x_post, x_post ],
 'ty': [380, 415, 470]})

text_post = alt.Chart(dftext_post).mark_text(color='black', align='left', dx=10, dy=0, fontSize=15, fontWeight=700).encode(
 x='tx:T',
 y=alt.Y('ty:Q'
 ),
 text='text'
)


# https://github.com/altair-viz/altair/issues/1694
alt_did_chart = (rides + boundary_line + did_points + did_lines + count_fact_line + text_res + text_pre + text_post).resolve_scale(color='independent')

st.altair_chart(alt_did_chart)
st.info('Here we applied the Differences in Differences casual inference technique to the rain event on January 17th. The fitted lines are for illustrative puprposes only, and all computations were performed seperately.')


st.title(' ')
st.markdown(
    "We did try to set up an experiment using the hours of 9am-noon and \
        noon-3pm as a morning/afternoon boundary for a differences in differences. Our control group was days with both dry mornings \
            and dry afternoons, and our treatment group was days with a dry morning and a wet afternoon.")
st.title(' ')

df_weather = pd.read_csv('streamlit/data/cb_weather_to_join.csv')
df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])
df_weather_rides = pd.merge(df_weather, df_rides,  how='left', left_on=['DATE','afternoon_dummy'], right_on = ['pickup_date','post_treatment_time_dummy'])
df_reg = df_weather_rides.groupby(['DATE', 'afternoon_dummy', 'HourlyPrecipitation',
       'HourlyDryBulbTemperature', 'treatment', 'pickup_date',
       'post_treatment_time_dummy',
       'pickup_day_of_week', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
       'Friday', 'Saturday', 'Sunday'])['RidesCount'].sum().reset_index()

st.dataframe(df_reg)
st.markdown('\n\n')
st.info('Sample of dataframe used for regression')
st.markdown('\n\n')
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


st.markdown('\n\n')
# https://github.com/altair-viz/altair/issues/1331
base = alt.Chart(df_err_bars, width=750, height=250)
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



st.markdown('\n\n')

st.altair_chart((error_bars + points + rule).interactive())
st.markdown('\n\n')
st.info(
    "Visual results of the regression with 95% confidence bars.")
st.markdown('''The results of our regression were not statistically significant, as you can see the 95% confidence interval of the
 interaction term (treatment:afternoon_dummy) crossing zero. We cannot say with confidence that the treatment(rain) had any kind of effect 
 during the treatment timefream(afternoon). This was disappointing, though we did learn a lot. We would like to explore this in the future.
''')
st.title('')
st.header(' A seperate general inquiry')
st.markdown('\n\n')
st.markdown('''Before starting this project, we had ideas to investigate average tips per taxi ride for each neighborhood, and also the general relationships between the top most active neighborhoods. This was a separate inquiry from our investigation on rain, but nonetheless we pursued these idea and obtained some interesting results. 
\n\n We split our data into two groups, taxi rides that were paid in cash, and taxi rides that were paid by credit card; we felt this was an important step because we expected rides paid by cash to have somewhat under-reported tips and did not want to lump these two groups together.
We expected Manhattan to broadly have the highest average tip, but surprisingly tips were generally higher outside of Manhattan. There were even two outliers in Manhattan for zones Upper East Side North and Union SQ with a tip of percentages of 3.2% and 10.8 % respectively
''')

st.title(' ')
HtmlFile = open("streamlit/data/credit_card_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)
st.info('Tips for rides paid via credit card were on average higher outside of Manhattan. Note the two outlier zones in Manhattan for zones Upper East Side North and Union SQ ')
st.markdown('\n\n')
st.title(' ')
st.markdown('We expected taxi rides paid in cash to under report tips, but to our surprise, the under-reporting was much more egregious than expected.')
st.markdown(' ')
st.markdown(' ')
HtmlFile = open("streamlit/data/cash_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)
st.info('Taxi rides paid via cash dramatically underreporrted tips, or didn\'t report them at all')

st.title(' ')
st.markdown('''We wanted to investigate relationships between the different neighborhoods in NYC, so we created a heatmap for the top 50 relationships for pick up and drop off locations. To pull out underlying relationships, such as subnetworks and connections between the groups of pickup and drop-off locations, we used a clustering algorithm to arrange the locations on each axis by similarity.''')
st.markdown('''The similarity was computed using Euclidean distance, and the inherent patterns within the charts can be interpreted as subnetworks between different neighborhoods. For example, the blue square in the upper left corner of each plot represents a strong subnetwork between the Upper east Side North and Upper east Side South zones. Similar interpretations can be made for other observed patterns in the below charts (patterns of shapes and consecutive strips).
This method was repeated for single passenger rides, double passenger rides, and multi passenger rides.
''')

st.title(' ')
HtmlFile = open("streamlit/data/single_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title(' ')
HtmlFile = open("streamlit/data/double_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title(" ")
HtmlFile = open("streamlit/data/multi_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 680, width=700,)





st.info(
    "Further analysis is needed for this time series, with some hints given by [Moraffah et al](https://arxiv.org/pdf/2102.05829v1.pdf)")













