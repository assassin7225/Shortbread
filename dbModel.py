from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://pitrrzstebthsl:389430106b6333d0bb2f4d8dea6ff7c2b56f3d7e15ae61f45ac1a4ebb0fe9a55@ec2-50-19-224-165.compute-1.amazonaws.com:5432/d1g96st35na3qp'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class URLData(db.Model):
    __tablename__ = 'URLData'

    Id = db.Column(db.Integer, primary_key=True)
    OriginURL = db.Column(db.String(256))
    ShortURL = db.Column(db.String(64))

    def __init__(self
                 , OriginURL
                 , ShortURL
                 ):
        self.OriginURL = OriginURL
        self.ShortURL = ShortURL


if __name__ == '__main__':
    manager.run()
