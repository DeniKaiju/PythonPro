from dataclasses import dataclass, field
from typing import List

EXCHANGE_RATES = {
    "CHF": {
        "CHF": 1.0,
        "UAH": 42.99,
        "USD": 0.87,
        "EUR": 1.05,
        "GBP": 0.90,
        "PLN": 4.59,
    },
    "UAH": {
        "CHF": 0.023,
        "UAH": 1.0,
        "USD": 0.026,
        "EUR": 0.024,
        "GBP": 0.021,
        "PLN": 0.11,
    },
    "USD": {
        "CHF": 0.88,
        "UAH": 37.97,
        "USD": 1.0,
        "EUR": 0.93,
        "GBP": 0.79,
        "PLN": 4.0,
    },
    "EUR": {
        "CHF": 0.95,
        "UAH": 40.91,
        "USD": 1.08,
        "EUR": 1.0,
        "GBP": 0.85,
        "PLN": 4.32,
    },
    "GBP": {
        "CHF": 1.12,
        "UAH": 48.09,
        "USD": 1.27,
        "EUR": 1.18,
        "GBP": 1.0,
        "PLN": 5.08,
    },
    "PLN": {
        "CHF": 0.22,
        "UAH": 9.74,
        "USD": 0.25,
        "EUR": 0.23,
        "GBP": 0.20,
        "PLN": 1.0,
    },
}

MIDDLE_CURRENCY = "CHF"


def convert(value: float, currency_from: str, currency_to: str) -> float:
    coefficient: float = EXCHANGE_RATES[currency_from][currency_to]
    return value * coefficient


@dataclass
class Price:
    value: float
    currency: str

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=(self.value + other.value), currency=self.currency
            )

        left_in_middle: float = convert(
            value=self.value,
            currency_from=self.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle + right_in_middle
        total_in_left_currency: float = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=self.currency,
        )

        return Price(value=total_in_left_currency, currency=self.currency)

    def __sub__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(
                value=(self.value - other.value), currency=self.currency
            )

        left_in_middle: float = convert(
            value=self.value,
            currency_from=self.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        right_in_middle: float = convert(
            value=other.value,
            currency_from=other.currency,
            currency_to=MIDDLE_CURRENCY,
        )

        total_in_middle: float = left_in_middle - right_in_middle
        total_in_left_currency: float = convert(
            value=total_in_middle,
            currency_from=MIDDLE_CURRENCY,
            currency_to=self.currency,
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
