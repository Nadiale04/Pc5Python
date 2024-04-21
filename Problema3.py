import pandas as pd
df_reactiva = pd.read_excel("./data/reactiva.xlsx", header=1)
def limpiar_titulo(titulo):
    if isinstance(titulo, str):   # Verifica si el título es una cadena de texto
        titulo_limpio = titulo.replace(" ", "").lower()  # Elimina espacios y convierte a minúsculas
        # Remueve tildes
        caracteres_con_tilde = 'áéíóúüÁÉÍÓÚÜ'
        caracteres_sin_tilde = 'aeiouuAEIOUU'
        tabla = str.maketrans(caracteres_con_tilde, caracteres_sin_tilde)
        titulo_limpio = titulo_limpio.translate(tabla)
        return titulo_limpio
    else:
        return titulo

df_reactiva.columns = [limpiar_titulo(titulo) for titulo in df_reactiva.columns]

#Quitar duplicador
columnas_sin_duplicados = ~df_reactiva.columns.duplicated()
df_reactiva = df_reactiva.loc[:, columnas_sin_duplicados]

#Eliminar comas de DispositivoLegal
df_reactiva['dispositivo_2'] = df_reactiva['dispositivo_2'].str.replace(',', '')

#Aplicar API
import requests
url="https://api.apis.net.pe/v1/tipo-cambio-sunat"
response=requests.get(url)
data = response.json()
dolar_compra = data['compra']

#Creación de las columnas en dólares
df_reactiva['montoinversiondolares']=df_reactiva.montodeinversion*dolar_compra
df_reactiva['montotransferenciadolares']=df_reactiva.montodetransferencia2020*dolar_compra

#Para la columna “Estado” cambie los valores
def d_estado (estadossp):
    if estadossp=='Actos Previos':
        return 'Actos Previos'
    elif estadossp=='Convenio y/o Contrato Resuelto, ':
        return 'Resuelto'
    elif estadossp=='En Ejecución':
        return 'Ejecucion'
    elif estadossp=='Concluido':
        return 'Concluido'
    else:
        return None
df_reactiva['estadossp'] = df_reactiva['estadossp'].apply(d_estado)

#Cree una nueva columna que puntue el estado
def puntuar (estadossp):
    if estadossp=='Actos Previos':
        return 1
    elif estadossp=='Resuelto':
        return 0
    elif estadossp=='Ejecucion':
        return 2
    elif estadossp=='Concluido':
        return 3
    else:
        return None
df_reactiva['puntuacion']=df_reactiva['estadossp'].apply(puntuar)

# Guardar en un nuevo archivo Excel
df_reactiva.to_excel('ReactivaNuevo.xlsx', index=False)


##GENERAR REPORTES##

#Reporte1
reporte1 = df_reactiva[['ubigeo','region','provincia','distrito']].drop_duplicates(subset=['ubigeo','region','provincia','distrito'])
reporte1.to_excel('ReporteLocación.xlsx', index=False)

#Reporte2
filtro = df_reactiva[(df_reactiva['ambito'] == 'URBANO') & (df_reactiva['puntuacion'].isin([1, 2, 3]))]
for region, grupo in filtro.groupby('region'):
    top5 = grupo.sort_values(by='montodeinversion', ascending=False).head(5)
    if not top5.empty:
        top5.to_excel(f'./ReportesRegion/Costo_inversion_{region}.xlsx', index=False)