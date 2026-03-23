from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import Email, InputRequired, NumberRange, Optional
from web.validators import NumberLength

# Форма регистрации для /registration
class RegistrationForm(FlaskForm):
    email = StringField(
        "email",
        validators=[
            InputRequired("Email is required."),
            Email("Invalid email format.")
        ]
    )
    phone = IntegerField(
        "phone",
        validators=[
            InputRequired("Phone is required."),
            NumberRange(min=0, message="Phone must be a positive number."),
            NumberLength(10, 10, "Phone must be exactly 10 digits.")
        ]
    )
    name = StringField("name", validators=[InputRequired("Name is required.")])
    address = StringField("address", validators=[InputRequired("Address is required.")])
    index = IntegerField("index", validators=[InputRequired("Index is required.")])
    comment = StringField("comment", validators=[Optional()])