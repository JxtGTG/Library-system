from app import db


# model for assessment
class Affairs(db.Model):
    __tablename__ = 'Affairs'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    a_name = db.Column(db.Text, nullable=False)
    des = db.Column(db.Text, nullable=False, default="......", name="Description")
    setdate = db.Column(db.String(100), nullable=False)
    ddl = db.Column(db.String(100), nullable=True)
    state = db.Column(db.Integer, default=0)
    priority = db.Column(db.String(100), default="low")
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), default=1)
    big = db.Column(db.Integer, nullable=True)
    create = db.Column(db.Integer, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), default=1)
    

    def __init__(self, a_name, des, setdate, ddl, priority, big, create, user_id, category_id):
        self.a_name = a_name
        self.des = des
        self.setdate = setdate
        self.ddl = ddl
        self.priority = priority
        self.user_id = user_id
        self.big = big
        self.create = create
        self.category_id = category_id

# model for users
class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    affairs = db.relationship("app.models.Affairs", backref="user")

    def __init__(self, Name, Password, Email):
        self.Password = Password
        self.Name = Name
        self.Email = Email


# model for category
class Category(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    affairs = db.relationship("app.models.Affairs", backref="category")
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
