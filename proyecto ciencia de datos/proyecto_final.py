import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Cargar y preparar datos
df = pd.read_excel("WHO_GHO_NUTRITION_ANAEMIA_PREGNANT_PREV jueves.xlsx")
df = df[['REF_AREA_LABEL', 'TIME_PERIOD', 'OBS_VALUE']]
df = df.rename(columns={'REF_AREA_LABEL': 'Pais', 'TIME_PERIOD': 'Anio', 'OBS_VALUE': 'Prevalencia'})

# Lista de países de América Latina
paises_latam = [
    'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Ecuador',
    'El Salvador', 'Guatemala', 'Honduras', 'Nicaragua', 'Panamá', 'Paraguay',
    'Perú', 'Uruguay', 'Venezuela, RB'
]

# Filtrar países LATAM y agrupar correctamente (eliminar duplicados por promedio)
df_latam = df[df['Pais'].isin(paises_latam)]
df_latam = df_latam.groupby(['Pais', 'Anio'])['Prevalencia'].mean().reset_index()

# Asegurar que los datos están ordenados antes de graficar
df_latam = df_latam.sort_values(by=['Pais', 'Anio'])

df_latam = df[df['Pais'].isin(paises_latam)]

# Pre-calcular promedio para opción 3
promedio_por_pais = df_latam.groupby('Pais')['Prevalencia'].mean().sort_values(ascending=False)

# Pre-calcular pivot para heatmap opción 4
pivot = df_latam.pivot_table(index='Pais', columns='Anio', values='Prevalencia')

def mostrar_tendencia():
    tendencia_pais = df_latam.groupby(['Pais', 'Anio'])['Prevalencia'].mean().reset_index()
    tendencia_pais = tendencia_pais.sort_values(by=['Pais', 'Anio'])  # CORREGIDO

    paises_unicos = tendencia_pais['Pais'].unique()
    palette = sns.color_palette("tab20", n_colors=len(paises_unicos))

    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=tendencia_pais,
        x='Anio',
        y='Prevalencia',
        hue='Pais',
        palette=palette,
        marker="o"
    )
    plt.title('Tendencia de Anemia en Mujeres Embarazadas por País (2000–2019)')
    plt.ylabel('Prevalencia (%)')
    plt.xlabel('Año')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='País')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def mostrar_regresion_pais():
    print("Selecciona un país para ver su gráfica de regresión lineal:")
    for i, pais in enumerate(paises_latam):
        print(f"{i + 1} - {pais}")

    try:
        seleccion = int(input("Escribe el número del país: "))
        if seleccion < 1 or seleccion > len(paises_latam):
            print("Número fuera de rango.")
            return
        pais_input = paises_latam[seleccion - 1]
    except ValueError:
        print("Entrada no válida. Debes escribir un número.")
        return

    data_pais = df_latam[df_latam['Pais'] == pais_input].dropna().sort_values('Anio')

    if len(data_pais) < 10:
        print(f"No hay suficientes datos para hacer regresión en {pais_input}.")
        return

    X = data_pais[['Anio']]
    y = data_pais['Prevalencia']

    modelo = LinearRegression()
    modelo.fit(X, y)
    predicciones = modelo.predict(X)

    plt.figure(figsize=(8, 5))
    plt.plot(X, y, label="Datos reales", marker='o')
    plt.plot(X, predicciones, label="Predicción", linestyle='--')
    plt.title(f"Regresión Lineal - {pais_input}")
    plt.xlabel("Año")
    plt.ylabel("Prevalencia (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def mostrar_promedio():
    print("\nPromedio de Prevalencia (2000–2019):")
    print(promedio_por_pais)
    plt.figure(figsize=(10, 6))
    promedio_por_pais.plot(kind='bar', color='skyblue')
    plt.title('Promedio de Prevalencia de Anemia (2000–2019)')
    plt.ylabel('Prevalencia promedio (%)')
    plt.xlabel('País')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def mostrar_heatmap():
    pivot_ordenado = pivot[sorted(pivot.columns)]  # CORREGIDO

    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot_ordenado, cmap='Reds', linewidths=0.5, linecolor='gray')
    plt.title('Mapa de Calor: Prevalencia de Anemia por País y Año')
    plt.ylabel('País')
    plt.xlabel('Año')
    plt.tight_layout()
    plt.show()

print("¡Hola! Bienvenido al análisis de anemia en América Latina.")
while True:
    print("\nMenú de opciones:")
    print("1 - Mostrar tendencia de anemia (gráfico de líneas por país)")
    print("2 - Mostrar regresión lineal de un país específico")
    print("3 - Mostrar promedio de prevalencia por país (gráfico de barras)")
    print("4 - Mostrar mapa de calor de prevalencia por país y año")
    print("0 - Salir")

    opcion = input("Elige una opción: ").strip()

    if opcion == '1':
        mostrar_tendencia()
    elif opcion == '2':
        mostrar_regresion_pais()
    elif opcion == '3':
        mostrar_promedio()
    elif opcion == '4':
        mostrar_heatmap()
    elif opcion == '0':
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")
