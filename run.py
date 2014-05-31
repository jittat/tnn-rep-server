from flask import Flask
from flask import request
from flask import render_template, redirect, url_for

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
    if request.method == 'POST':
        save_report()

    return render_template('report.html')

def save_report():
    blocked_url = request.form['blocked_url'].strip()
    landing_url = request.form['landing_url'].strip()
    if 'REMOTE_ADDR' in request.environ:
        reported_from_addr = request.environ['REMOTE_ADDR']
    else:
        reported_from_addr = '0.0.0.0'

    report = BlockageReport(blocked_url,
                            reported_from_addr)
    report.landing_url = landing_url

    db.session.add(report)
    db.session.commit()
    

if __name__ == '__main__':
    app.run()
