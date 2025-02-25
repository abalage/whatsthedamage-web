from flask import Blueprint, request, render_template, redirect, url_for, session, flash, current_app
from whatsthedamage.whatsthedamage import main as process_csv
from whatsthedamage.config import AppArgs
from forms import UploadForm
from werkzeug.utils import secure_filename
import os
import shutil
from datetime import datetime

bp = Blueprint('main', __name__)

def clear_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
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
    if 'form_data' in session:
        form_data = session['form_data']
        form.filename.data = form_data.get('filename')
        form.config.data = form_data.get('config')
        form.start_date.data = datetime.strptime(form_data.get('start_date'), '%Y-%m-%d') if form_data.get('start_date') else None
        form.end_date.data = datetime.strptime(form_data.get('end_date'), '%Y-%m-%d') if form_data.get('end_date') else None
        form.verbose.data = form_data.get('verbose')
        form.no_currency_format.data = form_data.get('no_currency_format')
        form.filter.data = form_data.get('filter')
    return render_template('index.html', form=form)

@bp.route('/process', methods=['POST'])
def process():
    form = UploadForm()
    if form.validate_on_submit():
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # Save the uploaded files
        filename = secure_filename(form.filename.data.filename)
        config = secure_filename(form.config.data.filename)
        filename_path = os.path.join(upload_folder, filename)
        config_path = os.path.join(upload_folder, config)
        form.filename.data.save(filename_path)
        form.config.data.save(config_path)

        # Check if files are saved
        if not os.path.exists(filename_path):
            flash(f"Failed to save file {filename} to {filename_path}")

        if not os.path.exists(config_path):
            flash(f"Failed to save config file {config} to {config_path}")

        args = AppArgs(
            filename=filename_path,
            start_date=form.start_date.data.strftime('%Y-%m-%d') if form.start_date.data else None,
            end_date=form.end_date.data.strftime('%Y-%m-%d') if form.end_date.data else None,
            verbose=form.verbose.data,
            config=config_path,
            category='category',
            no_currency_format=form.no_currency_format.data,
            output_format='html',
            filter=form.filter.data
        )

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
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
        return redirect(url_for('main.index'))

@bp.route('/clear', methods=['POST'])
def clear():
    session.pop('form_data', None)
    flash('Form data cleared.', 'success')
    return redirect(url_for('main.index'))