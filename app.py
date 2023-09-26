from flask import Flask, render_template, request

from utils import *

app = Flask(__name__)
rc = StrictRedis(connection_pool = get_rp())


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        param1 = request.form.get('param1')
        param2 = request.form.get('param2')
        param3 = request.form.get('param3')
        param4 = request.form.get('param4')
        param5 = request.form.get('param5')
        param6 = request.form.get('param6')
        param7 = request.form.get('param7')
        param8 = request.form.get('param8')
        param9 = request.form.get('param9')

        filename = f'{param1}_{param2}_{param3}x{param4}_from{param5}_to{param6}'
        path = r'static/' + filename
        generate_word_cloud(get_reviews_for_airline(rc, param1), filename)
        return render_template('index.html', result = path)
    else:
        return render_template('index.html', result = 'waiting')


if __name__ == '__main__':
    app.run()
