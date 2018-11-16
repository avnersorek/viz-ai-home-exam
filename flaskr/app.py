import flask
import azure_face_analyzer
import os
import base64


app = flask.Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload_images', methods=['POST'])
def upload_images():
    uploaded_files = flask.request.files.getlist('images')
    for image in uploaded_files:
        result = azure_face_analyzer.recognize_face(image)
        app.logger.info(result)
    return 'success'

if __name__ == '__main__':
    flask_debug = os.getenv('FLASK_DEBUG', False)
    app.run(debug=flask_debug, host='0.0.0.0')
