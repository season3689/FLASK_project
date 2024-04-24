from flask import Blueprint, render_template

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