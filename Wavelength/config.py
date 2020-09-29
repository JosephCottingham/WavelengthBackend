import os, json


class Config:
    __instance__ = None

    MODES = {
    "PRODUCTION" : 0,
    "TEST" : 1,
    "DEVPRODUCTION" : 2
    }

    def __init__(self, mode=1):
        """ Constructor."""
        if Config.__instance__ is None:
            path = ''
            if Config.MODES.get("PRODUCTION") == mode:
                path = os.path.join(os.getcwd(), os.path.join('configs', 'productionConfig.json'))
            elif Config.MODES.get("TEST") == mode:
                path = os.path.join(os.getcwd(), os.path.join('configs', 'testConfig.json'))
            elif Config.MODES.get("DEVPRODUCTION") == mode:
                path = os.path.join(os.getcwd(), os.path.join('configs', 'devInProductionConfig.json'))
            else:
                raise Exception('Invalid mode')
            with open(path) as config_file:
	            config = json.load(config_file)
                
            self.MODE = mode
            self.SECRET_KEY = config.get('SECRET_KEY')
            self.SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
            Config.__instance__ = self
        else:
            raise Exception("You cannot create another Config class")

    @staticmethod
    def get_instance(mode=1):
        """ Static method to fetch the current instance."""
        if not Config.__instance__:
            Config(mode=mode)
        return Config.__instance__
    
    # @staticmethod
    # def get_mode(MODE):
    #     MODES = {
    #     "PRODUCTION" : 0,
    #     "TEST" : 1
    #     }
    #     return MODES.get(MODE)