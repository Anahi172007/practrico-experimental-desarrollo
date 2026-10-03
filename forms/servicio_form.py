from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ServicioForm(FlaskForm):
    nombre = StringField('Nombre del Servicio', validators=[DataRequired()])
    precio = DecimalField('Precio ($)', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción')
    disponible = BooleanField('Disponible')
    
    # Campo para seleccionar la categoría cargada desde la base de datos
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Guardar Servicio')