import streamlit as st
import math
import uuid

# --- Données disponibles ---
traces_dict = {
    "TENNIS": 750,
    "TOUCH TENNIS 12x6m": 450,
    "BASKET 3X3 - 15X11m": 650,
    "BASKET5X5 - 26X14m": 950,
    "HANDBALL 40X20m": 1200,
    "FOOT SOCCER de 40mx20m (surf. Arrondie)": 1100,
    "FUTSAL 30X15m": 750,
    "VOLLEY BALL 18x9m": 450,
    "BADMINTON 13,40X6,10m": 650,
    "TMS 24X12m": 650,
}


# --- Paramètres modifiables ---
prix_kit_peinture = 750
prix_pose_1j = 1400
prix_pose_2j = 2500
prix_pose_3j = 3500
prix_jour_supplementaire = 950


# --- Fonctions ---
def arrondi_métier(valeur):
    decimal = valeur % 1
    return math.ceil(valeur) if decimal >= 0.5 else math.floor(valeur)



# --- Paramètres globauxdef format_euro(valeur):
def format_euro(valeur):
    return f"{valeur:,.2f}".replace(",", " ").replace(".", ",") + " €"
coeff_dilat_mm = 3
coeff_dilat_m = coeff_dilat_mm / 1000

def init_session():
    st.session_state["longueur"] = 36.0
    st.session_state["largeur"] = 18.0

st.set_page_config(page_title="Calculateur de dalles", layout="centered")
st.title("🧮 Calculateur de dalles modulaires")

if "longueur" not in st.session_state:
    init_session()

# --- Saisie utilisateur ---
st.header("1. Indiquez les dimensions de votre terrain")
col1, col2 = st.columns(2)
with col1:
    longueur = st.number_input("Longueur du terrain (en mètres)", min_value=1.0, step=0.1, key="longueur")
with col2:
    largeur = st.number_input("Largeur du terrain (en mètres)", min_value=1.0, step=0.1, key="largeur")

# --- Calculs de surface et calepinage ---
dim_dalle_sans_dilat = 0.254
surface_par_dalle = dim_dalle_sans_dilat ** 2
prix_unitaire_dalle = 2.29
prix_m2_equivalent = prix_unitaire_dalle / surface_par_dalle
dim_dalle_avec_dilat = dim_dalle_sans_dilat + coeff_dilat_m
dalles_par_palette = 780

nb_dalles_long = arrondi_métier(longueur / dim_dalle_sans_dilat)
nb_dalles_larg = arrondi_métier(largeur / dim_dalle_sans_dilat)
nb_total_dalles = nb_dalles_long * nb_dalles_larg
longueur_sans_dilat = nb_dalles_long * dim_dalle_sans_dilat
largeur_sans_dilat = nb_dalles_larg * dim_dalle_sans_dilat
surface_sans_dilat = nb_total_dalles * surface_par_dalle
longueur_avec_dilat = nb_dalles_long * dim_dalle_avec_dilat
largeur_avec_dilat = nb_dalles_larg * dim_dalle_avec_dilat
surface_hors_tout = longueur_avec_dilat * largeur_avec_dilat
nb_palettes = math.ceil(nb_total_dalles / dalles_par_palette)

# --- Aperçu des dimensions réelles ---
with st.expander("👉 Consulter le détail de l'emprise au sol du terrain"):
    st.markdown(f"**Dimensions saisies :** {longueur} m × {largeur} m = {longueur * largeur:.2f} m²")
    st.markdown(f"**Nombre de dalles :** {nb_dalles_long} en longueur × {nb_dalles_larg} en largeur")
    st.markdown(f"**Dimensions réelles sans dilatation :** {longueur_sans_dilat:.2f} m × {largeur_sans_dilat:.2f} m = {surface_sans_dilat:.2f} m²")
    st.markdown(f"**Dimensions hors-tout avec dilatation (3 mm):** {longueur_avec_dilat:.2f} m × {largeur_avec_dilat:.2f} m = {surface_hors_tout:.2f} m²")

