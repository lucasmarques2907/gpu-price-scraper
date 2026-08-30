import questionary
from bs4 import BeautifulSoup
from curl_cffi import Session


def search_gpu(session: Session, gpu_name: str) -> str:
    r = session.get(f"https://technical.city/pt/search",params={"q":gpu_name})
    
    if r.status_code != 200:
        raise RuntimeError("Falha ao coletar dados.")
    
    soup = BeautifulSoup(r.text, "html.parser")

    gpus_found = list(map(lambda x: (
        x.get_text(" ", strip=True)
    ), soup.select("strong.type")))

    if len(gpus_found) == 0:
        raise ValueError("GPU não encontrada.")
    
    selected_gpu = gpus_found[0]
    
    if len(gpus_found) > 1:
        selected_gpu:str = questionary.select("Escolha sua GPU: ", choices=gpus_found).ask(kbi_msg="")
        if selected_gpu is None:
            raise KeyboardInterrupt
    
    return selected_gpu