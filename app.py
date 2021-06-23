from flask import Flask,render_template,request, redirect,send_from_directory,abort
import pandas as pd
import matplotlib.pyplot as plt 
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "files_uploaded"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["CSV","XLSX"]
filename = ""
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/",methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    ls = 3
    if request.method == "POST":
        if request.files:
            file = request.files["image"]
            if file.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(file.filename):
                ls=1
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("File Saved")
                try:
                    if filename.rsplit(".", 1)[1]=="xlsx":
                        data = pd.read_excel('files_uploaded/'+filename,engine='openpyxl')
                        sec = data.head(62)
                        plt.rcParams['figure.figsize']=(10,6)
                        sec.plot.bar(figsize=(20,10))
                        plt.savefig('plot.png',dpi=400) 
                        plt.show()  
                        print("Image saved") 
                    if filename.rsplit(".", 1)[1]=="csv":
                        data = pd.read_csv('files_uploaded/'+filename)
                        sec = data.head(62)
                        plt.rcParams['figure.figsize']=(10,6)
                        sec.plot.bar(figsize=(20,10))
                        plt.savefig('plot.png',dpi=400)   
                        print("Image saved")
                        plt.show() 
                except:
                    ls=2
                    print("Upload a proper file")
            else:
                ls =0
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("index.html",value = 'plot.png')

str = os.getcwd()
app.config["CLIENT_IMAGES"] = str.replace("\\","\\\\")
print(app.config["CLIENT_IMAGES"])

@app.route("/download/<image_name>")
def dowmload(image_name):
    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"],path = image_name, as_attachment = True
            )

    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(debug = True)