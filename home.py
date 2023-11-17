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
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

#my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
#st.sidebar.image(my_logo)
#st.sidebar.header("Configuration")
#st.sidebar.subheader("Servicio Civil.")

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
df_concursos_eepp_aviso=pd.read_csv('EEPP/df_concursos_eepp_Aviso.csv',sep=";",encoding='utf-8')
df_concursos_eepp_Postulacion=pd.read_csv('EEPP/df_concursos_eepp_Postulacion en linea.csv',sep=";",encoding='utf-8')
df_concursos_eepp=pd.concat([df_concursos_eepp_aviso,df_concursos_eepp_Postulacion])

df_concursos_adp=pd.read_csv('ADP/df_concursos.csv',sep=";",encoding='utf-8')


vacantes = df_concursos_eepp.agg({'Nº de Vacantes':'sum'}).reset_index()
postulaciones=df_concursos_eepp['Número Postulaciones'].sum()
postulaciones_laborales=df_concursos_eepp['Número Postulaciones'].sum()
concursos_adp=df_concursos_adp.CD_Concurso.count()
nombrados_adp=df_concursos_adp.query("Estado=='Nombrado'").CD_Concurso.count()



with st.container():
    col1,col2,col3,col4,col5,col6=st.columns(6,gap='small')
    with col1:
        image = Image.open('cgonzalezavalos/WebDatosAbiertosSC/imagenes/job_application.jpg')
        st.image(image)
        st.subheader(f"{postulaciones:,}".replace(",", "."))
        st.subheader('Total postulaciones portal EEEPP')
    with col2:
        st.subheader(f"{vacantes.iat[0,1]:,}".replace(",", "."))
        st.subheader('Total vacantes ofrecidas EEPP')
    with col3:
        st.subheader(f"{concursos_adp:,}".replace(",", "."))
        st.subheader('Total concursos ADP')
    with col4:
        st.subheader(f"{nombrados_adp:,}".replace(",", "."))
        st.subheader('Nombramientos ADP')
    with col5:
        st.subheader(f'{vacantes.iat[0,1]}')
        st.subheader('Seleccionados en Practicas Chile')
    with col6:
        st.subheader(f'{vacantes.iat[0,1]}')
        st.subheader('Directores/as Seleccionados/as')
                           


image = Image.open('./imagenes/datosabiertos.png')
st.image(image, width=1000)
