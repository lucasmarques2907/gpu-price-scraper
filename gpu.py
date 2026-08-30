def format_brl(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

class Gpu():
    name: str
    price_pix: float | None
    price_card: float | None
    url: str | None

    def __init__(self, name: str, price_pix: float | None = None, price_card: float | None = None, url: str | None = None) -> None:
        self.name = name.upper()
        self.price_pix = price_pix
        self.price_card = price_card
        self.url = url

    def __repr__(self) -> str:
        return f"""
Nome: {self.name}
Preço PIX: R$ {format_brl(self.price_pix)}
Preço cartão: R$ {format_brl(self.price_card)}
Link: {self.url}
    """