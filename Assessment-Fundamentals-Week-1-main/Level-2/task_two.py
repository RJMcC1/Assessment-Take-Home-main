"""
Note: Do not add ANY variables to the global scope. This WILL break the tests.
The only variable you are allowed to use in the global scope is the basket below.
"""

basket = []

#####
#
# COPY YOUR CODE FROM LEVEL 1 BELOW
#
#####


def add_to_basket(item: dict) -> list:
    basket.append(item)
    return basket


def multiple_foods_with_count(basket: list) -> list:
    """This function will remove duplicate items from basket and add count of them"""
    new_basket = []
    for item in basket:
        if item not in new_basket:
            count = basket.count(item)
            item["count"] = count
            new_basket.append(item)
    if count > 1:
        for item in new_basket:
            if item["count"] > 1:
                item["price"] = item["price"] * item["count"]
    return new_basket



def generate_receipt(basket: list) -> str:
    if len(basket) == 0:
        return "Basket is empty"
    receipt = ""
    new_basket = multiple_foods_with_count(basket)
    for item in new_basket:
        if item["price"] == 0.0:
            receipt += f"{item['name']} x {item['count']} - Free\n"
        else:
            receipt += f"{item['name']} x {item['count']} - £{item['price']:.2f}\n"
    total = sum(item['price'] for item in basket)
    receipt += f"Total: £{total:.2f}"
    return receipt

#####
#
# COPY YOUR CODE FROM LEVEL 1 ABOVE
#
#####


if __name__ == "__main__":
    add_to_basket({
        "name": "Bread",
        "price": 1.80
    })
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
