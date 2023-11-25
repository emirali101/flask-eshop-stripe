import os
import datetime
import stripe
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import OrderForm
from models import db, Product, Order, PaidOrder
from functions import stripe_charge


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
stripe.api_key = os.environ["STRIPE_SECRET"]


db.init_app(app)


with app.app_context():
    db.create_all()


@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}


@app.route('/', methods=["GET", "POST"])
def home():
    all_id = db.session.query(Product).all()
    data = (request.form.to_dict())
    sorting = str(*(data.values()))
    if sorting == "id":
        reverse = True
    else:
        reverse = False
    return render_template("index.html", all_id=all_id, sorting=sorting, selected=sorting, reverse=reverse)


@app.route('/add_chart<int:num>')
def add_chart(num):
    all_id = db.session.query(Product).all()
    id = all_id[num - 1]
    order_product = Order(title=id.title, price=id.price)
    db.session.add(order_product)
    db.session.commit()
    flash("Item added to cart")
    return redirect(url_for('home'))


@app.route('/show_cart')
def show_cart():
    form = OrderForm()
    cart_items = db.session.query(Order).all()
    return render_template("show_cart.html", cart=cart_items, form=form)


@app.route('/remove_item<int:num>')
def remove_item(num):
    item_id = num
    item_to_remove = Order.query.get(item_id)
    db.session.delete(item_to_remove)
    db.session.commit()
    return redirect(url_for('show_cart'))


@app.route('/clear_cart')
def clear_cart():
    db.session.query(Order).delete()
    db.session.commit()
    return redirect(url_for('show_cart'))


@app.route('/make_order', methods=["POST"])
def make_order():
    form = OrderForm()
    cart_item_titles = db.session.query(Order.title).all()
    try:
        new_order = PaidOrder(
            title=form.email.data,
            description=''.join(str(l) for l in cart_item_titles),
            date=str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
            shipping_address=form.shipping_address.data,
            total_paid=float(''.join(form.price_total.raw_data)),
        )
        url = stripe_charge()
        db.session.add(new_order)
        db.session.query(Order).delete()
        db.session.commit()
    except Exception as exception:
        return str(exception)
    return redirect(url)


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/failed')
def failed():
    return render_template("failed.html")


if __name__ == "__main__":
    app.run(debug=True)
