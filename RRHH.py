import streamlit as st
import pandas as pd
import requests
import io
import openpyxl

# Cargar datos de empleados desde el archivo Excel
file_path = "BASE_DE_DATOS_EMPLEADOS_ANALISIS_RRHH_DASHBOARD.xlsx"
employee_data = pd.read_excel(file_path, sheet_name=0)

# Generar URLs de fotos de perfil usando la API Random User
def generate_profile_pictures(num):
    response = requests.get(f"https://randomuser.me/api/?results={num}")
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [user["picture"]["large"] for user in results]
    return ["https://via.placeholder.com/150"] * num

# Agregar columna de fotos de perfil y URL de foto
num_employees = len(employee_data)
profile_pictures = generate_profile_pictures(num_employees)
employee_data["Foto de Perfil"] = profile_pictures
employee_data["URL de Foto"] = profile_pictures  # Se agrega como columna separada

# Configuración de la página
st.set_page_config(page_title="Base de Datos de Empleados", layout="wide")

# Título principal
st.title("📊 Base de Datos de Análisis de Empleados RRHH 👥")


# Función para mostrar la tabla con imágenes en Streamlit
def render_table_with_images(df):
    styled_table = df.copy()
    styled_table["Foto de Perfil"] = styled_table["Foto de Perfil"].apply(
        lambda url: f'<img src="{url}" style="height:80px;">'
    )
    return styled_table.to_html(escape=False, index=False)

# Mostrar la tabla completa con el texto personalizado en amarillo
st.markdown('<p style="color: yellow; font-size: 18px;">💡 Creado por Ingeniero Juancito Peña 👨‍💻</p>', unsafe_allow_html=True)
st.markdown(render_table_with_images(employee_data), unsafe_allow_html=True)

# Mostrar la tabla completa con el texto normal
st.subheader("Información de Empleados")
st.markdown(render_table_with_images(employee_data), unsafe_allow_html=True)

# Funciones para exportar datos
def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def convert_to_json(df):
    return df.to_json(orient="records", indent=4).encode('utf-8')

def convert_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Empleados")
    return output.getvalue()

# Barra lateral con botones para exportar
st.sidebar.title("Exportar Datos")
st.sidebar.download_button(
    label="Descargar en CSV",
    data=convert_to_csv(employee_data),
    file_name="empleados.csv",
    mime="text/csv"
)
st.sidebar.download_button(
    label="Descargar en JSON",
    data=convert_to_json(employee_data),
    file_name="empleados.json",
    mime="application/json"
)
st.sidebar.download_button(
    label="Descargar en Excel",
    data=convert_to_excel(employee_data),
    file_name="empleados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
