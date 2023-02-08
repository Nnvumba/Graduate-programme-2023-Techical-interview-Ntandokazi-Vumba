from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('quiz',__name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET','POST'])
def your_dets():
    if request.method == 'POST':
        usr_data = {}

        if os.path.exists('usrs.json'):
            with open('usrs.json') as l_name_file:
                usr_data = json.load(l_name_file)

        # if request.form['f_name'] in l_name.keys():
        #     flash('That first name has already been taken. Please select another name.')
        #     return redirect(url_for('home'))

        f = request.files['my_file']
        file_name = request.form['f_name'] + secure_filename(f.filename)
        f.save('quiz/static/user_files/' + file_name)
        usr_data[request.form['f_name']] = {'l_name':request.form['l_name'], 'file':file_name}

        with open('usrs.json','w') as data_file:
            json.dump(usr_data, data_file)
        return render_template('your_url.html', code=request.form['f_name'])
    else:
        return redirect(url_for('quiz.home'))

@bp.route('/<string:f_name>')
def redirect_to_url(f_name):
    if os.path.exists('usrs.json'):
        with open('usrs.json') as usrs_file:
            l_name = json.load(usrs_file)
            if f_name in l_name.keys():
                if 'l_name' in l_name[f_name].keys():
                    return redirect(l_name[f_name]['l_name'])
                else:
                    return redirect(url_for('static', filename='user_files/' + l_name[f_name]['myfile']))
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
