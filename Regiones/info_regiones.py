import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

st.title('Información Regional', anchor=None, *, help=None)
import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
   st.markdown("*Conoce la información del Servicio Civil por regiones*.")

with col2:
   st.header("Principales Indicadores")

with col3:
   st.image("imagenes/Fotos_Regiones/biobio.jpg")
