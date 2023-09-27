import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout='wide')

st.title('Información Regional', anchor=None, help=None)

col1, col2, col3 = st.columns(3)

with col1:
   st.markdown("**Conoce la información del Servicio Civil por regiones**.")
   st.markdown("Selecciona zona y región")
   col4, col5, col6, col7=st.columns(4)
   with col4:
      zona=st.selectbox("Zona", ["Norte", "Centro", "Sur", "Austral"])
   with col5:
      if zona=='Norte':
         region=st.selectbox("Región", ["Tarapacá", "Antofagasta", "Atacama", "Coquimbo"])
      if zona=='Centro':
         region=st.selectbox("Región", ["Valparaíso","Metropolitana" ,"O’Higgins", "Maule"])
      if zona=='Sur':
         region=st.selectbox("Región", ["Ñuble", "Biobío", "La Araucanía", "Los Ríos","Los Lagos"])
      if zona=='Austral':
         region=st.selectbox("Región", ["Aysén", "Magallanes"])

with col2:
   st.markdown("*Principales indicadores regionales*.")

with col3:
   # zona norte
   if region=='Tarapacá':
      st.image("imagenes/Fotos_Regiones/Iquique_night_skyline.jpg", caption='Ciudad de Iquique - Región de Tarapacá')
   if region=='Antofagasta':
      st.image("imagenes/Fotos_Regiones/Mano_del_desierto_07.jpg", caption='La Mano del Desierto - Región de Antofagasta')
   if region=='Atacama':
      st.image("imagenes/Fotos_Regiones/Desierto_florido.jpg", caption='Desierto florido - Región de Atacama')
   if region=='Coquimbo':
      st.image("imagenes/Fotos_Regiones/la-serena.jpg",caption='Faro de La Serena - Región de Coquimbo')
   # zona centro
   if region=='Valparaíso':
      st.image("imagenes/Fotos_Regiones/valparaiso_gr-740x540.jpg")
   if region=='Metropolitana':
      st.image("imagenes/Fotos_Regiones/Plaza_de_la_Constitución_Chile.jpg")
   if region=='O’Higgins':
      st.image("imagenes/Fotos_Regiones/ohiggins.jpg")
   if region=='Maule':
      st.image("imagenes/Fotos_Regiones/maule.jpg")
   # zona sur
   if region=='Ñuble':
      st.image("imagenes/Fotos_Regiones/ñuble.jpg")
   if region=='Biobío':
      st.image("imagenes/Fotos_Regiones/biobio.jpg")
   if region=='La Araucanía':
      st.image("imagenes/Fotos_Regiones/araucania.jpg")
   if region=='Los Ríos':
      st.image("imagenes/Fotos_Regiones/800px-Valdivia_y_su_río.jpg")
   if region=='Los Lagos':
      st.image("imagenes/Fotos_Regiones/lagos.jpg")
   # zona Austral
   if region=='Aysén':
      st.image("imagenes/Fotos_Regiones/caleta_tortel_2012-10.jpg")
   if region=='Magallanes':
      st.image("imagenes/Fotos_Regiones/torrespaine.jpg")
