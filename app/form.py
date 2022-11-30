# 引入Form基类
from flask_wtf import FlaskForm
# 引入Form元素父类
from wtforms import StringField, PasswordField
# 引入Form验证父类
from wtforms.validators import DataRequired, Length
from wtforms.validators import Email

# form for register form
class Register(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(message=u"Name should not be Null")
        , Length(1, 20, message=u'Length between 1~20')])

    Password = PasswordField('Password', validators=[DataRequired(message=u"Password should not be Null")
        , Length(1, 20, message=u'Length between 1~20')])
    Email = StringField('Email', validators=[DataRequired(message=u"Email should not be Null"),
                                             Email(message=u'Please input a valid email')])

# form for Login form
class fLogin(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(message=u"Name should not be Null")
        , Length(1, 20, message=u'Length between 1~20')])

    Password = PasswordField('Password', validators=[DataRequired(message=u"Password should not be Null")
        , Length(1, 20, message=u'Length between 1~20')])

# form for create assessment
class Todo(FlaskForm):
    Des = StringField(render_kw={'placeholder': u"Add New Assessment Description"},
                      validators=[DataRequired(message=u"Depict should not be Null")
                          , Length(1, 150, message=u'Length between 1~150')])
    ddl = StringField()
    setdate = StringField()
    big = StringField()
    create = StringField()
    name = StringField(render_kw={'placeholder': u"Add Name"},
                       validators=[DataRequired(message=u"Name should not be Null")
                           , Length(1, 50, message=u'Length between 1~50')])

# form for search
class Search(FlaskForm):
    search = StringField(render_kw={'placeholder': u"Search for description"})
    date1 = StringField()
    all = StringField(render_kw={'placeholder': u"Search whatever you want"})

# form for change assessment
class Edit(FlaskForm):
    Des = StringField()
    ddl = StringField()
    setdate = StringField()
    big = StringField()
    create = StringField()
    name = StringField()

#form for create category
class tCategory(FlaskForm):
    C_name = StringField(render_kw={'placeholder': u"Create Category"})
