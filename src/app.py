import flask
import logging
import os
import azure_face_analyzer
import viz_exceptions


app = flask.Flask(__name__)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/upload_images', methods=['POST'])
def upload_images():
    images = flask.request.files.getlist('images')
    best_face = azure_face_analyzer.find_most_common_face(images)
    best_face['filename'] = best_face['original_image'].filename
    best_face.pop('original_image')
    return flask.jsonify(best_face)


@app.errorhandler(viz_exceptions.VizException)
def handle_exception(ex):
    return ex.message, ex.status_code


def run_app():
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level)
    flask_debug = os.getenv('FLASK_DEBUG', False)
    app.run(debug=flask_debug, host='0.0.0.0')


if __name__ == '__main__':
    run_app()
