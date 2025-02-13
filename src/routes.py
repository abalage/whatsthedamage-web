from flask import Blueprint, request, render_template, redirect, url_for, session
from whatsthedamage.whatsthedamage import main as process_csv
from whatsthedamage.config import AppArgs
import os

bp = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    if args['output_format'] == 'html':
        return render_template('result.html', table=result)
    elif args['output']:
        return redirect(url_for('main.index'))
    else:
        return f"<pre>{result}</pre>"