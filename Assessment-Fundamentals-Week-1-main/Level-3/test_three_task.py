# pylint: skip-file

"""Task 3 tests."""

from task_three import generate_invoice
import pytest

def test_gen_invoice():
    assert generate_invoice("""Bread x 2 - £3.60
Milk x 1 - £0.80
Butter x 1 - £1.20
Total: £5.60""") == """VAT RECEIPT

Bread x 2 - £2.88
Milk x 1 - £0.64
Butter x 1 - £0.96

Total: £4.48
VAT: £1.12
Total inc VAT: £5.60"""


def test_gen_invoice_2():
    receipt = """Bread x 2 - £3.60
Milk x 1 - £0.80
Butter x 1 - £1.20
Total: £5.60"""

    invoice = """VAT RECEIPT

Bread x 2 - £2.88
Milk x 1 - £0.64
Butter x 1 - £0.96

Total: £4.48
VAT: £1.12
Total inc VAT: £5.60"""

    assert generate_invoice(receipt) == invoice


def test_gen_invoice_one_item():
    receipt = """Bread x 2 - £3.60
Total: £3.60"""

    invoice = """VAT RECEIPT

Bread x 2 - £2.88

Total: £2.88
VAT: £0.72
Total inc VAT: £3.60"""

    assert generate_invoice(receipt) == invoice


def test_gen_invoice_empty():
    receipt = """Total: £0.00"""

    invoice = """VAT RECEIPT

Total: £0.00
VAT: £0.00
Total inc VAT: £0.00"""

    assert generate_invoice(receipt) == invoice


def test_gen_large_value():
    receipt = """Bread x 1000 - £3600.00
Total: £3600.00"""

    invoice = """VAT RECEIPT

Bread x 1000 - £2880.00

Total: £2880.00
VAT: £720.00
Total inc VAT: £3600.00"""

    assert generate_invoice(receipt) == invoice


def test_gen_rounding():
    receipt = """Bread x 10 - £36.20
Total: £36.20"""

    invoice = """VAT RECEIPT

Bread x 10 - £28.96

Total: £28.96
VAT: £7.24
Total inc VAT: £36.20"""

    assert generate_invoice(receipt) == invoice


def test_gen_rounding_multiple():
    receipt = """Bread x 10 - £36.20
Yogurt x 1 - £55.54
Total: £91.74"""

    print(generate_invoice(receipt))

    invoice = """VAT RECEIPT

Bread x 10 - £28.96
Yogurt x 1 - £44.43

Total: £73.39
VAT: £18.35
Total inc VAT: £91.74"""

    assert generate_invoice(receipt) == invoice
