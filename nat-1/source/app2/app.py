from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    result = None
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                process = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                result = f"STDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"
            except Exception as e:
                result = f"Error executing command: {str(e)}"
    return render_template('admin.html', result=result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)