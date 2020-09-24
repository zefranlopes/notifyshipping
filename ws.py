__title__  = 'WebService Notify Shipping'
__author__ = 'ZE'

import json
import logging
import aiohttp
import asyncio
import datetime
import traceback

from aiohttp import web, request

from exceptions import ApiNotifyShippingException
from db import DB
from controller import Notify

class WS:   

    def __init__(self, mock=False):
        '''
            Objective............: Initialize WebService (Pattern Dependency Injection)
            Return...............: None, More WS with Log and Atributes Instances
        '''

        #FIXME WS
        self.ws = web.Application()

        #FIXME LOG
        logging.basicConfig(format="%(asctime)s: %(name)s: %(levelname)8s: %(message)s")
        self.log = logging.getLogger('ws')
        self.log.setLevel(logging.DEBUG)

        #FIXME DATABASE
        self.DB = DB(ws=self, mock=mock)

        #FIXME CONTROLLER
        self.NY = Notify(ws=self)

    def run(self, runner=True):
        '''
            Objective............: Connect Endpoints of the List Urls
            Parameters...........: 
                runner...........: Flag for Say WebServer Start
            Return...............: None, More WS Start Running
        '''
        try:
            self.log.info('ws|run|ini')

            #POST
            self.ws.router.add_post('/notify', self.post_notify)

            #GET
            self.ws.router.add_get('/notify/{id}', self.get_notify)

            #PUT
            self.ws.router.add_put('/notify/{id}', self.put_notify)

            #DELETE
            self.ws.router.add_delete('/notify/{id}', self.del_notify)

            if runner:
                self.log.info('RUN BABY RUN')
                web.run_app(self.ws)

            self.ws

        except Exception as e:
            self.log.error('ws|run|error')
            self.log.error(str(e))
            self.log.error(traceback.format_exc())

    def eco(self, data=None, status=200, message=''):
        '''
            Objective............: Format Default Responses of the Requests
            Parameters...........: 
                data.............: Data Object Json
                status...........: HTTP Status Code
                message..........: Message Return of the Resquests
            Return...............: Data Object Json
        '''
        try:
            self.log.info('ws|eco|ini')

            resp = {
                'data': data,
                'status': status,
                'message': message,
            }

            self.log.debug(resp)

            return web.Response(text=json.dumps(resp), status=status)

        except Exception as e:
            self.log.error('ws|eco|error')
            self.log.error(str(e))
            self.log.error(traceback.format_exc())
            return self.eco(data=None, status=500, message=str(e))
        finally:
            self.log.info('ws|eco|fin')

    async def post_notify(self, request):
        '''
            Objective............: Method POST for URL Notify Insert 
            Parameters...........: 
                request..........: Data of the Requests from Consumption API 
            Return...............: Response Object JSON 
        '''    
        try:
            self.log.info('ws|post_notify|ini')
            if not request.body_exists:
                raise ApiNotifyShippingException('No Body is Present in the Request. Verify your Request and Try Again')

            data = await request.json()
            data = self.NY.post_notify(data.get('data'))

            return self.eco(data=data, status=201, message='Notify Successfully Created')

        except Exception as e:
            self.log.error('ws|post_notify|error')
            self.log.error(str(e))            
            self.log.error(traceback.format_exc())
            return self.eco(data=None, status=500, message=str(e))
        finally:
            self.log.info('ws|post_notify|fin')


    async def get_notify(self, request):
        '''
            Objective............: Method GET for URL Notify Captured
            Parameters...........: 
                request..........: Data of the Requests from Consumption API 
            Return...............: Response Object JSON
        '''
        try:
            self.log.info('ws|get_notify|ini')
            id = request.match_info.get('id', '')
            if not id:
                raise ApiNotifyShippingException('No QueryString "/id" is Present in the Request. Verify your Request and Try Again')

            data = self.NY.get_notify(id)

            return self.eco(data=data, status=200, message='Notify Successfully Captured')

        except Exception as e:
            self.log.error('ws|get_notify|error')
            self.log.error(str(e))            
            self.log.error(traceback.format_exc())
            return self.eco(data=None, status=500, message=str(e))
        finally:
            self.log.info('ws|get_notify|fin')

    async def put_notify(self, request):
        '''
            Objective............: Method PUT for URL Notify Update
            Parameters...........: 
                request..........: Data of the Requests from Consumption API 
            Return...............: Response Object JSON
        '''
        try:
            self.log.info('ws|put_notify|ini')
            id = request.match_info.get('id', '')
            if not id:
                raise ApiNotifyShippingException('No QueryString "/id" is Present in the Request. Verify your Request and Try Again')

            if not request.body_exists:
                raise ApiNotifyShippingException('No Body is Present in the Request. Verify your Request and Try Again')

            data = await request.json()
            data = self.NY.put_notify(id, data.get('data'))

            return self.eco(data=data, status=202, message='Notify Successfully Update')

        except Exception as e:
            self.log.error('ws|put_notify|error')
            self.log.error(str(e))            
            self.log.error(traceback.format_exc())
            return self.eco(data=None, status=500, message=str(e))
        finally:
            self.log.info('ws|put_notify|fin')   

    async def del_notify(self, request):
        '''
            Objective............: Method DELETE for URL Notify Delete
            Parameters...........: 
                request..........: Data of the Requests from Consumption API 
            Return...............: Response Object JSON 
        '''
        try:
            self.log.info('ws|del_notify|ini')
            id = request.match_info.get('id', '')
            if not id:
                raise ApiNotifyShippingException('No QueryString "/id" is Present in the Request. Verify your Request and Try Again')

            data = self.NY.del_notify(id)

            return self.eco(data=data, status=204, message='Notify Successfully Delete')

        except Exception as e:
            self.log.error('ws|del_notify|error')
            self.log.error(str(e))            
            self.log.error(traceback.format_exc())
            return self.eco(data=None, status=500, message=str(e))
        finally:
            self.log.info('ws|del_notify|fin')     


if __name__ == "__main__":
    WS().run()
