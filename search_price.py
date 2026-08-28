import re
from bs4 import BeautifulSoup
from curl_cffi import Session
from gpu import Gpu

def search_price(session: Session, gpu: Gpu):
    min_price = float("inf")
    current_page = 1
    max_page = 1
    
    gpu_list: list[Gpu] = []
    
    while current_page <= max_page:
        r = session.get(
            "https://www.pichau.com.br/search", 
            params={"q": gpu.name, "product_category": "6459", "page": current_page}
        )
        
        if r.status_code != 200:
            exit("Unable to fetch data.")
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        titles = list(map(lambda x: (
                x.get_text()
            ),soup.select("h2")))
        
        prices_pix = list(map(lambda x: (
                x.get_text()
            ),soup.select("div.mui-12athy2-price_vista")))
        
        prices_card = list(map(lambda x: (
                x.get_text()
            ),soup.select("div.mui-10zdolh-price_total")))
        
        for i in range(len(titles)):
            if gpu.name not in titles[i]:
                continue
            
            if "XT" not in gpu.name and "XT" in titles[i]:
                continue
            
            
            price_regex: str = r"[\d.,]+"
            
            match_pix = re.search(price_regex, prices_pix[i])
            match_card = re.search(price_regex, prices_card[i])
            
            if not match_pix or not match_card:
                exit("Failed to format prices.")
            
            new_gpu = Gpu(
                titles[i],
                match_pix.group(),
                match_card.group()
            )
            
            gpu_list.append(new_gpu)
    
        if current_page == 1:
                pages = list(map(lambda x: (
                    x.get_text()
                    ),soup.select("a.mui-1ub82wb")))[1:-1]

                max_page = int(pages[-1])

        current_page += 1