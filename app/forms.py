from flask_wtf import Form
import wtforms


class RegisterForm(Form):
    name = wtforms.StringField('Name')
    username = wtforms.StringField('UserName')
    password = wtforms.StringField('Password')
    password2 = wtforms.StringField('Repeat Password')


class LoginForm(Form):
    username = wtforms.StringField('UserName')
    password = wtforms.StringField('Password')


class ActivityForm(Form):
    activity_name = wtforms.StringField('Game')
    activity_info = wtforms.TextAreaField('Detail')
    price = wtforms.IntegerField('Price')
    limit = wtforms.IntegerField('Number of Ticket')
    time = wtforms.DateTimeField('Time')
    deadline = wtforms.DateField('Time to Buy Tickets')
    location = wtforms.StringField('Location')
    lon = wtforms.FloatField('Longitude')
    lat = wtforms.FloatField('Latitude')
