import os
import tg
from tg.configuration import AppConfig

class TestConfig(AppConfig):

    def __init__(self, folder, values=None):
        AppConfig.__init__(self)
        #First we setup some base values that we know will work
        self.renderers = ['genshi'] 
        self.render_functions = tg.util.Bunch()
        self.package = tg.test_stack
        self.default_renderer = 'genshi'
        self.globals = self
        self.helpers = {}
        self.auth_backend = None
        self.auto_reload_templates = False
        self.use_legacy_renderer = True
        self.use_dotted_templatenames = True
        self.serve_static = False
        

        #Then we overide those values with what was passed in
        for key, value in values.items():
            setattr(self, key, value)

        
        root = "."
        test_base_path = os.path.join(root,'tg', 'test_stack',)
        test_config_path = os.path.join(test_base_path, folder)
        print test_config_path
        self.paths=tg.util.Bunch(
                    root=test_base_path,
                    controllers=os.path.join(test_config_path, 'controllers'),
                    static_files=os.path.join(test_config_path, 'public'),
                    templates=[os.path.join(test_config_path, 'templates')]
                    )

    def setup_helpers_and_globals(self):
        tg.config['pylons.app_globals'] = self.globals
        tg.config['pylons.h'] = self.helpers

def teardown():
    global_config = {'debug': 'true', 
                     'error_email_from': 'paste@localhost', 
                     'smtp_server': 'localhost'}

    base_config = TestConfig(folder = 'rendering', 
                             values = {'use_sqlalchemy': False,
                                       'pylons.helpers': tg.util.Bunch(),
                                       'use_legacy_renderer': True,
                                       }
                             )
    env_loader = base_config.make_load_environment()
    app_maker = base_config.setup_tg_wsgi_app(env_loader)
    app = app_maker(global_config, full_stack=True)
