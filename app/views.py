from flask import render_template, request, redirect, url_for
from os import listdir, environ
from os.path import isfile, join
from app import app
from app.forms import LoginForm

# /index logic
ipsum = '' \
        'Lorem ipsum dolor sit amet, ' \
        'consectetur adipiscing elit. ' \
        'Aliquam a orci nisi. ' \
        'Suspendisse quis tempus leo. ' \
        'Ut luctus nunc lacinia arcu tincidunt sodales. ' \
        'Duis felis massa, mollis eget enim in, porta iaculis arcu. ' \
        'Nam ut arcu auctor, elementum arcu nec, vulputate dolor. ' \
        'Duis mattis pharetra euismod. Quisque interdum nisi quam, ' \
        'id ultrices nibh sagittis ac. Nulla scelerisque molestie lacus, ' \
        'quis interdum leo mattis a. Nunc non nisl lorem.'
# end /index


# /screenshot logic
# Get path to screenshot folder from environment variables, be sure to set this!
images_folder = environ['SS_DIR']

images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]

images.sort()
images.reverse()
# end /screenshot


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Mathias Thusholt',
        ipsum=ipsum,
        index_active='active'
    )


@app.route('/about')
def about():
    return render_template(
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
    return render_template(
        'screenshot.html',
        title='Screenshots',
        images=images
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('admin'))
    return render_template('login.html', form=form)