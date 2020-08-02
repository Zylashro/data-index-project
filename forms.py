from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import widgets, SelectMultipleField
from wtforms.validators import DataRequired

class MultiCheckboxfield(SelectMultipleField):
    widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()

class Form(FlaskForm):
    