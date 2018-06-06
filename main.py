from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from urllib.parse import urlparse
import math
import sys

BASE = 62

UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48
host = 'https://shortbread.herokuapp.com/r/'

def true_ord(char):
    """
    Turns a digit [char] in character representation
    from the number system with base [BASE] into an integer.
    """
    
    if char.isdigit():
        return ord(char) - DIGIT_OFFSET
    elif 'A' <= char <= 'Z':
        return ord(char) - UPPERCASE_OFFSET
    elif 'a' <= char <= 'z':
        return ord(char) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character" % char)

def true_chr(integer):
    """
    Turns an integer [integer] into digit in base [BASE]
    as a character representation.
    """
    if integer < 10:
        return chr(integer + DIGIT_OFFSET)
    elif 10 <= integer <= 35:
        return chr(integer + UPPERCASE_OFFSET)
    elif 36 <= integer < 62:
        return chr(integer + LOWERCASE_OFFSET)
    else:
        raise ValueError("%d is not a valid integer in the range of base %d" % (integer, BASE))


def saturate(key):
    """
    Turn the base [BASE] number [key] into an integer
    """
    int_sum = 0
    reversed_key = key[::-1]
    for idx, char in enumerate(reversed_key):
        int_sum += true_ord(char) * int(math.pow(BASE, idx))
    return int_sum


def dehydrate(integer):
    """
    Turn an integer [integer] into a base [BASE] number
    in string representation
    """
    
    # we won't step into the while if integer is 0
    # so we just solve for that case here
    if integer == 0:
        return '0'
    
    string = ""
    while True:
        remainder = integer % BASE
        string = true_chr(remainder) + string
        # fix string startwith 0
        if integer == 0:
            break
        integer //= BASE
    return string

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://pitrrzstebthsl:389430106b6333d0bb2f4d8dea6ff7c2b56f3d7e15ae61f45ac1a4ebb0fe9a55@ec2-50-19-224-165.compute-1.amazonaws.com:5432/d1g96st35na3qp'
    # 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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



@app.route('/short', methods=['GET'])
def shorten_url():
	origin_url = request.args.get('url')
	add_data = URLData(
		OriginURL = origin_url,
		ShortURL = 'short'
		)
	db.session.add(add_data)
	db.session.flush()
	short_url = dehydrate(add_data.Id)
	add_data.ShortURL = short_url

	db.session.commit()

	return host+short_url 

@app.route('/r/<short_url>')
def redirect_to_url(short_url):

	# print('redirect_to_url(%d)%s'%(len(short_url), short_url))
	query_id = saturate(short_url)
	
	query = URLData.query.filter_by(Id=query_id).first()

	if query.OriginURL is None:
		return 'we are sorry'
	else:
		# queryURL='http://'+query.OriginURL
		return redirect('http://'+query.OriginURL)
		# return redirect('www.google.com')

if __name__ == '__main__':
	app.run(debug=True)
	manager.run()