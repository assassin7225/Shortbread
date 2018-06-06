from flask import Flask, request, redirect
from urllib.parse import urlparse
import math
import sys
from dbModel import *

BASE = 62

UPPERCASE_OFFSET = 55
LOWERCASE_OFFSET = 61
DIGIT_OFFSET = 48
KEYCOUNT = 0
host = 'https://shortbread.herokuapp.com/'

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

@app.route('/short', methods=['GET'])
def short_url():
	origin_url = request.args.get('url')
	add_data = URLData(
		OriginURL = origin_url,
		ShortURL = ''
		)
	db.session.add(add_data)
	db.session.flush()
	short_url = dehydrate(add_data.id)
	add_data.ShortURL = short_url

	db.session.commit()

	


	return host+dehydrate() 

@app.route('/<short_url>')
def redirect_to_url(short_url):
	query_id = saturate(short_url)
	query = URLData.query.filter_by(id=query_id).first()

	if query.OriginURL is None:
		return 'we are sorry'
	else:
		return redirect(query.OriginURL)

if __name__ == '__main__':
	app.run(debug=True)