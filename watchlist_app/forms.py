# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddItemForm(FlaskForm):  # Flask-WTF
    title = StringField(validators=[DataRequired(), Length(1, 60)])
    year = StringField(validators=[DataRequired(), Length(4)])
    submit = SubmitField("Add")
