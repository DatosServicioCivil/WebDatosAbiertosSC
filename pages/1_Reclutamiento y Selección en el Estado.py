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


# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
st.image(my_logo)

# Set Page Header
st.header("Reclutamiento y Selección de Personas en el Estado")
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

with st.sidebar:
    a=st.radio('Reclutamiento y Selección: ',['Alta Dirección Pública','Empleo Público','Prácticas Chile'])

if a=='Alta Dirección Pública':
    with st.container():
       st.radio('Seleccionar: ',["Concursos", "Postulaciones","Nombramientos"],horizontal=True)
if a=='Empleo Público':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)
if a=='Prácticas Chile':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)

Nivel=['Nivel I', 'Nivel II']

with st.container():
    col1,col2,col3=st.columns(3,gap="large")
    with col1:
       option_1 = st.selectbox('Nivel Jerárquico',Nivel)
    with col2:
       option_2 = st.selectbox('Región',('Región de Metropolitana de Santiago',
       'Región de Magallanes y de la Antártica Chilena',
       'Región del Libertador General Bernardo OHiggins',
       'Región del Maule', 'Región del Biobío', 'Región de Los Ríos',
       'Región de  Valparaíso', 'Región de Los Lagos',
       'Región de Arica y Parinacota', 'Región de la Araucanía',
       'Región de Antofagasta', 'Región de  Atacama',
       'Región de  Coquimbo',
       'Región de Aysén del General Carlos Ibañez del Campo',
       'Región de Tarapacá', 'Región del Ñuble'))
    with col3:
       option_3 = st.selectbox('Ministerio',('Ministerio de Hacienda', 'Ministerio de Educación',
       'Ministerio de Economía, Fomento y Turismo', 'Ministerio de Salud',
       'Ministerio del Trabajo y Previsión Social',
       'Ministerio de Agricultura', 'Ministerio del Deporte',
       'Ministerio de Minería', 'Ministerio de Energía',
       'Ministerio de Defensa Nacional', 'Ministerio de Obras Públicas',
       'Ministerio de Justicia y Derechos Humanos',
       'Ministerio del Interior y Seguridad Pública',
       'Administración Central',
       'Ministerio de las Culturas, las artes y el Patrimonio',
       'Ministerio de Desarrollo Social y Familia',
       'Ministerio de Vivienda y Urbanismo',
       'Ministerio de Ciencia, Tecnología, Conocimiento e Innovación',
       'Ministerio de Relaciones Exteriores',
       'Ministerio del Medio Ambiente',
       'Ministerio de Transportes y Telecomunicaciones',
       'Ministerio de la Mujer y la Equidad de Género',
       'Ministerio Secretaría General de Gobierno', 'Autónomo'))
