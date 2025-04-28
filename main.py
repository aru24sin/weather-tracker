import requests
from bs4 import BeautifulSoup
import customtkinter as ctk
from tkinter import messagebox

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
    forecast_textbox.configure(state="normal")
    forecast_textbox.delete("1.0", ctk.END)
    forecast_data = get_canton_weather()
    if forecast_data:
        for forecast in forecast_data:
            forecast_textbox.insert(ctk.END, forecast + "\n\n")
    forecast_textbox.configure(state="disabled")

# GUI Setup
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = ctk.CTk()
root.title("Canton, MI 7-Day Weather Forecast")
root.geometry("600x500")

# Title Label
title_label = ctk.CTkLabel(root, text="Canton, MI 7-Day Weather Forecast", font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=20)

frame = ctk.CTkFrame(root)
frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

# Forecast Textbox
forecast_textbox = ctk.CTkTextbox(frame, font=ctk.CTkFont(size=14), wrap="word")
forecast_textbox.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
forecast_textbox.configure(state="disabled")

# Refresh Button
refresh_button = ctk.CTkButton(root, text="Refresh Forecast", command=show_forecast)
refresh_button.pack(pady=15)

# Initial Load
show_forecast()

root.mainloop()