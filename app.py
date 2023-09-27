from flask import Flask, render_template, request
import os, random
from utils import *


def random_background_picture(exception_pic: str | None = None) -> str:
    pic_ls = [f for f in os.listdir(r'static/background_picture')]
    if exception_pic:
        pic_ls.remove(exception_pic)
    return random.choice(pic_ls)


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
    'background_picture': f'static/background_picture/{random_background_picture()}'
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

    result['input_text1'] = request.form['input_text1']
    result['input_text2'] = request.form['input_text2']
    result['input_text3'] = request.form['input_text3']
    result['input_text4'] = request.form['input_text4']
    result['input_text5'] = request.form['input_text5']
    result['input_text6'] = request.form['input_text6']

    filename = (f'{request.form["input_text1"]}_'
                f'{request.form["input_text2"]}_'
                f'{request.form["input_text3"]}x{request.form["input_text4"]}_'
                f'from{request.form["input_text5"]}_to{request.form["input_text6"]}.png')
    image_path = r'static/' + 'temp_word_cloud.png'
    result['word_cloud_title'] = generate_word_cloud(
        text = get_reviews_for_airline(
            redis_client = rc,
            arl_name = request.form["input_text1"]),
        path = image_path,
        arl_name = request.form["input_text1"],
        width = request.form["input_text4"],
        height = request.form["input_text5"],
        bc = request.form["input_text6"])

    return render_template(template_name_or_list = 'index.html',
                           result = result,
                           image_path = image_path)


if __name__ == '__main__':
    app.run(debug = True)
