from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = SearchField('Search', validators=[DataRequired('A keyword is required!')])
    submit = SubmitField('Find Query')
