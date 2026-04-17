# Level 1

You are tasked with writing the code to support a shopping basket for an e-commerce site. The application should allow a user to add items to the basket and calculate the total cost of the basket.

- `add_to_basket(item)` should take an item as a dictionary and return the basket with all the items so far in it
- `generate_receipt(basket)` should take a basket and return a receipt rendered in the following format

```
Bread - £1.80
Milk - £0.80
Butter - £1.20
Total: £3.80
```

## Edge Cases

Ensure you handle the following edge cases:

- If the basket is empty, the receipt should read `Basket is empty`
- If an item is added with a price of 0, the receipt should read `Free`. Total should still be calculated correctly.
