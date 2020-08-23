from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired


class Encryption(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()],  render_kw={"rows": 30, "cols": 200})
    password = PasswordField('Password:', [validators.DataRequired()])
    submit = SubmitField('Encrypt')


class Decryption(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"rows": 30, "cols": 200})
    password = PasswordField('Password:', [validators.DataRequired()])
    submit = SubmitField('Decrypt')
