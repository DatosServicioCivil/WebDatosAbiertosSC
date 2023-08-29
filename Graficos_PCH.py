import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

df_postulaciones=pd.read_csv('PCH/postulaciones_x_año.csv',encoding='utf-8')    
df_convocatorias=pd.read_csv('PCH/Convocatorias_x_año.csv')
df_seleccionados=pd.read_csv('PCH/Seleccionado_x_año.csv',sep=";",encoding='utf-8')

date='31 de Marzo de 2023'

st.title('Estadísticas Portal Prácticas Chile')
st.subheader(date)

# define si se ven los ejes Y
visible_y_axis=True
color_line='#216d41'
color_bar='#802dcb'
#----------------------------------------------------------------------------------------------------------------------------
# grafico Evolución de Postulaciones por Año
graf1=px.line(df_postulaciones,x='año',y='Postulaciones',title='<b>Evolución de postulaciones por año</b>').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
#----------------------------------------------------------------------------------------------------------------------------

# grafico Convocatorias por Año
graf2=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
#----------------------------------------------------------------------------------------------------------------------------
# grafico Seleccionados por Año
# Create the line plot
graf3 = px.line(df_seleccionados, x='year', y='Seleccionados ', title='<b>Evolución de cantidad estudiantes seleccionados/as por año</b>')\
    .update_yaxes(visible=visible_y_axis, title_text=None)\
    .update_xaxes(title_text=None)

graf3.update_traces(mode='lines+markers', marker=dict(size=8), line_shape='spline', line_color=color_line)
#----------------------------------------------------------------------------------------------------------------------------


col1,col2=st.columns(2,gap='small')
with col1:
    st.plotly_chart(graf1,use_container_width=True)
with col2:
    st.plotly_chart(graf2,use_container_width=True)


col3, col4=st.columns(2,gap='small')
with col3:
        st.plotly_chart(graf3,use_container_width=True)
with col4:
        st.text('Prácticas Chile es un programa gestionado por el Servicio Civil, \nque busca promover y atraer talento joven al Estado, y que permite a estudiantes de carreras \nuniversitarias y técnicas realizar sus prácticas en ministerios y servicios públicos, poniendo al servicio del país sus conocimientos y habilidades.')
