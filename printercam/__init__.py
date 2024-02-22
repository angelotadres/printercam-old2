import os
import time

from flask import Flask
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO

from .database import db
from .modules.auth import routes as auth_routes
from .modules.cameras import routes as camera_routes
from .services import system_info


def emit_system_info(socketio):
    while True:
        disk = system_info.get_main_disk_space()
        data = {
            "hostname": system_info.get_host_name(),
            "ip": system_info.get_local_ip(),
            "disk_total_space": disk['result'],
            "disk_percentage_used": disk['percentage_used']
        }
        socketio.emit('system_info', data)
        socketio.sleep(2)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    assets = Environment(app)

    css = Bundle(
        'scss/globals.scss',
        filters=['libsass'],
        output='dist/globals.css',
        depends='scss/*.scss'
        )
    assets.register("asset_css", css)
    css.build()

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'printercam.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(camera_routes.bp)
    app.add_url_rule('/', endpoint='/cameras')
    socketio = SocketIO(app)

    socketio.start_background_task(emit_system_info, socketio)

    return app, socketio
