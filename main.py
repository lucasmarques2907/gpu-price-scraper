import questionary
from search_gpu import search_gpu
from search_price import search_price
from curl_cffi import requests
from gpu import Gpu, format_brl
from rich.console import Console
from rich.panel import Panel

console = Console()
session = requests.Session( impersonate="chrome150")


def ask_user() -> str:
    while True:
        gpu_name = questionary.text("Qual GPU está procurando? (ex: RX 9070 XT)").ask(kbi_msg="")
        if gpu_name is None:
            raise KeyboardInterrupt
        if gpu_name.strip():
            return gpu_name


def main():
    try:
        gpu_name = ask_user()
        
        with console.status("Buscando GPUs..."):
            selected_gpu = search_gpu(session, gpu_name)
        
        with console.status(f"Buscando preços de {selected_gpu}..."):
            gpu = search_price(session, Gpu(selected_gpu))
        
        console.print(Panel(
            f"[bold cyan]{gpu.name}[/bold cyan]\n\n"
            f"[green]PIX[/green]     R$ {format_brl(gpu.price_pix)}\n"
            f"[yellow]Cartão[/yellow]  R$ {format_brl(gpu.price_card)}\n\n"
            f"[dim]{gpu.url}[/dim]",
            title="Menor preço",
            border_style="green",
            padding=(1, 2),
        ))
    except (RuntimeError, ValueError) as e:
        print(f"Erro: {e}")
    except KeyboardInterrupt:
        print("\nCancelado.")


main()
