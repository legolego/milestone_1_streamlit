
import streamlit as st
import streamlit.components.v1 as components

# https://drive.google.com/drive/folders/13cpp-BNdP6Sc623PyR8_Fq0YzwK6lZ1Z?usp=sharing

# url = ' google drive sharing link'
# path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]

st.title("Predict New Imagekjhkjhs")
st.header("test html import")

# import os
# st.header(os.listdir())

HtmlFile = open(r"\streamlit\data\total_pickups.html", 'r')
source_code = HtmlFile.read() 
#print(source_code)
components.html(source_code,  height = 600, width=700,)

# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\dropoffs.html", 'r')
# source_code = HtmlFile.read() 
# #print(source_code)
# components.html(source_code,  height = 600, width=700,)

# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\credit_card_tips.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\cash_tips.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\specific_day.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\single_pass.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\double_pass.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

# st.title(" ")
# st.title(" ")
# st.title("Predict New Imagekjhkjhs")
# HtmlFile = open(r"milestone_1_streamlit\streamlit\data\multi_pass.html", 'r')
# source_code = HtmlFile.read() 
# components.html(source_code,  height = 600, width=700,)

