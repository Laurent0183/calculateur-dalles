
import streamlit as st
from io import BytesIO
from xhtml2pdf import pisa

st.set_page_config(page_title="Estimation", layout="centered")
st.title("📄 Générateur de devis PDF")

st.header("Informations client")
client_nom = st.text_input("Nom / Prénom ou Société", key="nom")
client_email = st.text_input("Adresse e-mail", key="email")
st.text_area("Commentaire (optionnel)", height=100, key="commentaire")

html_table = """
<table border='1' cellpadding='5' cellspacing='0'>
<tr><th>Désignation</th><th>Quantité</th><th>Prix</th></tr>
<tr><td>Dalles modulaires</td><td>324</td><td>741,96 €</td></tr>
<tr><td>Rampes clipsables</td><td>68 modules</td><td>122,40 €</td></tr>
<tr><td><strong>Total TTC</strong></td><td></td><td><strong>1 036,03 €</strong></td></tr>
</table>
"""

def create_pdf(html_content):
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=pdf_file)
    if not pisa_status.err:
        return pdf_file.getvalue()
    return None

if st.button("📄 Télécharger le fichier PDF maintenant"):
    nom = st.session_state.get("nom", "")
    email = st.session_state.get("email", "")
    commentaire = st.session_state.get("commentaire", "")

    if not nom or not email:
        st.warning("Merci de renseigner votre nom et votre adresse e-mail.")
    else:
        commentaire_html = f"<p><strong>Commentaire :</strong><br>{commentaire.replace(chr(10), '<br>')}</p>" if commentaire else ""
        html_pdf = f"""
        <h2>Estimation personnalisée</h2>
        <p><strong>Nom / Société :</strong> {nom}<br>
        <strong>Email :</strong> {email}</p>
        {commentaire_html}
        {html_table}
        """
        pdf_bytes = create_pdf(html_pdf)
        if pdf_bytes:
            st.download_button(
                label="📥 Télécharger le fichier PDF",
                data=pdf_bytes,
                file_name="estimation.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Une erreur est survenue lors de la génération du PDF.")
