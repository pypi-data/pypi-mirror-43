import requests
import json


class MetroSaoPaulo():

        
    def get_metro_status(self):
        response = requests.get('http://www.metro.sp.gov.br/Sistemas/direto-do-metro-via4/diretodoMetroHome.aspx')
        body = response.text
        begin = body.index('objArrLinhas')
        end = body.index('var objArrL4') - 7
        str = body[begin:end]
        str_obj = str.replace('objArrLinhas = ', '')
        obj = json.loads(str_obj)
        begin = body.index('objArrL4')
        end = body.index('"codigo" : "4"') + 15
        str = body[begin:end]
        str_obj = str.replace('objArrL4 = [', '')
        obj_l4= json.loads(str_obj)
        obj.append(obj_l4)
        ret = {}
        for l in obj:
            ret[l.get('linha')] = l.get('status')
        return ret

