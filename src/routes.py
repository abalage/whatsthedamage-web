from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from whatsthedamage.whatsthedamage import main as process_csv
from whatsthedamage.config import AppArgs
from forms import UploadForm
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
    form = UploadForm()
    return render_template('index.html', form=form)

@bp.route('/process', methods=['POST'])
def process():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.filename.data
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)

        config_file = form.config.data
        if config_file:
            config = os.path.join(UPLOAD_FOLDER, config_file.filename)
            config_file.save(config)

        args: AppArgs = {
            'filename': filename,
            'start_date': form.start_date.data.strftime('%Y-%m-%d') if form.start_date.data else None,
            'end_date': form.end_date.data.strftime('%Y-%m-%d') if form.end_date.data else None,
            'verbose': form.verbose.data,
            'config': config,
            'category': 'category',
            'no_currency_format': form.no_currency_format.data,
            'output_format': 'html',
            'filter': form.filter.data
        }

        # Store form data in session
        session['form_data'] = request.form.to_dict()

        try:
            result = process_csv(args)
        except Exception as e:
            flash(f'Error processing CSV: {e}')
            return redirect(url_for('main.index'))

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
    else:
        flash('Form validation failed. Please check your inputs.')
        return redirect(url_for('main.index'))