# --- Finition périphérique ---
st.header("3. Choisissez votre finition périphérique")
option_finition = st.radio("Finition souhaitée :", ("Aucune", "Rampes clipsables", "Cornières en aluminium"))

total_finition, designation_finition, quantite_finition, pu_finition = 0, "", "", 0
prix_rampe, prix_corniere = 1.80, 14.00

if option_finition == "Rampes clipsables":
    nb_modules_rampe = 2 * nb_dalles_long + 2 * nb_dalles_larg
    nb_modules_angle = 4
    total_finition = (nb_modules_rampe + nb_modules_angle) * prix_rampe
    designation_finition = "Rampes clipsables"
    quantite_finition = f"{nb_modules_rampe + nb_modules_angle} modules"
    pu_finition = prix_rampe
elif option_finition == "Cornières en aluminium":
    perimetre = 2 * (longueur_avec_dilat + largeur_avec_dilat)
    nb_cornieres = math.ceil(perimetre / 1.0)
    total_finition = nb_cornieres * prix_corniere
    designation_finition = "Cornières aluminium"
    quantite_finition = f"{nb_cornieres} m linéaires"
    pu_finition = prix_corniere

# --- Pose ou fourniture ---
st.header("4. Choisissez la prestation")
option_pose = st.radio("Souhaitez-vous la pose ou uniquement la fourniture ?", ["Fourniture seule", "Fourniture + pose"])

designation_pose, quantite_pose, pu_pose, total_pose = "", "", 0, 0
designation_kit, total_kit, nb_kits = "", 0, 0
afficher_traces = option_pose == "Fourniture + pose"

if option_pose == "Fourniture + pose":
    if surface_sans_dilat <= 200:
        total_pose = prix_pose_1j
        quantite_pose = "1 jour"
    elif surface_sans_dilat <= 700:
        total_pose = prix_pose_2j
        quantite_pose = "2 jours"
    elif surface_sans_dilat <= 1250:
        total_pose = prix_pose_3j
        quantite_pose = "3 jours"
    else:
        surface_sup = surface_sans_dilat - 1250
        jours_sup = math.ceil(surface_sup / 550)
        total_pose = prix_pose_3j + (jours_sup * prix_jour_supplementaire)
        quantite_pose = f"{3 + jours_sup} jours"
    designation_pose = "Main d’œuvre – Pose des dalles"
    pu_pose = "—"
else:
    st.markdown("#### Souhaitez-vous ajouter un kit de peinture pour réaliser les tracés vous-même ?")
    key_kit_dyn = "kit_peinture_check"
    ajouter_kit = st.checkbox("Oui, ajouter un kit de peinture", key=key_kit_dyn)
    if ajouter_kit:
        nb_kits = st.number_input("Nombre de kits souhaités :", min_value=1, step=1)
        total_kit = nb_kits * prix_kit_peinture
        designation_kit = "Kit peinture tracés sportifs"
        afficher_traces = False

# --- Bloc des tracés (affiché uniquement avec la pose) ---
if afficher_traces:
    st.header("5. Tracés sportifs")
    st.markdown("*Sélectionnez les tracés que vous souhaitez intégrer à votre terrain.*")
    selected_traces = []
    total_traces = 0
    for discipline, prix in traces_dict.items():
        if st.checkbox(f"{discipline} – {format_euro(prix)}", key=f"trace_{discipline}"):
            selected_traces.append(discipline)
            total_traces += prix
    st.info("Vous avez besoin d’un tracé spécifique ? Nous réalisons aussi des marquages sur mesure : pédagogiques, logos, plans personnalisés… [Contactez-nous](mailto:contact@tonsite.fr) !")
else:
    selected_traces = []
    total_traces = 0


# --- Fonction utilitaire pour ajouter une ligne HTML au tableau ---
def ajouter_ligne_tableau(designation, quantite, pu, total):
    return f"""<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>{designation}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{quantite}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{pu}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{total}</td>
</tr>"""


