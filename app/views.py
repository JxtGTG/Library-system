from flask import request, flash, url_for, redirect, render_template
from flask_paginate import get_page_parameter
from sqlalchemy import or_

from app import app
from app import db
from app.form import Register, fLogin, Todo, Search, tCategory
from app.models import Affairs, Users, Category

# function for the login page
@app.route('/', methods=['GET', 'POST'])
def show():
    form = Register()
    form2 = fLogin()
    if form.validate_on_submit():
        first = db.session.query(Users).filter(Users.Name == form.Name.data).all()
        # check if the name was used
        if len(first) > 0:
            flash('Can not register with a registered name', 'error')
            return redirect(url_for('show'))
        else:
            try:
                user = Users(form.Name.data, form.Password.data,
                             form.Email.data)
                db.session.add(user)
                db.session.commit()
                flash('Record was successfully added', 'good')
                return redirect(url_for('show'))
            except Exception as e:
                db.session.rollback()
                raise e

    return render_template('Login.html', form=form, form2=form2)

# function for the login process
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = fLogin()

    if form.validate_on_submit():
        name = form.Name.data
        password = form.Password.data
        user = db.session.query(Users).filter(Users.Name == name, Users.Password == password).all()
        # check if it is correct
        if len(user) == 1:
            id = user[0].id
            username = user[0].Name
            flash('welcome' + username, 'good')
            return redirect(url_for('add', id=id, c_id=0))
        else:
            flash('Username or password is invalid', 'error')
            return redirect(url_for('show'))
    return ""

# function for adding assessment
@app.route('/add/<int:id> <int:c_id>', methods=['GET', 'POST'])
def add(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()

    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)
        blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("incomplete.html", items=items, id=id, c_id=0, pagination=blogs, form=form, form2=form2,
                               form3=form3, category_now=None, categories=categories)
    if c_id == 0:
        c_id = categories[0].id
    if form.validate_on_submit():
        des = form.Des.data
        ddl = form.ddl.data
        a_name = form.name.data
        setdate = form.setdate.data
        big = int(form.big.data)
        priority = request.form['pri']

        create = int(form.create.data)
        category_id = request.form['category']

        try:
            todo = Affairs(a_name, des, setdate, ddl, priority, big, create, id, category_id)
            db.session.add(todo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        pageSize = 5
        category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
        categories = Category.query.filter_by(user_id=id).all()
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)

        blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("incomplete.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                               form2=form2, form3=form3, category_now=category, categories=categories)

    categories = Category.query.filter_by(user_id=id).all()
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
    pageSize = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize
    end = start + pageSize
    items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)
    blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
    return render_template("incomplete.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form, form2=form2,
                           form3=form3, category_now=category, categories=categories)


# function for adding category
@app.route('/add_ca/<int:id> <int:c_id>', methods=['GET', 'POST'])
def add_ca(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()

    if form3.validate_on_submit():
        category = form3.C_name.data
        try:
            ca = Category(category, id)

            db.session.add(ca)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        categories = Category.query.filter_by(user_id=id).all()

        if c_id == 0:
            c_id = categories[0].id

        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
        categories = Category.query.filter_by(user_id=id).all()
        items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)

        blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("incomplete.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                               form2=form2, form3=form3, category_now=category, categories=categories)

# function for deleting category
@app.route('/delete_catcory/<int:id> <int:c_id>')
def delete_category(id, c_id):
    item = Category.query.get_or_404(c_id)
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        c_id = 0
    else:
        c_id = Category.query.filter_by(user_id=id).all()[0].id
    return redirect(url_for('add', id=id, c_id=c_id))

# function for marking assessment as done state
@app.route('/done/<int:id> <int:c_id>', methods=['GET', 'POST'])
def done(id, c_id):
    item = Affairs.query.get_or_404(id)
    item.state = 1
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('add', id=item.user_id, c_id=c_id))

