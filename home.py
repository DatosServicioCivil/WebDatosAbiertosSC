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
#st.title("Datos Abiertos Servicio Civil")
st.markdown("<h1 style='text-align: center; '><strong>Datos Abiertos Servicio Civil</strong></h1>", unsafe_allow_html=True)

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
        image = Image.open('imagenes/job_application.jpg')
        st.image(image)
        valor_col1=f"{postulaciones:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col1}</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'>Total postulaciones portal EEEPP</h1>", unsafe_allow_html=True)
    with col2:
        image = Image.open('imagenes/job_offer.png')
        st.image(image)
        valor_col2=f"{vacantes.iat[0,1]:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Total vacantes ofrecidas EEPP</h2>", unsafe_allow_html=True)
    with col3:
        image = Image.open('imagenes/mannager_selection.png')
        st.image(image)
        valor_col3=f"{concursos_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'>Total concursos ADP</h1>", unsafe_allow_html=True)
    with col4:
        image = Image.open('imagenes/adp_nombrado.PNG')
        st.image(image)
        valor_col4=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'>Total nombramientos ADP</h1>", unsafe_allow_html=True)
    with col5:
        image = Image.open('imagenes/Directores.png')
        st.image(image)
        valor_col5=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'>Seleccionados/as en Practicas Chile</h1>", unsafe_allow_html=True)
    with col6:
        image = Image.open('imagenes/trainee.PNG')
        st.image(image)
        valor_col6=f"{nombrados_adp:,}".replace(",", ".")
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col6}</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: grey;'>Directores/as Seleccionados/as</h1>", unsafe_allow_html=True)
                           


#image = Image.open('./imagenes/datosabiertos.png')
#st.image(image, width=1000)
