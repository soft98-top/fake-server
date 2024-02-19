import flask
import requests
import argparse

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
        req_datas = flask.request.get_data().decode('utf-8').split('&')
        print(req_datas)
        for param in req_datas:
            k_v = param.split('=')
            if k_v[0] == 'product_id':
                product_id = k_v[1]
            if k_v[0] =='vendor_id':
                vendor_id = k_v[1]
        # 解析参数
        print(product_id)
        return {
            "success": True,
            "response": {
                "product_id": product_id,
                "activation_id": vendor_id,
                "type": "personal",
                "expires": 1,
                "expiry_date": 1999999999999
            }
        }

    @app.route(f'{prefix}/license/verify',methods=['POST'])
    def verify():
        return {
            "success": True,
            "response": {
                "activation_id": "admin",
                "type": "personal",
                "expires": 1,
                "expiry_date": 1999999999999
            }
        }
    
    
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
        # print(req.status_code,req.content)
        response = flask.make_response(req.content)
        response.status_code = req.status_code
        return response
    # 启动服务
    app.run(host=args.host,port=args.port,debug=args.debug)