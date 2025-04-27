import tkinter as tk
from tkinter import messagebox
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

    # Zpráva o dokončení
    messagebox.showinfo("Úspěch", "Výkres byl úspěšně vygenerován a uložen jako 'floorplan.pdf'.")

# Funkce pro zpracování formuláře
def generate():
    try:
        width = int(entry_width.get())
        depth = int(entry_depth.get())
        num_columns_width = int(entry_num_columns_width.get())
        num_columns_depth = int(entry_num_columns_depth.get())
        
        # Zavolání funkce pro generování výkresu
        generate_floorplan(width, depth, num_columns_width, num_columns_depth)
    except ValueError:
        messagebox.showerror("Chyba", "Zadejte prosím platná čísla!")

# Vytvoření hlavního okna
root = tk.Tk()
root.title("Generátor půdorysu")

# Vytvoření vstupních polí
tk.Label(root, text="Šířka (mm):").grid(row=0, column=0)
entry_width = tk.Entry(root)
entry_width.grid(row=0, column=1)

tk.Label(root, text="Hloubka (mm):").grid(row=1, column=0)
entry_depth = tk.Entry(root)
entry_depth.grid(row=1, column=1)

tk.Label(root, text="Počet sloupků po šířce:").grid(row=2, column=0)
entry_num_columns_width = tk.Entry(root)
entry_num_columns_width.grid(row=2, column=1)

tk.Label(root, text="Počet sloupků po hloubce:").grid(row=3, column=0)
entry_num_columns_depth = tk.Entry(root)
entry_num_columns_depth.grid(row=3, column=1)

# Tlačítko pro generování výkresu
generate_button = tk.Button(root, text="Generovat výkres", command=generate)
generate_button.grid(row=4, columnspan=2)

# Spuštění aplikace
root.mainloop()