# function for marking assessment as undone state
@app.route('/indone/<int:id> <int:c_id>', methods=['GET', 'POST'])
def indone(id, c_id):
    item = Affairs.query.get_or_404(id)
    item.state = 0
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('complete', id=item.user_id, c_id=c_id))


# function for deleting assessment
@app.route('/delete/<int:id> <int:c_id>')
def deleteitem(id, c_id):
    item = Affairs.query.get_or_404(id)
    id = item.user_id
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for('add', id=id, c_id=c_id))

# function for deleting assessment in complete page
@app.route('/delete-c/<int:id> <int:c_id>')
def deleteitem_c(id, c_id):
    item = Affairs.query.get_or_404(id)
    id = item.user_id
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for('complete', id=id, c_id=c_id))

# function for edit assessment
@app.route('/edit-item/<int:id> <int:c_id>', methods=['GET', 'POST'])
def edit_item(id, c_id):
    item = Affairs.query.get_or_404(id)
    item.a_name = request.form['a_name']
    item.des = request.form['des']
    item.ddl = request.form['ddl']
    item.setdate = request.form['setdate']
    item.big = int(request.form['big'])
    item.create = int(request.form['create'])
    item.priority = request.form['pri']
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for('add', id=item.user_id, c_id=c_id))

# function for edit assessment in complete page
@app.route('/edit-item-c/<int:id> <int:c_id>', methods=['GET', 'POST'])
def edit_item_c(id, c_id):
    item = Affairs.query.get_or_404(id)
    item.a_name = request.form['a_name']
    item.ddl = request.form['ddl']
    item.big = int(request.form['big'])
    item.create = int(request.form['create'])
    item.des = request.form['des']
    item.setdate = request.form['setdate']
    item.priority = request.form['pri']
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return redirect(url_for('complete', id=item.user_id, c_id=c_id))

# function for show the assessments of completed state
@app.route('/complete/<int:id> <int:c_id>', methods=['GET', 'POST'])
def complete(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    pageSize = 5
    categories = Category.query.filter_by(user_id=id).all()
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]

    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize
    end = start + pageSize
    items = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).slice(start, end)

    blogs = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).paginate(page=page, per_page=5)
    return render_template("complete.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                           form2=form2, form3=form3, category_now=category, categories=categories)

# function for search function in incomplete page
@app.route('/search/<string:keyword><int:id><string:type> <int:c_id>', methods=['GET', 'POST'])
def search(keyword, id, type, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    # search form on submit
    if form2.validate_on_submit():
        # get type
        if type == "None":
            type = request.form['type']

        if type == "Des":
            # get keyword
            keyword = form2.search.data
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                # check if empty
                if len(itemss) == 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword, form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('add', id=id, c_id=c_id))

        elif type == "Date":
            keyword = form2.date1.data
            if keyword != "No DDL":
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword, form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)

        elif type == "All":
            keyword = form2.all.data
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                names = db.session.query(Affairs).filter(Affairs.a_name.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).all()
                des = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                       Affairs.state == 0, Affairs.category_id == c_id).all()
                ddls = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                        Affairs.state == 0, Affairs.category_id == c_id).all()
                setdates = db.session.query(Affairs).filter(Affairs.setdate.contains(keyword), Affairs.user_id == id,
                                                            Affairs.state == 0, Affairs.category_id == c_id).all()
                priority = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                            Affairs.state == 0, Affairs.category_id == c_id).all()
                itemss = names + des + ddls + setdates + priority
                items = db.session.query(Affairs).filter(
                    or_(Affairs.a_name.contains(keyword), Affairs.des.contains(keyword), Affairs.ddl.contains(keyword),
                        Affairs.setdate.contains(keyword), Affairs.priority.contains(keyword)),
                    Affairs.user_id == id, Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(
                    or_(Affairs.a_name.contains(keyword), Affairs.des.contains(keyword), Affairs.ddl.contains(keyword),
                        Affairs.setdate.contains(keyword), Affairs.priority.contains(keyword)),
                    Affairs.user_id == id, Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)

        else:
            keyword = request.form['pri1']
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 0,
                                                         Affairs.category_id == c_id).slice(start, end)
                blogs = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 0,
                                                         Affairs.category_id == c_id).paginate(page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('add', id=id, c_id=c_id))
    else:
        if type == "Des":
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) == 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('add', id=id, c_id=c_id))
        elif type == "Date":
            if keyword != "No DDL":
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 0, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
        else:
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 0,
                                                         Affairs.category_id == c_id).slice(start, end)
                blogs = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 0,
                                                         Affairs.category_id == c_id).paginate(page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 0, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('add', id=id, c_id=c_id))

