# pylint: skip-file

from task_two import generate_receipt, add_to_basket, basket
import pytest

def reset_basket():
    basket.clear()


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    # Setup: fill with any logic you want
    reset_basket()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want


def test_add_to_basket():
    item = {
        "name": "Bread",
        "price": 1.80
    }
    basket = add_to_basket(item)
    assert generate_receipt(
        basket) == "Bread x 1 - £1.80\nTotal: £1.80"
    basket = add_to_basket(item)
    assert generate_receipt(
        basket) == "Bread x 2 - £3.60\nTotal: £3.60"


def test_empty_basket():
    assert generate_receipt([]) == "Basket is empty"


def test_generate_receipt_single_item():
    item = {'name': 'Apple', 'price': 0.5}
    add_to_basket(item)
    add_to_basket(item)
    result = generate_receipt(basket)
    assert result == "Apple x 2 - £1.00\nTotal: £1.00"


def test_generate_receipt_single_item_rounded():
    item = {'name': 'Apple', 'price': 0.555555}
    add_to_basket(item)
    add_to_basket(item)
    result = generate_receipt(basket)
    assert result == "Apple x 2 - £1.11\nTotal: £1.11"


def test_generate_receipt_multiple_items():
    item1 = {'name': 'Apple', 'price': 0.5}
    item2 = {'name': 'Banana', 'price': 0.3}
    add_to_basket(item1)
    add_to_basket(item1)
    add_to_basket(item2)
    result = generate_receipt(basket)
    assert result == "Apple x 2 - £1.00\nBanana x 1 - £0.30\nTotal: £1.30"


def test_generate_receipt_different_quantities():
    item1 = {'name': 'Apple', 'price': 0.5}
    item2 = {'name': 'Toffee', 'price': 0.3}
    add_to_basket(item1)
    add_to_basket(item1)
    add_to_basket(item1)
    add_to_basket(item2)
    add_to_basket(item2)
    result = generate_receipt(basket)
    assert result == "Apple x 3 - £1.50\nToffee x 2 - £0.60\nTotal: £2.10"


def test_generate_receipt_different_prices():
    item1 = {'name': 'Apple', 'price': 0.5}
    item2 = {'name': 'Banana', 'price': 0.7}
    item3 = {'name': 'Apple', 'price': 1}
    add_to_basket(item1)
    add_to_basket(item2)
    add_to_basket(item3)
    result = generate_receipt(basket)
    assert result == "Apple x 1 - £0.50\nBanana x 1 - £0.70\nApple x 1 - £1.00\nTotal: £2.20"
