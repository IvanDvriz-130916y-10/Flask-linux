from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class ExecuteCodeForm(FlaskForm):
# Поле для кода текст до 10 тысяч символов
    code = TextAreaField(
        "code",
        validators=[
            DataRequired(message="code is required"),
            Length(max=10000, message="code is too long"),
        ]
    )
# Таймаут целое число от 1 до 30
    timeout = IntegerField(
        "timeout",
        validators=[
            DataRequired(message="timeout is required"),
            NumberRange(min=1, max=30, message="timeout must be between 1 and 30 seconds"),
        ]
    )