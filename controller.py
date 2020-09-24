__title__   = 'Controller API Notify Shipping'
__author__  = 'ZE'

import json
import hashlib
import datetime
import traceback

from model import NotifyModel
from exceptions import ApiNotifyShippingException

class Notify():


    def __init__(self, ws):
        '''
            Objective............: Controller Class Notify Execute Commands on DataBase
            Parameters...........: 
                ws...............: WebService with Log and your Another Attributes
            Return...............: Self Object Previous Instance
        '''
        self.ws = ws

    def post_notify(self, data):
        '''
            Objective............: Method POST for URL /profile
            Parameters...........: 
                data.............: Data Object Json of the Notify
            Return...............: Response Object JSON
        '''
        try:
            self.ws.log.info('notify|post_notify|ini')

            #FIXME Waning for Cost Time.
            session = self.ws.DB.session()

            NM = NotifyModel()
            data['id'] = hashlib.md5(f'{NM.ts_updt}{NM.ts_send}{NM.remittee}'.encode()).hexdigest()
            data['ts_updt'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            NM.id = data['id']
            NM.ts_updt = data['ts_updt']
            NM.ts_recv = data.get('ts_recv')
            NM.ts_send = data.get('ts_send')
            NM.status = data.get('status')
            NM.remittee = data.get('remittee')
            NM.payload = data.get('payload')

            #TODO Return Notify ID or UUID of the DataBase
            data['id'] = NM.id

            self.ws.log.debug(NM)

            session.add(NM)
            session.commit()

            return data

        except Exception as e:
            self.ws.log.error('notify|post_notify|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            raise ApiNotifyShippingException(str(e))
        finally:
            self.ws.log.info('notify|post_notify|fin')

    def get_notify(self, id):
        '''
            Objective............: Method GET for URL /profile/id
            Parameters...........: 
                id...............: ID Reference Data Object of the Notify
            Return...............: Response Object JSON
        '''
        try:
            self.ws.log.info('notify|get_notify|ini')

            #FIXME Waning for Cost Time.
            session = self.ws.DB.session()
            NM = session.query(NotifyModel).get(id)

            return {} if not NM else NM.to_dict()

        except Exception as e:
            self.ws.log.error('notify|get_notify|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            raise ApiNotifyShippingException(str(e))
        finally:
            self.ws.log.info('notify|get_notify|fin')

    def put_notify(self, id, data):
        '''
            Objective............: Method PUT for URL /notify/id
            Parameters...........: 
                id...............: ID Reference Data Object of the Notify
                data.............: Data Object Json of the Notify
            Return...............: Response Object JSON
        '''
        try:
            self.ws.log.info('notify|put_notify|ini')

            #FIXME Waning for Cost Time.
            session = self.ws.DB.session()

            NM = session.query(NotifyModel).get(id)
            NM.ts_updt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            NM.ts_recv = data.get('ts_recv')
            NM.ts_send = data.get('ts_send')
            NM.status = data.get('status')
            NM.remittee = data.get('remittee')
            NM.payload = data.get('payload')

            session.commit()

            return NM.to_dict()

        except Exception as e:
            self.ws.log.error('notify|put_notify|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            raise ApiNotifyShippingException(str(e))
        finally:
            self.ws.log.info('notify|put_notify|fin')

    def del_notify(self, id):
        '''
            Objective............: Method DELETE for URL /notify/id
            Parameters...........: 
                id...............: ID Reference Data Object of the Notify
            Return...............: Response Object JSON
        '''
        try:
            self.ws.log.info('notify|del_notify|ini')

            #FIXME Waning for Cost Time.
            session = self.ws.DB.session()
            NM = session.query(NotifyModel).get(id)
            session.delete(NM)
            session.commit()

            return {} if not NM else NM.to_dict()

        except Exception as e:
            self.ws.log.error('notify|del_notify|error')
            self.ws.log.error(str(e))
            self.ws.log.error(traceback.format_exc())
            raise ApiNotifyShippingException(str(e))
        finally:
            self.ws.log.info('notify|del_notify|fin')
