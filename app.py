from flask import Flask, render_template, request

app = Flask(__name__)

# 初始化变量
result = ""
image_path = "static/line_plot.png"


# 首页
@app.route('/')
def index():
    return render_template('index.html', result=result, image_path=image_path)


# 处理表单提交
@app.route('/process', methods=['POST'])
def process():
    global result  # 使用全局变量
    # 获取用户输入的信息
    input_text = request.form['input_text']
    result = input_text  # 更新全局变量
    return render_template('index.html', result=result, image_path=image_path)


if __name__ == '__main__':
    app.run(debug=True)
