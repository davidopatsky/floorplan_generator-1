import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Funkce pro generování výkresu
def generate_floorplan(width, depth, num_columns_width, num_columns_depth):
    fig, ax = plt.subplots(figsize=(8.3, 11.7))  # Formát A4

    # Vykreslení obdélníku
    ax.plot([0, width, width, 0, 0], [0, 0, depth, depth, 0], 'k-', linewidth=2)
    
    # Parametry sloupků
    column_size = 120  # Velikost sloupku (120x120 mm)
    offset = 60  # Střed sloupku je 60 mm uvnitř tvaru (zarovnáno vnější hranou obdélníku)

    # Vypočítání pozic sloupků
    col_x_positions = [i * (width / (num_columns_width + 1)) - offset for i in range(1, num_columns_width + 1)]
    col_y_positions = [i * (depth / (num_columns_depth + 1)) - offset for i in range(1, num_columns_depth + 1)]

    # Vykreslení sloupků (červené tečky)
    for x in col_x_positions:
        for y in col_y_positions:
            ax.plot(x, y, 'ro', markersize=5)  # Sloupek

    # Kóty - Celkový rozměr
    ax.annotate(f'{width} mm', xy=(width / 2, -200), ha='center', va='top', fontsize=10, arrowprops=dict(arrowstyle='<->'))
    ax.annotate(f'{depth} mm', xy=(-200, depth / 2), ha='right', va='center', rotation=90, fontsize=10, arrowprops=dict(arrowstyle='<->'))

    # Kóty - Středové osy sloupků
    for x in col_x_positions:
        ax.plot([x, x], [0, depth], 'r--', linewidth=0.5)  # Středová osa sloupku
    for y in col_y_positions:
        ax.plot([0, width], [y, y], 'r--', linewidth=0.5)  # Středová osa sloupku

    # Kóty pro střed sloupků
    for x in col_x_positions:
        ax.annotate(f'{x + offset} mm', xy=(x, -100), ha='center', va='top', fontsize=8, arrowprops=dict(arrowstyle='<->'))
    for y in col_y_positions:
        ax.annotate(f'{y + offset} mm', xy=(-100, y), ha='right', va='center', rotation=90, fontsize=8, arrowprops=dict(arrowstyle='<->'))

    # Nastavení os a zobrazení
    ax.set_aspect('equal')
    ax.axis('off')

    # Uložení do PDF
    with PdfPages('floorplan.pdf') as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

    return 'floorplan.pdf'

# Aplikace Streamlit
st.title('Generátor půdorysu s obdélníkem a sloupky')

# Uživatelské vstupy
width = st.number_input('Šířka (mm)', min_value=1000, value=5000)
depth = st.number_input('Hloubka (mm)', min_value=1000, value=3000)
num_columns_width = st.number_input('Počet sloupků po šířce', min_value=1, value=3)
num_columns_depth = st.number_input('Počet sloupků po hloubce', min_value=1, value=2)

# Tlačítko pro generování výkresu
if st.button('Generovat výkres'):
    pdf_path = generate_floorplan(width, depth, num_columns_width, num_columns_depth)
    st.success("Výkres byl úspěšně vygenerován.")
    
    # Nabídka pro stažení PDF
    with open(pdf_path, 'rb') as f:
        st.download_button('Stáhnout PDF', f, file_name='floorplan.pdf')

