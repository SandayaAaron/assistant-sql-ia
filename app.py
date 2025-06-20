import streamlit as st
import openai
import os

structure_table = """
Table: reservations
Colonnes :
- id_reservation (UUID)
- client_id (UUID)
- date_reservation (TIMESTAMP)
- statut (VARCHAR)
- prix (FLOAT)
- nombre_personnes (INT)
"""

st.set_page_config(page_title="Assistant SQL IA", layout="centered")
st.title("🧠 Assistant SQL IA")
st.markdown("Pose ta question métier → reçois la requête SQL correspondante")

question = st.text_area("💬 Question :", height=150)

if st.button("Générer la requête SQL"):
    if not question.strip():
        st.warning("Merci de poser une question.")
    else:
        with st.spinner("Génération en cours..."):
            prompt = f"""
Tu es un expert en SQL PostgreSQL. Voici la structure de la table :

{structure_table}

Génère une requête SQL correspondant à cette question :
{question}

Réponds uniquement avec la requête SQL.
"""
            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.code(response["choices"][0]["message"]["content"], language="sql")
            except Exception as e:
                st.error(f"Erreur : {e}")
