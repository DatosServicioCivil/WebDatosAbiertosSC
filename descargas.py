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

#-----inicio carga de datos------------------------------------------------
#st.cache(ttl=3*60*60, suppress_st_warning=True)
#def get_data_csv():
#    try:
#        Cargos = pd.read_csv('ADP/Cargos_ADP.csv', sep=";",encoding='latin1')
#        Publicaciones = pd.read_csv('ADP/Publicaciones_ADP.csv', sep=";", encoding='latin1')
#        return Cargos,Publicaciones
#    except Exception as e:
#        print(f"An error occurred: {e}")
#        return None
Cargos = pd.read_csv('ADP/Cargos_ADP.csv', sep=";",encoding='latin1')
Publicaciones = pd.read_csv('ADP/Publicaciones_ADP.csv', sep=";", encoding='latin1')
#-----fin carga de datos------------------------------------------------

#Cargos, Pubicaciones=get_data_csv()

st.markdown('# Descarga de Datasets y Reportes')
#st.markdown('## **EpiCenter for Disease Dynamics**') 
st.markdown('**Dirección Nacional del Servicio Civil**') 
#st.markdown("## Key COVID-19 Metrics")
st.markdown("El Servicio Civil pone a disposición una serie de reportes y datasets para descargar.")
st.markdown('Por información adicional contactanos a traves de nuestro sitio de *Atención Ciudadana y Contacto* (https://www.serviciocivil.cl/contacto)')

Tematica = st.radio('Selecciona una temática', ['ADP', 'Gestión de Persona en el Estado'],horizontal =True)
st.markdown("""---""")
if Tematica=='ADP':
  st.markdown('**Información de concursos de Alta Dirección Pública**')
  col1,col2,col3=st.columns(3,gap='small')
  with col1:
    st.write('**Cargos ADP**')
    st.markdown('Campos: IDcargo, RBD, Adscrito, Nivel, Ministerio, Servicio, Entidad, Cargo, Región')
    st.download_button(
          label='Descargar',
          data=Cargos,
          file_name='Cargos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col2:
    st.write('**Concursos ADP**')
    st.markdown('Campos: Nivel, Adscrito, Ministerio, Servicio, Cargo, Mes de convocatoria, Año de convocatoria, IdConcurso')
    st.download_button(
          label='Descargar',
          data=Publicaciones,
          file_name='Publicaciones_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col3:
    st.write('**Nóminas ADP**')
    st.markdown('Campos: Nivel, Adscrito, Ministerio, Servicio, Cargo, Mes envío nómina, Año envío nómina')
    st.download_button(
          label='Descargar',
          data='ADP/Nominas_ADP.csv',
          file_name='Nominas_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  
  col4,col5,col6=st.columns(3,gap='small')
  with col4:
    st.write('**Nombramientos ADP**')
    st.markdown('Campos Nivel, Adscrito, Ministerio, Servicio, Cargo, Fecha Nombramiento, Fecha Inicio de labor, IdConcurso, Sexo')
    st.download_button(
          label='Descargar',
          data='ADP/Nombramientos_ADP.csv',
          file_name='Nombramientos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col5:
    st.write('**Concursos desiertos**')
    st.markdown('Campos Adscrito, Nivel, N° Concurso, Ministerio, Servicio, Cargo, Fecha Convocatoria, Fecha Envío Nómina, Fecha Desierto, Tipo Desierto')
    st.download_button(
          label='Descargar',
          data='ADP/desiertos_ADP.csv',
          file_name='desiertos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col6:
    st.write('**Tiempos Concursos ADP**')
    st.markdown('Campos Año envío nómina, N° Concurso, Nivel, Adscrito, Ministerio, Servicio, Cargo, Fecha envío nómina, Fecha Convocatoria, días')
    st.download_button(
          label='Descargar',
          data='ADP/Tiempos_ADP.csv',
          file_name='Tiempos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
else:
   st.markdown('**Informe Trimestral Monitoreo de Resultados reportados referidos a Cumplimiento Norma Reclutamiento y Selección**')
   col7,col8=st.columns(2,gap='medium')
   with col7:
      st.write("Reporte de cumplimiento de norma de Reclutamieno y Selección - **I trimestre 2023**") 
      st.download_button(
          label='Descargar',
          data='GestionPersonas/1er-inf-trim-resultados-cumplimiento-norma-RyS_abril2023.pdf',
          file_name='1er-inf-trim-resultados-cumplimiento-norma-RyS_abril2023.pdf',
          mime='pdf'
          )
      st.write(':blue[Fecha de emisión abril 2023]')
   with col8:
      st.write("Reporte de cumplimiento de norma de Reclutamieno y Selección - **II trimestre 2023**") 
      st.download_button(
          label='Descargar',
          data='GestionPersonas/2do-inf-trim-resultados-cumplimiento-norma-RyS_julio2023 (1).pdf',
          file_name='2do-inf-trim-resultados-cumplimiento-norma-RyS_julio2023 (1).pdf',
          mime='pdf'
          )
      st.write(':blue[Fecha de emisión julio 2023]')
  #st.download_button('Download file', ADP/Nominas_ADP.csv)

