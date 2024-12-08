import flask
import requests
import argparse
import json

app = flask.Flask(__name__)

if __name__ == '__main__':
    # 解析启动命令
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=10013)
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--prefix', type=str, default='/v1', help="自定义前缀")
    args = parser.parse_args()
    prefix = args.prefix
    @app.route(f'{prefix}/licenses/register',methods=['POST'])
    def activate():
        # 获取请求参数
        req_datas = flask.request.get_data().decode('utf-8')
        req_datas = json.loads(req_datas)
        print(req_datas)
        return {
            "Code": 200,
            "Message": "Crack by Soft98",
            "Data": {
                "sign": "dW5rbm93bg==",
                "email": "admin@admin.com",
                "deviceID": req_datas.get('deviceID','unknown'),
                "deviceName": req_datas.get('deviceName','unknown'),
                "purchasedAt": "2999-12-31",
                "nextChargeAt": 9999999999999,
                "updatesAvailableUntil": "2999-12-31",
                "LicenseKey": "unknown"
            }
        }
        
    @app.route(f'{prefix}/apps/osx/tableplus',methods=['GET'])
    def getinfo():
        return {
            "Code": 200,
            "Message": "Ok",
            "Data": {
                "Build": "532",
                "DayBeforeExpiration": 999999999,
                "LicenseKey": "unknown",
                "NeedToUpdate": False,
                "NumOfUpdates": 0,
                "PushLocalNoti": False,
                "Tittle":"You\'re behind 0 update"
            }
        }
    
    @app.route(f'{prefix}/licenses/devices',methods=['GET'])
    def devices():
        # 获取请求参数
        device_id = flask.request.args.get('deviceId','unknown')
        device_name = flask.request.args.get('deviceName','unknown')
        platform = flask.request.args.get('platform','unknown')
        sign = flask.request.args.get('sign','ZFc1cmJtOTNiZz09')
        print(flask.request.args)
        return {
            "Code": 200,
            "Message": "Crack by Soft98",
            "Data": {
                "sign": sign,
                "email": "admin@admin.com",
                "deviceID": device_id,
                "deviceName": device_name,
                "platform": platform,
                "purchasedAt": "2999-12-31",
                "nextChargeAt": 9999999999999,
                "updatesAvailableUntil": "2999-12-31",
                "LicenseKey": "unknown"
            }
        }

    # 启动服务
    app.run(host=args.host,port=args.port,debug=args.debug)