# --- Livraison ---
st.header("6. Livraison")
departement_input = st.text_input(
    "Code du département de livraison (ex : 33 pour Gironde)",
    help="Uniquement les départements de France métropolitaine (hors Corse / DOM-TOM).",
    max_chars=2
)


def get_zone_from_departement(dept):
    departements_par_zone = {
        "Nord-Ouest": ["14", "22", "27", "28", "29", "35", "37", "41", "44", "45", "49", "50", "53", "56", "59", "60", "61", "62", "72", "76", "78", "80", "85", "86", "91", "92", "93", "94", "95"],
        "Nord-Est": ["02", "08", "10", "21", "25", "39", "51", "52", "54", "55", "57", "58", "67", "68", "70", "71", "88", "89", "90"],
        "Sud-Ouest": ["09", "16", "17", "19", "23", "24", "31", "32", "33", "40", "46", "47", "64", "65", "79", "81", "82", "87"],
        "Sud-Est": ["01", "03", "04", "05", "06", "07", "11", "12", "13", "15", "18", "26", "30", "34", "38", "42", "43", "48", "63", "66", "69", "73", "74", "83", "84"]
    }
    for zone, dpts in departements_par_zone.items():
        if dept in dpts:
            return zone
    return None

def get_coeff(nb_palettes):
    if nb_palettes <= 6:
        return 1.00
    elif nb_palettes <= 10:
        return 0.80
    elif nb_palettes <= 13:
        return 0.70
    else:
        return 0.60

def calcul_frais_livraison_majore(departement, nb_palettes, majoration=0.15):
    base_tarifs = {
        "Nord-Ouest": 1480,
        "Nord-Est": 1100,
        "Sud-Ouest": 1460,
        "Sud-Est": 1200
    }
    zone = get_zone_from_departement(departement)
    if not zone:
        return None, None, None, None
    base_unit = base_tarifs[zone] / 6
    coeff = get_coeff(nb_palettes)
    prix_unitaire = round(base_unit * coeff, 2)
    total_ht = round(prix_unitaire * nb_palettes, 2)
    supplement = round(total_ht * majoration, 2)
    total_majore = round(total_ht + supplement, 2)
    return zone, prix_unitaire, total_ht, total_majore

frais_livraison = 0
zone_livraison, prix_u_livraison, total_ht_livraison, total_livraison = None, None, None, None
if departement_input and departement_input.isdigit() and len(departement_input) == 2:
    zone_livraison, prix_u_livraison, total_ht_livraison, total_livraison = calcul_frais_livraison_majore(departement_input, nb_palettes)
    
if zone_livraison:
        frais_livraison = total_livraison
        st.success(f"**Frais de livraison estimés : {format_euro(total_livraison)}**")
        st.info("""
        Estimation des frais de livraison

        Les frais indiqués sont donnés à titre estimatif pour une livraison en semi-remorque.
        Ils peuvent varier selon les conditions d’accès, le prix du transporteur et les taxes en vigueur.

        👉 Un devis précis doit être demandé pour validation.
        """)
elif departement_input and (not departement_input.isdigit() or len(departement_input) != 2):
    st.warning("Le département saisi n'est pas reconnu.")
elif departement_input and departement_input.isdigit() and len(departement_input) == 2 and zone_livraison is None:
    st.warning("Ce département n’est pas pris en charge par notre service de livraison automatisé (Corse, DOM-TOM…). Veuillez nous contacter pour un devis personnalisé.")




# --- Affichage estimation ---
st.header("7. Estimation financière")
total_ht_dalles = nb_total_dalles * prix_unitaire_dalle

