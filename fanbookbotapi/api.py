import requests,json
import re
import base64
from .apilist import *

def getme(token:str) ->requests.models.Response:
    """获取bot信息

    Args:
        token (str): bot的token

    Returns:
        requests.models.Response: requests请求对象
    """
    r=requests.get(apiurl+token+apilist['getme'])
    return r

def sendmessage(token='',chatid=0,biaoti="标题",add_Key=False,ik=[[{"text":"下一页","callback_data":"{\"type\":\"next\",\"index\":2,\"msg\":\"114514\"}"}]],text='文本',biaoticolor='ffe4e4',type="text",shade=['ff764a','ffb39aff'],backgroundColor='ddeeff00',getjson=False) -> requests.models.Response|str:
    """发送消息

    Args:
        token (str, optional): botToken. Defaults to ''.
        chatid (int, optional): 频道id. Defaults to 0.
        ik (list, optional): 自定义键盘. Defaults to [[{"text":"下一页","callback_data":"{\"type\":\"next\",\"index\":2,\"msg\":\"114514\"}"}]].
        text (str, optional): 正文内容.
        type (str, optional): fanbook(特殊消息解析模式)/text(纯文本). Defaults to "text".
        getjson (bool, optional): 设置为True就是只返回编码完成的json，不请求. Defaults to False.
        add_Key (bool, optional): 是否添加键盘. Defaults to False.

    Returns:
        requests.models.Response|str: requests请求对象|编码完成的json
    """
    if len(shade)==1:
        color1,color2=shade[0],shade[0]
    else:
        color1,color2=shade[0],shade[1]
        
    url = apiurl+token+apilist['sendmessage']
    if type=="card":
        print("警告：card模式已经被废弃，请使用sendCard函数")
        text1="{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"gradient\\\":{\\\"colors\\\":[\\\""+str(color1)+"\\\",\\\""+str(color2)+"\\\"]},\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+str(biaoti)+"\\\",\\\"style\\\":{\\\"color\\\":\\\"#"+str(biaoticolor)+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\""+backgroundColor+"\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,0,0,4\\\",\\\"alignment\\\":\\\"-1,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+str(text)+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
        pm="Fanbook"
    elif type=='fanbook':
        pm='Fanbook'
        text1=text
    else:
        text1=text
        pm=None
    #print(text1)
    d={
    "chat_id": int(chatid),
    "text": text1,
    "parse_mode": pm
    }
    if add_Key:
        #添加"reply_markup": {
        #"inline_keyboard": ik
    #}  
        d['reply_markup']={
            "inline_keyboard": ik
        }
    payload=json.dumps(d)
    if getjson==False:
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    else:
        return payload

def getPrivateChat(token:str,userid:int) ->requests.models.Response:
    """创建私聊频道

    Args:
        token (str): botToken
        userid (int): 用户长id

    Returns:
        requests.models.Response: requests请求对象
    """
    url=apiurl+token+apilist['getPrivateChat']
    headers = {'content-type':"application/json;charset=utf-8"}
    jsonfile=json.dumps({
        "user_id":int(userid)
        })
    postreturn=requests.post(url,data=jsonfile,headers=headers)
    return postreturn

def process_markdown(text):
    # 正则表达式匹配 Markdown 格式的图片
    pattern = r'!\[.*?\]\((.*?)\)'
    
    # 找到所有匹配的图片链接
    matches = re.finditer(pattern, text)
    image_links = [match.group(1) for match in matches]
    
    # 使用正则表达式删除图片
    modified_text = re.sub(pattern, '', text)
    
    # 根据删除后的图片位置分割文本
    split_text = re.split(pattern, text)
    
    # 删除分割后的图片链接
    for i in range(len(split_text)):
        if split_text[i] in image_links:
            split_text[i]='[图片]'
    
    return image_links, modified_text, split_text

def sendCard(token:str,chatid:int,markdown:str,color=['#00afee','#f2f2f2'],bt='标题',textcolor='#f2f2f2',openbutton=False,btcolor='#00afee',burl='https://www.baidu.com',button='按钮',come_from_name=None,come_from_icon=None) -> dict:
    """发送消息卡片

    Args:
        token (str): 机器人token
        chatid (int): 频道id
        markdown (str): markdown文本
        color (list, optional): 标题颜色，16进制颜色，渐变色. Defaults to ['#00afee','#f2f2f2'].
        bt (str, optional): 标题文本. Defaults to '标题'.
        textcolor (str, optional): 标题文本颜色. Defaults to '#f2f2f2'.
        openbutton (bool, optional): 是否开启按钮. Defaults to False.
        btcolor (str, optional): 按钮颜色. Defaults to '#00afee'.
        burl (str, optional): 按钮按下时跳转的url. Defaults to 'https://www.baidu.com'.
        button (str, optional): 按钮文本. Defaults to '按钮'.
        come_from_name (_type_, optional): 显示在卡片下方的小字，一般用来显示来源服务器名称. Defaults to None.
        come_from_icon (_type_, optional): 显示在卡片下方的图标，一般用来显示来源服务器的图标. Defaults to None.

    Returns:
        dict: fanbook api返回的json
    """
    imgindex=0
    # fanbook不支持直接在markdown中插入图片，需要先提取图片链接并转换为base64编码，再插入图片组件
    image_links, modified_text, split_text = process_markdown(markdown)
    data={
        "crossAxisAlignment": "stretch",
        "tag": "column",
        "children": [
            {
                "tag": "container",
                "padding": "12,7",
                "gradient": {
                    "colors": color
                },
                "child": {
                    "tag": "text",
                    "data": bt,
                    "style": {
                        "color": textcolor,
                        "fontSize": 16,
                        "fontWeight": "medium"
                    }
                },
                "backgroundColor": "ddeeff00"
            }
        ],
    }
    for i in split_text:
        if i=='[图片]':
            img=image_links[imgindex]
            imgindex+=1
            # base64编码图片链接
            img = base64.b64encode(img.encode('utf-8')).decode('utf-8')
            data['children'].append({
                "tag": "container",
                "child": {
                    "tag": "column",
                    "padding": "12",
                    "children": [
                        {
                            "tag": "container",
                            "padding": "12",
                            "child": {
                                "tag": "image",
                                "src":  "1::00::0::"+img,
                            }
                        }
                    ]
                },
                "backgroundColor": "ffffff"
            })
        else:
            data['children'].append({
                    "tag": "container",
                    "child": {
                        "tag": "column",
                        "crossAxisAlignment": "start",
                        "padding": "12",
                        "children": [
                            {
                                "tag": "container",
                                "padding": "0,8,0,0",
                                "child": {
                                    "tag": "markdown",
                                    "data": i
                                }
                            }
                        ]
                    },
                    "backgroundColor": "ffffff"
                })
    if openbutton:
        data['children'].append({"tag":"container","padding":"12,0,12,12","child":{"tag":"button","category":"outlined","color":btcolor,"size":"medium","widthUnlimited":True,"href":burl,"label":button}})
    r=sendmessage(token=token,chatid=chatid,type='fanbook',text=json.dumps({'width': None, 'height': None, 'data':json.dumps(data) , 'notification': None, 'come_from_icon': None, 'come_from_name': come_from_name, 'template': None, 'no_seat_toast': None, 'type': 'messageCard'})).text
    return json.loads(r)

