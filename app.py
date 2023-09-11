from flask import Flask, render_template, request
import p,io

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])

def index():
    if request.method == 'POST':
        param1 = request.form.get('parm1')
        param2 = request.form.get('parm2')
        param3 = request.form.get('parm3')
        param4 = request.form.get('parm4')
        param5 = request.form.get('parm5')
        param6 = request.form.get('parm6')
        param7 = request.form.get('parm7')
        param8 = request.form.get('parm8')
        param9 = request.form.get('parm9')



        return render_template('index.html', result = p.image_data)

    else:
        return render_template('index.html', result = 'waiting')

if __name__ == '__main__':
    app.run()
