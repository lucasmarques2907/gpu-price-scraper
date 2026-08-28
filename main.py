import questionary
import requests
from bs4 import BeautifulSoup

def ask_user() -> tuple[str, list[str]]:
    gpu_name = ""
    while len(gpu_name) == 0:
        gpu_name = questionary.text("What GPU are you looking for? (ex: RX 9070 XT)").ask()
    
    options = questionary.checkbox(
        "What kind of information do you want to know?", choices=[
            "Specifications",
            "Price",
            "Comparison"
            ]
        ).ask()
    return gpu_name, options

def search_gpu(gpu_name: str) -> str:
    r = requests.get(f"https://technical.city/pt/search",params={"q":gpu_name})
    
    if r.status_code != 200:
        print(r.status_code)
        exit("Unable to fetch data.")
    
    soup = BeautifulSoup(r.text, "html.parser")

    gpus_found = list(map(lambda x: (
        x.get_text(strip=True)
    ), soup.select("strong.type")))

    if len(gpus_found) == 0:
        print("GPU Not found.")
        exit(0)
    
    selected_gpu = gpus_found[0]
    
    if len(gpus_found) > 1:
        selected_gpu:str = questionary.select("Choose your GPU: ", choices=gpus_found).ask()
    
    return selected_gpu
        
def main():
   gpu_name, options = ask_user()
   selected_gpu = search_gpu(gpu_name)
   
   
   
main()