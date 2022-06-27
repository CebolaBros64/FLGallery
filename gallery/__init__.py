from flask import Blueprint

FLGallery = Blueprint(
    'flgallery',  # Flask Gallery
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views
