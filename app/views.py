from flask import render_template, request, redirect, url_for, send_from_directory, g, flash
from flask_login import login_user, logout_user, current_user, login_required
from os import listdir
from os.path import isfile, join
from string import ascii_lowercase, digits
from random import choice
from app import app, lm, bcrypt
from .forms import LoginForm
from .models import User, Projects

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
images_folder = join(app.instance_path, 'app/screenshot')

images = [f for f in listdir(images_folder) if isfile(join(images_folder, f))]

images.sort()
images.reverse()
# end /screenshot


# Generator for random id for urls
def id_generator(size=6, chars=ascii_lowercase + digits + digits):
    return ''.join(choice(chars) for i in range(size))


def short_title_generator(title):
    return title.replace(' ', '_')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    g.projects = Projects.query.all()


@app.route('/index')
@app.route('/')
def index():
    # Remove anything but the latest four projects
    projects_list = Projects.query.all()
    for project in projects_list:
        if len(projects_list) > 4:
            projects_list.remove(project)

    return render_template(
        'index.html',
        title='Mathias Thusholt',
        index_active='active',
        ipsum=ipsum,
        four_latest_projects=reversed(projects_list)
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

        if user is None:
            flash('Fejl i brugernavn og/eller adgangskode!')
        elif bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))

        else:
            flash('Fejl i brugernavn og/eller adgangskode')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template(
        'admin.html',
        title='Admin',
        admin_active='active'
    )


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        join(app.instance_path, 'app'),
        'favicon.ico'
    )


@app.route('/screenshot/<path:filename>')
def screenshot(filename):
    return send_from_directory(
        join(app.instance_path, 'app/screenshot'),
        filename
    )


@app.route('/projects/<random_id>/<project_short_title>')
def projects(random_id, project_short_title):
    projects_by_short_title = Projects.query.filter(Projects.short_title.in_([project_short_title])).all()
    projects_by_random_id = Projects.query.filter(Projects.random_id.in_([random_id])).all()

    for project_by_short_title in projects_by_short_title:
        for project_by_random_id in projects_by_random_id:
            if project_by_random_id == project_by_short_title:
                project = project_by_random_id
                break
        if project is not None:
            break

    if 'project' in locals():
        markdown = open(join(join(app.instance_path, 'app/markdown'), project.filename), 'r').read()
        return render_template('project.html', markdown=markdown)
    else:
        return redirect('/404')

