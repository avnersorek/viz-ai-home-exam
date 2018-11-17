import flask
import azure_face_analyzer
import logging
import os
import base64

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
app = flask.Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload_images', methods=['POST'])
def upload_images():
    # print(flask.request.files[0].filename)
    images = flask.request.files.getlist('images')
    best_face = azure_face_analyzer.run_the_thing(images)
    return flask.jsonify(best_face)

if __name__ == '__main__':
    flask_debug = os.getenv('FLASK_DEBUG', False)
    app.run(debug=flask_debug, host='0.0.0.0')
