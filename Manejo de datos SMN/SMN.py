# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 10:33:38 2021
El programa carga un log de datos de la estacion del SMN.
Crea un nuevo dataframe limpiando las dobles columnas y las de sensores que no
estan instalados.
Guarda ese data frame como "corregido" y hace graficos de los principales 
parametros.

@author: NCLS
"""

import pandas as pd
import os
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib as plt
#--------------------------------------------------------------------

archivo = 'Bajada_15-6-2021.log'# nombre exacto del archivo a abrir

directorio = 'datos' #Nombre de la carpeta con los archivos que quiero abrir
nombre_carpeta_corregidos = 'Corregidos y graficas'
nombre_guardado = 'Corregido_'+ archivo #Nombre para guardar el archivo


print()
print('---------------------------------------')
print('---------------------------------------')
print('----Converter and Grafiqueitor 0.1-----')
print('---------------------------------------')
print('---------------------------------------')
print()
print(f'Archivo de entrada: "{archivo}"')
print()

#--------------------------------------------------------------------

#para hacer transparente el SO, uno nombre y carpeta:
fname = os.path.join(directorio,archivo)
df = pd.read_csv(fname, sep=",", error_bad_lines=False) #el archivete esta separado por ","

#--------------------------------------------------------------------
"""
Hago un nuevo dataframe para hacer algunos calculos y graficos
1- Convertir a numero lo necesario.
2- Corregir la velocidad Nudos a km/h

"""

dia = df['DATE']
horas = df['TIME']
dirVientoInst = df['WD_5s'].astype(float) # Dirección del viento instantánea (en grados respecto del Norte)
velVientoInst = df['WS_5s_KT'] # Velocidad del viento instantánea (en nudos)
velMax = df['WG_3s_KT'].astype(float) # Velocidad máxima de ráfaga en los últimos 3 segundos (en nudos)
temp = df['AT_5s_C'].astype(float) # Temperatura instantánea (ºC)
HumInst = df['RH_5s'].astype(float) # Humedad relativa instantánea (%)
presion = df['BP1_5s_Mb'] # Presión atmosférica instantánea (en miliBares)
radiacionSolar = df['SR1mW/m2'].astype(float) # Radiación solar instantánea (Watt / m2)
voltBat = df['V_DC'] # Voltaje de batería (en Volts)
dirVientoProm10 = df['dirwave10'].astype(float) # Dirección de viento promediada en los últimos 10 minutos (en grados respecto del Norte)
velVientoProm10 = df['spdwave10'].astype(float) # Velocidad de viento promediada en los últimos 10 minutos (en nudos)
dirRafagMax5 = df['dirwMax5'].astype(float) # Dirección de ráfaga de viento máxima en los últimos 5 min (en grados respecto del Norte)
velRafagaMax5 = df['SpdwMax5'].astype(float) #Velocidad de ráfaga de viento máxima en los últimos 5 min (en nudos)
puntoRocio = df['dewPoint'].astype(float) #Punto de rocío
tempMax5 = df['tempMax5'].astype(float) #Temperatura máxima en los últimos 5 minutos
tempMin5 = df['Tempmin5'].astype(float) # Temperatura mínima en los últimos 5 minutos
radSolMax5 = df['radMax5'].astype(float) #Radiación solar máxima en los últimos 5 minutos (Watt / m2)
radSolMin5 = df['radmin5'].astype(float) # Radiación solar mínima en los últimos 5 minutos (Watt / m2)

# corrijo los datos de presion, que son interpretados por pandas como 'objetos'.
presure = pd.to_numeric(presion, errors='coerce')

# corrijo los datos de Vel viento, que son interpretados por pandas como 'objetos'.
veloviento = pd.to_numeric(velVientoInst, errors='coerce')

veloviento = veloviento*1.852 # Nudos a Km/h

# Hago un DF uniendo los datos de la columna "dia" con los de la columna "horas".
df2 = pd.DataFrame({'DiayHora':(dia + ' ' + horas)}) 

# convierto la columna que cree a tipo datetime
dyh = pd.to_datetime(df2['DiayHora'], format='%y/%m/%d %H:%M:%S', errors = 'coerce') 

# hago un tercer data frame donde vuelco toda la informacion:
df3 = pd.DataFrame({'DiayHora':dyh, #dia y hora en una sola columna
                    'DirVientoInst':dirVientoInst,
                    'VelVientoInst':veloviento,
                    'VelMaxima':velMax,
                    'DirVientoProm10':dirVientoProm10,
                    'VelVientoProm10':velVientoProm10,
                    'DirRafagaMax5':dirRafagMax5,
                    'VelRafagaMax5':velRafagaMax5,
                    'TempInst':temp,
                    'TempMax5':tempMax5,
                    'TempMin5':tempMin5,                    
                    'HumedadInst':HumInst,
                    'PuntoDeRocio':puntoRocio,
                    'PresionInst':presure,
                    'RadSolarInst':radiacionSolar,
                    'RadSolarMax5':radSolMax5,
                    'RadSolarMin5':radSolMin5,
                    'VoltBat':voltBat,
                    })
#%%--------------------------------------------------------------------
"""
Manejo de archivos generados:
    Los datos los tengo en la carpeta "datos" dentro de ella creo una carpeta
    nueva que llamo con lo que indique en "nombre_carpeta_corregidos"
    El programa intenta crear la carpeta, si ya existe avisa por consola y continua.
    En esa carpeta guardo el data frame corregido y los graficos.
    
"""

os.chdir('datos')
try:
    os.mkdir(nombre_carpeta_corregidos)
    
except FileExistsError:
    print (f'Ya existe la carpeta: "{nombre_carpeta_corregidos}"')

os.chdir(nombre_carpeta_corregidos)

try:
    os.mkdir(archivo[0:len(archivo)-4])
    
except FileExistsError:
    print (f'Ya existe la carpeta: "{archivo[0:len(archivo)-4]}"')

os.chdir(archivo[0:len(archivo)-4])

df3.to_csv(nombre_guardado)

#df3.plot(x = 'DiayHora', y = 'VelVientoInst')
df3.plot(x = 'DiayHora', y = 'TempInst')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Temperatura Instantanea.png")
df3.plot(x = 'DiayHora', y = 'HumedadInst')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Humedad Instantanea.png")
df3.plot(x = 'DiayHora', y = 'PuntoDeRocio')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Punto de Rocio.png")
df3.plot(x = 'DiayHora', y = 'PresionInst')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Presion Instantanea.png")
df3.plot(x = 'DiayHora', y = 'RadSolarInst')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Radiacion Solar Instantanea.png")
df3.plot(x = 'DiayHora', y = 'VoltBat')
plt.pyplot.savefig(archivo[0:len(archivo)-4] + " " + "Voltaje Bateria.png")

"""
vuelvo los directorios necesarios para estar nuevamente trabajando en 
la carpeta original
"""
os.chdir('..')
os.chdir('..')
os.chdir('..')

#%%--------------------------------------------------------------------

