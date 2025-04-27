import streamlit as st
import matplotlib.pyplot as plt

# Funkce pro generování výkresu
def draw_dimensioned_rectangle(width, depth):
    fig, ax = plt.subplots(figsize=(8.3, 11.7))  # A4 formát

    # Vykreslení obdélníku
    ax.plot([0, width, width, 0, 0], [0, 0, depth, depth, 0], 'k-', linewidth=2)
    
    # Kóta pro šířku (šířka)
    ax.annotate(f'{width} mm', xy=(width / 2, -200), ha='center', va='top', fontsize=10,
                arrowprops=dict(arrowstyle='<->', lw=1))  # Šipka pro šířku

    # Kóta pro hloubku (výška)
    ax.annotate(f'{depth} mm', xy=(-200, depth / 2), ha='right', va='center', rotation=90, fontsize=10,
                arrowprops=dict(arrowstyle='<->', lw=1))  # Šipka pro hloubku

    # Kótovací čáry pro levý a pravý okraj
    ax.plot([0, 0], [0, depth], 'k--', lw=0.5)  # Levá kótu
    ax.plot([width, width], [0, depth], 'k--', lw=0.5)  # Pravá kótu

    # Kótovací čáry pro spodní a horní okraj
    ax.plot([0, width], [0, 0], 'k--', lw=0.5)  # Spodní kótu
    ax.plot([0, width], [depth, depth], 'k--', lw=0.5)  # Horní kótu

    # Středové osy (pro sloupky)
    ax.plot([width / 2, width / 2], [0, depth], 'r--', lw=0.5)  # Středová osa pro šířku
    ax.plot([0, width], [depth / 2, depth / 2], 'r--', lw=0.5)  # Středová osa pro hloubku

    # Nastavení grafu
    ax.set_aspect('equal')
    ax.axis('off')

    # Zobrazení grafu ve Streamlit
    st.pyplot(fig)

# Aplikace Streamlit
st.title('Generátor výkresu s evropskými kótami')

# Uživatelské vstupy
width = st.number_input('Šířka (mm)', min_value=1000, value=5000)
depth = st.number_input('Hloubka (mm)', min_value=1000, value=3000)

# Tlačítko pro generování výkresu
if st.button('Generovat výkres'):
    draw_dimensioned_rectangle(width, depth)
