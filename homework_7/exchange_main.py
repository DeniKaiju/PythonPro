from dataclasses import dataclass, field
from typing import List, Dict, Any
from exchange_constants import ALPHAVANTAGE_API_KEY, MIDDLE_CURRENCY
import requests
import json
from datetime import datetime


def log_exchange_request(currency_from: str, currency_to: str, rate: float):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = {
        "currency_from": currency_from,
        "currency_to": currency_to,
        "rate": rate,
        "timestamp": timestamp,
    }
    with open("logs.json", "r+") as file:
        data = json.load(file)
        data["results"].append(log_data)
        file.seek(0)
        json.dump(data, file, indent=4)


def convert(value: float, currency_from: str, currency_to: str) -> float:
    # coefficient: float = EXCHANGE_RATES[currency_from][currency_to]
    url = ("https://www.alphavantage.co/query?"
           f"function=CURRENCY_EXCHANGE_RATE"
           f"&from_currency={currency_from}"
           f"&to_currency={currency_to}"
           F"&apikey={ALPHAVANTAGE_API_KEY}")
    response: requests.Response = requests.get(url)
    result: Dict[str, Any] = response.json()
    coefficient: float = float(
        result["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    )
    log_exchange_request(currency_from, currency_to, coefficient)
    return value * coefficient


def convert_currency(
    value: float, currency_from: str, currency_to: str
) -> float:
    left_in_middle: float = convert(
        value=value,
        currency_from=currency_from,
        currency_to=MIDDLE_CURRENCY,
    )

    right_in_middle: float = convert(
        value=value,
        currency_from=currency_to,
        currency_to=MIDDLE_CURRENCY,
    )

    total_in_middle: float = left_in_middle + right_in_middle
    total_in_left_currency: float = convert(
        value=total_in_middle,
        currency_from=MIDDLE_CURRENCY,
        currency_to=currency_from,
    )

    return total_in_left_currency


@dataclass
class Price:
    value: float
    currency: str

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=(self.value + other.value), currency=self.currency
            )

        total_in_left_currency = convert_currency(
            self.value, self.currency, other.currency
        )

        return Price(value=total_in_left_currency, currency=self.currency)

    def __sub__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=(self.value - other.value), currency=self.currency
            )

        total_in_left_currency = convert_currency(
            self.value, self.currency, other.currency
        )

        return Price(value=total_in_left_currency, currency=self.currency)


price_hotel = Price(100, "UAH")
price_excursion = Price(500, "UAH")
price_flight = Price(200, "UAH")
price_car_rental = Price(180, "CHF")
price_glovo = Price(400, "USD")
price_rebate = Price(200, "USD")


@dataclass
class Product:
    name: str
    price: Price


hotel = Product("Hilton London", price_hotel)
excursion = Product("Excursion London Old Town", price_excursion)
flight = Product("Ryanair ticket Warsaw - London", price_flight)
car_rental = Product("Car rental class B, 5 days", price_car_rental)
food = Product("Завтраки с Glovo", price_glovo)
discount = Product("Скидка Booking", price_rebate)


@dataclass
class PaymentProcessor:
    shopping_cart: List["Product"] = field(default_factory=list)

    def checkout(self, product: Product):
        self.shopping_cart.append(product)

    def calculate_total(self) -> Price:
        total_price_value = sum(
            convert(
                product.price.value, product.price.currency, MIDDLE_CURRENCY
            )
            for product in self.shopping_cart
        )
        total_price_in_middle = Price(total_price_value, MIDDLE_CURRENCY)
        total_price = convert(
            total_price_in_middle.value,
            MIDDLE_CURRENCY,
            self.shopping_cart[0].price.currency,
        )
        return Price(total_price, self.shopping_cart[0].price.currency)


processor = PaymentProcessor()

processor.checkout(hotel)
processor.checkout(excursion)
processor.checkout(flight)
processor.checkout(car_rental)
processor.checkout(food)
processor.checkout(discount)

total = processor.calculate_total()
print("Список покупок:")
for product in processor.shopping_cart:
    print(f"{product.name}: {product.price.value} {product.price.currency}")
print(f"\nСуммарная стоимость: {total.value} {total.currency}")
