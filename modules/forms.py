from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired('Inserisci una email'), Email(), Length(max=120)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired('Inserisci una password'), Length(min=6)]
    )
    password2 = PasswordField(
        'Conferma password',
        validators=[DataRequired('Conferma la password'), EqualTo('password')]
    )
    submit = SubmitField('Registrati')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')


class SummaryForm(FlaskForm):
    title = StringField(
        'Titolo',
        validators=[DataRequired('Inserisci un titolo'), Length(max=150)]
    )
    original_text = TextAreaField(
        'Testo da riassumere',
        validators=[DataRequired('Inserisci il testo'), Length(max=30000)]
    )
    submit = SubmitField('Genera riassunto')
