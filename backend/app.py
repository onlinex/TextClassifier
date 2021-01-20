from flask import Flask, request, make_response, jsonify
import logging
import os

from modules import transformer

# define Flask backend
app = Flask(__name__)
# do not sort keys in jsonify
app.config['JSON_SORT_KEYS'] = False

# set up basic config for handling incoming requests
logging.basicConfig(filename=transformer.get_path('../logs/service.log'), level=logging.DEBUG,\
    format='%(asctime)s %(levelname)s : %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup a logger"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# second file logger
info_logger = setup_logger('info_logger', transformer.get_path('../logs/info.log'))

model = transformer.Model()

# handle incoming requests
@app.route('/', methods=['POST'])
def x():
    json = request.get_json()

    # run
    author, confidence, img, genres, periods = model.run(json['text'])
    # log request
    info_logger.info('{}, {} -> {}'.format(author, confidence, json['text']))

    # form json response
    return make_response(jsonify({
        'name': str(author), 'confidence': str(confidence), 'img_src': str(img),
        'genres': genres,
        'periods': periods
    }), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)