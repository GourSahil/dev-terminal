from flask import Blueprint, render_template

index_bp = Blueprint(
    'index',
    __name__, 
    url_prefix='/'
    )

@index_bp.get('/')
def index():
    return render_template('index.html')