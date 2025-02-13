# filepath: /home/balage/git/abalage/whatsthedamage-web/src/forms.py
from flask_wtf import FlaskForm
from wtforms import FileField, DateField, StringField, BooleanField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    filename = FileField('CSV file', validators=[DataRequired()])
    config = FileField('Config file', validators=[DataRequired()])
    start_date = DateField('Start Date:', format='%Y-%m-%d', render_kw={
        'class': 'form-control',
        'id': 'start_date',
        'aria-describedby': 'dateStartHelp'
    })
    end_date = DateField('End Date:', format='%Y-%m-%d', render_kw={
        'class': 'form-control',
        'id': 'end_date',
        'aria-describedby': 'dateEndHelp'
    })
    filter = StringField('Filter')
    verbose = BooleanField('Verbose logs')
    no_currency_format = BooleanField('No Currency Format')