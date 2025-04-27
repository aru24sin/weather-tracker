import requests
from bs4 import BeautifulSoup

def get_canton_weather():
    url = "https://forecast.weather.gov/MapClick.php?textField1=42.307&textField2=-83.486"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the seven-day forecast
    forecast_items = soup.find_all("div", class_="tombstone-container")
    if not forecast_items:
        print("Could not find forecast data on the page.")
        return

    print("7-Day Weather Forecast for Canton, MI:\n")
    for item in forecast_items:
        period = item.find("p", class_="period-name")
        short_desc = item.find("p", class_="short-desc")
        temp = item.find("p", class_="temp")

        if period and short_desc and temp:
            print(f"{period.get_text()}: {short_desc.get_text()}, {temp.get_text()}")
        else:
            continue

if __name__ == "__main__":
    get_canton_weather()