# function for search in complete page
@app.route('/search_c/<string:keyword><int:id><string:type> <int:c_id>', methods=['GET', 'POST'])
def search_c(keyword, id, type, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    if form2.validate_on_submit():

        if type == "None":
            type = request.form['type']

        if type == "Des":
            keyword = form2.search.data
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) == 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword, form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('complete', id=id, c_id=c_id))

        elif type == "Date":
            keyword = form2.date1.data
            if keyword != "No DDL":
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword, form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)

        elif type == "All":
            keyword = form2.all.data
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                names = db.session.query(Affairs).filter(Affairs.a_name.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).all()
                des = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                       Affairs.state == 1, Affairs.category_id == c_id).all()
                ddls = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                        Affairs.state == 1, Affairs.category_id == c_id).all()
                setdates = db.session.query(Affairs).filter(Affairs.setdate.contains(keyword), Affairs.user_id == id,
                                                            Affairs.state == 1, Affairs.category_id == c_id).all()
                priority = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                            Affairs.state == 1, Affairs.category_id == c_id).all()
                itemss = names + des + ddls + setdates + priority
                items = db.session.query(Affairs).filter(
                    or_(Affairs.a_name.contains(keyword), Affairs.des.contains(keyword), Affairs.ddl.contains(keyword),
                        Affairs.setdate.contains(keyword), Affairs.priority.contains(keyword)),
                    Affairs.user_id == id, Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(
                    or_(Affairs.a_name.contains(keyword), Affairs.des.contains(keyword), Affairs.ddl.contains(keyword),
                        Affairs.setdate.contains(keyword), Affairs.priority.contains(keyword)),
                    Affairs.user_id == id, Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)

        else:
            keyword = request.form['pri1']
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 1,
                                                         Affairs.category_id == c_id).slice(start, end)
                blogs = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 1,
                                                         Affairs.category_id == c_id).paginate(page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('complete', id=id, c_id=c_id))
    else:
        if type == "Des":
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.des.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) == 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('complete', id=id, c_id=c_id))
        elif type == "Date":
            if keyword != "No DDL":
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).slice(
                    start, end)
                blogs = db.session.query(Affairs).filter(Affairs.ddl.contains("date"), Affairs.user_id == id,
                                                         Affairs.state == 1, Affairs.category_id == c_id).paginate(
                    page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.ddl.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
        else:
            if keyword:
                pageSize = 5
                page = request.args.get(get_page_parameter(), type=int, default=1)
                start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
                end = start + pageSize
                items = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 1,
                                                         Affairs.category_id == c_id).slice(start, end)
                blogs = db.session.query(Affairs).filter(Affairs.priority.contains(keyword),
                                                         Affairs.user_id == id, Affairs.state == 1,
                                                         Affairs.category_id == c_id).paginate(page=page, per_page=5)
                itemss = db.session.query(Affairs).filter(Affairs.priority.contains(keyword), Affairs.user_id == id,
                                                          Affairs.state == 1, Affairs.category_id == c_id).all()
                categories = Category.query.filter_by(user_id=id).all()
                category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
                if len(itemss) is 0:
                    flash('The search result is empty', 'searcherror')
                return render_template("search_c.html", items=items, c_id=c_id, id=id, pagination=blogs, type=type,
                                       keyword=keyword,
                                       form=form, form2=form2, form3=form3, category_now=category,
                                       categories=categories)
            else:
                return redirect(url_for('complete', id=id, c_id=c_id))

