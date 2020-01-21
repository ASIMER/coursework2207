from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, Label, BooleanField, DateField, DateTimeField, FloatField
from wtforms import validators
from datetime import date


class UserForm(Form):

    login = StringField("Login: ", [validators.data_required("Please, enter user login.")])
    password = StringField("Password: ", [validators.data_required()])
    role = StringField("Role: ", [validators.data_required()])

    submit = SubmitField("Enter")


class SiteForm(Form):

    login = StringField("Login: ", [validators.data_required("Please, enter login.")])
    site_address = StringField("Site address: ", [validators.URL("Please, enter site adress.")])
    site_name = StringField("Site name: ", [validators.Optional()])
    create_date = DateField("Create date: ", [validators.Optional()], default=date.today())

    submit = SubmitField("Enter")


class PageForm(Form):

    site_address = StringField("Site address: ", [validators.URL("Please, enter site adress.")])
    path = StringField("Path: ", [validators.data_required("Please, enter path.")])
    title = StringField("Title: ", [validators.Optional()])

    submit = SubmitField("Enter")


class BlockForm(Form):

    site_address = StringField("Site address: ", [validators.URL("Please, enter site adress.")])
    path = StringField("Path: ", [validators.data_required("Please, enter path.")])
    position = StringField("Position: ", [validators.data_required("Please, enter position.")])
    theme_name = StringField("Theme name: ", [validators.data_required("Please, enter theme name.")])
    block_type = StringField("Block type: ", [validators.Optional()], default='div')
    content = StringField("Content: ", [validators.Optional()])
    focus_time = DateTimeField("Focus time: ", [validators.Optional()])

    submit = SubmitField("Enter")


class ThemeForm(Form):

    theme_name = StringField("Theme name: ", [validators.data_required("Please, enter theme name.")])
    theme_popularity = StringField("Theme popularity: ", [validators.Optional()], default=0)
    code = StringField("Code: ", [validators.Optional()])

    submit = SubmitField("Enter")
