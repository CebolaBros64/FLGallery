from flask import Flask
from flask_minify import minify

# Importing our gallery blueprint
from gallery import FLGallery

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)

# Not having an url_prefix in a blueprint
# can lead to issues with the static folder
app.register_blueprint(FLGallery, url_prefix='/gallery')

if __name__ == '__main__':
    app.run()
