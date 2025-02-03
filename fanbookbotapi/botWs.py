def bot_websocket(token:str,onOpen, onMessage, onError, onClose, log_level="DEBUG")-> None:
    """fanbook bot websocket接口

    Args:
        token (str): bot token
        onOpen (function): ws连接成功回调
        onMessage (function): ws收到消息回调
        onError (function): ws错误回调
        onClose (function): ws关闭回调
        log_level (str, optional): 日志等级. Defaults to "DEBUG".
    """
    import logging
    import coloredlogs
    # 创建日志记录器
    logger = logging.getLogger(__name__)
    # 配置 coloredlogs
    coloredlogs.install(level=log_level, logger=logger)
    logger.info("正在初始化")
    import requests#http请求
    import json#json数据处理
    import time#延时
    import websocket#ws接口链接
    import base64#请求体编码
    import threading
    from pygments import highlight#高亮
    from pygments.lexers import JsonLexer#高亮
    from pygments.formatters import TerminalFormatter#高亮
    from colorama import init, Fore, Back, Style#高亮

    lingpai=token
    websocket_url='wss://gateway-bot.fanbook.mobi/websocket'#websocket主机
    requests_url='https://a1.fanbook.mobi/api/bot/'#fb bot api主机

    init(autoreset=True)    #  初始化，并且设置颜色设置自动恢复
    def addmsg(msg, color="white"):#终端彩色提示信息
        if color == "white":#默认
            print(msg)
        elif color == "red":#错误文本
            print("\033[31m" + msg + "\033[39m")
        elif color == "yellow":#警告文本
            print("\033[33m" + msg + "\033[39m")
        elif color == "green":#成功文本
            print("\033[32m" + msg + "\033[39m")
        elif color == "aqua":#绿底提示文本
            print("\033[36m" + msg + "\033[39m")

    def colorprint(smg2,pcolor):#拓展的终端颜色（需要装colorama）
        if pcolor=='red':#红字
            print(Fore.RED + smg2)
        elif pcolor=='bandg':#蓝字
            print(Back.GREEN + smg2)
        elif pcolor=='d':
            print(Style.DIM + smg2)
        # 如果未设置autoreset=True，需要使用如下代码重置终端颜色为初始设置
        #print(Fore.RESET + Back.RESET + Style.RESET_ALL)  autoreset=True
        
    def colorize_json(smg2,pcolor=''):#格式化并高亮json字符串
        json_data=smg2
        try:
            parsed_json = json.loads(json_data)  # 解析JSON数据
            formatted_json = json.dumps(parsed_json, indent=4)  # 格式化JSON数据

            # 使用Pygments库进行语法高亮
            colored_json = highlight(formatted_json, JsonLexer(), TerminalFormatter())

            print(colored_json)
        except json.JSONDecodeError as e:#如果解析失败，则直接输出原始字符串
            print(json_data)

    def on_message(ws, message):#当收到消息
        # 处理接收到的消息
        logger.debug('↓[接收]↓\n'+str(json.loads(message))+'\n')
        onMessage(ws,message)
                    
    def on_error(ws, error):
        # 处理错误
        logger.warning("发生错误")
        onError(ws)
    def on_close(ws):
        # 连接关闭时的操作
        logger.warning("连接已关闭")
        onClose(ws)
    def on_open(ws):
        # 连接建立时的操作
        logger.info("连接已建立")
        # 发送心跳包
        def send_ping():
            logger.debug("↑[发送]↑\n"+str('{"type":"ping"}\n'))
            ws.send('{"type":"ping"}')
        send_ping()  # 发送第一个心跳包
        onOpen(ws)
        # 定时发送心跳包
    # 替换成用户输入的BOT令牌
    logger.info("正在获取BOT基本信息")
    url = requests_url+f"{lingpai}/getMe"
    # 发送HTTP请求获取基本信息
    response = requests.get(url)
    data = response.json()
    logger.debug(data)
    def send_data_thread():
        while True:
            # 在这里编写需要发送的数据
            time.sleep(25)
            ws.send('{"type":"ping"}')
            logger.debug("↑[发送]↑\n"+str('{"type":"ping"}\n'))
    if response.ok and data.get("ok"):
        user_token = data["result"]["user_token"]#获取user token以建立连接
        device_id = "your_device_id"
        version_number = "1.6.60"
        #拼接base64字符串
        super_str = base64.b64encode(json.dumps({
            "platform": "bot",
            "version": version_number,
            "channel": "office",
            "device_id": device_id,
            "build_number": "1"
        }).encode('utf-8')).decode('utf-8')
        ws_url = websocket_url+f"?id={user_token}&dId={device_id}&v={version_number}&x-super-properties={super_str}"#准备url
        logger.info("正在建立连接")
        try:
            threading.Thread(target=send_data_thread, daemon=True).start()#启动定时发送心跳包的线程
        except:
            logger.error('无法启动新线程，可能是环境限制')
        # 建立WebSocket连接
        websocket.enableTrace(True,level='INFO')
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    else:
        addmsg("无法获取BOT基本信息，请检查令牌是否正确。",color='red')

