import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Load Dataset ---
df = pd.read_csv("RTA Dataset.csv")

# --- Main Window ---
window = ThemedTk(theme="radiance")
window.title("🚦 Traffic Accident Analysis")
window.geometry("1000x700")
window.configure(bg="#f0f0f0")

# --- Chart Frame ---
chart_frame = tk.Frame(window, bg="#f0f0f0")
chart_frame.pack(pady=20)

# --- Dropdown Menu Options ---
chart_options = [
    "Accident Count by Area",
    "Accident Severity Distribution",
    "Accidents by Day of Week",
    "Vehicle Type Involved",
    "Weather Conditions",
    "Age Band of Driver"
]

# --- Draw Chart Function ---
def draw_chart(selected):
    fig = plt.Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)

    if selected == "Accident Count by Area":
        counts = df['Area_accident_occured'].value_counts()
        counts.plot(kind='bar', ax=ax, color="#007ACC")
        ax.set_title("Accidents by Area")
        ax.set_ylabel("Number of Accidents")

    elif selected == "Accident Severity Distribution":
        counts = df['Accident_Severity'].value_counts()
        counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140)
        ax.set_title("Accident Severity Distribution")
        ax.axis('equal')

    elif selected == "Accidents by Day of Week":
        counts = df['Day_of_week'].value_counts()
        counts.plot(kind='bar', ax=ax, color="orange")
        ax.set_title("Accidents by Day of Week")
        ax.set_ylabel("Number")

    elif selected == "Vehicle Type Involved":
        counts = df['Type_of_vehicle'].value_counts()
        counts.plot(kind='barh', ax=ax, color="#00B894")
        ax.set_title("Accidents by Vehicle Type")

    elif selected == "Weather Conditions":
        counts = df['Weather_conditions'].value_counts()
        counts.plot(kind='bar', ax=ax, color="#6C5CE7")
        ax.set_title("Accidents by Weather Condition")

    elif selected == "Age Band of Driver":
        counts = df['Age_band_of_driver'].value_counts()
        counts.plot(kind='bar', ax=ax, color="#E17055")
        ax.set_title("Driver Age Band in Accidents")
        ax.set_ylabel("Number")

    # Clear previous charts
    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --- UI Components ---
title = tk.Label(window, text="🚗 Traffic Accident Insights Dashboard",
                 font=("Segoe UI", 20, "bold"), bg="#f0f0f0", fg="#333")
title.pack(pady=10)

selected_option = tk.StringVar()
selected_option.set(chart_options[0])

dropdown = ttk.Combobox(window, textvariable=selected_option,
                        values=chart_options, state="readonly", font=("Segoe UI", 12), width=40)
dropdown.pack(pady=10)
dropdown.bind("<<ComboboxSelected>>", lambda e: draw_chart(selected_option.get()))

# --- Initial Chart ---
draw_chart(selected_option.get())

# --- Run ---
window.mainloop()
