# pylint: skip-file

from task_one import generate_receipt, add_to_basket, basket
import pytest


def reset_basket():
    basket.clear()


@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    # Setup: fill with any logic you want
    reset_basket()
    yield  # this is where the testing happens
    # Teardown : fill with any logic you want


def test_get_total():
    basket = [
        {
            "name": "Bread",
            "price": 1.80
        },
        {
            "name": "Milk",
            "price": 0.80
        },
        {
            "name": "Butter",
            "price": 1.20
        }
    ]
    assert generate_receipt(
        basket) == "Bread - £1.80\nMilk - £0.80\nButter - £1.20\nTotal: £3.80"


def test_add_to_basket_same():
    item = {
        "name": "Milk",
        "price": 1.80
    }
    add_to_basket(item)
    add_to_basket(item)
    assert generate_receipt(
        basket) == "Milk - £1.80\nMilk - £1.80\nTotal: £3.60"


def test_add_to_basket_different():
    item = {
        "name": "Milk",
        "price": 1.80
    }
    add_to_basket(item)
    item = {
        "name": "Donuts",
        "price": 1.10
    }
    add_to_basket(item)
    assert generate_receipt(
        basket) == "Milk - £1.80\nDonuts - £1.10\nTotal: £2.90"


def test_rounding():
    reset_basket()
    basket = [
        {
            "name": "Snozberrys",
            "price": 1.8888888
        }
    ]
    assert generate_receipt(
        basket) == "Snozberrys - £1.89\nTotal: £1.89"


def test_rounding_down():
    reset_basket()
    basket = [
        {
            "name": "Yogurt",
            "price": 1.881
        }
    ]
    assert generate_receipt(
        basket) == "Yogurt - £1.88\nTotal: £1.88"


def test_rounding_whole():
    reset_basket()
    basket = [
        {
            "name": "Yogurt",
            "price": 1.00000
        }
    ]
    assert generate_receipt(
        basket) == "Yogurt - £1.00\nTotal: £1.00"


def test_generate_receipt_empty_basket():
    basket = []
    expected_output = 'Basket is empty'
    assert generate_receipt(basket) == expected_output


def test_generate_receipt_single_item():
    basket = [{'name': 'apple', 'price': 1.0}]
    expected_output = 'apple - £1.00\nTotal: £1.00'
    assert generate_receipt(basket) == expected_output


def test_generate_receipt_large_basket():
    basket = [{'name': 'apple', 'price': 1.0}] * 100000
    result = generate_receipt(basket)
    assert result.endswith('Total: £100000.00')


def test_generate_receipt_large_and_small_price():
    basket = [{'name': 'cheap_item', 'price': 0.01},
              {'name': 'expensive_item', 'price': 1000000}]
    expected_output = 'cheap_item - £0.01\nexpensive_item - £1000000.00\nTotal: £1000000.01'
    assert generate_receipt(basket) == expected_output


def test_generate_receipt_duplicate_names():
    basket = [{'name': 'apple', 'price': 1.0}, {'name': 'apple', 'price': 2.0}]
    expected_output = 'apple - £1.00\napple - £2.00\nTotal: £3.00'
    assert generate_receipt(basket) == expected_output


def test_generate_receipt_zero_price():
    basket = [{'name': 'free_item', 'price': 0.0}]
    expected_output = 'free_item - Free\nTotal: £0.00'
    assert generate_receipt(basket) == expected_output


def test_generate_receipt_special_characters_and_spaces_in_name():
    basket = [{'name': 'item with spaces', 'price': 1.0}, {
        'name': 'item_with_underscore', 'price': 2.0}, {'name': 'item-with-dash', 'price': 3.0}]
    expected_output = 'item with spaces - £1.00\nitem_with_underscore - £2.00\nitem-with-dash - £3.00\nTotal: £6.00'
    assert generate_receipt(basket) == expected_output
