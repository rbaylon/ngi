from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField, SelectField
from wtforms_components import DateField
from wtforms.validators import InputRequired, Length
from datetime import date


class NgiForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name', validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    pseudonym = StringField('Pseudonym', validators=[InputRequired(), Length(min=2, max=20)])
    gender = SelectField('Gender', choices=[('male', 'Male'),('female','Female')])
    dob = DateField('Date of Birth',default=date.today(), format="%Y-%m-%d")
    contact_number = StringField('Contact Number', validators=[InputRequired(), Length(min=7, max=15)])
    address = TextAreaField('Address', validators=[InputRequired(), Length(min=2, max=200)])
    ngi_number = StringField('NGI Number', validators=[InputRequired(), Length(min=2, max=20)])
    member_since = DateField('Member Since',default=date.today(), format="%Y-%m-%d")
    rank = SelectField('Rank', choices=[('MG', 'MG'),('RMG','RMG'),('FRMG','FRMG'),('MF','MF'),('NF','NF'),
                                        ('SGF','SGF'),('SGM','SGM'),('GM','GM'),('GF','GF')])
    chapter = StringField('Chapter', validators=[InputRequired(), Length(min=2, max=50)])
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])
    edit = HiddenField('Edit', default='N', validators=[Length(max=1)])