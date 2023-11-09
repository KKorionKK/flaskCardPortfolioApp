from flask import Blueprint, request, render_template, make_response
from api.v1.services.forms import LoginForm, RegisterForm
from api.v1.services.auth import user_login, user_register
from api import db

auth_bp = Blueprint("authorization", __name__, url_prefix="/authorization")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user_data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        return user_login(user_data=user_data, db=db)

    return render_template("loginPage.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        user_data = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "username": request.form.get("username"),
        }
        return user_register(user_data=user_data, db=db)

    return render_template("loginPage.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
def logout():
    # TODO: проверку авторизации, в ином случае другой выход
    response = make_response()
    response.set_cookie("auth_token", "", expires=0)
    response.status = 200
    response.data = "Success"
    return response
