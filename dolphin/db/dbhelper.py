import sys

sys.path.append("..")
from config.confighelper import confighelper 

class pgsqlhelper:
    def __init__(self):
        self.conn = confighelper.init(self)