import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Load Titanic Data ---
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        global df
        df = pd.read_csv(file_path)

        # Data cleaning
        df['Age'].fillna(df['Age'].median(), inplace=True)
        df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
        df.drop(columns=['Cabin'], inplace=True)

        status_label.config(text="✅ Titanic dataset loaded successfully.")
        summary_btn.config(state="normal")
        heatmap_btn.config(state="normal")
        age_btn.config(state="normal")
        gender_btn.config(state="normal")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")

# --- Plot Functions ---
def show_plot(fig):
    for widget in chart_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def plot_summary():
    stats = df.describe(include='all').to_string()
    text_box = tk.Text(chart_frame, wrap="word", font=("Consolas", 10), bg="#1e1e1e", fg="white")
    text_box.insert("1.0", stats)
    text_box.pack(expand=True, fill="both")

def plot_heatmap():
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")
    show_plot(fig)

def plot_age_distribution():
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(df['Age'], bins=30, kde=True, color='#00bcd4', ax=ax)
    ax.set_title("Age Distribution")
    show_plot(fig)

def plot_gender_survival():
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(x='Sex', hue='Survived', data=df, palette='Set2', ax=ax)
    ax.set_title("Survival by Gender")
    show_plot(fig)

# --- GUI Setup ---
root = tk.Tk()
root.title("🚢 Titanic EDA Visualizer")
root.geometry("1000x700")
root.configure(bg="#121212")

# --- Header ---
title = tk.Label(root, text="Titanic Dataset Explorer", font=("Segoe UI", 24, "bold"),
                 bg="#121212", fg="white")
title.pack(pady=20)

# --- Button Frame ---
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)

load_btn = tk.Button(btn_frame, text="📂 Load Titanic CSV", font=("Segoe UI", 11),
                     command=load_data, bg="#333", fg="white", padx=15, pady=6)
load_btn.grid(row=0, column=0, padx=10)

summary_btn = tk.Button(btn_frame, text="📋 Data Summary", command=plot_summary,
                        state="disabled", bg="#444", fg="white", padx=15, pady=6)
summary_btn.grid(row=0, column=1, padx=10)

heatmap_btn = tk.Button(btn_frame, text="📊 Correlation Heatmap", command=plot_heatmap,
                        state="disabled", bg="#555", fg="white", padx=15, pady=6)
heatmap_btn.grid(row=0, column=2, padx=10)

age_btn = tk.Button(btn_frame, text="🎂 Age Distribution", command=plot_age_distribution,
                    state="disabled", bg="#666", fg="white", padx=15, pady=6)
age_btn.grid(row=0, column=3, padx=10)

gender_btn = tk.Button(btn_frame, text="🚻 Gender Survival", command=plot_gender_survival,
                       state="disabled", bg="#777", fg="white", padx=15, pady=6)
gender_btn.grid(row=0, column=4, padx=10)

# --- Chart Area ---
chart_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief="ridge")
chart_frame.pack(expand=True, fill="both", padx=20, pady=20)

# --- Status Bar ---
status_label = tk.Label(root, text="📁 Please load the Titanic CSV dataset to begin.",
                        font=("Segoe UI", 10), bg="#1e1e1e", fg="white")
status_label.pack(side="bottom", fill="x")

root.mainloop()
