from flask import Flask, redirect, url_for, jsonify

import program
from data.profile import Profile

app = Flask(__name__)


# @app.route('/score-gauge')
# def get_score_gauge():


# old part #----------------------
@app.route('/')
def home():
    return 'Hello, this is main page <h1>Hello</h1>'


@app.route('/a-url')
def admin_home():
    return 'This is home2 page'


@app.route('/<name>')
def user(name):
    return f'Hello, this is main page <h1>Hello {name} </h1>'


@app.route('/admin')
def admin():
    return redirect(url_for('admin_home'))


@app.route('/admin/')
def admin2():
    return redirect(url_for('user', name='Administrator!'))


@app.route('/json1')
def ret_json_1():
    program.launch_app()
    # p = Profile()
    # p.score = 10
    # p.star_count_average = 4
    p: Profile = Profile.objects(user_id=23).first()
    # return jsonify(p.to_json())
    # print(p.to_json())
    print(jsonify(p.to_json()))
    return p.to_json()


if __name__ == '__main__':
    app.run()
