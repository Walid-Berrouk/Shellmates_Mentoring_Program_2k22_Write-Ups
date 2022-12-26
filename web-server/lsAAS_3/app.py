import subprocess
from flask import Flask, request, render_template
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
folder_re = re.compile("^[/0-9A-Za-z_ ]+$")
option_re = re.compile("^(all|human-readable|reverse)$")

@app.route("/", methods=["GET", "POST"])
def index():
    output, error = '', ''
    if request.method == "POST" : 
        folder = request.form.get("folder", "")
        option = request.form.get("option", "")
        try : 
            if folder_re.match(folder) and option_re.match(option):
                output = subprocess.run(f"ls -l --{option} {folder}", shell=True, timeout=2, capture_output=True).stdout.decode()
            else:
                error = "That's not allowed"
        except:
            error = "Something went wrong and I'm too lazy to investigate"
    return render_template("index.html", statement=output, error=error) 

# Error handling

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500
