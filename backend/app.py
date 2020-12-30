from flask import Flask, request, make_response, jsonify
from model import transformer

# define Flask backend
app = Flask(__name__)

model = transformer.Model()

# handle incoming requests
@app.route('/', methods=['POST'])
def x():
    json = request.get_json()

    # run
    author, confidence, img = model.run(json['text'])

    # form json response
    return make_response(jsonify({
        "name": str(author),
        "confidence": str(confidence),
        "img_src": str(img)
    }), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)