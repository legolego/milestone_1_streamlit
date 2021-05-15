
import streamlit as st
import streamlit.components.v1 as components

st.title("Predict New Imagekjhkjhs")
st.header("test html import")

HtmlFile = open(r"streamlit\data\total_pickups.html", 'r')
source_code = HtmlFile.read() 
#print(source_code)
components.html(source_code,  height = 600, width=700,)

HtmlFile = open(r"streamlit\data\dropoffs.html", 'r')
source_code = HtmlFile.read() 
#print(source_code)
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\credit_card_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\cash_tips.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\specific_day.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\single_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\double_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

st.title(" ")
st.title(" ")
st.title("Predict New Imagekjhkjhs")
HtmlFile = open(r"streamlit\data\multi_pass.html", 'r')
source_code = HtmlFile.read() 
components.html(source_code,  height = 600, width=700,)

