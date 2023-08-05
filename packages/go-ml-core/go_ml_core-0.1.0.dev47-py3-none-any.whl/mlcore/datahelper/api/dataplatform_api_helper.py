from mlcore.datahelper.api.keycloak_sdk import KeycloakSDK
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import base64
import math
import sys
import logging

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)-s %(levelname)-7s %(name)-s.%(funcName)s(): %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')




class APIHelper():
    def __init__(self, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config['mlcore']['datahelper']['api']['dataplatform']

        self.keycloakSDK = KeycloakSDK(self.config['keycloak'])
        self.keycloak = self.config['keycloak']
        self.access_token = None

        # limit per page
        self.limit_per_page = 200


    def get_access_token(self):
        return self.keycloakSDK.get_access_token()

    #########################################################
    #
    #   MongoDB API
    #
    #########################################################

    def query_swap_logs(self, cond_dict):
        data = []
        res = self.query_swap_logs_with_page(cond_dict)

        total_count = res['total_count']
        data = res['data']

        num_page = math.ceil(int(total_count) / float(self.limit_per_page))

        # self.logger.info('total_count = %s' % total_count)
        # self.logger.info('num_page = %s' % num_page)
        # self.logger.info('data = %s' % data)
        # self.logger.info('# of data = %s' % len(data))

        for i in range(1, num_page+1):
            res = self.query_swap_logs_with_page(cond_dict, page=i)
            data = data + res['data']
            # self.logger.info('# of data = %s' % len(data))

        return data


    def query_swap_logs_with_page(self, cond_dict, page=0):
        url = '%s/swap-logs' % self.config['mongodb_url']

        self.access_token = self.get_access_token()

        headers = {
            'Go-Client':self.keycloak['resource'],
            'Authorization':'Bearer {}'.format(self.access_token),
        }

        get_data = {}
        # pagination
        get_data["pagination_criteria"] = {
            "offset": 0 + page * self.limit_per_page,
            "limit": self.limit_per_page
        }
        # essential
        if "exchange_time_start" in cond_dict:
            get_data["exchange_time_start"] = cond_dict["exchange_time_start"]
        if "exchange_time_end" in cond_dict:
            get_data["exchange_time_end"] = cond_dict["exchange_time_end"]
        if "source" in cond_dict:
            get_data["source"] = cond_dict["source"]
        # optinal
        if "create_time_start" in cond_dict:
            get_data["create_time_start"] = cond_dict["create_time_start"]
        if "create_time_end" in cond_dict:
            get_data["create_time_end"] = cond_dict["create_time_end"]
        if "swap_id" in cond_dict:
            get_data["swap_id"] = cond_dict["swap_id"]
        if "vm_guid" in cond_dict:
            get_data["vm_guid"] = cond_dict["vm_guid"]
        if "scooter_guid" in cond_dict:
            get_data["scooter_guid"] = cond_dict["scooter_guid"]

        json_obj = {
            'op_code': 'get',
            'get_data': get_data
        }
        json_option = None

        # print('url=%s' % url)
        # print('header=%s' % headers)
        # print('json=%s' % json_obj)
        # self.logger.info('pagination_criteria = %s' % get_data["pagination_criteria"])
        
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        #self.logger.info('r.content = %s' % r.content)
        res = json.loads(r.content.decode('utf-8'),**json_option)

        if res['code']==0:
            return res
        else:
            self.logger.warn('Failed to query_swap_logs_with_page: %s', res)
            return None

    def query_vm_status(self, cond_dict):
        data = []
        res = self.query_vm_status_with_page(cond_dict)

        total_count = res['total_count']
        data = res['data']

        num_page = math.ceil(int(total_count) / float(self.limit_per_page))

        # self.logger.info('total_count = %s' % total_count)
        # self.logger.info('num_page = %s' % num_page)
        # self.logger.info('data = %s' % data)
        # self.logger.info('# of data = %s' % len(data))

        for i in range(1, num_page+1):
            res = self.query_vm_status_with_page(cond_dict, page=i)
            data = data + res['data']
            # self.logger.info('# of data = %s' % len(data))

        return data

    def query_vm_status_with_page(self, cond_dict, page=0):
        url = '%s/vms/statuses' % self.config['mongodb_url']

        self.access_token = self.get_access_token()

        headers = {
            'Go-Client':self.keycloak['resource'],
            'Authorization':'Bearer {}'.format(self.access_token),
        }

        get_data = {}
        # pagination
        get_data["pagination_criteria"] = {
            "offset": 0 + page * self.limit_per_page,
            "limit": self.limit_per_page
        }
        # essential
        if "snap_time_start" in cond_dict:
            get_data["snap_time_start"] = cond_dict["snap_time_start"]
        if "snap_time_end" in cond_dict:
            get_data["snap_time_end"] = cond_dict["snap_time_end"]
        # optinal
        if "state" in cond_dict:
            get_data["state"] = cond_dict["state"]
        if "create_time_start" in cond_dict:
            get_data["create_time_start"] = cond_dict["create_time_start"]
        if "create_time_end" in cond_dict:
            get_data["create_time_end"] = cond_dict["create_time_end"]

        json_obj = {
            'op_code': 'get',
            'get_data': get_data
        }
        json_option = None

        # print('url=%s' % url)
        # print('header=%s' % headers)
        # print('json=%s' % json_obj)
        # self.logger.info('pagination_criteria = %s' % get_data["pagination_criteria"])
        
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        #self.logger.info('r.content = %s' % r.content)
        res = json.loads(r.content.decode('utf-8'),**json_option)

        if res['code']==0:
            return res
        else:
            self.logger.warn('Failed to query_vm_status_with_page: %s', res)
            return None

    #########################################################
    #
    #   Go Platform API
    #
    #########################################################

    def query_vms(self, vm_ids=None):
        return self.query_vms_v1(vm_ids=vm_ids)

    def query_vms_v1(self, vm_ids=None):
        url = '%s/v1/vms' % self.config['server_url']

        self.access_token = self.get_access_token()

        headers = {
            'Go-Client':self.keycloak['resource'],
            'Authorization':'Bearer {}'.format(self.access_token),
        }
        
        if vm_ids==None:
            get_data = {
                'fields_type': 'detail'
            }
        else:
            get_data = {
                'fields_type': 'detail',
                'vm_ids': vm_ids
            }

        json_obj = {
            'op_code': 'get',
            'get_data': get_data
        }
        json_option = None
        # print('url=%s' % url)
        # print('header=%s' % headers)
        # print('json=%s' % json_obj)
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        #self.logger.info('r.content = %s' % r.content)
        res = json.loads(r.content.decode('utf-8'),**json_option)

        if res['code']==0:
            return res['data']
        else:
            self.logger.warn('Failed to query_vms_v1: %s', res)

    def query_esrates(self):
        return self.query_esrates_v1()

    def query_esrates_v1(self):
        url = '%s/v1/es-rates' % self.config['server_url']

        self.access_token = self.get_access_token()

        headers = {
            'Go-Client':self.keycloak['resource'],
            'Authorization':'Bearer {}'.format(self.access_token),
        }
        json_obj = {
            'op_code': 'get',
            'get_data': {
                'get_flag': 1
            }
        }
        json_option = None
        # print('url=%s' % url)
        # print('header=%s' % headers)
        # print('json=%s' % json_obj)
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        res = json.loads(r.content.decode('utf-8'),**json_option)

        if res['code']==0:
            return res['data']
        else:
            self.logger.warn('Failed to query_esrates_v1: %s', res)

    def query_vms_nearby(self, vm_ids=None):
        return self.query_vms_nearby_v1(vm_ids=vm_ids)

    def query_vms_nearby_v1(self, vm_ids=None):
        if vm_ids==None:
            # query vms
            # vm_list = self.query_vms()
            # vm_ids = [vm['vm_id'] for vm in vm_list]
            # self.logger.info('# of vm_ids = %s' % len(vm_ids))
            # self.logger.info('vm_ids[0] = %s' % vm_ids[0])
            # get_data = {
            #     'fields_type': 'detail',
            #     'vm_ids': vm_ids
            # }
            get_data = {
                'fields_type': 'detail'
            }
        else:
            get_data = {
                'fields_type': 'detail',
                'vm_ids': vm_ids
            }

        url = '%s/v1/vms/nearby-vms' % self.config['server_url']
         
        self.access_token = self.get_access_token()

        headers = {
            'Go-Client':self.keycloak['resource'],
            'Authorization':'Bearer {}'.format(self.access_token),
        }
   
        json_obj = {
            'op_code': 'get',
            'get_data': get_data
        }

        # with open('data.json', 'w') as outfile:
        #     json.dump(json_obj, outfile)

        json_option = None
        # print('url=%s' % url)
        # print('header=%s' % headers)
        #print('json=%s' % json_obj)
        r = requests.post(url, headers=headers, json=json_obj)
        #print(r.content)
        if json_option is None:
            json_option = {}

        res = json.loads(r.content.decode('utf-8'),**json_option)

        if res['code']==0:
            return res['data']
        else:
            self.logger.warn('Failed to query_vms_nearby_v1: %s', res)

