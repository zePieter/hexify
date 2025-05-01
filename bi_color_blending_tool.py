
import streamlit as st

def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def blend_colors(fg, bg, alpha):
    return tuple(round(alpha * f + (1 - alpha) * b) for f, b in zip(fg, bg))

st.set_page_config(page_title="BI Color Blending Tool", layout="centered")

# --- Branding ---
st.markdown("### 🎨 BI Color Blending Tool")
st.markdown("_Voor het berekenen van mengkleuren bij transparantie op een achtergrondkleur._")
st.markdown("👁️‍🗨️ *Tip: gebruik deze tool als zwevend venster naast je Power BI-scherm.*")

with st.sidebar:
    st.markdown("#### 🔧 Instellingen & Branding")
    branding_name = st.text_input("Organisatienaam of dashboardnaam", "Jouw BI Team")
    theme_note = st.text_area("Toelichting of instructies voor gebruikers", 
        "Bijvoorbeeld: gebruik 25% transparantie voor achtergrondvulling. "
        "Gebruik 50% voor hovereffecten. Combineer met wit of grijs voor subtiele stijlen.")

# --- Standaardkleuren & Presets ---
st.markdown("#### Stap 1: Kies je voorgrondkleur")
preset_colors = {
    "Sky Blue (#00A8E8)": "#00A8E8",
    "Coral Red (#FF6B6B)": "#FF6B6B",
    "Charcoal (#333333)": "#333333",
    "Groene Signaal (#29B247)": "#29B247"
}
color_choice = st.selectbox("Standaardkleuren", list(preset_colors.keys()))
fg_color = preset_colors[color_choice]

# --- Achtergrondkleur en Opacity ---
st.markdown("#### Stap 2: Kies achtergrondkleur en transparantie")
bg_color = st.color_picker("Achtergrondkleur", "#FFFFFF")
opacity_label = st.select_slider(
    "Transparantie (opacity)",
    options=[0.1, 0.25, 0.5, 0.75, 1.0],
    value=0.25,
    format_func=lambda x: f"{int(x*100)}% - bijvoorbeeld {'achtergrond' if x == 0.25 else 'hover' if x == 0.5 else 'volledig'}"
)

# --- Berekening ---
fg_rgb = hex_to_rgb(fg_color)
bg_rgb = hex_to_rgb(bg_color)
blended_rgb = blend_colors(fg_rgb, bg_rgb, opacity_label)
blended_hex = rgb_to_hex(blended_rgb)

# --- Preview ---
st.markdown("#### Stap 3: Bekijk resultaat")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Voorgrondkleur (100%)**")
    st.color_picker("Volledig", fg_color, label_visibility="collapsed")
with col2:
    st.markdown(f"**Gemengd resultaat ({int(opacity_label*100)}%)**")
    st.color_picker("Resultaat", blended_hex, label_visibility="collapsed")

# --- JSON Output ---
st.markdown("#### Stap 4: Kopieer hexkleur of JSON")
st.code(blended_hex, language='text')

json_output = '{{\n  "name": "{} {}%",\n  "value": "{}"\n}}'.format(
    color_choice, int(opacity_label * 100), blended_hex
)

st.text_area("JSON-export (bijvoorbeeld voor Power BI thema)", value=json_output, height=100)

# --- Extra: Generator voor stijlen ---
st.markdown("#### Automatische stijlvarianten")
auto_colors = {f"{int(p*100)}%": rgb_to_hex(blend_colors(fg_rgb, bg_rgb, p)) for p in [1.0, 0.75, 0.5, 0.25, 0.1]}
for label, hexcode in auto_colors.items():
    st.write(f"**{label}**: `{hexcode}`")

# --- Footer ---
st.markdown("---")
st.caption(f"Gemaakt voor {branding_name} – door jouw designteam")
