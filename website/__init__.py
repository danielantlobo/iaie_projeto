from flask import Flask

SECRET_KEY = 'dsasjndnkjbifafbabio'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    from .views import views
    from .auth import auth
    from .supplier import supplier
    from .store import store

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(supplier, url_prefix='/supplier')
    app.register_blueprint(store, url_prefix='/store')
    
    return app