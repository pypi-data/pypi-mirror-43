# -*- coding: utf-8 -*-

"""Main module."""

import logging
logger = logging.getLogger(__name__)
logger.debug("Loaded " + __name__)

import os

from events import Events

from eve import Eve
from eve_swagger import swagger, add_documentation
from eve.io.mongo import Mongo, Validator, GridFSMediaStorage

from .rpc import methods
from .blueprints import *

class Eazy(Eve, Events):
    
    methods = methods
    
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    SETTINGS_INI = os.path.join(BASE_DIR, 'settings.ini')
    LOGGER_CONFIG = os.path.join(BASE_DIR, 'logger.conf')


    def __init__(
        self,
        import_name=__package__,
        settings="settings.py",
        validator=Validator,
        data=Mongo,
        auth=None,
        redis=None,
        url_converters=None,
        json_encoder=None,
        media=GridFSMediaStorage,
        configs=[],
        env_prefix="EAZY",
        **kwargs
    ):
        """ Eazy main WSGI app is implemented as a Eve subclass. Since we want
        to be able to launch our API by simply invoking Eve's run() method,
        we need to enhance our super-class a little bit.
        """

        super(Eazy, self).__init__(import_name, **kwargs)
        
        self.load_eazy_config(configs, env_prefix)
        self.logger = logger
        self.load_blueprints()
        

    def load_eazy_config(self, configs, env_prefix):
        """Loads the config from environment and settings file."""
        # 1. Loads from settings.ini [default settings]
        self.config.from_pyfile(self.SETTINGS_INI) 
        
        # 2. Loads user provided settings file
        for config_file in configs:
            if os.path.isfile(config_file):
                self.config.from_pyfile(config_file)
        
        # 3. Loads user provided settings file from environment variable
        if env_prefix + 'CONFIG_FILE' in os.environ: 
            self.config.from_pyfile(os.environ[env_prefix + 'CONFIG_FILE'])
        
        # 4. Finally loads from Environment Variables
        for a in os.environ: 
            if(a.startswith(env_prefix)):
                self.config[a[len(env_prefix):]] = os.getenv(a)

        
    def load_blueprints(self):
        if self.config["ENABLE_SWAGGER_ROUTES"]:
            self.register_blueprint(swagger)
        if self.config["ENABLE_INDEX_ROUTES"]:
            self.register_blueprint(index_bp)
        if self.config["ENABLE_CONFIG_ROUTES"]:
            self.register_blueprint(config_bp)
        if self.config["ENABLE_HEALTH_ROUTES"]:
            self.register_blueprint(health_bp)
        if self.config["ENABLE_JSONRPC_ROUTES"]:
            rpc_route = '/' + self.config["API_VERSION"] + '/' + self.config["RPC_BASE_ROUTE"] + '/' + self.config["RPC_ROUTE_NAME"]
            self.add_url_rule(
                rpc_route, "call_rpc", view_func=call_rpc, methods=["POST", "OPTIONS"]
            )
            self.add_url_rule(
                rpc_route, "list_rpc", view_func=list_rpc, methods=["GET", "OPTIONS"]
            )
