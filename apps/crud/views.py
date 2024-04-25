from apps.app import db
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for
from apps.crud.forms import UserForm

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static"
)





# @app.route("/") = @crud

@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    user = User(
        username="이부장",
        email="flask2@exple5.com",
        password="비밀번호2"
    )

    db.session.add(user)
    db.session.commit()

    # user = db.session.query(User).filter_by().delete()
    # user.username = "김부장"
    # user.emali = "flask100@exple5.com"
    # user.password = "비밀번호100"
    # db.session.add(user)
    # db.session.commit()
    db.session.query(User).all()
    return "콘솔 확인"
    
@crud.route("/users/new", methods=["GET", "POST"])
def create_user() :
    form = UserForm()

    if form.validate_on_submit() :
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
def users():
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))