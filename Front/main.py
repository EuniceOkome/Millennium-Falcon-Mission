import os
from flask import Flask, render_template, request, abort
from werkzeug.utils import secure_filename
import sys
sys.path.append('..')
from GetOdds import getresults

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Developer Technical Test'
app.config['UPLOAD_EXTENSIONS'] = ['.json']
app.config['UPLOAD_PATH'] = 'Data'

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/', methods=['POST'])
def givetheoods():
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
            
        empirefile = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(empirefile)
        results = getresults('Data/millennium-falcon.json', empirefile)
        return render_template('template.html', boolean = True, result = results)


if __name__ == "__main__":
    app.run(debug=True)
