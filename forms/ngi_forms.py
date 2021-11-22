from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, TextAreaField, SelectField, DecimalField,BooleanField
from wtforms_components import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, NumberRange, Regexp
from datetime import date
from Utils.variables import ranks, chapter_payments
from models import Person, Chapter, NgiPerson


def persons():
    return Person.query.all()


def persons_ngi():
    return NgiPerson.query.all()


def chapters():
    return Chapter.query.all()


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
    rank = SelectField('Rank', choices=ranks)
    chapter = QuerySelectField('Chapter',get_label='name', query_factory=chapters, allow_blank=True)
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])
    edit = HiddenField('Edit', default='N', validators=[Length(max=1)])


class ChapterPaymentForm(FlaskForm):
    received_from = QuerySelectField('Received from', allow_blank=True)
    received_date = DateField('Received date', default=date.today(), format="%Y-%m-%d")
    received_amount = DecimalField('Received amount', validators=[InputRequired()])
    payment_type = SelectField('Payment type', choices=chapter_payments)
    cpc = BooleanField('CPC Shared')
    chapter = QuerySelectField('Chapter',get_label='name', query_factory=chapters, allow_blank=True)
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])
    edit = HiddenField('Edit', default='N', validators=[Length(max=1)])


class ChapterForm(FlaskForm):
    name = StringField('Chapter name', validators=[InputRequired(), Length(min=2, max=100)])
    founder = StringField('Chapter founder', validators=[InputRequired(), Length(min=2, max=50)])
    founded = DateField('Founding date',default=date.today(), format="%Y-%m-%d")
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])
    edit = HiddenField('Edit', default='N', validators=[Length(max=1)])


class ChapterSelectForm(FlaskForm):
    chapter = QuerySelectField('Select Chapter', get_label='name', query_factory=chapters, allow_blank=False)
