
import datetime

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    session,
    request
)

from flask_login import current_user, login_user, logout_user

from image_labeller import db
from image_labeller.auth import bp
from image_labeller.schema import User
from image_labeller.auth.forms import LoginForm, RegistrationForm

def auto_logout():
    # Automatically logout after a period of inactivity
    # https://stackoverflow.com/a/40914886/1154005
    session.permanent = True
    current_app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    session.modified = True


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # log the user in if exists
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for("auth.login"))
        login_user(user)

        # record last_active time
        current_user.last_active = datetime.datetime.utcnow()
        db.session.commit()

        # Get the next page from the request (default to index)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")


        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))



@bp.route("/register", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))
    return render_template(
        "auth/register.html", title="Register", form=form
    )


@bp.route("/not_confirmed")
def not_confirmed():
    if current_user.is_anonymous or not current_user.is_confirmed:
        flash("Please login before accessing this page.")
        return redirect(url_for("auth.login"))
    else:
        flash("Account is already confirmed.")
        return redirect(url_for("main.index"))
