from flask import Flask, send_file, send_from_directory, render_template, request, redirect, url_for, abort
from werkzeug.utils import safe_join
import os
import zipfile


app = Flask(__name__, template_folder='/home/user/NirScanSweep/templates/')
app.config['WTF_CSRF_ENABLED'] = False
DataFolder = '/home/user/NirScanSweep/'

@app.route('/')
def list_files():
	# List all scan files on HTML.
	files = os.listdir(DataFolder)
	print(files)
	return render_template('files.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
	# Add option to download a scan file on HTML.
	try:
		return send_from_directory(DataFolder, filename, as_attachment=True)
	except FileNotFoundError:
		abort(404)
		

@app.route('/delete/<filename>')
def delete_file(filename):
	# Add option to delete a scan file on HTML.
	file_path = os.path.join(DataFolder, filename)
	try:
		os.remove(file_path)
	except FileNotFoundError:
		abort(404)
	return redirect(url_for('list_files'))
		
		
@app.route('/download-all')
def download_all_files():
	# Add option to download all scans file on HTML.
	directory_path = '/home/user/NirScanSweep/'
	zip_file_path = '/home/user/NirScanSweep/AllData.zip'

	with zipfile.ZipFile(zip_file_path, 'w') as zipf:
		for root, dirs, files in os.walk(DataFolder):
			for file in files: 
				file_path = os.path.join(root, file)
				zipf.write(file_path, os.path.relpath(file_path, directory_path))
	try:
		return send_from_directory('/home/user/NirScanSweep/', 'AllData.zip', as_attachment=True)
	except FileNotFoundError:
		abort(404)

@app.route('/delete-all')
def delete_all_files():
	# Add option to delete all scans file on HTML.
	try:
		for filename in os.listdir(DataFolder):
			file_path = os.path.join(DataFolder, filename)
			if os.path.isfile(file_path):
				os.remove(file_path)
		return 'All files deleted successfully', 200
	except Exception as e:
		return str(e), 500
		
		
		

if __name__ == '__main__':
	# Web server adress to access HTML page.
	app.run(host='10.42.0.1', port=8000)
