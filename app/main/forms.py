from flask_pagedown.fields import PageDownField
from flask_wtf import Form
from wtforms import StringField, SubmitField,TextAreaField,SelectField,BooleanField
from wtforms.validators import Required, Length , Email,Regexp

class PostForm(Form):
    body = PageDownField("what is on your mind?", validators=[Required()])
    submit = SubmitField("post")


class CommentForm(Form):
    body= StringField('', validators=[Required()])
    submit = SubmitField('Submit')
    
class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField ('Submit')

class EditProfileForm(Form):
    name = StringField('Real name ', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditprofileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alraedy Registered.')


    def validate_username(self, field):
        if field.data  != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
