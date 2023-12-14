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
import pyarrow.parquet as pq

st.set_page_config(layout='wide',
                   initial_sidebar_state="expanded")                                #collapsed


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

remote_css(
    "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css")
local_css("style.css")

# This function sets the logo and company name inside the sidebar

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

# Set Page Header
st.header("Datos Abiertos Servicio Civil")

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

#--------------------------------------------------------------------------------------------
@st.cache_data
def df_conc_eepp():
    df_conc_ep=pd.read_table('EEPP/df_concursos_eepp.parquet').to_pandas()
    return df_conc_ep


@st.cache_data
def df_con_adp():
    df_concursos_adp=pq.read_table('ADP/df_concursos.parquet').to_pandas()
    df_conc_adp=df_concursos_adp
    return df_conc_adp


df_concursos_eepp=df_conc_eepp()
df_concursos_adp=df_con_adp()


vacantes = df_concursos_eepp['Vacantes'].sum()
postulaciones=df_concursos_eepp['Total_Postulaciones'].sum()
postulaciones_laborales=df_concursos_eepp['Total_Postulaciones'].sum()
concursos_adp=df_concursos_adp.CD_Concurso.count()
nombrados_adp=df_concursos_adp.query("Estado=='Nombrado'").CD_Concurso.count()


with st.container():
    col1,col2,col3,col4,col5,col6=st.columns(6,gap='small')
    with col1:
        #image = Image.open('imagenes/job_application.jpg')
        image=add_logo(logo_path="./imagenes/job_application.jpg", width=150, height=150)
        st.image(image)
        valor_col1=f"{postulaciones:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col1}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total postulaciones portal EEEPP</h2>", unsafe_allow_html=True)
    with col2:
        #image = Image.open('imagenes/job_offer.png')
        image=add_logo(logo_path="./imagenes/job_offer.png", width=150, height=150)
        st.image(image)
        valor_col2=f"{vacantes.iat[0,1]:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total vacantes ofrecidas EEPP</h2>", unsafe_allow_html=True)
    with col3:
        #image = Image.open('imagenes/mannager_selection.png')
        image=add_logo(logo_path="./imagenes/mannager_selection.png", width=150, height=150)
        st.image(image)
        valor_col3=f"{concursos_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total concursos ADP</h2>", unsafe_allow_html=True)
    with col4:
        #image = Image.open('imagenes/adp_nombrado.PNG')
        image=add_logo(logo_path="./imagenes/adp_nombrado.PNG", width=150, height=150)
        st.image(image)
        valor_col4=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total nombramientos ADP</h2>", unsafe_allow_html=True)
    with col5:
        #image = Image.open('imagenes/Directores.png')
        image=add_logo(logo_path="./imagenes/Directores.png", width=150, height=150)
        st.image(image)
        valor_col5=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Personas seleccionadas en Prácticas Chile</h2>", unsafe_allow_html=True)
    with col6:
        #image = Image.open('imagenes/trainee.PNG')
        image=add_logo(logo_path="./imagenes/trainee.PNG", width=150, height=150)
        st.image(image)
        valor_col6=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col6}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Personas seleccionadas en Directores para Chile</h2>", unsafe_allow_html=True)
                           


#image = Image.open('./imagenes/datosabiertos.png')
#st.image(image, width=1000)
