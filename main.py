import cloudscraper
from datetime import datetime
from bs4 import BeautifulSoup
import locale

class DateFinderBackend:
    def __init__(self):
        self.today = datetime.today()
        # Set locale to Spanish
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    def get_today_date(self):
        return self.today.strftime('%Y-%m-%d')

    def is_date_valid(self, date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date <= self.today
        except ValueError:
            return False

    def get_exchange_rate(self, date_str):
        # Format the date as dd-monthinspanish-yyyy
        date = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date.strftime('%d-%B-%Y')

        # Construct the URL with the formatted date
        url = f"https://www.elcaribe.com.do/panorama/internacionales/precio-dolar-paralelo-dolar-bcv-venezuela-{formatted_date}/"

        # Use cloudscraper to bypass Cloudflare
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the first <p> tag containing <strong> and check the third <strong> tag for "BCV"
            p_tag = soup.find('p', text=lambda t: t and 'BCV' in t)
            if p_tag:
                strong_tags = p_tag.find_all('strong')
                if len(strong_tags) >= 3:
                    exchange_rate = strong_tags[2].text.strip()
                    return exchange_rate
                else:
                    return "Rate not found"
            else:
                return "Rate not found"
        else:
            return f"Error: {response.status_code}, {response.text}"

# Example usage
if __name__ == "__main__":
    backend = DateFinderBackend()
    print("Today's date:", backend.get_today_date())
    print("Is '2023-10-01' valid?", backend.is_date_valid('2023-10-01'))
    print("Exchange rate on '2023-10-01':", backend.get_exchange_rate('2023-10-01'))