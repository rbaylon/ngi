from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from Utils.variables import user_groups


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])
    group = SelectField('Group', choices=user_groups)


class UsersForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80),EqualTo('pwconfirm',
                                message='Passwords must match')])
    pwconfirm = PasswordField('Repeat Password')
    group = SelectField('Group', choices=user_groups)
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])


class UsersFormEdit(FlaskForm):
    username = StringField('Usersname', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])
    group = SelectField('Group', choices=user_groups)
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])


class UsersFormPassword(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=6, max=80),EqualTo('pwconfirm', message='Passwords must match')])
    pwconfirm = PasswordField('Repeat New Password')


    
