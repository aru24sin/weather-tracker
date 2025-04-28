import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font

def get_canton_weather():
    url = "https://forecast.weather.gov/MapClick.php?textField1=42.307&textField2=-83.486"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    forecast_items = soup.find_all("div", class_="tombstone-container")
    if not forecast_items:
        messagebox.showerror("Error", "Could not find forecast data on the page.")
        return []

    forecast_data = []
    for item in forecast_items:
        period = item.find("p", class_="period-name")
        short_desc = item.find("p", class_="short-desc")
        temp = item.find("p", class_="temp")

        if period and short_desc and temp:
            forecast_data.append(f"{period.get_text()}: {short_desc.get_text()}, {temp.get_text()}")

    return forecast_data

def show_forecast():
    forecast_list.delete(*forecast_list.get_children())
    forecast_data = get_canton_weather()
    if forecast_data:
        for forecast in forecast_data:
            forecast_list.insert("", "end", values=(forecast,))

# GUI Setup
root = tk.Tk()
root.title("Canton, MI 7-Day Weather Forecast")
root.geometry("600x500")
root.configure(bg="#21262e")

# Title Label
title_font = font.Font(family='Helvetica', size=18, weight='bold')
title_label = tk.Label(root, text="Canton, MI 7-Day Weather Forecast", font=title_font, bg="#21262e", fg="#f29d0a")
title_label.pack(pady=20)

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Style Configuration
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), rowheight=30)
style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
style.map("Treeview", background=[('selected', '#4e5951')])

# Forecast List
forecast_list = ttk.Treeview(frame, columns=("Forecast",), show="headings")
forecast_list.heading("Forecast", text="Forecast")
forecast_list.pack(fill=tk.BOTH, expand=True)

# Refresh Button
refresh_button = ttk.Button(root, text="Refresh Forecast", command=show_forecast)
refresh_button.pack(pady=15)

# Initial Load
show_forecast()

root.mainloop()