import socket

class FlaskSetup():
    
    def __init__(self, app_config = {}):
        self.extend_default_config(app_config)
        self.parse_config()

    # Configuration methods
    # =========================================================================
    def get_default_config(self):
        default_config = {
            'debug_mode_on_hostnames': ('localhost',)
        }
        return default_config

    def extend_default_config(self, app_config):
        default_config = self.get_default_config()
        default_config.update(app_config)
        self.config = default_config

    # Parse config methods
    # =========================================================================
    def parse_config(self):
        self.app = {}
        self.is_debug_mode()

    def is_debug_mode(self):
        hostname = socket.gethostname()
        if hostname in self.config.get('debug_mode_on_hostnames'):
            self.app['debug'] = True
        else:
            self.app['debug'] = False

    # Interface methods
    # =========================================================================
    def get_app_setup(self):
        return self.app

