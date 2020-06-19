from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField("Ім'я: ", validators=[DataRequired()], render_kw={"placeholder": "Ім'я:"})
    email = StringField("Пошта: ", validators=[Email()], render_kw={"placeholder": "Пошта:"})
    message = TextAreaField("Текст повідомлення", validators=[DataRequired()], render_kw={"placeholder": "Текст повідомлення:"})
    submit = SubmitField("Відправити")