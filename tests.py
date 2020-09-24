__title__   = 'Class Unit Tests API Notify Shipping'
__author__  = 'ZE'

import sys
import json
import hashlib
import logging
import datetime
import unittest
import traceback
import concurrent.futures

from aiohttp import web
from unittest.mock import patch
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from ws import WS
from db import DB
from model import NotifyModel
from controller import Notify
from exceptions import ApiNotifyShippingException

class Mocked:

    def __init__(self):
        '''
            Objective............: Initialize Data Mocked (Pattern Dependency Injection)
            Return...............: None, More Mock with Log and Atributes Instances
        '''

        #FIXME LOG
        logging.basicConfig(format="%(asctime)s: %(name)s: %(levelname)8s: %(message)s")
        self.log = logging.getLogger('mock')
        self.log.setLevel(logging.DEBUG)

        #FIXME DATABASE
        self.DB = DB(ws=self, mock=True)

        #FIXME CONTROLLER
        self.NY = Notify(self)

    def destroy(self):
        '''
            Objective............: Clear DataBase Mockeds 
            Return...............: None
        '''
        self.DB.uninstall()

    def create(self):
        self.destroy()

        session = self.DB.session()

        NM = NotifyModel()
        NM.ts_updt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        NM.ts_recv = "2020-01-01 01:01:01"
        NM.ts_send = "2020-01-01 01:01:01"
        NM.status = "INVOICED"
        NM.remittee = "TEST_ONE"
        NM.payload = {"payload": [{"message": "This order has waiting for payment"}]}
        NM.id = 'd2fd0634a97d12a9b10e976183d8e624'

        session.add(NM)

        NM = NotifyModel()
        NM.ts_updt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        NM.ts_recv = "2020-01-01 01:01:01"
        NM.ts_send = "2020-01-01 01:01:01"
        NM.status = "CANCELLED"
        NM.remittee = "TEST_TWO"
        NM.payload = {"payload": [{"message": "This order has been cancelled"}]}
        NM.id = '1c5a88da9829df3e0b1910350cce7c22'
      
        session.add(NM)
        
        session.commit()

        self.post_dict = {
            "data": {
                "ts_send": "2020-03-03 03:03:03",
                "status": "REFUNDED",
                "remittee": "TEST_THREE",
                "payload": [{'message': "REFUNDED"}]
            }
        }

        self.put_dict = {
            "data": {
                "ts_send": "2020-04-04 04:04:04",
                "status": "CANCELLED",
                "remittee": "ZE",
                "payload": [
                    {
                        "message": "CANCELLED"
                    }
                ]
            }
        }        

class TestNotifyModel(unittest.TestCase):

    def setUp(self):        
        mk.create()        

    def tearDown(self):
        mk.destroy()

class TestNotify(TestNotifyModel):

    def test_all_notify(self):
        '''
            Objective............: Tests all Records of the Dababase Local to Ensure Integration
            Return...............: Assert
        '''
        mk.log.info('1. Tests Ensure Integration')
        #FIXME Tests Differents Asserts and Name Message for Localization Testes

        notify_list = mk.DB.session().query(NotifyModel).all()
        self.assertNotEqual([], notify_list, '1.1')
        for notify in notify_list:
            self.assertTrue(len(notify.id) == 32, '1.2')
            self.assertFalse(len(notify.ts_updt) <= 0, '1.3')
            self.assertIsNot(notify.remittee, None, '1.4')
            self.assertIsNotNone(notify.payload, '1.5')
            self.assertIn(notify.status, ['INVOICED', 'CANCELLED', 'REFUNDED'], '1.6')

    def test_post_notify(self):
        '''
            Objective............: Tests POST Transiction from API for the Controller
            Return...............: Assert
        '''
        mk.log.info('2. POST Transiction from API for the Controller')

        self.assertIsNotNone(mk.post_dict, '2.1')
        self.assertIsNone(mk.post_dict.get('id'), '2.2')
        self.assertIsInstance(mk.NY.post_notify(mk.post_dict), dict, '2.3')

    def test_get_notify(self):
        '''
            Objective............: Tests GET Transiction from API for the Controller
            Return...............: Assert
        '''
        mk.log.info('3. GET Transiction from API for the Controller')

        notify_list = mk.DB.session().query(NotifyModel).all()
        self.assertIsNot(mk.NY.get_notify('NOT_KEY_VALID'), '3.1')
        self.assertIsNotNone(mk.NY.get_notify('1c5a88da9829df3e0b1910350cce7c22'), '3.2')
        self.assertIsInstance(mk.NY.get_notify('d2fd0634a97d12a9b10e976183d8e624'), dict, '3.3')

    def test_put_notify(self):
        '''
            Objective............: Tests PUT Transiction from API for the Controller
            Return...............: Assert
        '''
        mk.log.info('5. PUT Transiction from API for the Controller')

        self.assertIsNotNone(mk.post_dict, '2.1')
        self.assertIsNone(mk.post_dict.get('id'), '2.2')
        self.assertIsNotNone(mk.NY.put_notify('1c5a88da9829df3e0b1910350cce7c22', mk.put_dict), '2.3')
        self.assertIsInstance(mk.NY.put_notify('d2fd0634a97d12a9b10e976183d8e624', mk.put_dict), dict, '2.4')

    def test_del_notify(self):
        '''
            Objective............: Tests DELETE Transiction from API for the Controller
            Return...............: Assert
        '''
        mk.log.info('5. DELETE Transiction from API for the Controller')

        notify_list = mk.DB.session().query(NotifyModel).all()
        self.assertNotEqual([], notify_list, '5.1')
        for notify in notify_list:
            self.assertIsNot(mk.NY.del_notify(notify.id), '5.2')

        notify_list = mk.DB.session().query(NotifyModel).all()
        self.assertEqual([], notify_list, '5.3')

    def test_repr_notify(self):
        '''
            Objective............: Tests REGEX Model for the Controller
            Return...............: Assert
        '''
        mk.log.info('6. REGEX Model for the Controller')

        NM = NotifyModel()
        NM.id = '1c5a88da9829df3e0b1910350cce7c22'
        self.assertRegex(str(NM), "id='1c5a88da9829df3e0b1910350cce7c22'", '6.1')                     

