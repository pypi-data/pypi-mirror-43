from crawlerUtils import Post

url = "https://aip.baidubce.com/oauth/2.0/token"

params = {
    'grant_type': 'client_credentials',
    'client_id': 'YXVFHX8RtewBOSb6kUq73Yhh',
    'client_secret': 'ARhdQmGQy9QQa5x6nggz6louZq9jHXCk',
}

access_token_json = Post(url, params=params).json
access_token = access_token_json["access_token"]

contents = Post.base64encode("/Users/zhaojunyu/Library/Mobile Documents/com~apple~CloudDocs/study/python/CPU的时钟速度随时间的变化.jpeg")

image_recognize_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
image_recognize_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}
image_recognize_params = {
    "access_token": access_token,
}
image_recognize_data = {
    "image": contents[0],
    # "url": "https://img-blog.csdnimg.cn/2019030221472810.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MTg0NTUzMw==,size_16,color_FFFFFF,t_70",
    "detect_direction": False,
    "detect_language": False,
}

result_json = Post(image_recognize_url, image_recognize_headers, image_recognize_params, image_recognize_data).json
print(result_json)