# function for sort in ascending way
@app.route('/sort_as<int:id> <int:c_id>')
def sort_as(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)
        blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("incomplete.html", items=items, id=id, c_id=0, pagination=blogs, form=form, form2=form2,
                               form3=form3, category_now=None, categories=categories)
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
    pageSize = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
    end = start + pageSize
    items = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 0,
                                             Affairs.category_id == c_id).order_by(Affairs.big).slice(start, end)
    blogs = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 0,
                                             Affairs.category_id == c_id).order_by(Affairs.big).paginate(page=page,
                                                                                                         per_page=5)
    return render_template("sort_as.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                           form2=form2, form3=form3, category_now=category, categories=categories)

# function for sort in descending way
@app.route('/sort_ds<int:id> <int:c_id>')
def sort_ds(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    pageSize = 5
    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).slice(start, end)
        blogs = Affairs.query.filter_by(user_id=id, state=0, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("incomplete.html", items=items, id=id, c_id=0, pagination=blogs, form=form, form2=form2,
                               form3=form3, category_now=None, categories=categories)
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize  # limit后第一个参数 每一页开始位置
    end = start + pageSize
    items = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 0,
                                             Affairs.category_id == c_id).order_by(Affairs.big.desc()).slice(start, end)
    blogs = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 0,
                                             Affairs.category_id == c_id).order_by(Affairs.big.desc()).paginate(
        page=page, per_page=5)
    return render_template("sort_ds.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                           form2=form2, form3=form3, category_now=category, categories=categories)

# function for sorting completed assessment in ascending way
@app.route('/sort_cas<int:id> <int:c_id>')
def sort_cas(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).slice(start, end)
        blogs = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("complete.html", items=items, id=id, c_id=0, pagination=blogs, form=form, form2=form2,
                               form3=form3, category_now=None, categories=categories)
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
    pageSize = 5
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize
    end = start + pageSize
    items = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 1,
                                             Affairs.category_id == c_id).order_by(Affairs.big).slice(start, end)
    blogs = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 1,
                                             Affairs.category_id == c_id).order_by(Affairs.big).paginate(page=page,
                                                                                                         per_page=5)
    return render_template("sort_cas.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                           form2=form2, form3=form3, category_now=category, categories=categories)

# function for sorting completed assessment in descending way
@app.route('/sort_cds<int:id> <int:c_id>')
def sort_cds(id, c_id):
    form = Todo()
    form2 = Search()
    form3 = tCategory()
    pageSize = 5
    categories = Category.query.filter_by(user_id=id).all()
    if len(categories) == 0:
        pageSize = 5
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * pageSize
        end = start + pageSize
        items = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).slice(start, end)
        blogs = Affairs.query.filter_by(user_id=id, state=1, category_id=c_id).paginate(page=page, per_page=5)
        return render_template("complete.html", items=items, id=id, c_id=0, pagination=blogs, form=form, form2=form2,
                               form3=form3, category_now=None, categories=categories)
    category = Category.query.filter_by(id=c_id, user_id=id).all()[0]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * pageSize
    end = start + pageSize
    items = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 1,
                                             Affairs.category_id == c_id).order_by(Affairs.big.desc()).slice(start, end)
    blogs = db.session.query(Affairs).filter(Affairs.user_id == id, Affairs.state == 1,
                                             Affairs.category_id == c_id).order_by(Affairs.big.desc()).paginate(
        page=page, per_page=5)
    return render_template("sort_cds.html", items=items, id=id, c_id=c_id, pagination=blogs, form=form,
                           form2=form2, form3=form3, category_now=category, categories=categories)
