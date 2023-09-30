import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px 
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(layout='wide')

st.title('Información Regional', anchor=None, help=None)

col1, col2, col3 = st.columns(spec=[0.2,0.6,0.2],gap='small')

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
   html_table = """
   <table class=MsoTableGrid border=0 cellspacing=0 cellpadding=0
 style='border-collapse:collapse;border:none;mso-yfti-tbllook:1184;mso-padding-alt:
 0cm 5.4pt 0cm 5.4pt;mso-border-insideh:none;mso-border-insidev:none'>
 <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes'>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>Valor KPI1<o:p></o:p></span></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>Valor KPI2<o:p></o:p></span></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>Valor KPI3<o:p></o:p></span></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>Valor KPI4<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style='mso-yfti-irow:1;mso-yfti-lastrow:yes'>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><b><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>% mujeres nombradas en cargos ADP<o:p></o:p></span></b></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><b><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>% postulaciones de mujeres<o:p></o:p></span></b></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><b><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>% mujeres seleccionadas en EEPP<o:p></o:p></span></b></p>
  </td>
  <td width=147 valign=top style='width:110.35pt;padding:0cm 5.4pt 0cm 5.4pt'>
  <p class=MsoNormal><b><span style='font-size:14.0pt;font-family:"Arial",sans-serif;
  color:#7F7F7F;mso-themecolor:background1;mso-themeshade:128;mso-style-textfill-fill-color:
  #7F7F7F;mso-style-textfill-fill-themecolor:background1;mso-style-textfill-fill-alpha:
  100.0%;mso-style-textfill-fill-colortransforms:lumm=50000'>Texto KPI4<o:p></o:p></span></b></p>
  </td>
 </tr>
</table>






"""
# <div class="KPI regionales">
#        <div class="statistic">
#            <div class="value">41%</div>
#            <div class="label">% mujeres nombradas en cargos ADP</div>
#        </div>
#        <div class="statistic">
#            <div class="value">47%</div>
#            <div class="label">% postulaciones de mujeres</div>
#        </div>
#        <div class="statistic">
#            <div class="value">35%</div>
#            <div class="label">% mujeres seleccionadas en EEPP</div>
#        </div>
#        <div class="statistic">
#            <div class="value">47%</div>
#            <div class="label">% postulaciones de mujeres</div>
#        </div>
#        <div class="statistic">
#            <div class="value">55%</div>
#            <div class="label">% mujeres nombradas en cargos de directores/as de Escuelas</div>
#        </div>
#    </div>

   
   components.html(html_table)

   # st.markdown("*Principales indicadores regionales*.")
   # col_2_1,col_2_2,col_2_3,col_2_4=st.columns(4)
   # with col_2_1:
   #    st.markdown('Porcentaje de mujeres nombradas en cargos directivos del Sistema ADP')
   # with col_2_2:
   #    st.markdown('Porcentaje de postulaciones de mujeres')
   # with col_2_3:
   #    st.markdown('Porcentaje de mujeres seleccionadas en EEPP')
   # with col_2_4:
   #    st.markdown('Porcentaje de mujeres nombradas en cargos de directores/as de Escuelas')
      
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
