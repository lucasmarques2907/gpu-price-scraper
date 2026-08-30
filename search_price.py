import re
from bs4 import BeautifulSoup
from curl_cffi import Session
from gpu import Gpu
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

BATCH = 4

def search_price(session: Session, gpu: Gpu) -> Gpu:
    gpu_list: list[Gpu] = []

    html = fetch_page(session, gpu, 1)
    page_gpus, exhausted = parse_products(html, gpu)
    gpu_list.extend(page_gpus)
    if exhausted:
        return get_lowest_price(gpu_list)

    max_page = parse_max_page(html)

    with ThreadPoolExecutor(max_workers=BATCH) as pool:
        for start in range(2, max_page + 1, BATCH):
            pages = range(start, min(start + BATCH, max_page + 1))
            htmls = list(pool.map(lambda p: fetch_page(session, gpu, p), pages))

            for h in htmls:
                page_gpus, exhausted = parse_products(h, gpu)
                gpu_list.extend(page_gpus)
                if exhausted:
                    return get_lowest_price(gpu_list)
    
    return get_lowest_price(gpu_list)

def fetch_page(session: Session, gpu: Gpu, page: int) -> str:
        r = session.get(
            "https://www.pichau.com.br/search",
            params={
                "q": gpu.name,
                "product_category": "6459",
                "page": page
            }
        )

        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code} na página {page}")

        return r.text


def parse_products(html: str, gpu: Gpu) -> tuple[list[Gpu], bool]:
    soup = BeautifulSoup(html, "html.parser")
    found: list[Gpu] = []
    price_regex = r"\d{1,3}(?:,\d{3})*\.\d{2}"

    for card in soup.select("a:has(h2)"):
        title_el = card.select_one("h2")
        pix_el = card.select_one("div.mui-12athy2-price_vista")
        card_el = card.select_one("div.mui-10zdolh-price_total")

        if not title_el:
            continue
        if not pix_el or not card_el:
            return found, True

        title = title_el.get_text()

        if not matches(gpu.name, title):
            continue

        match_pix = re.search(price_regex, pix_el.get_text())
        match_card = re.search(price_regex, card_el.get_text())
        if not match_pix or not match_card:
            raise ValueError(f"Preço em formato inesperado: {title}")

        href = card.get("href")
        url = urljoin("https://www.pichau.com.br", href) if href else None
        found.append(Gpu(
            title,
            parse_price(match_pix.group()),
            parse_price(match_card.group()), 
            url
            ))
    return found, False

def parse_max_page(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    nums = [t.get_text() for t in soup.select("a.mui-1ub82wb")]
    nums = [int(n) for n in nums if n.strip().isdigit()]
    return max(nums) if nums else 1

def get_lowest_price(gpus :list[Gpu]) -> Gpu:
    if len(gpus) == 0:
        raise ValueError("Nenhuma GPU encontrada.")
    
    lowest_price = float("inf")
    gpu_to_return = gpus[0]
    
    for gpu in gpus:
        if gpu.price_pix < lowest_price:
            lowest_price = gpu.price_pix
            gpu_to_return = gpu
    
    return gpu_to_return

def parse_price(text: str) -> float:
    return float(text.replace(",", ""))

def matches(gpu_name: str, title: str) -> bool:
    t = title.upper().replace(" ", "")
    return all(token in t for token in gpu_name.upper().split())