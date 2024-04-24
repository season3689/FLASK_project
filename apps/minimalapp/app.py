import logging
import os
from email_validator import validate_email, EmailNotValidError
from flask import (Flask, 
                   render_template, 
                   url_for, 
                   request, 
                   redirect,
                   flash)
from flask_mail import Mail, Message
# from flask_debugtoolbar import DebugToolbarExtension

# 서버 프로그램 객체를 만든다.
# __name__: 실행 중인 모듈의 시스템 상의 이름
app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# toolbar = DebugToolbarExtension(app)

app.config["SECRET_KEY"] = "2lasdf2lasdf"

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

# 기본 주소("/")로 요청이 왔을 때 무엇을 할지 정의하기
@app.route("/")
def index() :
    return "Hello, Flask!"

# 메소드에 따른 처리를 원한다면 구별해서 정의할 수 있다. ex) ["GET", "POST"]
@app.route("/hello/<name>", methods=["GET","POST"],
           endpoint="hello-endpoint")
def hello(name):
    return f"hello, {name}!"

@app.route("/name/<id>")
def show_name(id):
    # 변수를 템플릿 엔진에게 건넨다.
    return render_template("index.html", name=id)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", id="AK", page="1"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


# post 요청이 오면, 필요한 데이터 관련 처리를 하고나서
# contact_complete.html 템플릿을 주는 get 처리를 하면서 마무리
@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        is_valid = True

        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        
        flash("문의해 주셔서 감사합니다")
        
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)