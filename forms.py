from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email


class OrderForm(FlaskForm):
    name = StringField("Name", render_kw={'placeholder': 'Full name*'},
                       validators=[DataRequired("Please enter your name.")])
    email = StringField("Email", render_kw={'placeholder': 'Email*'},
                        validators=[DataRequired("Please enter your email address."), Email()])
    country = StringField("Country", render_kw={'placeholder': 'Country*'},
                          validators=[DataRequired("Please enter your country.")])
    shipping_address = TextAreaField("Shipping address", render_kw={'placeholder': 'Shipping address*'},
                                     validators=[DataRequired("Please enter shipping address.")])
    price_total = HiddenField("Price_total")
    submit = SubmitField("Pay")

