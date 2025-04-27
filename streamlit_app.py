import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Definice obdélníku a výchozích anotací
obdelnik = {"sirka": 4000, "vyska": 3000}
anotace = {
    "Šířka": {"x": 2000, "y": -200, "text": "4000 mm", "rotation": 0},
    "Výška": {"x": -200, "y": 1500, "text": "3000 mm", "rotation": 90},
}

def vykresli_obdelnik_s_kotami(obdelnik, anotace):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Vykreslení obdélníku
    rect = patches.Rectangle((0, 0), obdelnik['sirka'], obdelnik['vyska'],
                              linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

    # Kótovací šipky a texty
    for nazev, info in anotace.items():
        ax.annotate(
            '', xy=(0, info['y']) if nazev == "Výška" else (info['x'], 0),
            xytext=(obdelnik['sirka'], info['y']) if nazev == "Šířka" else (info['x'], obdelnik['vyska']),
            arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue')
        )
        ax.text(info['x'], info['y'], info['text'], 
                ha='center', va='center', fontsize=12, color='blue', rotation=info['rotation'])
    
    # Nastavení vzhledu
    ax.set_xlim(-500, obdelnik['sirka'] + 500)
    ax.set_ylim(-500, obdelnik['vyska'] + 500)
    ax.set_aspect('equal')
    ax.axis('off')

    return fig

def main():
    st.title("Interaktivní obdélník s editací kót")

    # Výběr anotace
    selected_anotace = st.selectbox("Vyberte kótu k editaci:", list(anotace.keys()))
    nova_hodnota = st.text_input("Nová hodnota:", value=anotace[selected_anotace]['text'])

    # Aktualizace hodnoty
    anotace[selected_anotace]['text'] = nova_hodnota

    # Vykreslení
    fig = vykresli_obdelnik_s_kotami(obdelnik, anotace)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
