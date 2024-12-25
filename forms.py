from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField


class AddForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    url = StringField('Blog Image URL', validators=[DataRequired(), URL(require_tld=True, message='You must contain a valid URL')])
    body = CKEditorField('Blog Content')
    submit = SubmitField('Submit Post')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('SIGN ME UP!')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('LET ME IN!')

class CommentForm(FlaskForm):
    comment_text = CKEditorField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')