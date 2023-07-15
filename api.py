from distutils.log import debug
from fileinput import filename
from flask import *  
from main import *
import os

app = Flask(__name__)  

@app.route('/classify', methods = ['POST'])  
def success():  
    print("hererreer")
    if request.method == 'POST':  
        f = request.files['file']
        f.save("storage/" + f.filename)

        result = main_program()
        files = os.listdir("storage")
        for file in files:
            os.remove("storage/{}".format(file))

        return jsonify(result)
  
if __name__ == '__main__':  
    app.run(debug=False, host='0.0.0.0')