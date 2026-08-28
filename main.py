import questionary
from search_gpu import search_gpu
from search_price import search_price
from curl_cffi import requests
from gpu import Gpu

session = requests.Session( impersonate="chrome150")


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


def main():
#    gpu_name, options = ask_user()
#    selected_gpu = search_gpu(session, gpu_name)
   
#    if "Price" in options:
        # search_price(gpu_name)
    selected_gpu = Gpu("RX 9060")
    search_price(session, selected_gpu)


main()