import pandas as pd
df_reactiva = pd.read_excel("./data/reactiva.xlsx")
#Genere una función de limpieza que permita el renombre de las columnas
#eliminando espacios, tildes y convirtiendo los nombres de columna a minúscula.
#De ser necesario cambie el nombre de columna a uno que le sea de más ayuda.
def f_limpieza(df_reactiva):