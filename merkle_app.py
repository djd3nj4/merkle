import streamlit as st
import google.generativeai as generative_ai
import re  # Importamos regex para extraer el código SQL correctamente

# Configuración de la barra lateral con descripción de la app
st.sidebar.title("Acerca de esta App")
st.sidebar.markdown("""
👋 **Bienvenido al Generador de Código SQL con Gemini**  
Esta aplicación usa la inteligencia artificial de Google Gemini para generar código SQL a partir de una descripción de una base de datos y un problema específico.  

**¿Cómo usarla?**  
1. Ingresa tu API Key de Google Gemini.  
2. Describe tu base de datos.  
3. Explica qué consulta SQL necesitas.  
4. Haz clic en **"Generar código SQL"** y obtendrás el código con una explicación.  
""")

# Entrada para la API Key del usuario
CLAVE_DE_API = st.text_input("🔑 Ingresa tu API Key de Gemini:", type="password")

if not CLAVE_DE_API:
    st.warning("⚠️ Ingresa tu API Key para continuar.")
else:
    generative_ai.configure(api_key=CLAVE_DE_API)

    st.title("📝 Generador de código SQL con Gemini")

    # Entradas de usuario
    database_description = st.text_area("📂 Describe la base de datos:", height=150)
    problem_description = st.text_area("❓ Describe el problema:", height=150)

    if st.button("🚀 Generar código SQL"):
        prompt = f"""
        Base de datos:
        {database_description}

        Problema:
        {problem_description}

        Genera el código SQL correspondiente y proporciona una explicación detallada.

        **Formato de respuesta:**
        1. Escribe el código SQL en un bloque con ```sql ... ```
        2. Luego, proporciona una explicación clara.
        """

        try:
            model = generative_ai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt, generation_config={"max_output_tokens": 500})

            if response and hasattr(response, "text"):
                response_text = response.text

                # Extraer código SQL con regex
                sql_match = re.search(r"```sql\n(.*?)\n```", response_text, re.DOTALL)
                sql_code = sql_match.group(1) if sql_match else "Código no encontrado"

                # Extraer explicación después del código SQL
                explanation_start = response_text.find("```sql")
                if explanation_start != -1:
                    explanation = response_text[explanation_start + len(sql_code):].strip()
                else:
                    explanation = "Explicación no encontrada"

                # Mostrar resultados
                st.subheader("📜 Código SQL Generado:")
                st.code(sql_code, language="sql")

                st.subheader("💡 Explicación del Código:")
                st.write(explanation)

            else:
                st.error("❌ No se recibió una respuesta válida de la API.")

        except Exception as e:
            st.error(f"⚠️ Error al generar código SQL: {str(e)}")





