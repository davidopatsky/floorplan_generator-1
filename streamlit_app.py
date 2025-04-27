import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from streamlit_drawable_canvas import st_canvas

# Výchozí obdélník
obdelnik = {"sirka": 4000, "vyska": 3000}

# Výchozí anotace
anotace = {
    "Šířka": {"x": 2000, "y": -150, "text": "4000 mm", "rotation": 0},
    "Výška": {"x": -150, "y": 1500, "text": "3000 mm", "rotation": 90},
}

def vykresli_obdelnik_s_kotami(ax, obdelnik, anotace, selected=None):
    rect = patches.Rectangle((0, 0), obdelnik['sirka'], obdelnik['vyska'],
                              linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    for nazev, info in anotace.items():
        color = 'red' if nazev == selected else 'blue'
        if "mm" in info['text']:
            if info['rotation'] == 0:
                ax.annotate('', xy=(0, info['y']), xytext=(obdelnik['sirka'], info['y']),
                            arrowprops=dict(arrowstyle='<->', lw=1.5, color=color))
            else:
                ax.annotate('', xy=(info['x'], 0), xytext=(info['x'], obdelnik['vyska']),
                            arrowprops=dict(arrowstyle='<->', lw=1.5, color=color))
        ax.text(info['x'], info['y'], info['text'],
                ha='center', va='center', fontsize=12, color=color, rotation=info['rotation'])
    ax.set_xlim(-500, obdelnik['sirka'] + 500)
    ax.set_ylim(-500, obdelnik['vyska'] + 500)
    ax.set_aspect('equal')
    ax.axis('off')

def najdi_nejblizsi_anotaci(anotace, klik_x, klik_y):
    nejblizsi = None
    min_vzdalenost = float('inf')
    for nazev, info in anotace.items():
        vzdalenost = math.sqrt((klik_x - info['x'])**2 + (klik_y - info['y'])**2)
        if vzdalenost < min_vzdalenost:
            min_vzdalenost = vzdalenost
            nejblizsi = nazev
    return nejblizsi

st.set_page_config(layout="wide")
st.title("Testovací verze - klikání na anotace")

st.header("Nastavení obdélníku")
obdelnik['sirka'] = st.number_input('Šířka (mm)', min_value=500, max_value=10000, value=4000)
obdelnik['vyska'] = st.number_input('Výška (mm)', min_value=500, max_value=10000, value=3000)

# Canvas bez pozadí
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    update_streamlit=True,
    height=800,
    width=1200,
    drawing_mode="transform",
    background_color="white",
    key="canvas",
)

selected = None
if canvas_result.json_data is not None:
    if len(canvas_result.json_data["objects"]) > 0:
        posledni_klik = canvas_result.json_data["objects"][-1]
        klik_x = posledni_klik["left"]
        klik_y = posledni_klik["top"]
        selected = najdi_nejblizsi_anotaci(anotace, klik_x, 800 - klik_y)  # invertujeme Y osu

fig, ax = plt.subplots(figsize=(10, 8))
vykresli_obdelnik_s_kotami(ax, obdelnik, anotace, selected)
st.pyplot(fig)

if selected:
    st.success(f"Vybrána anotace: {selected}")
    nova_hodnota = st.text_input(f"Zadejte novou hodnotu pro '{selected}':", value=anotace[selected]['text'])
    anotace[selected]['text'] = nova_hodnota
