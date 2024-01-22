import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import time
import plotly.express as px 
import plotly.graph_objects as go
from PIL import Image

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
st.title('Información Regional', anchor=None, help=None)
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
    
#https://framework.digital.gob.cl/colors.html
color_line='#2D717C'
color_bar='#6633CC'


# https://github.com/mydgd/snowflake-table-catalog/blob/main/snowflake-table-catalog.py

col1, col2, col3 = st.columns(spec=[0.2,0.5,0.3],gap='small')

df_kpi_region=pd.read_csv('kpi/indicadores_regionales.csv',sep=";")
# muestra kpi regionales
#-----------------------------------------------------------
kpi1=df_kpi_region[df_kpi_region.id=='t_2_100'].resultado.values[0]
kpi2=df_kpi_region[df_kpi_region.id=='t_1_100'].resultado.values[0]
kpi3=df_kpi_region[df_kpi_region.id=='t_5_100'].resultado.values[0]

# cambio formato de str a float
#-----------------------------------------------------------
kpi1 = kpi1.replace(',', '.')
kpi1 = float(kpi1)

kpi2 = kpi2.replace(',', '.')
kpi2 = float(kpi2)

kpi3 = kpi3.replace(',', '.')
kpi3 = float(kpi3)

# df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8') 

with col1:
   st.markdown("**Conoce la información del Servicio Civil por regiones**.")
   st.markdown("Selecciona zona y región")
   zona=st.selectbox("Zona", ["Todas","Norte", "Centro", "Sur", "Austral"])
   if zona=='Norte':
      region=st.selectbox("Región", ["Todas","Arica y Parinacota","Tarapacá", "Antofagasta", "Atacama", "Coquimbo"])
   elif zona=='Centro':
      region=st.selectbox("Región", ["Todas","Valparaíso","Metropolitana" ,"O'Higgins", "Maule"])
   elif zona=='Sur':
      region=st.selectbox("Región", ["Todas","Ñuble", "Biobío", "La Araucanía", "Los Ríos","Los Lagos"])
   elif zona=='Austral':
      region=st.selectbox("Región", ["Todas","Aysén", "Magallanes"])
   else:
       region=st.selectbox("Región", ["Todas","Arica y Parinacota","Tarapacá", "Antofagasta", "Atacama", "Coquimbo","Valparaíso","Metropolitana" ,"O'Higgins", "Maule","Ñuble", "Biobío", "La Araucanía", "Los Ríos","Los Lagos","Aysén", "Magallanes"])

with col2:
      col21,col22,col23=st.columns(spec=[1,1,1],gap='small')
      with col21:
         valor_col2=f"{kpi1:.2%}"
         st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
         st.markdown("<h3 style='text-align: center; color: grey;'>% Cargos ADP Nombrados</h3>", unsafe_allow_html=True)
      with col22:
         valor_col3=f"{kpi2:.2%}"
         st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
         st.markdown("<h3 style='text-align: center; color: grey;'>% Seleccionados EEPP en Región de Residencia</h3>", unsafe_allow_html=True)
      with col23:
         valor_col4=f"{kpi3:.2%}"
         st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
         st.markdown("<h3 style='text-align: center; color: grey;'>% Seleccionados PCH en Región de Residencia</h3>", unsafe_allow_html=True)
#   components.html(html_table)
      
with col3:
   # zona norte
   if region=='Arica y Parinacota':
      st.image("imagenes/Fotos_Regiones/Parinacota_volcano.jpg", caption='Volcán Parinacota y el Lago Chungará - Región de Arica y Parinacota',width=500)
   if region=='Tarapacá':
      st.image("imagenes/Fotos_Regiones/Iquique_night_skyline.jpg", caption='Ciudad de Iquique - Región de Tarapacá',width=500)
   if region=='Antofagasta':
      st.image("imagenes/Fotos_Regiones/Mano_del_desierto_07.jpg", caption='La Mano del Desierto - Región de Antofagasta',width=500)
   if region=='Atacama':
      st.image("imagenes/Fotos_Regiones/Desierto_florido.jpg", caption='Desierto florido - Región de Atacama',width=500)
   if region=='Coquimbo':
      st.image("imagenes/Fotos_Regiones/la-serena.jpg",caption='Faro de La Serena - Región de Coquimbo',width=500)
   # zona centro
   if region=='Valparaíso':
      st.image("imagenes/Fotos_Regiones/valparaiso_gr-740x540.jpg", caption='Ciudad de Valparaiso - Región de Valparaíso',width=500)
   if region=='Metropolitana':
      st.image("imagenes/Fotos_Regiones/Plaza_de_la_Constitución_Chile.jpg",caption='Plaza de la Constitución - Región Metropolitana',width=500)
   if region=="O'Higgins":
      st.image("imagenes/Fotos_Regiones/ohiggins.jpg",caption='Ciudad de Rancagua - Región del Libertador General Bernardo O’Higgins',width=500)
   if region=='Maule':
      st.image("imagenes/Fotos_Regiones/maule.jpg",caption='Parque Nacional Radal Siete Tazas - Región del Maule',width=500)
   # zona sur
   if region=='Ñuble':
      st.image("imagenes/Fotos_Regiones/ñuble.jpg",caption='Catedral de Chillan - Región de Ñuble',width=500)
   if region=='Biobío':
      st.image("imagenes/Fotos_Regiones/biobio.jpg",caption='Ciudad de Concepción - Región del Biobío',width=500)
   if region=='La Araucanía':
      st.image("imagenes/Fotos_Regiones/araucania.jpg",caption='Volcan Villarrica - Región de la Araucanía',width=500)
   if region=='Los Ríos':
      st.image("imagenes/Fotos_Regiones/800px-Valdivia_y_su_río.jpg",caption='Rio Calle Calle - Región de los Ríos',width=500)
   if region=='Los Lagos':
      st.image("imagenes/Fotos_Regiones/lagos.jpg",caption='Isla de Chiloé - Región de Los Lagos',width=500)
   # zona Austral
   if region=='Aysén':
      st.image("imagenes/Fotos_Regiones/caleta_tortel_2012-10.jpg",caption='Caleta Tortel - Región de Aysén del General Carlos Ibáñez del Campo',width=500)
   if region=='Magallanes':
      st.image("imagenes/Fotos_Regiones/torrespaine.jpg",caption='Torres del Paine - Región de Magallanes y de la Antártica Chilena',width=500)


all_region_values=pd.read_excel('Regiones/all_region_values.xlsx')
df_ind_eepp_residencia=pd.read_excel('Regiones/df_ind_region.xlsx')
df_ind_eepp_residencia=pd.merge(df_ind_eepp_residencia,all_region_values,how='left',left_on='id_region',right_on='ID_Region')

if region=='Todas':
   df_ind_eepp_residencia=df_ind_eepp_residencia
else:
   df_ind_eepp_residencia=df_ind_eepp_residencia[df_ind_eepp_residencia['Region_Homologada']==region]

graf1=px.line(df_ind_eepp_residencia, x="mes", y="resultado",title=f"Porcentaje de Seleccionados EEPP y PCH en Región de Residencia - {region}")
graf1.update_xaxes(title_text='Mes',tickmode='linear', dtick=1)
graf1.update_yaxes(title_text='Porcentaje')
graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
#labels={"Region_Homologada":"Región","Porcentaje":"Porcentaje","Tipo":"Tipo de Seleccionado"}

if region!='Todas':
   graf1.update_layout(legend_title_text='Región')
   st.plotly_chart(graf1,use_container_width=True)
else:
   st.text('Selecciona una región para ver el gráfico')