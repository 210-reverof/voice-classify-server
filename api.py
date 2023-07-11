
from distutils.log import debug
from fileinput import filename
from flask import *  
from main import *

app = Flask(__name__)  

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save("storage/" + f.filename) 

        main_program()

        return "success"
  
if __name__ == '__main__':  
    app.run(debug=True)