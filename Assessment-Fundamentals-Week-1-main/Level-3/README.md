# Level 3

## Setup

No setup needed

## Instructions

Given a 'receipt' string, convert it into an 'invoice' string.

Invoices are used by businesses and so have slightly different information on them. They also have a different format.

VAT is calculated as 20% of every line item

For the receipt

```
Bread x 2 - £3.60
Milk x 1 - £0.80
Butter x 1 - £1.20
Total: £5.60
```

The invoice would look like this:

```
VAT RECEIPT

Bread x 2 - £2.88
Milk x 1 - £0.64
Butter x 1 - £0.96

Total: £4.48
VAT: £1.12
Total inc VAT: £5.60
```

## Tips

- Remember to check for your edge cases. What happens if the receipt given doesn't have any items?
- Don't worry about `Free` items. We won't be giving any items that are free in the tests.
