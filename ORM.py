from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iftysdsitdzwda:2977781e219a7a1fa528d991fa97cb28a4fd66fb30907079f3f6560f914af552@ec2-174-129-255-10.compute-1.amazonaws.com:5432/dci7r4hl6v22to'

db = SQLAlchemy(app)


#lab 2 part ===========================

class User(db.Model):

    __tablename__ = 'user'
    login = db.Column('login', db.String(64), primary_key=True)
    password = db.Column('password', db.String(64), primary_key=False, nullable=False)
    role = db.Column('role', db.String(64), primary_key=False, nullable=False)
    sites = db.relationship('Site', backref='User', lazy=True)
    def __init__(self, login, password, role):

        self.login = login
        self.password = password
        self.role = role

    def __repr__(self):

        return '<user: login=%r; password=%r; role=%r>' % \
        self.login, self.password, self.role


#lab 2 part end =======================


class Site(db.Model):

    __tablename__ = 'site'
    site_address = db.Column('site_address', db.String(64), primary_key=True)
    login = db.Column('login', db.String(64), db.ForeignKey('user.login'),
        nullable=False)
    site_name = db.Column('site_name', db.String(64), primary_key=False)
    create_date = db.Column('create_date', db.Date(), primary_key=False, nullable=False)
    pages = db.relationship('Page', backref='Site', lazy=True)

    def __init__(self, site_address, login, site_name, create_date):

        self.site_address = site_address
        self.login = login
        self.site_name = site_name
        self.create_date = create_date

    def __repr__(self):

        return '<site: site_address=%r; login=%r; site_name=%r; create_date=%r>' % \
        self.site_address, self.login, self.site_name, self.create_date



class Page(db.Model):

    __tablename__ = 'page'
    site_address = db.Column('site_address', db.String(64), db.ForeignKey('site.site_address'), primary_key=True)
    path = db.Column('path', db.String(64), primary_key=True)
    title = db.Column('title', db.String(64), primary_key=False)
    
    blocks = db.relationship('Block', backref='Page', lazy=True)

    def __init__(self, site_address, path, title):

        self.site_address = site_address
        self.path = path
        self.title = title

    def __repr__(self):

        return '<page: site_address=%r; path=%r; title=%r>' % \
        self.site_address, self.path, self.title



class Block(db.Model):

    __tablename__ = 'block'
    site_address = db.Column('site_address', db.String(64), primary_key=True)
    path = db.Column('path', db.String(64), primary_key=True)
    position = db.Column('position', db.String(64), primary_key=True)
    theme_name = db.Column('theme_name', db.String(64), db.ForeignKey('theme.theme_name'), primary_key=True)
    block_type = db.Column('block_type', db.String(64), primary_key=True)
    content = db.Column('content', db.String(64), primary_key=True)
    focus_time = db.Column('focus_time', db.Time(64), primary_key=True)
    __table_args__ = (db.ForeignKeyConstraint(('site_address', 'path'),
                                              ('page.site_address', 'page.path')), {})


    def __init__(self, site_address, path, position, theme_name, block_type, content, focus_time):

        self.site_address = site_address
        self.path = path
        self.position = position
        self.theme_name = theme_name
        self.block_type = block_type
        self.content = content
        self.focus_time = focus_time

    def __repr__(self):

        return '<sites: site_address=%r; path=%r; position=%r; theme_name=%r; block_type=%r; content=%r; focus_time=%r>' % \
        self.site_address, self.path, self.position, self.theme_name, self.block_type, self.content, self.focus_time


class Theme(db.Model):

    __tablename__ = 'theme'
    theme_name = db.Column('theme_name', db.String(64), primary_key=True)
    theme_popularity = db.Column('theme_popularity', db.String(64), primary_key=False,
        nullable=False)
    code = db.Column('code', db.String(64), primary_key=False)
    blocks = db.relationship('Block', backref='Theme', lazy=True)

    def __init__(self, theme_name, theme_popularity, code):

        self.theme_name = theme_name
        self.theme_popularity = theme_popularity
        self.code = code

    def __repr__(self):

        return '<sites: theme_name=%r; theme_popularity=%r; code=%r>' % \
        self.theme_name, self.theme_popularity, self.code