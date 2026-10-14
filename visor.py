import os
import streamlit as st
import mammoth

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CARVIMSA - PLANTA MOLINO",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURACIÓN DE LA CARPETA BASE ---
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
CARPETA_OFICIAL = os.path.join(CARPETA_ACTUAL, "oficial")

# --- ESTILOS CSS REFORZADOS ---
st.markdown("""
    <style>
    /* Fondo general azul oscuro de CARVIMSA */
    .stApp {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
    }
    /* Panel Lateral Izquierdo */
    [data-testid="stSidebar"] {
        background-color: #1b263b !important;
        border-right: 1px solid #415a77;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Estilo para los botones de la lista de archivos */
    .stButton > button {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1px solid #415a77 !important;
        text-align: left !important;
        display: block !important;
        width: 100% !important;
        padding: 10px !important;
        font-size: 13px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        border-radius: 6px !important;
    }
    .stButton > button:hover {
        border-color: #38bdf8 !important;
        background-color: #0f172a !important;
        color: #38bdf8 !important;
    }
    
    /* Banner Superior Azul */
    .banner-principal {
        background: linear-gradient(135deg, #0077b6, #0096c7);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Caja de la Vista Previa (Máxima legibilidad) */
    .contenedor-vista-previa {
        background-color: #ffffff !important;
        color: #1e293b !important;
        padding: 30px;
        border-radius: 10px;
        border: 3px solid #0077b6;
        min-height: 500px;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-top: 15px;
    }
    .contenedor-vista-previa h1, .contenedor-vista-previa h2, .contenedor-vista-previa h3 {
        color: #0f172a !important;
        border-bottom: 2px solid #cbd5e1;
        padding-bottom: 8px;
        margin-top: 15px;
    }
    .contenedor-vista-previa p, .contenedor-vista-previa li, .contenedor-vista-previa td, .contenedor-vista-previa tr {
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    .contenedor-vista-previa table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 15px;
    }
    .contenedor-vista-previa th, .contenedor-vista-previa td {
        border: 1px solid #cbd5e1;
        padding: 8px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAR EL ESTADO DE MEMORIA DE SELECCIÓN ---
if "archivo_activo" not in st.session_state:
    st.session_state.archivo_activo = None

# --- OBTENER TODOS LOS ARCHIVOS DISPONIBLES ---
archivos_disponibles = []
if os.path.exists(CARPETA_OFICIAL):
    try:
        todos_los_archivos = os.listdir(CARPETA_OFICIAL)
        archivos_disponibles = [f for f in todos_los_archivos if f.endswith('.docx') and not f.startswith('.') and not f.startswith('~$')]
        archivos_disponibles.sort()
        
        if archivos_disponibles and st.session_state.archivo_activo is None:
            st.session_state.archivo_activo = archivos_disponibles[0]
    except Exception as e:
        st.sidebar.error(f"Error al leer la carpeta oficial: {str(e)}")

# --- 1. PANEL LATERAL IZQUIERDO (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; margin-bottom:0;'>CARVIMSA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#94a3b8; text-align:center; margin-top:0;'>GRUPO COMECA - PERÚ</p>", unsafe_allow_html=True)
    st.write("---")
    
    buscar = st.text_input("🔍 Filtrar archivos de la lista:", placeholder="Escribe aquí para buscar...")
    st.write("---")
    
    if buscar:
        archivos_mostrar = [f for f in archivos_disponibles if buscar.strip().lower() in f.lower()]
    else:
        archivos_mostrar = archivos_disponibles

    st.markdown(f"### 📂 DOCUMENTOS ({len(archivos_mostrar)})")
    
    for f_name in archivos_mostrar:
        marca = "▶️ " if f_name == st.session_state.archivo_activo else "📄 "
        if st.button(f"{marca}{f_name}", key=f"btn_lista_{f_name}", use_container_width=True):
            st.session_state.archivo_activo = f_name
            st.rerun()

# --- 2. ÁREA PRINCIPAL (PANEL DE VISTA PREVIA) ---
st.markdown("""
    <div class="banner-principal">
        <span style="background-color:#ffffff; color:#0077b6; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:bold;">📌 CATÁLOGO DE PLANTA • VISTA PREVIA</span>
        <h1 style="color:white; margin-top:10px; margin-bottom:0; font-size:32px;">CARVIMSA - PLANTA MOLINO</h1>
        <p style="color:#e0e1dd; margin-top:5px; font-size:14px;">Consulta en tiempo real de documentos técnicos en pantalla.</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.archivo_activo and os.path.exists(os.path.join(CARPETA_OFICIAL, st.session_state.archivo_activo)):
    archivo_actual = st.session_state.archivo_activo
    ruta_completa = os.path.join(CARPETA_OFICIAL, archivo_actual)
    
    st.markdown(f"<h3 style='color: #38bdf8;'>👁️ Vista Previa Activa: <span style='color: white;'>{archivo_actual}</span></h3>", unsafe_allow_html=True)
    
    # --- PROCESAR E INCRUSTAR EL CONTENIDO EN LA CAJA BLANCA ---
    try:
        with open(ruta_completa, "rb") as docx_file:
            resultado = mammoth.convert_to_html(docx_file, ignore_empty_paragraphs=True)
            html_contenido = resultado.value
            
            # Formatear subniveles de listas conflictivas para que no reinicien a 1
            html_contenido = html_contenido.replace("<li>1. ", "<li style='list-style-type: none; margin-left: -15px;'>🔹 <b>")
            
            if not html_contenido.strip():
                html_contenido = "<p style='color: #64748b; font-style: italic;'>El documento seleccionado está vacío o no contiene texto legible.</p>"
            
            st.markdown(f"""
                <div class="contenedor-vista-previa">
                    {html_contenido}
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as err_lectura:
        st.error(f"No se pudo cargar la vista previa: {str(err_lectura)}")
else:
    if not archivos_disponibles:
        st.error(f"❌ No se detectan archivos de Word (.docx) en la carpeta 'oficial'.")
    else:
        st.info("👈 Selecciona un archivo de la lista lateral izquierda para ver su contenido.")