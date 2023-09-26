from flask import Flask, render_template, request

from utils import *

app = Flask(__name__)
rc = StrictRedis(connection_pool = get_rp())

# 初始化变量
result = {
    'input_text1': '',
    'input_text2': '',
    'input_text3': '',
    'input_text4': '',
    'input_text5': '',
    'input_text6': ''
}
image_path = "static/white.png"


# 首页
@app.route('/')
def index():
    return render_template('index.html', result = result, image_path = image_path)


# 处理表单提交
@app.route('/process', methods = ['POST'])
def process():
    global image_path
    global result  # 使用全局变量
    # 获取用户输入的信息
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
    image_path = r'static/' + filename
    generate_word_cloud(get_reviews_for_airline(rc, request.form["input_text1"]), image_path)

    return render_template('index.html', result = result, image_path = image_path)


if __name__ == '__main__':
    app.run(debug = True)
