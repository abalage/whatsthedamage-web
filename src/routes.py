from flask import Blueprint, request, render_template, redirect, url_for, session
from whatsthedamage.whatsthedamage import main as process_csv
from whatsthedamage.config import AppArgs
import os
import shutil

bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def clear_upload_folder():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@bp.route('/')
def index():
    # Retrieve form data from session if available
    form_data = session.get('form_data', {})
    return render_template('index.html', form_data=form_data)

@bp.route('/process', methods=['POST'])
def process():
    file = request.files['filename']
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

    config_file = request.files['config']
    if config_file:
        config = os.path.join(UPLOAD_FOLDER, config_file.filename)
        config_file.save(config)

    args: AppArgs = {
        'filename': filename,
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date'),
        'verbose': 'verbose' in request.form,
        'config': config,
        'category': 'category',
        'no_currency_format': 'no_currency_format' in request.form,
        'output_format': request.form.get('output_format', 'html'),
        'filter': request.form.get('filter')
    }

    # Store form data in session
    session['form_data'] = request.form.to_dict()

    result = process_csv(args)
    # Hack to make the table look better with Bootstrap as Pandas' CSS support is limited
    # Also this leaves the choice of output format to the frontend
    result = result.replace('<table class="dataframe">', '<table class="table table-bordered table-striped">')
    result = result.replace('<tbody>', '<tbody class="table-group-divider">')
    result = result.replace('<thead>', '<thead class="table-dark">')

    # Clear the upload folder after processing
    clear_upload_folder()

    if args['output_format'] == 'html':
        return render_template('result.html', table=result)
    elif args['output']:
        return redirect(url_for('main.index'))
    else:
        return f"<pre>{result}</pre>"