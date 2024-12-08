import flask
import argparse

app = flask.Flask(__name__)

if __name__ == '__main__':
    # 解析启动命令
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=10012)
    parser.add_argument('--debug', action='store_true', default=False)
    parser.add_argument('--prefix', type=str, default='', help="自定义前缀")
    args = parser.parse_args()
    prefix = args.prefix
    @app.route(f'{prefix}/verifyReceipt',methods=['POST'])
    def activate():
        # 获取请求参数
        req_datas = flask.request.get_data().decode('utf-8')
        print(req_datas)
        return {
        "status":0,
        "receipt":{
          "in_app":[
            {
                "expires_date_ms":"1999999999999"
            }
          ]
        }
      }
    # 启动服务
    app.run(host=args.host,port=args.port,debug=args.debug)