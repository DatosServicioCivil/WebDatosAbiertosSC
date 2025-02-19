import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.style as style
from datetime import date
from PIL import Image

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

def generate_file_content(df):
    # Generate the file content (e.g., CSV, JSON, etc.)
    # In this example, we'll generate a CSV file
    csv_content = df.to_csv(index=False)
    return csv_content


#-----inicio carga de datos------------------------------------------------
st.cache(ttl=3*60*60, suppress_st_warning=True)
def get_data_csv():
    try:
        Cargos = pd.read_csv('ADP/Cargos_ADP.csv', sep=";",encoding='latin1')
        Publicaciones = pd.read_csv('ADP/Publicaciones_ADP.csv', sep=";", encoding='latin1')
        Nominas = pd.read_csv('ADP/Nominas_ADP.csv', sep=";", encoding='latin1')
        Nombramientos = pd.read_csv('ADP/Nombramientos_ADP.csv', sep=";", encoding='latin1')
        Desiertos = pd.read_csv('ADP/desiertos_ADP.csv', sep=";", encoding='latin1')
        Tiempos = pd.read_csv('ADP/Tiempos_ADP.csv', sep=";", encoding='latin1')
        return Cargos,Publicaciones,Nominas,Nombramientos,Desiertos,Tiempos
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@st.cache_data()
def egresos_adp():
        df_1=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf I Nivel Datastudio')
        df_2=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf II Nivel Datastudio')
        df_1_2=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf I y II Nivel Datastudio')
        df_egresos_adp=pd.concat([df_1,df_2,df_1_2])
        return df_egresos_adp

df_egresos_adp=egresos_adp()


#-----fin carga de datos------------------------------------------------

Cargos, Publicaciones ,Nominas,Nombramientos,Desiertos,Tiempos=get_data_csv()

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)

# Set Page Header
st.title('Descarga de Datasets y Reportes', anchor=None, help=None)
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

# Set Page Header
#st.header('# Descarga de Datasets y Reportes')




st.markdown("El Servicio Civil pone a disposición una serie de reportes y datasets para descargar.")
st.markdown('Por información adicional contactanos a traves de nuestro sitio de *Atención Ciudadana y Contacto* (https://www.serviciocivil.cl/contacto)')

Tematica = st.radio('Selecciona una temática', ['ADP', 'Gestión de Persona en el Estado'],horizontal =True)
#st.markdown("""---""")
if Tematica=='ADP':
  st.markdown('**Información de concursos de Alta Dirección Pública**')
  col1,col2,col3=st.columns(3,gap='small')
  with col1:
    st.write('**Cargos ADP**')
    st.markdown('Campos: IDcargo, RBD, Adscrito, Nivel, Ministerio, Servicio, Entidad, Cargo, Región')
    file_content = generate_file_content(Cargos)
    st.download_button(
          label='Descargar',
          data=file_content,
          file_name='Cargos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col2:
    st.write('**Concursos ADP**')
    st.markdown('Campos: Nivel, Adscrito, Ministerio, Servicio, Cargo, Mes de convocatoria, Año de convocatoria, IdConcurso')
    file_content = generate_file_content(Publicaciones)
    st.download_button(
        label='Descargar',
        data=file_content,
        file_name='data.csv',
        mime='text/csv'
        )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col3:
    st.write('**Nóminas ADP**')
    st.markdown('Campos: Nivel, Adscrito, Ministerio, Servicio, Cargo, Mes envío nómina, Año envío nómina')
    file_content = generate_file_content(Nominas)
    st.download_button(
          label='Descargar',
          data=file_content,
          file_name='Nominas_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  
  col4,col5,col6=st.columns(3,gap='small')
  with col4:
    st.write('**Nombramientos ADP**')
    st.markdown('Campos Nivel, Adscrito, Ministerio, Servicio, Cargo, Fecha Nombramiento, Fecha Inicio de labor, IdConcurso, Sexo')
    file_content = generate_file_content(Nombramientos)
    st.download_button(
          label='Descargar',
          data=file_content,
          file_name='Nombramientos_ADP.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col5:
    columnas_df_egresos=['Gobierno','Año','Semana','Motivo','Cargos','Egresos','% Egreso Acumulado','Nivel']
    st.write('**Egresos ADP**')
    st.markdown('Gobierno,Año,Seman,Motivo,Cargos,Egresos,% Egreso Acumulado,Nivel')
    file_content = generate_file_content(df_egresos_adp[columnas_df_egresos])
    st.download_button(
          label='Descargar',
          data=file_content,
          file_name='df_egresos_adp.csv',
          mime='text/csv'
          )
    st.write(':blue[Fecha de actualización agosto 2023]')
  with col6:
    st.write('**Tiempos Concursos ADP**')
    st.markdown('Campos Año envío nómina, N° Concurso, Nivel, Adscrito, Ministerio, Servicio, Cargo, Fecha envío nómina, Fecha Convocatoria, días')
    file_content = generate_file_content(Tiempos)
    st.download_button(
          label='Descargar',
          data=file_content,
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
          file_name='2do-inf-trim-resultados-cumplimiento-norma-RyS_julio2023.pdf',
          mime='pdf'
          )
      st.write(':blue[Fecha de emisión julio 2023]')
    
   col9,col10=st.columns(2,gap='medium')
   with col7:
      st.write("Reporte de cumplimiento de norma de Reclutamieno y Selección - **III trimestre 2023**") 
      st.download_button(
      label='Descargar',
            data='GestionPersonas/3er inf trim resultados cumplimiento norma RyS_octubre2023.pdf',
            file_name='3er-inf-trim-resultados-cumplimiento-norma-RyS_sept2023.pdf',
            mime='pdf'
            )
      st.write(':blue[Fecha de emisión septiembre 2023]')
   with col8:
      st.write("Reporte de cumplimiento de norma de Reclutamieno y Selección - **IV trimestre 2023**") 
      st.download_button(
            label='Descargar',
            data='GestionPersonas/4to inf trim resultados cumplimiento norma RyS_diciembre2023.pdf',
            file_name='4to-inf-trim-resultados-cumplimiento-norma-RyS_dic2023.pdf',
            mime='pdf'
            )
      st.write(':blue[Fecha de emisión diciembre 2023]')
  #st.download_button('Download file', ADP/Nominas_ADP.csv)