class TestNotifyApiAsync(AioHTTPTestCase):
    
    async def get_application(self):
        '''
            Objective............: Tests API with Endpoints Originals of the Application
            Return...............: Assert
        '''
        mk.log.info('7. Start Api Application Mocked')

        mk.create()

        ws = WS(mock=True) #SERVER MOCKED IN DINAMIC MEMORY
        ws.run(runner=False)
        return ws.ws

    @unittest_run_loop
    async def test_post_notify_api(self):
        resp = await self.client.post("/notify", data=json.dumps(mk.post_dict))
        data = await resp.json(content_type=None)

        self.assertIsInstance(data, dict, '7.1.1')
        self.assertEqual(resp.status, 201, '7.1.2')

    @unittest_run_loop
    async def test_get_notify_api(self):
        resp = await self.client.get("/notify/1c5a88da9829df3e0b1910350cce7c22")
        data = await resp.json(content_type=None)

        self.assertIsInstance(data, dict, '7.1.3')
        self.assertEqual(resp.status, 200, '7.1.4')

    @unittest_run_loop
    async def test_put_notify_api(self):
        resp = await self.client.put("/notify/1c5a88da9829df3e0b1910350cce7c22", data=json.dumps(mk.put_dict))
        data = await resp.json(content_type=None)

        self.assertIsInstance(data, dict, '7.1.4')
        self.assertEqual(resp.status, 202, '7.1.5')

    @unittest_run_loop
    async def test_del_notify_api(self):
        resp = await self.client.delete("/notify/1c5a88da9829df3e0b1910350cce7c22")
        data = await resp.json(content_type=None)

        self.assertIsNone(data, '7.1.6')
        self.assertEqual(resp.status, 204, '7.1.7')        

    def test_post_notify_api_async(self):
        async def test_post_notify_api_async_route():
            resp = await self.client.post("/notify", data=json.dumps(mk.post_dict))
            data = await resp.json(content_type=None)

            self.assertIsInstance(data, dict, '7.2.1')
            self.assertEqual(resp.status, 201, '7.2.2')

        self.loop.run_until_complete(test_post_notify_api_async_route())

    def test_get_notify_api_async(self):
        async def test_get_notify_api_async_route():
            resp = await self.client.get("/notify/d2fd0634a97d12a9b10e976183d8e624")
            data = await resp.json(content_type=None)

            self.assertIsInstance(data, dict, '7.2.3')
            self.assertEqual(resp.status, 200, '7.2.4')

        self.loop.run_until_complete(test_get_notify_api_async_route())

    def test_put_notify_api_async(self):
        async def test_put_notify_api_async_route():
            resp = await self.client.put("/notify/1c5a88da9829df3e0b1910350cce7c22", data=json.dumps(mk.put_dict))
            data = await resp.json(content_type=None)

            self.assertIsInstance(data, dict, '7.2.5')
            self.assertEqual(resp.status, 202, '7.2.6')

        self.loop.run_until_complete(test_put_notify_api_async_route())

    def test_del_notify_api_async(self):
        async def test_del_notify_api_async_route():
            resp = await self.client.delete("/notify/d2fd0634a97d12a9b10e976183d8e624")
            data = await resp.json(content_type=None)

            self.assertIsNone(data, '7.2.7')
            self.assertEqual(resp.status, 204, '7.2.8')

        self.loop.run_until_complete(test_del_notify_api_async_route())        

if __name__ == '__main__':

    mk = Mocked()

    unittest.main()