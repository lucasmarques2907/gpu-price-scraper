import questionary
from search_gpu import search_gpu
from search_price import search_price
from curl_cffi import requests
from gpu import Gpu

session = requests.Session( impersonate="chrome150")

def ask_user() -> str:
    gpu_name = ""
    while len(gpu_name) == 0:
        gpu_name = questionary.text("Qual GPU está procurando? (ex: RX 9070 XT)").ask()

    return gpu_name


def main():
    gpu_name = ask_user()
    selected_gpu = search_gpu(session, gpu_name)
    gpu = search_price(session, Gpu(selected_gpu))
    print(gpu)

main()
