from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.core.os_manager import ChromeType

class PegandoLogotipo:
    def __init__(self, ticker: str, driver_firefox: webdriver.Firefox | None = None) -> None:
        self.ticker = ticker
        self.driver_firefox = driver_firefox
        
    def options(self) -> webdriver.ChromeOptions:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-features=NetworkService")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        return chrome_options
    
    
    def service(self) -> Service:
        svc = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        return svc

    def driver(self) -> webdriver.Chrome:
        svc = self.service()
        driver = webdriver.Chrome(service=svc, options=self.options())
        return driver

    def pegar_logotipo(self) -> str | None:
        if self.driver_firefox:
            driver = self.driver_firefox
        else:
            driver = self.driver()
        driver.get(f"https://br.tradingview.com/symbols/BMFBOVESPA-{self.ticker}/")
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/div[4]/div[2]/div[1]/div[1]/div/div/div/div[1]/img[3]",
                )
            )
        )

        # Extrai o link da imagem (atributo 'src')
        image_link = image_element.get_attribute("src")
        return image_link
