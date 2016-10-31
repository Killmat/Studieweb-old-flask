from flask import Flask, render_template
from config import ss_dir
from os import listdir
from os.path import isfile, join

app = Flask(__name__)


images_folder = ss_dir
images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]
images.sort()
images.reverse()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/screenshot')
def screenshot():
    return render_template('screenshot.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)


