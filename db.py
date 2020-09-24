__title__   = 'DataBase Object API Notify Shipping'
__author__  = 'ZE'

import traceback

from model import MB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URI_MOCK = 'sqlite:///db.sqlite'
URI_DATABASE = 'postgres://npcnbkylpfggja:25ae90ffda127bdb7caf1264382ce05c964a30762d626bcacf43c296dd12302a@ec2-52-73-199-211.compute-1.amazonaws.com:5432/d70ak0tgjn0ubl'

class DB():

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance

    def __init__(self, ws, mock=False):
        '''
            Objective............: Pattern Singleton Class
            Parameters...........: 
                ws...............: WebService with Log and your Another Attributes
            Return...............: Object DataBase Connection
        '''

        if not hasattr(self, 'has_instance'):
            self.has_instance = True
            self.MB = MB
            self.ws = ws
            self.engine = None
            self.session = None
            self.connect(mock)

    def connect(self, mock=False):
        '''
            Objective............: Connect First Database Postgres and Initialze Engine and Session
            Return...............: Boolean with Connection Success
        '''
        try:
            self.ws.log.info('db|connect|ini')

            #FIXME connect database production or local for unittests
            db = URI_MOCK if mock else URI_DATABASE

            self.engine = create_engine(db)
            self.session = sessionmaker(bind=self.engine)

            self.ws.log.debug('db|connect|%s' % db)

            self.setup()

            return True

        except Exception as e:
            self.ws.log.error('db|connect|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
        finally:
            self.ws.log.info('db|connect|fin')    

    def setup(self):
        '''
            Objective............: Setup Initial for the Construnctions and Structures Database
            Return...............: Boolean with Connection Success
        '''
        try:
            self.ws.log.info('db|setup|ini')
            if not self.engine:
                self.ws.log.warn("engine not created, use method connect for initialize database")
                return False
            self.ws.log.info("db|setup|engine: %s " % self.engine)
            self.MB.metadata.create_all(self.engine)
            return True
        except Exception as e:
            self.ws.log.error('db|setup|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            return False
        finally:
            self.ws.log.error('db|setup|fin')

    def uninstall(self):
        '''
            Objective............: Unistall Structures Database in Memory SQlite for the Tests Mocks
            Return...............: Boolean with Connection Success
        '''
        try:
            self.ws.log.info('db|uninstall|ini')
            if not self.engine:
                self.ws.log.warn("Engine not Created, Use Method connect for Initialize Database")
                return False
            self.ws.log.info("db|uninstall|engine: %s " % self.engine)

            self.ws.log.warning("DROP NOTIFY MOCK TESTS")
            for tbl in reversed(self.MB.metadata.sorted_tables):
                self.engine.execute(tbl.delete())  

            return True
        except Exception as e:
            self.ws.log.error('db|uninstall|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            return False
        finally:
            self.ws.log.info('db|uninstall|fin')
