import questionary
from bs4 import BeautifulSoup
from curl_cffi import Session

def search_gpu(session: Session, gpu_name: str) -> str:
    r = session.get(f"https://technical.city/pt/search",params={"q":gpu_name})
    
    if r.status_code != 200:
        exit("Falha ao coletar dados.")
    
    soup = BeautifulSoup(r.text, "html.parser")

    gpus_found = list(map(lambda x: (
        x.get_text(strip=True)
    ), soup.select("strong.type")))

    if len(gpus_found) == 0:
        exit("GPU não encontrada.")
    
    selected_gpu = gpus_found[0]
    
    if len(gpus_found) > 1:
        selected_gpu:str = questionary.select("Choose your GPU: ", choices=gpus_found).ask()
    
    return selected_gpu