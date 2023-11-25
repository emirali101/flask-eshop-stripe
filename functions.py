import stripe
from flask import  url_for
from forms import OrderForm

def stripe_charge():
    form = OrderForm()
    total_paid = float(''.join(form.price_total.raw_data))
    checkout = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "unit_amount": int(total_paid * 100),
                    "product_data": {"name": "Your Order"},
                    "currency": "eur",
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=url_for('success', _external=True),
        cancel_url=url_for('failed', _external=True),
    )
    url = checkout.url
    return url