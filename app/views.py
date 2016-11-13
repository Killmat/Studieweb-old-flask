from flask import render_template, request, redirect, url_for, send_from_directory, g, flash
from flask_login import login_user, logout_user, current_user, login_required
from os import listdir
from os.path import isfile, join
from app import app, db, lm
from .forms import LoginForm
from .models import User

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
images_folder = join(app.instance_path, 'app/screenshot')

images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]

images.sort()
images.reverse()
# end /screenshot


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/index')
@app.route('/')
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
def screenshot_gallery():
    return render_template(
        'screenshot.html',
        title='Screenshots',
        images=images
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()

        next_view = request.args.get('next')
        print next_view
        if user is None:
            flash('Fejl i brugernavn og/eller adgangskode')
        elif user.password == form.password.data:
            login_user(user)
            return redirect(next_view or url_for('index'))

        else:
            flash('Fejl i brugernavn og/eller adgangskode')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return '<p>Du er admin lol</p>'


@app.route('/screenshot/<path:filename>')
def screenshot(filename):
    return send_from_directory(
        join(app.instance_path, 'app/screenshot'),
        filename
    )
