import pandas as pd

# 1. Cargar el archivo
df = pd.read_csv('datos_para_limpiar.csv')

# 2. Eliminar columnas innecesarias (ID y Notas)
df = df.drop(columns=['ID', 'Notas'], errors='ignore')

# 3. Normalizar nombres de columnas (minúsculas, sin espacios ni tildes)
df.columns = df.columns.str.lower().str.strip()
df.columns = df.columns.str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')
df.columns = df.columns.str.replace(' ', '_')

# 4. Limpiar nombres de las ciudades
df['ciudad'] = df['ciudad'].astype(str).str.lower().str.strip()
df['ciudad'] = df['ciudad'].replace('nan', pd.NA) # Convertir 'nan' de texto a NaN real
df['ciudad'] = df['ciudad'].replace({
    '.*bogot.*': 'bogota',
    '.*medell.*': 'medellin',
    '.*cali.*': 'cali'
}, regex=True)

# Normalizar también 'genero' para evitar conflictos con 'nan'
df['genero'] = df['genero'].astype(str).str.lower().str.strip()
df['genero'] = df['genero'].replace('nan', pd.NA)

# 5. Tratamiento de valores nulos
df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
# Media solo con edades válidas (0 a 120 años)
media_edad = df[(df['edad'] >= 0) & (df['edad'] <= 120)]['edad'].mean()
df['edad'] = df['edad'].fillna(media_edad)

df['salario'] = pd.to_numeric(df['salario'], errors='coerce')
df['salario'] = df['salario'].fillna(df['salario'].median())

df['ciudad'] = df['ciudad'].fillna(df['ciudad'].mode()[0])
df['genero'] = df['genero'].fillna(df['genero'].mode()[0])

# Tratamiento de nulos para ingresos y gastos (necesario para utilidad y escalado)
df['ingresos'] = pd.to_numeric(df['ingresos'], errors='coerce')
df['gastos'] = pd.to_numeric(df['gastos'], errors='coerce')

df['ingresos'] = df['ingresos'].fillna(df['ingresos'].median())
df['gastos'] = df['gastos'].fillna(df['gastos'].median())

# 6. Formato de fecha
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

# 7. Filtrar datos fuera de rango
df = df[(df['edad'] >= 0) & (df['edad'] <= 120)]
df = df[df['salario'] <= 1000000000]

# 8. Convertir nivel a números (bajo -> 1, medio -> 2, alto -> 3)
mapa_nivel = {'bajo': 1, 'medio': 2, 'alto': 3}
df['nivel'] = df['nivel'].astype(str).str.lower().str.strip().map(mapa_nivel)

# 12. Crear la columna utilidad (ingresos - gastos)
df['utilidad'] = df['ingresos'] - df['gastos']

# 10. Escalar edad e ingresos en un rango de 0 a 1 (forma manual con pandas)
df['edad'] = (df['edad'] - df['edad'].min()) / (df['edad'].max() - df['edad'].min())
df['ingresos'] = (df['ingresos'] - df['ingresos'].min()) / (df['ingresos'].max() - df['ingresos'].min())

# 9. Codificar genero y ciudad (get_dummies)
df = pd.get_dummies(df, columns=['genero', 'ciudad'], drop_first=True)

# 11. Eliminar filas duplicadas
df = df.drop_duplicates()

# 13. Guardar el archivo final
df.to_csv('datos_limpios.csv', index=False)
print("¡Limpieza finalizada con éxito y archivo guardado!")