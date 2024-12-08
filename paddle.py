import flask
import requests
import argparse
import hmac
import hashlib
import base64
import json

def calculate_hmac(api_key, response_data):
    # 使用HMAC-SHA256算法计算签名
    hmac_signature = hmac.new(
        key=api_key.encode('utf-8'),
        msg=response_data.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    # 将签名编码为Base64
    return base64.b64encode(hmac_signature).decode('utf-8')

app = flask.Flask(__name__)

if __name__ == '__main__':
    # 解析启动命令
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=10010)
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--prefix', type=str, default='/3.2', help="自定义前缀")
    args = parser.parse_args()
    prefix = args.prefix
    @app.route(f'{prefix}/license/activate',methods=['POST'])
    def activate():
        # 获取请求参数
        product_id = ''
        vendor_id = ''
        api_key = ''
        req_datas = flask.request.get_data().decode('utf-8').split('&')
        print(req_datas)
        for param in req_datas:
            k_v = param.split('=')
            if k_v[0] == 'product_id':
                product_id = k_v[1]
            if k_v[0] =='vendor_id':
                vendor_id = k_v[1]
            if k_v[0] =='api_key':
                api_key = k_v[1]
        # 解析参数
        print(product_id)
        license = {
            "product_id": product_id,
            "activation_id": str(vendor_id),
            "type": "personal",
            "expires": 1,
            "expiry_date": "1999999999"
        }
        print(license)
        return {
            "success": True,
            "response": license,
            "signature": calculate_hmac(api_key, json.dumps(license))
        }

    @app.route(f'{prefix}/license/verify',methods=['POST'])
    def verify():
        api_key = ''
        req_datas = flask.request.get_data().decode('utf-8').split('&')
        print(req_datas)
        for param in req_datas:
            k_v = param.split('=')
            if k_v[0] =='api_key':
                api_key = k_v[1]
        license = {
                "activation_id": "admin",
                "type": "personal",
                "expires": 1,
                "expiry_date": "1999999999999"
            }
        return {
            "success": True,
            "response": license,
            "signature": calculate_hmac(api_key, json.dumps(license))
        }
    
    @app.route(f'{prefix}/product/data',methods=['POST'])
    def product():
        api_key = ''
        req_datas = flask.request.get_data().decode('utf-8').split('&')
        print(req_datas)
        for param in req_datas:
            k_v = param.split('=')
            if k_v[0] =='api_key':
                api_key = k_v[1]
        url = f'https://v3.paddleapi.com/3.2/product/data'
        headers = dict(flask.request.headers)
        headers['Host'] = 'v3.paddleapi.com'
        data = flask.request.get_data().decode('utf-8')
        req = requests.post(url, headers=headers, data=data, verify=False)
        res_data = json.loads(req.text)
        res_data["response"]["trial"]["duration"] = 9999999
        res_data["signature"] = calculate_hmac(api_key, json.dumps(res_data["response"]))
        return res_data
    
    @app.route(f'{prefix}/<path:subpath>',methods=['POST','GET'])
    def reverse_proxy(subpath):
        # 反向代理
        url = f'https://v3.paddleapi.com/3.2/{subpath}'
        method = flask.request.method
        headers = dict(flask.request.headers)
        headers['Host'] = 'v3.paddleapi.com'
        data = flask.request.get_data().decode('utf-8')
        # print(url, data, method, headers)
        if method == 'GET':
            req = requests.get(url, headers=headers, data=data, verify=False)
        else:
            req = requests.post(url, headers=headers, data=data, verify=False)
        # 创建response
        print(req.status_code,req.content)
        response = flask.make_response(req.content)
        response.status_code = req.status_code
        return response
    # 启动服务
    app.run(host=args.host,port=args.port,debug=args.debug)