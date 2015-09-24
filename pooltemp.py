from flask import Flask
from flask.ext.restless.manager import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey, Column
from sqlalchemy.sql.sqltypes import Integer, Text, Float, DateTime

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pooltemp.db'
db = SQLAlchemy(app)


class Meas(db.Model):
    id = Column(Integer, primary_key=True)
    h2o_temp = Column(Float, unique=False)
    air_temp = Column(Float, unique=False)
    humidity = Column(Float, unique=False)
    wind_speed = Column(Float, unique=False)
    wind_direction = Column(Integer, unique=False)
    press = Column(Float, unique=False)

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Meas, methods=['GET', 'POST', 'DELETE', 'PUT'])



@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

db.create_all()
app.debug = True


if __name__ == '__main__':
    app.run()
