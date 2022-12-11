from flask import Flask, render_template, url_for, request


app = Flask(__name__)


# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         return 'BLANK'
#     else:
#         return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

