from flask import Flask, render_template, url_for, redirect, request, flash, abort
from datetime import datetime
import smtplib
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from forms import AddForm, RegisterForm, LoginForm, CommentForm
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import hashlib
import os



OWN_EMAIL = os.environ.get("OWN_EMAIL")
OWN_PASSWORD = os.environ.get("OWN_PASSWORD")

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Bootstrap5(app)
app.jinja_env.globals['current_year'] = datetime.now().year

ckeditor = CKEditor(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")

db = SQLAlchemy(app)

migrate = Migrate(app, db)



login_manager = LoginManager()
login_manager.init_app(app)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def gravatar_url(email, size=100, rating='g', default='retro', force_default=False):
    hash_value = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}&f={force_default}"


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# parent
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(500), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

# child
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    comments = relationship("Comment", back_populates="parent_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)




@app.route("/")
def home():
    posts_data = BlogPost.query.all()
    return render_template("index.html", posts=posts_data)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        send_email(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, form=comment_form)

@app.route("/new-post", methods=["POST", "GET"])
@admin_only
def make_post():
    h1_content = "New Post"
    add_form = AddForm()
    if add_form.validate_on_submit():
        new_post = BlogPost(title=add_form.title.data,
                            subtitle=add_form.subtitle.data,
                            author_id=current_user.id,
                            date=datetime.now().strftime("%B %d, %Y"),
                            body=add_form.body.data,
                            img_url=add_form.url.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("make-post.html", form=add_form, title=h1_content)

@app.route("/edit-post/<int:post_id>", methods=["POST","GET"])
@admin_only
def edit_post(post_id):
    h1_content = "Edit Post"
    current_post = BlogPost.query.get(post_id)
    dit_form = AddForm(
        title=current_post.title,
        subtitle=current_post.subtitle,
        url=current_post.img_url,
        body=current_post.body
    )
    if dit_form.validate_on_submit():
        current_post.title = dit_form.title.data
        current_post.subtitle = dit_form.subtitle.data
        current_post.img_url = dit_form.url.data
        current_post.body = dit_form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))
    return render_template("make-post.html", form=dit_form, title=h1_content)

@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/register", methods=["POST", "GET"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        password = register_form.password.data
        name = register_form.name.data
        if not User.query.filter_by(email=email).first():
            hashed_salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            avatar = gravatar_url(email)
            new_user = User(email=email, password=hashed_salted_password, name=name, avatar_url=avatar)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        flash("You've already signed up with that email, log in instead.")
        return redirect(url_for('login'))
    return render_template("register.html", form=register_form)

@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Password incorrect, please try again.")
                return redirect(url_for('login'))
        else:
            flash("That email does not exist, please try again")
            return redirect(url_for('login'))
    return render_template("login.html", form=login_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=False)