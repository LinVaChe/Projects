import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

# [GF]0 по G0
table1_GF0 = {
    1.2: [1.35, 1.51, 1.60, 1.69, 1.78, 1.82, 1.92],
    1.4: [1.50, 1.67, 1.78, 1.89, 1.96, 2.04, 2.20],
    1.6: [1.67, 1.80, 1.90, 2.00, 2.13, 2.24, 2.35]
}

# коэффициент C1 по alpha1
table2_C1 = {
    70: 0.56,
    80: 0.62,
    90: 0.68,
    100: 0.74,
    110: 0.79,
    120: 0.83,
    130: 0.87,
    140: 0.90,
    150: 0.93,
    160: 0.96,
    170: 0.98,
    180: 1.00,
}

# коэффициент C2 по v
table3_C2 = {
    5: 1.04,
    10: 1.0,
    15: 0.94,
    20: 0.85,
    25: 0.74,
    30: 0.6
}

# коэффициент C3 по характеру нагрузки и типу двигателя
table4_C3 = {
    ("Спокойная нагрузка. Пусковая нагрузка до 120% номинальной", "I"): 1.0,
    ("Спокойная нагрузка. Пусковая нагрузка до 120% номинальной", "II"): 0.9,
    ("Умеренные колебания нагрузки. Пусковая нагрузка до 150% номинальной", "I"): 0.9,
    ("Умеренные колебания нагрузки. Пусковая нагрузка до 150% номинальной", "II"): 0.8,
    ("Значительные колебания нагрузки. Пусковая нагрузка до 200% номинальной", "I"): 0.8,
    ("Значительные колебания нагрузки. Пусковая нагрузка до 200% номинальной", "II"): 0.7,
    ("Весьма неравномерная и ударная нагрузка. Пусковая нагрузка до 300% номинальной", "I"): 0.7,
    ("Весьма неравномерная и ударная нагрузка. Пусковая нагрузка до 300% номинальной", "II"): 0.6,
}

# площадь S1 по профилю ремня
table5_S1 = {
    "О": 47,
    "А": 81,
    "Б": 138,
    "В": 230,
}


def get_from_table(value, table, name):
    if value not in table:
        messagebox.showerror(
            "Ошибка",
            f"Для такого числа {name} нет соответствующего значения в таблице"
        )
        return None
    return table[value]

def get_random_from_table(value, table):
    if value not in table:
        messagebox.showerror(
            "Ошибка",
            f"Для такого числа G0 нет соответствующего значения в таблице"
        )
        return None
    return random.choice(table[value])

def calculate():
    try:
        N = float(entry_N.get())
        v = float(entry_v.get())
        G0 = float(entry_G0.get())
        alpha1 = float(entry_alpha.get())
        profile = combo_profile.get()
        XN = combo_XN.get()
        TPD = combo_TPD.get()

        F = 1000 * N / v
        GF0 = get_random_from_table(G0, table1_GF0) # на рандом потому что там разные значения на один ключ
        C1 = get_from_table(alpha1, table2_C1, "C1")
        C2 = get_from_table(v, table3_C2, "C2")
        C3 = table4_C3.get((XN, TPD))

        # ошибки если кто-то решит вбить значения ручную вместо того чтобы выбирать из списка
        if C3 is None:
            messagebox.showerror("Ошибка", "Нет соответствия для ХН и ТПД в таблице 4.")
            return

        S1 = table5_S1.get(profile)
        if S1 is None:
            messagebox.showerror("Ошибка", "Нет подходящего профиля в таблице 5")
            return

        Gf = GF0 * C1 * C2 * C3
        Z = F / (S1 * Gf)

        result_text = (
            f"Окружная сила F = {F:.2f} Н\n"
            f"[GF]0 = {GF0:.3f}\n"
            f"C1 = {C1:.3f}\n"
            f"C2 = {C2:.3f}\n"
            f"C3 = {C3:.3f}\n"
            f"[Gf] = {Gf:.3f}\n"
            f"S1 = {S1} мм²\n\n"
            f"Количество ремней Z = {Z:.2f}"
        )

        result_label.config(text=result_text)

    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный ввод числа.")


# графоний

root = tk.Tk()
root.title("Расчет количества клиновых ремней")

title = tk.Label(root, text="Введите эмпирические данные для расчета количества ремней",
                 font=("Arial", 12))
title.pack(pady=20)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10) # если убрать шапку это будет регулировать мне отступы НЕ ТРОГАТЬ

labels = [
    ("Мощность N (кВт):", "entry_N"),
    ("Скорость ремня v (м/с):", "entry_v"),
    ("Начальное натяжение G0:", "entry_G0"),
    ("Угол обхвата alpha1 (градусы):", "entry_alpha"),
]
entries = {}

# делаю поля под первую половину величин на них потом проверку повесить
for text, varname in labels:
    lbl = tk.Label(frame, text=text, anchor="w")
    lbl.pack(fill="x") 
    ent = tk.Entry(frame)
    ent.pack(fill="x", pady=3)
    entries[varname] = ent

entry_N = entries["entry_N"]
entry_v = entries["entry_v"]
entry_G0 = entries["entry_G0"]
entry_alpha = entries["entry_alpha"]

tk.Label(frame, text="Характер нагрузки (ХН):").pack(fill="x")
combo_XN = ttk.Combobox(frame, values=["Спокойная нагрузка. Пусковая нагрузка до 120% номинальной", "Умеренные колебания нагрузки. Пусковая нагрузка до 150% номинальной",
                                       "Значительные колебания нагрузки. Пусковая нагрузка до 200% номинальной", "Весьма неравномерная и ударная нагрузка. Пусковая нагрузка до 300% номинальной"])
combo_XN.pack(fill="x", pady=3)

tk.Label(frame, text="Тип приводного двигателя (ТПД):").pack(fill="x")
combo_TPD = ttk.Combobox(frame, values=["I", "II"])
combo_TPD.pack(fill="x", pady=3)

tk.Label(frame, text="Профиль ремня:").pack(fill="x")
combo_profile = ttk.Combobox(frame, values=["О", "А", "Б", "В"])
combo_profile.pack(fill="x", pady=3)

btn = tk.Button(root, text="Рассчитать", command=calculate)
btn.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()
