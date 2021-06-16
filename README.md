# SMN
Manejo de datos de la estación meteorológica

El programa `SMN.py` trabaja con datos de la estacion meteorologica del SMN (Coastal/Zeno...).
La estacion entrega por puerto serie un dato cada 5 minutos. Por ejemplo:

DATE,TIME,WD_5s,WS_5s_KT,WG_3s_KT,AT_5s_C,RH_5s,BP1_5s_Mb,BP2_5s_Mb,BP3_5s_Mb,PP_24h_Mm,PP_30s_Mm,SR1mW/m2,BIT,WS_STAT,V_DC,dirwave10,spdwave10,dirwMax5,SpdwMax5,BP1_5s_Mb,PP_30s_Mm,Pp3hs,AT_5s_C,dewPoint,tempMax5,Tempmin5,SR1mW/m2,radMax5,radmin5,V_DC,
19/03/09,03:19:56,0,///,0.0,3.3,56,758.7,758.7,758.7,0.000,0.000,-3,8,///,11.9,0,0.0,0,0.0,758.7,0.000,0.000,3.3,-4.5,3.5,3.3,-3,-2,-3,11.9,

Esa lista de datos contiene varios inconvenientes:
- datos repetidos
- datos de sensores que no estan instalados
- complejidad para entender el encabezado de los datos

Para facilitar el manejo de los datos se desarrolló un programa en lenguaje Python que realiza diversas tareas sobre los datos:

- abre los datos bajados de la estación
- acomoda las columnas segun el tipo de dato (temperatura, viento, presion, etc)
- convierte los datos de velocidad de viento (nudos a km/h)
- elimina las columnas que contienen informacion de sensores no instalados
- elimina columnas duplicadas
- Unifica las columnas de Fecha y Hora y las convierte en un dato del tipo `datetime`
- Guarda en un nuevo archivo todas la modificaciones sobre los datos originales
- Grafica los datos principales `Humedad, Temperatura, Radiacion Solar, Punto de Rocio, Presion y Voltaje de alimentacion` (por el momento NO funcionan los sensores realcionados con el viento)
- Crea una carpeta donde guarda los datos corregidos y las graficas 

Es necsario que el archivo de trabajo contenga solamente el encabezado y los datos. Procurar "limpiar" datos generados durante la bajada de los mismos, por ejemplo lineas descargadas de los menu de la estacion, lineas agregadas por el "terminal", etc.
