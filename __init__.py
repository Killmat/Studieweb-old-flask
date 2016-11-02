from flask import Flask, render_template
from config import ss_dir
from os import listdir
from os.path import isfile, join

app = Flask(__name__)


images_folder = ss_dir
images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]
images.sort()
images.reverse()

ipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a orci nisi. Suspendisse quis tempus leo. Ut luctus nunc lacinia arcu tincidunt sodales. Duis felis massa, mollis eget enim in, porta iaculis arcu. Nam ut arcu auctor, elementum arcu nec, vulputate dolor. Duis mattis pharetra euismod. Quisque interdum nisi quam, id ultrices nibh sagittis ac. Nulla scelerisque molestie lacus, quis interdum leo mattis a. Nunc non nisl lorem.'


@app.route('/')
@app.route('/index')
def index():
    return render_template (
        'index.html',
        title='Mathias Thusholt',
        ipsum=ipsum,
        index_active='active'
    )


@app.route('/about')
def about():
    return render_template (
        'about.html',
        title='Om mig',
        about_active='active'
    )


@app.route('/docs')
def docs():
    return render_template(
        'docs.html',
        title='Dokumentation',
        docs_active='active'
    )


@app.route('/screenshot')
def screenshot():
    return render_template('screenshot.html', title='Screenshots', images=images)

if __name__ == '__main__':
    app.run(debug=True)


