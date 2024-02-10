from typing import Dict, List

currency_exchange: Dict[str, float] = {
    'CHF': 1.0,
    'UAH': 42.99,
    'USD': 0.87,
    'EUR': 0.94,
    'GBP': 0.90,
    'PLN': 4.59
}

class Price:
    def __init__(self, value: int, currency: str) -> None:
        self.value: int = value
        self.currency: str = currency

price_hotel = Price(100, 'USD')
price_excursion = Price(500, 'UAH')
price_flight = Price(200, 'EUR')
price_car_rental = Price(180, 'CHF')
price_glovo = Price(400, 'PLN')

class Product:
    def __init__(self, name: str, price: Price) -> None:
        self.name = name
        self.price = price

hotel = Product("Hilton London", price_hotel)
excursion = Product("Excursion London Old Town", price_excursion)
flight = Product("Ryanair ticket Warsaw - London", price_flight)
car_rental = Product("Car rental class B, 5 days", price_car_rental)
food = Product("Завтраки с Glovo", price_glovo)

class PaymentProcessor:
    def __init__(self, currency_exchange: Dict[str, float]) -> None:
        self.currency_exchange = currency_exchange
        self.shopping_cart: List[Product] = []

    def checkout(self, product: Product):
        self.shopping_cart.append(product)

    def calculate_total_in_uah(self) -> float:
        total_price_uah = 0
        for product in self.shopping_cart:
            price_in_product_currency = product.price.value
            if product.price.currency != 'UAH':
                if product.price.currency == 'CHF':
                    price_in_uah = price_in_product_currency* self.currency_exchange['UAH']
                else:
                    price_in_chf = price_in_product_currency / self.currency_exchange[product.price.currency]
                    price_in_uah = price_in_chf * self.currency_exchange['UAH']
            else:
                price_in_uah = price_in_product_currency

            total_price_uah += price_in_uah
        
        total_price_uah = round(total_price_uah, 2)

        return total_price_uah

processor = PaymentProcessor(currency_exchange)

processor.checkout(hotel)
processor.checkout(excursion)
processor.checkout(flight)
processor.checkout(car_rental)
processor.checkout(food)

total_uah = processor.calculate_total_in_uah()
print("Список покупок:")
for product in processor.shopping_cart:
    print(f"{product.name}: {product.price.value} {product.price.currency}")
print(f"\nСуммарная стоимость в UAH: {total_uah} UAH")


