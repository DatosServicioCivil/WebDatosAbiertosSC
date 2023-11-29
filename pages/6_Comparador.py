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
import plotly.express as px 
import plotly.graph_objects as go

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
st.header("Comparador de datos")
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

# define si se ven los ejes Y
visible_y_axis=True

with st.container():
    seleccion=st.selectbox("Selecciona el tipo de información a comparar",["Por región","Por organismo"])

    if seleccion=="Por región":
        st.subheader("Región N°1")
        col1,col2=st.columns(2)
        with col1:
            st.write("Selecciona región N°1")
            region1=st.selectbox("Región 1",["Arica y Parinacota","Tarapacá","Antofagasta","Atacama","Coquimbo","Valparaíso","Metropolitana","O’Higgins","Maule","Ñuble","Biobío","Araucanía","Los Ríos","Los Lagos","Aysén","Magallanes"])
        with col2:
            st.subheader("Selecciona región N°2")
            region2=st.selectbox("Región 1",["Arica y Parinacota","Tarapacá","Antofagasta","Atacama","Coquimbo","Valparaíso","Metropolitana","O’Higgins","Maule","Ñuble","Biobío","Araucanía","Los Ríos","Los Lagos","Aysén","Magallanes"])
        if region1==region2:
            st.error("No se pueden seleccionar dos regiones iguales")
            st.stop()
        
        st.write("Selecciona el tipo de información a comparar")
        tipo=st.selectbox("Tipo de información",["Casos nuevos","Casos totales","Casos activos","Fallecidos","Casos recuperados","Casos nuevos con sintomas","Casos nuevos sin sintomas","Casos nuevos sin notificar","Casos nuevos con sintomas por 100 mil habitantes","Casos nuevos sin sintomas por 100 mil habitantes","Casos nuevos sin notificar por 100 mil habitantes","Casos totales por 100 mil habitantes","Casos activos por 100 mil habitantes","Fallecidos por 100 mil habitantes","Casos recuperados por 100 mil habitantes"])

        st.write("Selecciona el rango de fechas a comparar")
        fecha1=st.date_input("Fecha 1",value=pd.to_datetime("2020-03-03"))
        fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))

        st.write("Selecciona el tipo de gráfico a mostrar")
        grafico=st.selectbox("Tipo de gráfico",["Gráfico de líneas","Gráfico de barras"])

        st.write("Selecciona el tipo de datos a mostrar")
        datos=st.selectbox("Tipo de datos",["Datos absolutos","Datos por 100 mil habitantes"])

        st.write("Selecciona el tipo de eje Y a mostrar")
        eje=st.selectbox("Tipo de eje Y",["Eje Y por región","Eje Y global"])
