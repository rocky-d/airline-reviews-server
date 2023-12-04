from datetime import datetime

from flask import Flask, render_template, request, make_response
from redis import StrictRedis

from utils import *

random.seed(datetime.now().timestamp())

app = Flask(__name__)
rc = StrictRedis(connection_pool = get_rp())

# 初始化变量
result = {
    'input_text1': '',
    'input_text2': '',
    'input_text3': '',
    'input_text4': '',
    'input_text5': '',
    'input_text6': '',
    'word_cloud_title': '',
    'background_picture': random_background_picture('IMG_0233(20230927-092232).JPG')
}
image_path = "static/transparentpicture.png"


# 首页
@app.route('/')
def index():
    return render_template('index.html', result = result, image_path = image_path)


# 处理表单提交
@app.route('/process', methods = ['POST'])
def process():
    global image_path, result

    filename = (f'{request.form["input_text1"]}_'
                f'{request.form["input_text2"]}_'
                f'{request.form["input_text3"]}x{request.form["input_text4"]}_'
                f'from{request.form["input_text5"]}_to{request.form["input_text6"]}.png')
    image_path = r'static/' + 'temp_word_cloud.png'

    result['input_text1'] = request.form['input_text1']
    result['input_text2'] = request.form['input_text2']
    result['input_text3'] = request.form['input_text3']
    result['input_text4'] = request.form['input_text4']
    result['input_text5'] = request.form['input_text5']
    result['input_text6'] = request.form['input_text6']
    result['background_picture'] = random_background_picture(result['background_picture'])
    result['word_cloud_title'] = generate_word_cloud(
        text = get_reviews_for_airline(
            redis_client = rc,
            arl_name = request.form["input_text1"]),
        path = image_path,
        arl_name = request.form["input_text1"],
        width = request.form["input_text4"],
        height = request.form["input_text5"],
        bc = request.form["input_text6"]
    )

    return render_template(
        template_name_or_list = 'index.html',
        result = result,
        image_path = image_path
    )


@app.route('/android', methods = ['POST'])
def handle_android():
    # 图片在服务器的本地路径
    global image_path
    image_path = r'static/' + 'temp_word_cloud.png'

    request_body = {key: value for key, value in request.json.items()}
    # print(request_body)
    image_title = generate_word_cloud(
        text = get_reviews_for_airline(redis_client = None, arl_name = request_body['arl_name']),
        path = image_path,
        arl_name = request_body['arl_name'],
        width = request_body['width'],
        height = request_body['height'],
        bc = request_body['bc']
    )

    # 读取图片数据
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # 创建自定义响应
    response = make_response(image_data)

    # 设置响应头部信息
    response.headers['Content-Type'] = 'image/png'
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run(debug = True)
