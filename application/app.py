import flask
import prices.route as pricesRoutes
import rabbit.rabbit_service as rabbitService
import utils.config as config
import os.path
from flask_cors import CORS


class MainApp:
    def __init__(self):
        self.flask_app = flask.Flask(__name__, static_folder='../public')
        CORS(self.flask_app, supports_credentials=True, automatic_options=True)
        print("hola desde app")
        # self._generate_api_doc()
        self._init_routes()
        # self._init_rabbit()
        self._init_prices()

    def _generate_api_doc(self):
        os.system("apidoc -i ./ -o ./public")

    def _init_routes(self):
        @self.flask_app.route('/')
        def api_index(path):
            return flask.send_from_directory('../public', path)

        @self.flask_app.route('/')
        def index():
            return flask.send_from_directory('../public', "index.html")
    
    def _init_rabbit(self):
        # rabbitService.init()
        pass

    def _init_prices(self):
        pricesRoutes.init(self.flask_app)

    def get_flask_app(self):
            return self.flask_app
    
    def start(self):
        # debug True para que escuche los cambios
        self.flask_app.run(port= config.get_server_port(),debug=True)
