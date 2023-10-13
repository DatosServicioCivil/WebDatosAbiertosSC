import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px 
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout='wide')

st.title('Información Regional', anchor=None, help=None)

# https://github.com/mydgd/snowflake-table-catalog/blob/main/snowflake-table-catalog.py

col1, col2, col3 = st.columns(spec=[0.2,0.6,0.2],gap='small')

df_kpi_region=pd.read_csv('kpi/indicadores_regionales.csv',sep=";",encoding='utf-8')
kpi1=df_kpi_region[df_kpi_region.id=='t_1_1'].resultado.value[0]
# df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8') 

with col1:
   st.markdown("**Conoce la información del Servicio Civil por regiones**.")
   st.markdown("Selecciona zona y región")
   zona=st.selectbox("Zona", ["Norte", "Centro", "Sur", "Austral"])
   if zona=='Norte':
      region=st.selectbox("Región", ["Tarapacá", "Antofagasta", "Atacama", "Coquimbo"])
   if zona=='Centro':
      region=st.selectbox("Región", ["Valparaíso","Metropolitana" ,"O’Higgins", "Maule"])
   if zona=='Sur':
      region=st.selectbox("Región", ["Ñuble", "Biobío", "La Araucanía", "Los Ríos","Los Lagos"])
   if zona=='Austral':
      region=st.selectbox("Región", ["Aysén", "Magallanes"])
with col2:
   html_table ="""
   <table class="editorDemoTable">
  <tbody>
    <tr>
      <td style="text-align: center; font-family: Arial;"><strong>% Cargos ADP Nombrados</strong></td>
      <td style="text-align: center; font-family: Arial;"><strong>% Seleccionados EEPP en Región de Residencia</strong></td>
      <td style="text-align: center; font-family: Arial;"><strong>% Seleccionados PCH en Región de Residencia</strong></td>
    </tr>
    <tr>
      <td style="text-align: center; font-family: Arial; font-size: 18px;"><span style="color: #999999;"><strong>+kpi1+</strong></span></td>
      <td style="text-align: center; font-family: Arial; font-size: 18px;"><span style="color: #999999;"><strong>40%</strong></span></td>
      <td style="text-align: center; font-family: Arial; font-size: 18px;"><span style="color: #999999;"><strong>90%</strong></span></td>
    </tr>
  </tbody>
</table>
<p><td style="text-align: center; font-family: Arial; font-size: 8px;"><span style="color: #999999;">Fecha Actualizacion: 30/09/2023</span></td>.</p>
   """
   components.html(html_table)
      
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
      st.image("imagenes/Fotos_Regiones/valparaiso_gr-740x540.jpg", caption='Ciudad de Valparaiso - Región de Valparaíso')
   if region=='Metropolitana':
      st.image("imagenes/Fotos_Regiones/Plaza_de_la_Constitución_Chile.jpg",caption='Plaza de la Constitución - Región Metropolitana')
   if region=='O’Higgins':
      st.image("imagenes/Fotos_Regiones/ohiggins.jpg",caption='Ciudad de Rancagua - Región del Libertador General Bernardo O’Higgins')
   if region=='Maule':
      st.image("imagenes/Fotos_Regiones/maule.jpg",caption='Parque Nacional Radal Siete Tazas - Región del Maule')
   # zona sur
   if region=='Ñuble':
      st.image("imagenes/Fotos_Regiones/ñuble.jpg",caption='Catedral de Chillan - Región de Ñuble')
   if region=='Biobío':
      st.image("imagenes/Fotos_Regiones/biobio.jpg",caption='Ciudad de Concepción - Región del Biobío')
   if region=='La Araucanía':
      st.image("imagenes/Fotos_Regiones/araucania.jpg",caption='Volcan Villarrica - Región de la Araucanía')
   if region=='Los Ríos':
      st.image("imagenes/Fotos_Regiones/800px-Valdivia_y_su_río.jpg",caption='Rio Calle Calle - Región de los Ríos')
   if region=='Los Lagos':
      st.image("imagenes/Fotos_Regiones/lagos.jpg",caption='Isla de Chiloé - Región de Los Lagos ')
   # zona Austral
   if region=='Aysén':
      st.image("imagenes/Fotos_Regiones/caleta_tortel_2012-10.jpg",caption='Caleta Tortel - Región de Aysén del General Carlos Ibáñez del Campo ')
   if region=='Magallanes':
      st.image("imagenes/Fotos_Regiones/torrespaine.jpg",caption='Torres del Paine - Región de Magallanes y de la Antártica Chilena')
