from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404 # return a tuple

@error_pages.app_errorhandler(403)
def error_404(error):
    return render_template('error_pages/403.html'), 403 # return a tuple