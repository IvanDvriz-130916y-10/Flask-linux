from dataclasses import dataclass
from typing import Callable, Optional

from flask_wtf import FlaskForm
from wtforms.fields import Field
from wtforms.validators import ValidationError


def number_len_validator(min_len: int, max_len: int, msg: Optional[str] = None) -> Callable:
    """Функция-фабрика валидатора длины числа."""
    if min_len < 0 or max_len < 0 or min_len > max_len:
        raise ValueError("min_len and max_len must be >=0 and min_len <= max_len")

    def _validate(form: FlaskForm, field: Field) -> None:
        val = field.data
        if val is None:
            return
# удаляем возможный минус и проверяем что остальное цифры
        s = str(val).lstrip('-')
        if not s.isdigit():
            raise ValidationError(msg or "Must be a number.")
        if not (min_len <= len(s) <= max_len):
            raise ValidationError(msg or f"Number length must be between {min_len} and {max_len} digits.")

    return _validate


@dataclass
class LengthCheck:
    """Класс-валидатор для проверки длины числа."""
    min: int
    max: int
    message: Optional[str] = None

    def __post_init__(self):
        if self.min < 0 or self.max < 0 or self.min > self.max:
            raise ValueError("min and max must be non-negative and min <= max")

    def __call__(self, form: FlaskForm, field: Field) -> None:
        val = field.data
        if val is None:
            return
        s = str(val).lstrip('-')
        if not s.isdigit():
            raise ValidationError(self.message or "Must be a number.")
        if not (self.min <= len(s) <= self.max):
            raise ValidationError(self.message or f"Number length must be between {self.min} and {self.max} digits.")