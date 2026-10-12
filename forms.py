
from flask_wtf import FlaskForm

from wtforms import (
    FileField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    PasswordField,
    SubmitField,
    HiddenField,
    TextAreaField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


# =========================================================
# LOGIN FORM
# =========================================================

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    next = HiddenField()

    submit = SubmitField(
        "Login"
    )


# =========================================================
# REGISTRATION FORM
# =========================================================

class RegistrationForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    submit = SubmitField(
        "Create Account"
    )


# =========================================================
# SELLER APPLICATION FORM
# =========================================================

class SellerApplicationForm(FlaskForm):

    store_name = StringField(
        "Store Name",
        validators=[
            DataRequired(),
            Length(min=2, max=120)
        ]
    )

    description = TextAreaField(
        "Tell us about your farm or business",
        validators=[
            DataRequired(),
            Length(min=10, max=500)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            DataRequired(),
            Length(min=2, max=150)
        ]
    )

    submit = SubmitField(
        "Apply to Become a Seller"
    )


# =========================================================
# STORE FORM
# =========================================================

class StoreForm(FlaskForm):

    name = StringField(
        "Store Name",
        validators=[
            DataRequired(),
            Length(min=2, max=120)
        ]
    )

    description = TextAreaField(
        "Store Description",
        validators=[
            DataRequired(),
            Length(min=10, max=500)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            DataRequired(),
            Length(min=2, max=150)
        ]
    )

    submit = SubmitField(
        "Create Store"
    )


# =========================================================
# PRODUCT FORM
# =========================================================

class ProductForm(FlaskForm):

    name = StringField(
        "Product Name",
        validators=[
            DataRequired(),
            Length(min=2, max=150)
        ]
    )

    description = TextAreaField(
        "Product Description",
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )

    price = FloatField(
        "Price",
        validators=[
            DataRequired()
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired()
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("fruit", "🍎 Fruit"),
            ("vegetable", "🥬 Vegetable"),
            ("seed", "🌱 Seed")
        ],
        validators=[
            DataRequired()
        ]
    )

    image = FileField(
        "Product Image"
    )

    submit = SubmitField(
        "Add Product"
    )


class CheckoutForm(FlaskForm):

    delivery_address = TextAreaField(
        "Delivery Address",
        validators=[
            DataRequired(),
            Length(min=10, max=300)
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=7, max=30)
        ]
    )

    payment_method = SelectField(
        "Payment Method",
        choices=[
            (
                "Cash on Delivery",
                "Cash on Delivery"
            )
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Place Order"
    )   

