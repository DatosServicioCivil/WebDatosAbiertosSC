import streamlit as st
from streamlit_option_menu import option_menu
# import snowflake.connector
import pandas as pd
from PIL import Image
import plotly.express as px
import numpy as np
# import base64
import time
# import altair as alt
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
st.image(my_logo)

# Set Page Header
st.header("Mujeres en el Estado")
# Set custom CSS for hr element
st.markdown(
    """
        <style>
            hr {
                margin-top: 0.0rem;
                margin-bottom: 0.5rem;
                height: 3px;
                background-color: #333;
                border: none;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

# Add horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

texto_mas_mujeres="""Mas Mujeres: Conoce los principales indicadores del Servicio Civil que 
potencian y aumentab la presencia laboral y el liderazgo de las mujeres en el Estado"""
valor_col2=0.5
valor_col3=0.31
valor_col4=0.7
with st.container():
    col1,col2,col3,col4=st.columns(4,gap='small')
    with col1:
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{texto_mas_mujeres}</h1>", unsafe_allow_html=True)
    with col2:
        #image = Image.open('imagenes/job_offer.png')
        #st.image(image)
        valor_col2=f"{valor_col2}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total vacantes ofrecidas EEPP</h2>", unsafe_allow_html=True)
    with col3:
        valor_col3=f"{valor_col3}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total concursos ADP</h2>", unsafe_allow_html=True)
    with col4:
        #image = Image.open('imagenes/mannager_selection.png')
        #st.image(image)
        valor_col4=f"{valor_col4}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total nombramientos ADP</h2>", unsafe_allow_html=True)
                           
