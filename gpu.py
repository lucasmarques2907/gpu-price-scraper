class Gpu():
    name: str
    price_pix: float | None
    price_card: float | None
    
    def __init__(self, name: str, price_pix: float | None = None, price_card: float | None = None) -> None:
        self.name = name
        self.price_pix = price_pix
        self.price_card = price_card
        
    def __repr__(self) -> str:
        return f"Name: {self.name} | Preço PIX: R$ {self.price_pix} | Preço cartão: R$ {self.price_card}"