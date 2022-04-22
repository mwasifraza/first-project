from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.form import RegistrationForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase Item
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name}", category="success")
            else:
                flash(f"Unfortunately! You don't have enough money!", category="danger")
        # Sell Item
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"You sold {s_item_object.name} back to market!", category="success")
            else:
                flash(f"Something went wrong!", category="danger")

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/users')
def user_page():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/update')
def update_page():
    return render_template('update.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_to_create = User(fullname=form.fullname.data,
                              username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password.data,
                              budget=form.budget.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created! You are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error: {err_msg}', category='danger')
            
    if current_user.is_authenticated:
        return redirect(url_for('market_page'))
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as {attempted_user.username}", category="success")
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password incorrect', category='danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('market_page'))
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out!", category="info")
    
    return redirect(url_for('home_page'))
    




