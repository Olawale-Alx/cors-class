from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initiated a flask app instance
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initiated cors: flask_app = app, resources tells the resource for cors and
# origins * tells that the server can accept cors request from any website
cors = CORS(app, resources={r'*/api/*': {'origins': '*'}})


class Plant(db.Model):
    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    is_poisonous = db.Column(db.Boolean, nullable=False)
    primary_color = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Name: {self.name} primary_color: {self.primary_color}>'

    def format_res(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'is_Poisonous': self.is_poisonous,
            'primary_color': self.primary_color
        }


# ewedu = Plant(name='Ewedu', scientific_name='Blenga', is_poisonous=False,
#               primary_color='Green')
# db.session.add(ewedu)
# db.session.commit()


# CORS Headers - Adds headers for the response to the client with after_request
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, '
                                                         'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, '
                                                         'OPTIONS')

    return response


@app.route('/')
def home():
    return jsonify({
        'success': True,
        'message': 'Hello World'
    })


@app.route('/plants')
@cross_origin()
def plants_res():
    plants = db.session.query(Plant).all()
    formatted_response = [plant.format_res() for plant in plants]
    return jsonify({
        'success': True,
        'plant': formatted_response
    })


# Call the app route and add cors cross_origin
@app.route('/messages/')
@cross_origin()
def messages():
    return 'Getting Messages'


@app.route('/messages/<int:message_id>')
def entrees(message_id):
    answer = int(message_id) + 500
    return f'{answer}'


# Initiate a live server
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=3000)
