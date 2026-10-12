
from flask import Blueprint, render_template

from models import Product, Store, User

main = Blueprint("main", __name__)


@main.route("/")
def home():

    # Latest active products from verified sellers
    featured_products = (
        Product.query
        .join(Store, Product.store_id == Store.id)
        .join(User, Store.user_id == User.id)
        .filter(
            Product.is_active.is_(True),
            User.is_seller.is_(True),
            User.is_verified.is_(True)
        )
        .order_by(Product.created_at.desc())
        .limit(8)
        .all()
    )

    # Real stores belonging to verified sellers
    verified_stores = (
        Store.query
        .join(User, Store.user_id == User.id)
        .filter(
            User.is_seller.is_(True),
            User.is_verified.is_(True)
        )
        .order_by(Store.created_at.desc())
        .limit(4)
        .all()
    )

    return render_template(
        "pages/home.html",
        featured_products=featured_products,
        verified_stores=verified_stores
    )

