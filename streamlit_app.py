import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# Výchozí obdélník
obdelnik = {"sirka": 4000, "vyska": 3000}

# Výchozí anotace (kóty)
anotace = {
    "Šířka": {"x": 2000, "y": -150, "text": "4000 mm", "rotation": 0},
    "Výška": {"x": -150, "y": 1500, "text": "3000 mm", "rotation": 90},
}

def vykresli_obdelnik_s_kotami(obdelnik, anotace):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Vykreslení obdélníku
    rect = patches.Rectangle((0, 0), obdelnik['sirka'], obdelnik['vyska'],
                              linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

    # Vykreslení anotací
    for nazev, info in anotace.items():
        # Kótovací šipka pokud jde o rozměrovou kótu (obsahuje "mm")
        if "mm" in info['text']:
            if info['rotation'] == 0:
                ax.annotate(
                    '', xy=(0, info['y']), xytext=(obdelnik['sirka'], info['y']),
                    arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue')
                )
            else:
                ax.annotate(
                    '', xy=(info['x'], 0), xytext=(info['x'], obdelnik['vyska']),
                    arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue')
                )
        # Text anotace
        ax.text(info['x'], info['y'], info['text'],
                ha='center', va='center', fontsize=12, color='blue', rotation=info['rotation'])

    # Vzhled plátna
    ax.set_xlim(-500, obdelnik['sirka'] + 500)
    ax.set_ylim(-500, obdelnik['vyska'] + 500)
    ax.set_aspect('equal')
    ax.axis('off')

    return fig

def main():
    st.title("Interaktivní kreslení obdélníku a kót")

    st.header("Nastavení obdélníku")
    obdelnik['sirka'] = st.number_input('Šířka obdélníku (mm)', min_value=500, max_value=10000, value=4000)
    obdelnik['vyska'] = st.number_input('Výška obdélníku (mm)', min_value=500, max_value=10000, value=3000)

    st.header("Editace existujících kót")
    selected_anotace = st.selectbox("Vyberte kótu k editaci:", list(anotace.keys()))
    nova_hodnota = st.text_input("Nová hodnota:", value=anotace[selected_anotace]['text'])
    anotace[selected_anotace]['text'] = nova_hodnota

    st.header("Přidání nové kóty / popisu")
    with st.form("pridani_koty"):
        nazev = st.text_input("Název nové anotace (např. PŘÍPRAVA NA ODTOK)")
        text = st.text_input("Text nové anotace", value="Nový text")
        x = st.number_input("X pozice (mm)", min_value=-1000, max_value=10000, value=1000)
        y = st.number_input("Y pozice (mm)", min_value=-1000, max_value=10000, value=1000)
        rotation = st.selectbox("Rotace textu", [0, 90])
        pridat = st.form_submit_button("Přidat kótu")
    
    if pridat:
        anotace[nazev] = {"x": x, "y": y, "text": text, "rotation": rotation}
        st.success(f"Kóta '{nazev}' byla přidána.")

    st.header("Výkres")
    fig = vykresli_obdelnik_s_kotami(obdelnik, anotace)
    st.pyplot(fig)

    # Export obrázku jako PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(label="Stáhnout výkres jako PNG", data=buf.getvalue(), file_name="vykres.png", mime="image/png")

if __name__ == "__main__":
    main()
