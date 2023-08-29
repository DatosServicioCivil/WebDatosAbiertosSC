import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8')    
df_postulaciones_sexo=pd.read_csv('EEPP/porcentaje_postulaciones_sexo_e.csv',sep=";")
df_postulaciones_promedio=pd.read_csv('EEPP/Postulacion_Promedio_x_Año.csv')
df_convocatorias=pd.read_csv('EEPP/Convocatorias_x_año.csv')
df_vacantes=pd.read_csv('EEPP/Vacantes.csv')
df_ConvEnLinea=pd.read_csv('EEPP/ConvEnLineaxAño.csv',sep=";")

date='31 de Marzo de 2023'

st.title('Estadísticas Portal Empleos Públicos')
st.subheader(date)

# define si se ven los ejes Y
visible_y_axis=True
color_line='#216d41'
color_bar='#802dcb'
#----------------------------------------------------------------------------------------------------------------------------
# grafico Evolución de Postulaciones por Año
graf1=px.line(df_postulaciones,x='año',y='postulaciones',title='<b>Evolución de postulaciones por año</b>').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
#----------------------------------------------------------------------------------------------------------------------------
#grafico 2: Distribución de Postulaciones por Sexo
# Create separate DataFrames for "Mujeres" and "Hombres"
df_mujeres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Mujeres']
df_hombres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Hombres']

# Asignar colores de acuerdo a una paleta de colores a cada sexo
sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue'}  # Mapeo de colores por sexo


# Create the line plot using Plotly Express
graf2 = px.line(
    title='<b>Evolución de postulaciones por año y sexo</b>',
    labels={'year': 'Año', 'Porcentaje': 'Porcentaje'},  # Customize axis labels
)

# Cambiar el formato del eje y a porcentaje (0.1 se mostrará como 10%)
graf2.update_layout(yaxis_tickformat='.2%')

# Add lines for "Mujeres" and "Hombres"
graf2.add_trace(
    go.Scatter(x=df_mujeres['year'], y=df_mujeres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Mujeres',line_color=sexo_color_map['Mujeres'])
)
graf2.add_trace(go.Scatter(x=df_hombres['year'], y=df_hombres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Hombres',line_color=sexo_color_map['Hombres']))

#----------------------------------------------------------------------------------------------------------------------------
# grafico Postulación Promedio por Año
graf3=px.line(df_postulaciones_promedio,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
#----------------------------------------------------------------------------------------------------------------------------
# grafico Convocatorias por Año
graf4=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
#----------------------------------------------------------------------------------------------------------------------------
# grafico Vacantes Concursadas por Año
graf5=px.bar(df_vacantes,x='Año',y='Vacantes',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)
#----------------------------------------------------------------------------------------------------------------------------
# grafico Porcentaje de Convocatorias en Linea por Año
graf6=px.line(df_ConvEnLinea,x='year',y='Porcentaje Convocatorias Postulacion en Linea',title='<b>Evolución de convocatorias en línea por año</b>').\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                update_xaxes(title_text=None)

graf6.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_bar)
#----------------------------------------------------------------------------------------------------------------------------



col1,col2,col3=st.columns(3,gap='small')
with col1:
    st.plotly_chart(graf1,use_container_width=True)
with col2:
    st.plotly_chart(graf2,use_container_width=True)
with col3:
    st.plotly_chart(graf4,use_container_width=True)


col4, col5, col6=st.columns(3,gap='small')
with col4:
        st.plotly_chart(graf3,use_container_width=True)
with col5:
        st.plotly_chart(graf5,use_container_width=True)
with col6:
        st.plotly_chart(graf6,use_container_width=True)
