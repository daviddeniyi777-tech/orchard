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
from models import Store
from forms import SellerApplicationForm, StoreForm


store = Blueprint(
    "store",
    __name__
)


# ==========================================
# SELLER APPLICATION
# ==========================================

@store.route(
    "/seller/apply",
    methods=["GET", "POST"]
)
@login_required
def seller_apply():

    if current_user.is_seller:

        flash(
            "You are already a seller.",
            "info"
        )

        return redirect(
            url_for("store.create_store")
        )


    if current_user.seller_request_status == "pending":

        flash(
            "Your seller application is already being reviewed.",
            "info"
        )

        return redirect(
            url_for("auth.account")
        )


    form = SellerApplicationForm()


    if form.validate_on_submit():

        current_user.seller_requested = True

        current_user.seller_request_status = "pending"

        db.session.commit()


        flash(
            "Your seller application has been submitted.",
            "success"
        )


        return redirect(
            url_for("auth.account")
        )


    return render_template(
        "stores/apply.html",
        form=form
    )


# ==========================================
# CREATE STORE
# ==========================================

@store.route(
    "/store/create",
    methods=["GET", "POST"]
)
@login_required
def create_store():

    if not current_user.is_seller:

        flash(
            "You must be an approved seller to create a store.",
            "error"
        )

        return redirect(
            url_for("auth.account")
        )


    if current_user.store:

        flash(
            "You already have a store.",
            "info"
        )

        return redirect(
            url_for("store.dashboard")
        )


    form = StoreForm()


    if form.validate_on_submit():

        new_store = Store(

            name=form.name.data,

            description=form.description.data,

            location=form.location.data,

            user_id=current_user.id
        )


        db.session.add(new_store)

        db.session.commit()


        flash(
            "Your Orchard store has been created! 🌱",
            "success"
        )


        return redirect(
            url_for("store.dashboard")
        )


    return render_template(
        "stores/create.html",
        form=form
    )


# ==========================================
# SELLER STORE DASHBOARD
# ==========================================

@store.route(
    "/store/dashboard"
)
@login_required
def dashboard():

    if not current_user.is_seller:

        flash(
            "You must be a seller to access the store dashboard.",
            "error"
        )

        return redirect(
            url_for("auth.account")
        )


    if not current_user.store:

        return redirect(
            url_for("store.create_store")
        )


    return render_template(
        "stores/dashboard.html",
        store=current_user.store
    )


# ==========================================
# PUBLIC STORE LIST
# ==========================================

@store.route(
    "/stores/"
)
def stores():

    stores = Store.query.order_by(
        Store.created_at.desc()
    ).all()


    return render_template(
        "stores/stores.html",
        stores=stores
    )


# ==========================================
# PUBLIC INDIVIDUAL STORE
# ==========================================

@store.route(
    "/stores/<int:store_id>"
)
def store_detail(store_id):

    store_item = Store.query.get_or_404(
        store_id
    )


    products = store_item.products


    return render_template(
        "stores/store.html",
        store=store_item,
        products=products
    )