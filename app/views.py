from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session, Response, jsonify, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, ActivityForm
from .models import db, Admin, User, Activity

main_routes = Blueprint('', __name__)


@main_routes.route('/')
def index():
    date_now = datetime.now().date()
    new_activities = Activity.query.filter(Activity.deadline >= date_now).limit(4)
    return render_template('index.html', new_activities=new_activities)


@main_routes.route('/all-games')
def all_games():
    key = request.args.get('s', '')
    date_now = datetime.now().date()
    new_activities = Activity.query.filter(Activity.deadline >= date_now).filter(
        Activity.activity_name.contains(key)).all()
    old_activities = Activity.query.filter(Activity.deadline < date_now).filter(
        Activity.activity_name.contains(key)).all()
    return render_template('all_games.html', new_activities=new_activities, old_activities=old_activities)


@main_routes.route('/detail/<int:id>')
@login_required
def detail(id):
    activity = Activity.query.filter_by(id=id).first()
    return render_template('detail.html', activity=activity)


@main_routes.route('/apply', methods=['POST'])
@login_required
def apply():
    if request.method == 'POST':
        try:
            data = request.get_json()
            activity_id = data
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            date_now = datetime.now().date()
            activity = Activity.query.filter_by(id=activity_id).filter(Activity.deadline >= date_now).first()
            if not activity:
                message = 'Opps, it is too late to buy ticket!'
                return jsonify(message=message)
            if activity.limit == activity.applied:
                message = 'No more ticket!'
                return jsonify(message=message)
            if activity in user.activities:
                message = 'One account can only buy one ticket!'
                return jsonify(message=message)
            activity.applied += 1
            user.activities.append(activity)
            db.session.commit()
            message = 'Purchase Success!'
            return jsonify(message=message)
        except:
            return Response(status=404)


@main_routes.route('/refund', methods=['POST'])
@login_required
def refund():
    if request.method == 'POST':
        try:
            data = request.get_json()
            activity_id = data
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            date_now = datetime.now().date()
            activity = Activity.query.filter_by(id=activity_id).first()
            if activity.deadline <= date_now:
                message = 'Opps, it is too late to refine ticket!'
                return jsonify(message=message)
            activity.applied -= 1
            user.activities.remove(activity)
            db.session.commit()
            message = 'Refine Success!'
            return jsonify(message=message)
        except:
            return Response(status=404)


@main_routes.route('/applied', methods=['GET', 'POST'])
@login_required
def applied():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    applied_activities = user.activities.all()
    return render_template('applied.html', applied_activities=applied_activities)


# login
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user = User()
        form = LoginForm(obj=user)
        return render_template('login.html', form=form)

    if request.method == 'POST':
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data
        if not username or not password:
            flash('Wrong Input!')
            return redirect(url_for('login'))

        # match username and password
        user = User.query.filter_by(username=username).first()
        # if match successfully
        if user is not None and user.validate_password(password):
            login_user(user)  # login
            session['user_id'] = user.id
            return redirect(url_for('index'))  # redirect to homepage
        else:
            flash('Wrong username or password!')  # if match fail
            return redirect(url_for('login'))  # redirect to login page


@main_routes.route('/logout')
@login_required
def logout():
    logout_user()  # logout
    session.clear()
    flash('Logout success!')
    return redirect(url_for('index'))  # redirect to homepage


# change personal information
@main_routes.route('/change-info', methods=['GET', 'POST'])
@login_required
def change_info():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'GET':
        form = RegisterForm(obj=user)
        form.password.data = None
        return render_template('change_info.html', form=form)

    if request.method == 'POST':
        form = RegisterForm(request.form)
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        if not username or not password:
            flash('Wrong Input!')
            return redirect(url_for('change_info'))
        if password != password2:
            flash('Please enter the same password!')
            return redirect(url_for('change_info'))
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.commit()
        flash('Login Again!')
        return redirect(url_for('logout'))


# register
@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        user = User()
        form = RegisterForm(obj=user)
        return render_template('register.html', form=form)

    if request.method == 'POST':
        form = RegisterForm(request.form)
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        if not username or not password:
            flash('Wrong Input')
            return redirect(url_for('register'))
        if password != password2:
            flash('Please enter the same password!')
            return redirect(url_for('register'))

        # match username and password
        user = User.query.filter_by(username=username).first()
        # if match success
        if user is not None:
            flash('Username already exists!')
            return redirect(url_for('register'))
        else:
            user = User()
            form.populate_obj(user)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)  # login
            session['user_id'] = user.id
            flash('Login Success!')
            return redirect(url_for('index'))  # redirect to homepage


# admin login
@main_routes.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        admin = Admin()
        form = LoginForm(obj=admin)
        return render_template('admin_login.html', form=form)

    if request.method == 'POST':
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data
        if not username or not password:
            flash('Wrong Input')
            return redirect(url_for('admin_login'))

        # match username and password
        admin = Admin.query.filter_by(username=username).first()
        # if match
        if admin is not None and admin.validate_password(password):
            login_user(admin)  # login
            session['admin_id'] = admin.id
            return redirect(url_for('admin_index'))  # redirect to homepage
        else:
            flash('Wrong username or password!')  # if not match
            return redirect(url_for('admin_login'))  # redirect to admin login


@main_routes.route('/admin/activity/list')
def admin_index():
    activities = Activity.query.all()
    return render_template('activity_list.html', activities=activities)


@main_routes.route('/admin/activity/add', methods=['GET', 'POST'])
def activity_add():
    if request.method == 'GET':
        activity_form = ActivityForm()
        return render_template('activity_add.html', form=activity_form)

    if request.method == 'POST':
        form = ActivityForm(request.form)
        if form.validate():
            activity = Activity()
            form.populate_obj(activity)
            db.session.add(activity)
            db.session.commit()
            flash('Add success')
            return redirect(url_for('admin_index'))
        else:
            flash('Add Failed')
            return render_template('activity_add.html', form=form)


@main_routes.route('/admin/activity/edit/<int:id>', methods=['GET', 'POST'])
def activity_edit(id):
    activity = Activity.query.filter_by(id=id).first()
    if request.method == 'GET':
        activity_form = ActivityForm(obj=activity)
        return render_template('activity_add.html', form=activity_form)

    if request.method == 'POST':
        form = ActivityForm(request.form)
        if form.validate():
            form.populate_obj(activity)
            db.session.commit()
            flash('Edit success!')
            return redirect(url_for('admin_index'))
        else:
            return render_template('activity_add.html', form=form)


@main_routes.route('/admin/activity/delete/<int:id>')
def activity_delete(id):
    activity = Activity.query.filter_by(id=id).first()
    db.session.delete(activity)
    db.session.commit()
    flash('Delete success!')
    return redirect(url_for('admin_index'))


@main_routes.route('/admin/apply/list')
def apply_list():
    users = User.query.all()
    activities_list = []
    for user in users:
        activities_list.append({user: user.activities.all()})
    return render_template('apply_list.html', activities_list=activities_list)