html_table = f"""
<table style='width:100%; border-collapse: collapse;'>
<thead>
<tr style='background-color:#f2f2f2;'>
  <th style='border: 1px solid #ddd; padding: 8px;'>Désignation</th>
  <th style='border: 1px solid #ddd; padding: 8px;'>Quantité</th>
  <th style='border: 1px solid #ddd; padding: 8px;'>Prix unitaire HT</th>
  <th style='border: 1px solid #ddd; padding: 8px;'>Total HT</th>
</tr>
</thead>
<tbody>
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>Dalles modulaires</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{nb_total_dalles} dalles</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(prix_unitaire_dalle)}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_ht_dalles)}</td>
</tr>
"""

if designation_finition:
    html_table += f"""
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>{designation_finition}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{quantite_finition}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(pu_finition)}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_finition)}</td>
</tr>
"""

if designation_pose:
    html_table += f"""
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>{designation_pose}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{quantite_pose}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{pu_pose}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_pose)}</td>
</tr>
"""

if designation_kit:
    html_table += f"""
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>{designation_kit}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{nb_kits} kit(s)</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(prix_kit_peinture)}</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_kit)}</td>
</tr>
"""

if selected_traces:
    html_table += f"""
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>Tracés sportifs (peinture)</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{len(selected_traces)} tracé(s)</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>—</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_traces)}</td>
</tr>
"""
if frais_livraison > 0:
    html_table += f"""
<tr>
  <td style='border: 1px solid #ddd; padding: 8px;'>Frais de livraison</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{nb_palettes} palette(s)</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>—</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(frais_livraison)}</td>
</tr>
"""


total_global = total_ht_dalles + total_finition + total_pose + total_kit + total_traces + frais_livraison
html_table += f"""

<tr style='font-weight: bold;'>
  <td colspan='3' style='border: 1px solid #ddd; padding: 8px;'>Total général HT</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_global)}</td>
</tr>

<tr>
  <td colspan='3' style='border: 1px solid #ddd; padding: 8px;'>TVA (20 %)</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_global * 0.20)}</td>
</tr>
<tr style='font-weight: bold; background-color: #f9f9f9;'>
  <td colspan='3' style='border: 1px solid #ddd; padding: 8px;'>Total TTC</td>
  <td style='border: 1px solid #ddd; padding: 8px;'>{format_euro(total_global * 1.20)}</td>
</tr>

</tbody>
</table>
<p style='margin-top: 10px; font-size: 0.9em;'>
🔹 <strong>Surface couverte</strong> : {surface_sans_dilat:.2f} m²<br>
🔹 <strong>Prix des dalles (revêtement seul)</strong> : {format_euro(prix_m2_equivalent)} HT / m²<br>
🔹 <strong>Prix global du projet</strong> : {format_euro(total_global / surface_sans_dilat)} HT / m²
</p>

"""

st.markdown(html_table, unsafe_allow_html=True)

# --- Coordonnées utilisateur et génération PDF ---
from io import BytesIO
from xhtml2pdf import pisa

st.header("8. Télécharger mon estimation")
client_nom = st.text_input("Nom / Prénom ou Société")
client_email = st.text_input("Adresse e-mail")

def create_pdf(html_content):
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(src=html_content, dest=pdf_file)
    if not pisa_status.err:
        return pdf_file.getvalue()
    return None

# Ajouter les coordonnées + HTML tableau dans un bloc pour export PDF
if st.button("📄 Télécharger mon estimation en PDF"):
    if not client_nom or not client_email:
        st.warning("Merci de renseigner votre nom et votre adresse e-mail pour générer le PDF.")
    else:
        html_pdf = f"""
        <h2>Estimation personnalisée</h2>
        <p><strong>Nom / Société :</strong> {client_nom}<br>
        <strong>Email :</strong> {client_email}</p>
        {html_table}
        """
        pdf_bytes = create_pdf(html_pdf)
        if pdf_bytes:
            st.download_button("📥 Télécharger le fichier PDF", data=pdf_bytes, file_name="estimation.pdf", mime="application/pdf")
        else:
            st.error("Une erreur est survenue lors de la génération du PDF.")
