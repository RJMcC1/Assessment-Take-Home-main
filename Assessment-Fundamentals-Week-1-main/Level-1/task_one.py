
"""
Note: Do not add ANY variables to the global scope. This WILL break the tests.
The only variable you are allowed to use in the global scope is the basket below.
"""

basket = []


def add_to_basket(item: dict) -> list:
    basket.append(item)
    return basket


def generate_receipt(basket: list) -> str:
    if len(basket) == 0:
        return "Basket is empty"
    receipt = ""
    for item in basket:
        if item["price"] == 0.0:
            receipt += f"{item['name']} - Free\n"
        else:
            receipt += f"{item['name']} - £{item['price']:.2f}\n"
    total = sum(item['price'] for item in basket)
    receipt += f"Total: £{total:.2f}"
    return receipt


if __name__ == "__main__":
    add_to_basket({
        "name": "Bread",
        "price": 1.80
    })
    add_to_basket({
        "name": "Milk",
        "price": 0.80
    })
    add_to_basket({
        "name": "Butter",
        "price": 1.20
    })
    print(generate_receipt(basket))
