from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from extensions import db

from models import (
    User,
    Store,
    Product,
    Order
)


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def admin_required():
    return current_user.is_authenticated and current_user.is_admin


@admin.route("/")
@login_required
def dashboard():

    if not admin_required():
        flash(
            "You do not have permission to access the admin area.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    total_users = User.query.count()

    total_sellers = User.query.filter_by(
        is_seller=True
    ).count()

    total_stores = Store.query.count()

    total_products = Product.query.count()

    total_orders = Order.query.count()


    pending_sellers = User.query.filter_by(
        seller_request_status="pending"
    ).count()


    return render_template(
        "admin/dashboard.html",

        total_users=total_users,

        total_sellers=total_sellers,

        total_stores=total_stores,

        total_products=total_products,

        total_orders=total_orders,

        pending_sellers=pending_sellers
    )


@admin.route("/seller-applications")
@login_required
def seller_applications():

    if not admin_required():
        flash(
            "Access denied.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    users = User.query.filter_by(
        seller_request_status="pending"
    ).order_by(
        User.id.desc()
    ).all()


    return render_template(
        "admin/seller_applications.html",
        users=users
    )


@admin.route(
    "/approve-seller/<int:user_id>",
    methods=["POST"]
)
@login_required
def approve_seller(user_id):

    if not admin_required():
        flash(
            "Access denied.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    user = User.query.get_or_404(
        user_id
    )


    user.is_seller = True

    user.is_verified = True

    user.seller_requested = True

    user.seller_request_status = "approved"


    db.session.commit()


    flash(
        f"{user.username} is now a verified Orchard seller.",
        "success"
    )


    return redirect(
        url_for("admin.seller_applications")
    )


@admin.route(
    "/reject-seller/<int:user_id>",
    methods=["POST"]
)
@login_required
def reject_seller(user_id):

    if not admin_required():
        flash(
            "Access denied.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    user = User.query.get_or_404(
        user_id
    )


    user.seller_requested = False

    user.seller_request_status = "rejected"

    user.is_seller = False

    user.is_verified = False


    db.session.commit()


    flash(
        f"{user.username}'s seller application was rejected.",
        "info"
    )


    return redirect(
        url_for("admin.seller_applications")
    )


@admin.route("/orders")
@login_required
def orders():

    if not admin_required():
        flash(
            "Access denied.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()


    return render_template(
        "admin/orders.html",
        orders=orders
    )