from datetime import datetime

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for, flash, get_flashed_messages

from models import db
from models import BlockageReport

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('report'))

@app.route('/report/', methods=['GET','POST'])
def report():
    flashed_messages = get_flashed_messages()
    error_message = None
    
    if request.method == 'POST':
        result, msg = save_report_from_request()
        if result:
            flash('Submitted successfully')
            return redirect(url_for('report'))
        else:
            error_message = 'Error saving report: ' + msg

    return render_template('report.html',
                           flashed_messages=flashed_messages,
                           error_message=error_message)


def get_and_strip_or_none(form, key):
    if key in form:
        return form[key].strip()
    else:
        return None

    
def save_report_from_request():
    blocked_url = get_and_strip_or_none(request.form, 'blocked_url')

    if (not blocked_url) or blocked_url == '':
        return (False, 'no blocked url provided')

    landing_url = get_and_strip_or_none(request.form, 'landing_url')

    if 'REMOTE_ADDR' in request.environ:
        reported_from_addr = request.environ['REMOTE_ADDR']
    else:
        reported_from_addr = '0.0.0.0'

    report = BlockageReport(blocked_url,
                            reported_from_addr)
    report.landing_url = landing_url

    if 'detailed_form' in request.form:
        title = get_and_strip_or_none(request.form, 'title')
        accessing_from = get_and_strip_or_none(request.form, 'accessing_from')
        comments = get_and_strip_or_none(request.form, 'comments')

        if ('observed_choice' in request.form and
            request.form['observed_choice'] != 'now'):
            observed_at = get_and_strip_or_none(request.form, 'observed_at')
        else:
            observed_at = datetime.now()

        if title:
            report.title = title
        if observed_at:
            report.observed_at = observed_at
        if accessing_from:
            report.accessing_from = accessing_from
        if comments:
            report.comments = comments

    db.session.add(report)
    db.session.commit()

    return (True, 'OK')
    
if __name__ == '__main__':
    app.run()
