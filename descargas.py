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
