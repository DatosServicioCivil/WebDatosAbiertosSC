import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.style as style
from datetime import date

st.set_page_config(layout='wide')

today = date.today()
#sns.set_style('whitegrid')
style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1
dpi = 1000
plt.rcParams['font.size'] = 13
#plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
plt.rcParams['figure.figsize'] = 8, 8



st.markdown('# Descarga de Datasets y Reportes')
#st.markdown('## **EpiCenter for Disease Dynamics**') 
st.markdown('**Dirección Nacional del Servicio Civil**') 
#st.markdown("## Key COVID-19 Metrics")
st.markdown("El Servicio Civil pone a disposición una serie de reportes y datasets para descargar.")
st.markdown('Por información adicional contactanos a traves de nuestro sitio de *Atención Ciudadana y Contacto* (https://www.serviciocivil.cl/contacto)')

Tematica = st.radio('Selecciona una temática', ['ADP', 'Gestión de Persona en el Estado'],horizontal =True)

if Tematica=='ADP':
  col1,col2,col3=st.columns(3,gap='small')
  with col1:
    st.text('Cargos ADP')
    st.download_button(
          label='Descargar',
          data='ADP/Cargos_ADP.csv',
          file_name='Cargos_ADP.csv',
          mime='text/csv'
          )
  with col2:
    st.text('Concursos ADP')
    st.download_button(
          label='Descargar',
          data='ADP/Publicaciones_ADP.csv',
          file_name='Publicaciones_ADP.csv',
          mime='text/csv'
          )
  with col3:
    st.text('Nóminas ADP')
    st.download_button(
          label='Descargar',
          data='ADP/Nominas_ADP.csv',
          file_name='Nominas_ADP.csv',
          mime='text/csv'
          )
  
  col4,col5,col6=st.columns(3,gap='small')
  with col4:
    st.text('Nombramientos ADP')
    st.download_button(
          label='Descargar',
          data='ADP/Nombramientos_ADP.csv',
          file_name='Nombramientos_ADP.csv',
          mime='text/csv'
          )
  with col5:
    st.text('Concursos desiertos')
    st.download_button(
          label='Descargar',
          data='ADP/desiertos_ADP.csv',
          file_name='desiertos_ADP.csv',
          mime='text/csv'
          )
  with col6:
    st.text('Tiempos Concursos ADP')
    st.download_button(
          label='Descargar',
          data='ADP/Tiempos_ADP.csv',
          file_name='Tiempos_ADP.csv',
          mime='text/csv'
          )
else:
   col7,col8=st.columns(2,gap='medium')
   with col7:
      st.text('Reporte de cumplimiento de norma de Reclutamieno y Selección - I trimestre 2023')
      st.download_button(
          label='Descargar',
          data='GestionPersonas/1er-inf-trim-resultados-cumplimiento-norma-RyS_abril2023.pdf',
          file_name='1er-inf-trim-resultados-cumplimiento-norma-RyS_abril2023.pdf',
          mime='pdf'
          )
   with col8:
      st.text('Reporte de cumplimiento de norma de Reclutamieno y Selección - II trimestre 2023')
      st.download_button(
          label='Descargar',
          data='GestionPersonas/2do-inf-trim-resultados-cumplimiento-norma-RyS_julio2023 (1).pdf',
          file_name='2do-inf-trim-resultados-cumplimiento-norma-RyS_julio2023 (1).pdf',
          mime='pdf'
          )
  #st.download_button('Download file', ADP/Nominas_ADP.csv)

