from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange


class ServicioForm(FlaskForm):

    nombre = StringField(
        "Nombre del servicio",
        validators=[DataRequired()]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(),
            NumberRange(min=0.01)
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[DataRequired()]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("Tecnología", "Tecnología"),
            ("Educación", "Educación"),
            ("Salud", "Salud"),
            ("Transporte", "Transporte")
        ],
        validators=[DataRequired()]
    )