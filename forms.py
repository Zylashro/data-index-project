from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = SearchField('Search', validators=[DataRequired('A keyword is required!')])
    submit = SubmitField('Find Query')
