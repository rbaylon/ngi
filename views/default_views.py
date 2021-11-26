from baseapp import app, captcha
from werkzeug.security import check_password_hash
from models import Users
from controllers import UsersController
from forms import LoginForm, UsersForm, UsersFormEdit, UsersFormPassword
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import render_template, request, redirect, url_for, abort


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    cleanweeks = []

    return render_template('index.html', weeks=cleanweeks)


@app.route("/users/<int:page_num>")
@login_required
def users(page_num):
    if not current_user.admin:
        abort(401)

    users = Users.query.paginate(per_page=100, page=page_num, error_out=True)
    return render_template('users.html', username=current_user.username, users=users)


@app.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user(user_id):
    if not current_user.is_authenticated:
        abort(401)

    form = UsersFormEdit()
    user = Users.query.get_or_404(user_id)

    if not current_user.admin:
        if current_user.username != user.username:
            abort(401)

    if form.validate_on_submit():
        userc = UsersController()
        user_data = {}
        if form.delete.data == 'Y':
            user_data['id'] = user.id
            userc.delete(user_data)
            return redirect(url_for('users', page_num=1))
        else:
            user_data['username'] = form.username.data
            user_data['email'] = form.email.data
            user_data['group'] = form.group.data
            user_data['id'] = user.id
            userc.edit(user_data)
            return redirect(url_for('users', page_num=1))

    form.username.data = user.username
    form.email.data = user.email
    delete = request.args.get('delete', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    return render_template('user.html', username=current_user.username, form=form, uid=user.id)


@app.route("/user/add", methods=["GET", "POST"])
@login_required
def adduser():
    if not current_user.admin:
        abort(401)

    form = UsersForm()
    if form.validate_on_submit():
        userc = UsersController()
        user_data = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data,
                     'group': form.group.data}
        userc.add(user_data)
        return redirect(url_for('users', page_num=1))

    return render_template('register.html', form=form)


@app.route("/resetpw", methods=["GET", "POST"])
@login_required
def reset():
    form = UsersFormPassword()
    if form.validate_on_submit():
        userc = UsersController()
        user_data = {'user_id': current_user.id, 'password': form.password.data}
        userc.resetpw(user_data)

        return redirect(url_for('logout'))

    return render_template('resetpw.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    form = LoginForm()
    remember = False
    nexturl = request.args.get('next', None)
    if form.validate_on_submit():
        if captcha.validate():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    if form.remember.data:
                        remember = True

                    login_user(user, remember=remember)
                    if nexturl:
                        return redirect(nexturl)

                    return redirect(url_for('home'))

            msg = "Invalid username or password!"
            return render_template('login.html', form=form, msg=msg, nexturl=nexturl)

        msg = "Incorrect captcha code. Try again"
    return render_template('login.html', form=form, msg=msg, nexturl=nexturl)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
