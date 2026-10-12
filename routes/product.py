from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)

from flask_login import (
    login_required,
    current_user
)

from flask import session
from extensions import db
import uuid
from models import Product
from models import Order
from models import OrderItem

from forms import ProductForm
from forms import CheckoutForm
import os

from werkzeug.utils import secure_filename

from flask import current_app


product = Blueprint(
    "product",
    __name__,
    url_prefix="/products"
)

def allowed_file(filename):

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in current_app.config[
        "ALLOWED_EXTENSIONS"
    ]

@product.route("/add", methods=["GET", "POST"])
@login_required
def add_product():

    if not current_user.is_seller:

        flash(
            "You must be a seller to add products.",
            "error"
        )

        return redirect(
            url_for("auth.account")
        )


    if not current_user.store:

        flash(
            "Create your store before adding products.",
            "error"
        )

        return redirect(
            url_for("store.create_store")
        )


    form = ProductForm()


    if form.validate_on_submit():

        image_filename = None


        # --------------------------------
        # HANDLE IMAGE
        # --------------------------------

        if form.image.data:

            file = form.image.data


            if not file.filename:

                flash(
                    "Please select a valid image.",
                    "error"
                )

                return render_template(
                    "products/add.html",
                    form=form
                )


            if not allowed_file(file.filename):

                flash(
                    "Invalid image type. Use PNG, JPG, JPEG or WEBP.",
                    "error"
                )

                return render_template(
                    "products/add.html",
                    form=form
                )


            original_filename = secure_filename(
                file.filename
            )


            if not original_filename:

                flash(
                    "Invalid image filename.",
                    "error"
                )

                return render_template(
                    "products/add.html",
                    form=form
                )


            extension = original_filename.rsplit(
                ".",
                1
            )[1].lower()


            image_filename = (
                f"{uuid.uuid4().hex}.{extension}"
            )


            upload_folder = current_app.config[
                "UPLOAD_FOLDER"
            ]


            os.makedirs(
                upload_folder,
                exist_ok=True
            )


            file.save(
                os.path.join(
                    upload_folder,
                    image_filename
                )
            )


        # --------------------------------
        # CREATE PRODUCT
        # --------------------------------

        new_product = Product(

            name=form.name.data,

            description=form.description.data,

            price=form.price.data,

            stock=form.stock.data,

            category=form.category.data,

            image_url=(
                f"images/products/{image_filename}"
                if image_filename
                else None
            ),

            store_id=current_user.store.id

        )


        db.session.add(
            new_product
        )

        db.session.commit()


        flash(
            "Product added successfully! 🍊",
            "success"
        )


        return redirect(
            url_for("product.products")
        )


    return render_template(
        "products/add.html",
        form=form
    )







@product.route("/")
def products():

    category = request.args.get("category", "").lower()

    query = Product.query.filter_by(is_active=True)

    if category in {"fruit", "vegetable", "seed"}:
        query = query.filter_by(category=category)

    products = query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "products/products.html",
        products=products,
        selected_category=category
    )



@product.route("/<int:product_id>")
def detail(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    return render_template(
        "products/detail.html",
        product=product
    )


@product.route("/cart")
def cart():

    cart_data = session.get("cart", {})

    cart_items = []

    total = 0


    for product_id, quantity in cart_data.items():

        item = Product.query.get(
            int(product_id)
        )

        if not item:
            continue


        subtotal = item.price * quantity

        total += subtotal


        cart_items.append({
            "product": item,
            "quantity": quantity,
            "subtotal": subtotal
        })


    return render_template(
        "products/cart.html",
        cart_items=cart_items,
        total=total
    )
@product.route(
    "/<int:product_id>/add-to-cart",
    methods=["POST"]
)
def add_to_cart(product_id):

    product = Product.query.get_or_404(
        product_id
    )


    quantity = request.form.get(
        "quantity",
        1,
        type=int
    )


    if quantity < 1:
        quantity = 1


    if quantity > product.stock:

        flash(
            "There is not enough stock available.",
            "error"
        )

        return redirect(
            url_for(
                "product.detail",
                product_id=product.id
            )
        )


    cart = session.get(
        "cart",
        {}
    )


    product_key = str(product.id)


    current_quantity = cart.get(
        product_key,
        0
    )


    new_quantity = (
        current_quantity + quantity
    )


    if new_quantity > product.stock:

        new_quantity = product.stock


    cart[product_key] = new_quantity


    session["cart"] = cart

    session.modified = True


    flash(
        f"{product.name} added to your basket! 🍊",
        "success"
    )


    return redirect(
        url_for("product.cart")
    )

@product.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
def remove_from_cart(product_id):

    cart = session.get(
        "cart",
        {}
    )


    cart.pop(
        str(product_id),
        None
    )


    session["cart"] = cart

    session.modified = True


    return redirect(
        url_for("product.cart")
    )

@product.route(
    "/checkout",
    methods=["GET", "POST"]
)
@login_required
def checkout():

    cart_data = session.get(
        "cart",
        {}
    )

    if not cart_data:

        flash(
            "Your basket is empty.",
            "error"
        )

        return redirect(
            url_for("product.products")
        )


    cart_items = []

    total = 0


    for product_id, quantity in cart_data.items():

        item = Product.query.get(
            int(product_id)
        )

        if not item:
            continue


        if quantity > item.stock:

            flash(
                f"Not enough stock for {item.name}.",
                "error"
            )

            return redirect(
                url_for("product.cart")
            )


        subtotal = (
            item.price * quantity
        )

        total += subtotal


        cart_items.append({
            "product": item,
            "quantity": quantity,
            "subtotal": subtotal
        })


    if not cart_items:

        session.pop("cart", None)

        flash(
            "Your basket is empty.",
            "error"
        )

        return redirect(
            url_for("product.products")
        )


    form = CheckoutForm()


    if form.validate_on_submit():

        order = Order(

            user_id=current_user.id,

            total=total,

            status="pending",

            delivery_address=(
                form.delivery_address.data
            ),

            phone=form.phone.data,

            payment_method=(
                form.payment_method.data
            )
        )

        db.session.add(order)


        for item in cart_items:

            product = item["product"]

            quantity = item["quantity"]

            subtotal = item["subtotal"]


            product.stock -= quantity


            order_item = OrderItem(

                order=order,

                product_id=product.id,

                product_name=product.name,

                price=product.price,

                quantity=quantity,

                subtotal=subtotal
            )

            db.session.add(order_item)


        db.session.commit()


        session.pop(
            "cart",
            None
        )


        flash(
            "Your order has been placed successfully! 🍊",
            "success"
        )


        return redirect(
            url_for(
                "product.order_confirmation",
                order_id=order.id
            )
        )


    return render_template(
        "products/checkout.html",
        form=form,
        cart_items=cart_items,
        total=total
    )

@product.route("/orders")
@login_required
def orders():

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()


    return render_template(
        "products/orders.html",
        orders=orders
    )

