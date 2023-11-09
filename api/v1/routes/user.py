from flask import Blueprint, request, render_template
from api.v1.services.users import get_user_by_username, card_create, get_user_by_jwt
from api.v1.services.auth import authorization_required
from api import db
from api.v1.services.forms import CreateForm

user_bp = Blueprint("user", __name__)


@user_bp.get("/<username>")
def get_user(username):
    user = get_user_by_username(username=username, db=db)
    if user:
        return render_template("userPage.html", **user.to_dict())
    else:
        return ("Пользователь не найден", 404)


@user_bp.route("/create", methods=["GET", "POST"])
@authorization_required
def create_card():
    form = CreateForm()
    if request.method == "POST":
        card_data = {
            "header": request.form.get("header"),
            "content": request.form.get("content"),
            "links": request.form.get("link"),
            "emoji": request.form.get("emoji"),
            "picture": request.form.get("file"),  # TODO: подумать
        }
        user_uuid = get_user_by_jwt(request.cookies.get("auth_token"), db)
        return card_create(
            card_data=card_data,
            db=db,
            user_uuid=user_uuid,
        )

    return render_template("createCard.html", form=form)
