from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Halutut sanat
halutut_sanat = ["Lempäälä", "Jyväskylä"]

# Verkkosivun URL
url = "https://www.tilannehuone.fi/halytys.php"

# Asetukset Seleniumille
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ajettavaksi taustalla
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Polku ChromeDriverille, jos tarpeen
service = Service('/path/to/chromedriver')  # Muista asettaa polku omalle ChromeDriverillesi

# Luo selainistunto
driver = webdriver.Chrome(service=service, options=chrome_options)

def tarkista_sanat():
    try:
        # Ladataan verkkosivu
        driver.get(url)
        
        # Etsitään kaikki <td>-elementit, joissa on luokka "kunta"
        td_elements = driver.find_elements(By.CSS_SELECTOR, 'td.kunta')
        
        # Käydään läpi löydetyt <td>-elementit
        for td in td_elements:
            for sana in halutut_sanat:
                if sana in td.text:
                    print(f'Sana "{sana}" löytyi: {td.text}')
                    
    except Exception as e:
        print(f'Virhe verkkosivun käsittelyssä: {e}')

# Pääsilmukka, joka suorittaa tarkistuksen 5 minuutin välein
while True:
    tarkista_sanat()
    time.sleep(300)  # Odotetaan 5 minuuttia (300 sekuntia) ennen seuraavaa tarkistusta

# Sulje selainistunto, kun et enää tarvitse sitä
# driver.quit()
