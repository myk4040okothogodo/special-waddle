from flask import render_template,request,jsonify
from . import main
from datetime import datetime

@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'sike!,not found'})
        response.status_code = 404
        return response
    return render_template('404.html',current_time=datetime.utcnow()),404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'sike!, internal server error'})
        reponse.status_code = 500
        return response
    return render_template('500.html',current_time=datetime.utcnow()),500
