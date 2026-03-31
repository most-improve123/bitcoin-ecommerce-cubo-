import csv
from invoice import generate_invoice

def load_products():
    products = []
    with open('src/products.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "name": row["nombre"],
                "price_usd": float(row["precio_usd"]),
                "price_btc": float(row["precio_usd"]) / 50000  # 1 BTC = $50,000 (ejemplo)
            })
    return products

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        self.items.append({
            "product": product,
            "quantity": quantity,
            "total_usd": product["price_usd"] * quantity,
            "total_btc": product["price_btc"] * quantity
        })

    def generate_invoice(self, customer_name):
        total_btc = sum(item["total_btc"] for item in self.items)
        invoice_path = generate_invoice(customer_name, self.items, total_btc)
        return invoice_path

def validate_payment(invoice_path, paid_amount_btc):
    # Simular que el total de la factura es 0.0004 BTC (ejemplo)
    expected_amount = 0.0004
    if paid_amount_btc == expected_amount:
        return "✅ Pago válido. Transacción confirmada."
    else:
        return f"❌ Pago inválido. Se esperaba {expected_amount} BTC, pero se pagó {paid_amount_btc} BTC."

if __name__ == "__main__":
    products = load_products()
    cart = ShoppingCart()
    cart.add_item(products[3], 2)  # Agregar 2 libros al carrito
    invoice_path = cart.generate_invoice("Levi Palacios")
    print(f"Factura generada: {invoice_path}")

    # Ejemplo de uso de validate_payment:
    print(validate_payment(invoice_path, 0.0004))  # Simula un pago correcto