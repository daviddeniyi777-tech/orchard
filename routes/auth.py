from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db
from models import User
from forms import RegistrationForm, LoginForm
from utils.emails import send_email


auth = Blueprint(
    "auth",
    __name__
)



@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("auth.account")
        )

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_username = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_username:

            flash(
                "That username is already taken.",
                "error"
            )

            return render_template(
                "auth/register.html",
                form=form
            )


        existing_email = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_email:

            flash(
                "That email is already registered.",
                "error"
            )

            return render_template(
                "auth/register.html",
                form=form
            )


        hashed_password = generate_password_hash(
            form.password.data
        )


        user = User(

            username=form.username.data,

            email=form.email.data,

            password=hashed_password

        )


        db.session.add(user)

        db.session.commit()

        send_email(
            user.email,
            "Welcome To Our Store",
            f"<p> Hi {user.username},</p><p>Your account has been created successfully.</p>"
            f"<p>Thank you for signing up!.</p>"
            f"<p>Best regards.</p>"
        )


        login_user(user)



        flash(
            "Welcome to Orchard!",
            "success"
        )


        return redirect(
            url_for("auth.account")
        )


    return render_template(
        "auth/register.html",
        form=form
    )



@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("auth.account")
        )

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()


        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash(
                "Welcome back!",
                "success"
            )

            next_page = form.next.data

            if next_page:
                return redirect(next_page)

            return redirect(
                url_for("auth.account")
            )


        flash(
            "Incorrect email or password.",
            "error"
        )


    return render_template(
        "auth/login.html",
        form=form
    )



@auth.route("/account")
@login_required
def account():

    return render_template(
        "auth/account.html"
    )




@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("main.home")
    )


