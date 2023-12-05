import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import numpy as np


st.set_page_config(layout='wide')

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)

# Set Page Header
st.header("Otros links de interes")
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

with st.container():
    col1,col2,col3=st.columns(3,gap='large')
    with col1:
        st.markdown('En este link podras encntrar los perfiles de cargos ADP publicados')
        st.write("<a href='https://www.serviciocivil.cl/consejo-alta-direccion-publica/perfiles-vigentes-cargos-adp/' id='my-link'>Perfiles cargos ADP</a>", unsafe_allow_html=True)
    with col2:
        st.markdown('Aca puedes encontrar las actas del Consejo de Alta Dirección Pública')
        st.write("<a href='https://www.serviciocivil.cl/consejo-alta-direccion-publica/actas-del-consejo-de-alta-direccion-publica/' id='my-link'>Actas de Consejo ADP</a>", unsafe_allow_html=True)

