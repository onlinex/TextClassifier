from flask import Flask, request, make_response, jsonify
import logging
import os

from modules import transformer

# define Flask backend
app = Flask(__name__)

logging.basicConfig(filename=transformer.get_path('../log.txt'), level=logging.DEBUG,\
    format='%(asctime)s %(levelname)s : %(message)s')

model = transformer.Model()

# handle incoming requests
@app.route('/', methods=['POST'])
def x():
    json = request.get_json()

    # run
    author, confidence, img, genres, periods = model.run(json['text'])

    # form json response
    return make_response(jsonify({
        'name': str(author), 'confidence': str(confidence), 'img_src': str(img),
        'genres': genres,
        'periods': periods
    }), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)