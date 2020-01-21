import plotly
import plotly.graph_objs as go
import json

from flask import render_template, flash, request, redirect, session, url_for
from ORM import *
from WTForms import *
from datetime import date

selected_row = None

app.secret_key = 'development key'

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/edit_user', methods = ['GET', 'POST'])
def edit_user():

    form = UserForm()

    if request.method == 'POST':
        user = User.query.filter_by(login=form.login.data).first()

        if not form.validate():
            flash_errors(form)
            return render_template("edit_user.html", row=selected_row, form=form)

        elif user:
            flash("This login already exists in 'user' entity")
            return render_template('user.html', data=select_result, form=form)

        else:
            login = session['user_edit_pk_data']
            user = User.query.filter_by(login=login).first()
            user.login = form.login.data
            user.password = form.password.data
            user.role = form.role.data
            
            if user.role == None:
                user.role = "user"
            elif user.password == None:
                user.password = 123456

            db.session.commit()

    return redirect("user")



@app.route('/user', methods=['GET', 'POST'])
def user():
    
    global selected_row
    form = UserForm()
    select_result = User.query.filter_by().all()

    if request.method == 'POST':
        user = User.query.filter_by(login=form.login.data).first()

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data
            selected_row = User.query.filter_by(login=selected_pk_data).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('user.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data
            selected_row = User.query.filter_by(login=selected_pk_data).first()
            selected_row = {
                'login': selected_row.login,
                'password' : selected_row.password,
                'role': selected_row.role,
                'sites':selected_row.sites
            }
            session['user_edit_pk_data'] = selected_pk_data
            return render_template("edit_user.html", row=selected_row, form=form)

        if not form.validate():
            flash_errors(form)
            return render_template('user.html', data=select_result, form=form)

        elif user:
            flash("This login already exists in 'user' entity")
            return render_template('user.html', data=select_result, form=form)

        else:
            user_password = form.password.data
            user_role = form.role.data
            if user_role == None:
                user_role = "user"
            elif user_password == None:
                user_password = 123456
            user = User(form.login.data, user_password, user_role)
            db.session.add(user)
            db.session.commit()
            select_result.append(user)

    return render_template('user.html', data=select_result, form=form)


@app.route('/edit_site', methods=['GET', 'POST'])
def edit_site():

    form = SiteForm()

    if request.method == 'POST':
        login = User.query.filter_by(login=form.login.data).first()
        site = Site.query.filter_by(site_address=form.site_address.data).first()

        if not form.validate():
            flash_errors(form)
            return render_template('edit_site.html', row=selected_row, form=form)

        elif not login:
            flash("Can't find this login in 'user' entity")
            return render_template('edit_site.html', row=selected_row, form=form)
        elif site:
            flash("This site_address already exists in 'site' entity")
            return render_template('edit_site.html', row=selected_row, form=form)

        else:
            selected_pk_data_list = session['site_edit_pk_data']
            selected_pk1 = selected_pk_data_list[0]
            selected_pk2 = selected_pk_data_list[1]
            site = Site.query.filter_by(login=selected_pk1, site_address = selected_pk2).first()

            site.login = form.login.data
            site.site_address = form.site_address.data
            site.site_name = form.site_name.data
            site.create_date = form.create_date.data

            if site.create_date == None:
                site.create_date = date.today()

            db.session.commit()

    return redirect(url_for("site"))


@app.route('/site', methods=['GET', 'POST'])
def site():
    global selected_row
    form = SiteForm()
    select_result = Site.query.filter_by().all()

    if request.method == 'POST':
        login = User.query.filter_by(login=form.login.data).first()
        site = Site.query.filter_by(site_address=form.site_address.data).first()

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data[0]
            selected_pk2 = selected_pk_data[1]
            selected_row = Site.query.filter_by(login=selected_pk1, site_address = selected_pk2).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            session['site_edit_pk_data'] = selected_pk_data

            return render_template('site.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data[0]
            selected_pk2 = selected_pk_data[1]
            selected_row = Site.query.filter_by(login=selected_pk1, site_address = selected_pk2).first()
            selected_row = {
                'login': selected_row.login,
                'site_address' : selected_row.site_address,
                'site_name': selected_row.site_name,
                'create_date':selected_row.create_date
            }
            session['site_edit_pk_data'] = selected_pk_data
            return render_template("edit_site.html", row=selected_row, form=form)

        site_create_date = form.create_date.data
        if site_create_date == None:
                site_create_date = date.today()
        if not form.validate():
            flash_errors(form)
            return render_template('site.html', data=select_result, form=form)

        elif not login:
            flash("Can't find this login in 'user' entity")
            return render_template('site.html', data=select_result, form=form)
        elif site:
            flash("This site_address already exists in 'site' entity")
            return render_template('site.html', data=select_result, form=form)

        else:
            site = Site(form.site_address.data, form.login.data, form.site_name.data, site_create_date)
            db.session.add(site)
            db.session.commit()
            select_result.append(site)

    return render_template('site.html', data=select_result, form=form)


@app.route('/edit_page', methods=['GET', 'POST'])
def edit_page():

    form = PageForm()

    if request.method == 'POST':
        login = User.query.filter_by(login=form.login.data).first()
        site = Site.query.filter_by(site_address=form.site_address.data).first()
        page = Page.query.filter_by(path=form.path.data).first()

        if not form.validate():
            flash_errors(form)
            return render_template("edit_page.html", row=selected_row, form=form)
        
        elif page:
            flash("This path already exists in 'page' entity")
            return render_template('edit_page.html', row=selected_row, form=form)
        elif not login:
            flash("Can't find this login in 'user' entity")
            return render_template('edit_page.html', row=selected_row, form=form)
        elif not site:
            flash("Can't find this site_address in 'site' entity")
            return render_template('edit_page.html', row=selected_row, form=form)

        else:
            selected_pk_data_list = session['page_edit_pk_data']
            selected_pk1 = selected_pk_data_list[0]
            selected_pk2 = selected_pk_data_list[1]
            page = Page.query.filter_by(site_address=selected_pk1, path = selected_pk2).first()

            page.site_address = form.site_address.data
            page.path = form.path.data
            page.title = form.title.data

            db.session.commit()

    return redirect(url_for("page"))


@app.route('/page', methods=['GET', 'POST'])
def page():
    
    global selected_row
    form = PageForm()
    select_result = Page.query.filter_by().all()

    if request.method == 'POST':
        site = Site.query.filter_by(site_address=form.site_address.data).first()
        page = Page.query.filter_by(path=form.path.data).first()

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data[0]
            selected_pk2 = selected_pk_data[1]
            selected_row = Page.query.filter_by(site_address=selected_pk1, path = selected_pk2).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            session['page_edit_pk_data'] = selected_pk_data
            return render_template('page.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data[0]
            selected_pk2 = selected_pk_data[1]
            selected_row = Page.query.filter_by(site_address=selected_pk1, path = selected_pk2).first()
            selected_row = {
                'site_address': selected_row.site_address,
                'path' : selected_row.path,
                'title': selected_row.title
            }
            session['page_edit_pk_data'] = selected_pk_data
            return render_template("edit_page.html", row=selected_row, form=form)

        if not form.validate():
            flash_errors(form)
            return render_template('page.html', data=select_result, form=form)

        elif page:
            flash("This path already exists in 'page' entity")
            return render_template('page.html', data=select_result, form=form)

        elif not site:
            flash("Can't find this site_address in 'site' entity")
            return render_template('page.html', data=select_result, form=form)

        else:
            page = Page(form.site_address.data, form.path.data, form.title.data)
            db.session.add(page)
            db.session.commit()
            select_result.append(page)

    return render_template('page.html', data=select_result, form=form)




@app.route('/edit_block', methods=['GET', 'POST'])
def edit_block():

    form = BlockForm()

    if request.method == 'POST':
        
        block = Block.query.filter_by(position=form.position.data).first()
        site = Site.query.filter_by(site_address=form.site_address.data).first()
        page_site = Page.query.filter_by(site_address=form.site_address.data).first()
        page_page = Page.query.filter_by(path=form.path.data).first()
        page = Page.query.filter_by(path=form.path.data, site_address=form.site_address.data).first()
        theme = Theme.query.filter_by(theme_name=form.theme_name.data).first()

        if not form.validate():
            flash_errors(form)
            return render_template('edit_block.html', row=selected_row, form=form)


        elif not site:
            flash("Can't find this site_address in 'site' entity")
            return render_template('edit_block.html', row=selected_row, form=form)
        elif not page_site:
            flash("Can't find this site_address in 'page' entity")
            return render_template('block.html', data=select_result, form=form)
        elif not page_page:
            flash("Can't find this path in 'page' entity")
            return render_template('block.html', data=select_result, form=form)
        elif not page:
            flash("Can't find this site_address or path in 'page' entity in one row")
            return render_template('edit_block.html', row=selected_row, form=form)
        elif not theme:
            flash("Can't find this theme_name in 'theme' entity")
            return render_template('edit_block.html', row=selected_row, form=form)
        elif block:
            flash("This position already exists in 'block' entity")
            return render_template('edit_block.html', row=selected_row, form=form)


        else:
            selected_pk_data_list = session['block_edit_pk_data'].split("█")
            selected_pk1 = selected_pk_data_list[0]
            selected_pk2 = selected_pk_data_list[1]
            selected_pk3 = selected_pk_data_list[2]
            selected_pk4 = selected_pk_data_list[3]
            block = Block.query.filter_by(site_address=selected_pk1, path = selected_pk2, position = selected_pk3, theme_name = selected_pk4).first()

            block.site_address = form.site_address.data
            block.path = form.path.data
            block.position = form.position.data
            block.theme_name = form.theme_name.data
            block.block_type = form.block_type.data
            block.content = form.content.data
            block.focus_time = form.focus_time.data
            if block.focus_time == None:
                block.focus_time = '0:0:0.0'

            db.session.commit()

    return redirect(url_for("block"))


@app.route('/block', methods=['GET', 'POST'])
def block():

    global selected_row
    form = BlockForm()
    select_result = Block.query.filter_by().all()

    if request.method == 'POST':

        block = Block.query.filter_by(position=form.position.data).first()
        site = Site.query.filter_by(site_address=form.site_address.data).first()
        page_site = Page.query.filter_by(site_address=form.site_address.data).first()
        page_page = Page.query.filter_by(path=form.path.data).first()
        page = Page.query.filter_by(path=form.path.data, site_address=form.site_address.data).first()
        theme = Theme.query.filter_by(theme_name=form.theme_name.data).first()

        selected_pk_data = request.form.get('del')
        
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data[0]
            selected_pk2 = selected_pk_data[1]
            selected_pk3 = selected_pk_data[2]
            selected_pk4 = selected_pk_data[3]
            selected_row = Block.query.filter_by(site_address=selected_pk1, path = selected_pk2, position = selected_pk3, theme_name = selected_pk4).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            session['block_edit_pk_data'] = selected_pk_data
            return render_template('block.html', data=select_result, form=form)


        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data.split("█")
            selected_pk1 = selected_pk_data_list[0]
            selected_pk2 = selected_pk_data_list[1]
            selected_pk3 = selected_pk_data_list[2]
            selected_pk4 = selected_pk_data_list[3]
            selected_row = Block.query.filter_by(site_address=selected_pk1, path = selected_pk2, position = selected_pk3, theme_name = selected_pk4).first()
            selected_row = {
                'site_address': selected_row.site_address,
                'path' : selected_row.path,
                'position': selected_row.position,
                'theme_name' : selected_row.theme_name,
                'block_type' : selected_row.block_type,
                'content' : selected_row.content,
                'focus_time' : selected_row.focus_time
            }
            session['block_edit_pk_data'] = selected_pk_data
            return render_template("edit_block.html", row=selected_row, form=form)

        if not form.validate():
            flash_errors(form)
            return render_template('block.html', data=select_result, form=form)

        elif not site:
            flash("Can't find this site_address in 'site' entity")
            return render_template('block.html', data=select_result, form=form)
        elif not page_site:
            flash("Can't find this site_address in 'page' entity")
            return render_template('block.html', data=select_result, form=form)
        elif not page_page:
            flash("Can't find this path in 'page' entity")
            return render_template('block.html', data=select_result, form=form)
        elif not page:
            flash("Can't find this site_address or path in 'page' entity in one row")
            return render_template('block.html', data=select_result, form=form)
        elif not theme:
            flash("Can't find this theme_name in 'theme' entity")
            return render_template('block.html', data=select_result, form=form)
        elif block:
            flash("This position already exists in 'block' entity")
            return render_template('block.html', data=select_result, form=form)

        else:
            block_focus_time = form.focus_time.data
            if block_focus_time == None:
                block_focus_time = '0:0:0.0'
            block = Block(form.site_address.data, form.path.data, form.position.data, form.theme_name.data, form.block_type.data, form.content.data, block_focus_time)
            db.session.add(block)
            db.session.commit()
            select_result.append(block)

    return render_template('block.html', data=select_result, form=form)

@app.route('/edit_theme', methods = ['GET', 'POST'])
def edit_theme():

    form = ThemeForm()

    if request.method == 'POST':
        theme = Theme.query.filter_by(theme_name=form.theme_name.data).first()

        if not form.validate():
            flash_errors(form)
            return render_template('edit_theme.html', row=selected_row, form=form)

        elif theme:
            flash("This theme_name already exists in 'theme' entity")
            return render_template('edit_theme.html', row=selected_row, form=form)

        else:
            theme_name = session['theme_edit_pk_data']
            theme = Theme.query.filter_by(theme_name=theme_name).first()
            theme.theme_name = form.theme_name.data
            theme.popularity = form.theme_popularity.data
            if form.theme_popularity.data == None:
                theme.popularity = 0
            theme.code = form.code.data
            
            

            db.session.commit()

    return redirect(url_for("theme"))


@app.route('/theme', methods=['GET', 'POST'])
def theme():

    global selected_row
    form = ThemeForm()
    select_result = Theme.query.filter_by().all()

    if request.method == 'POST':
        theme = Theme.query.filter_by(theme_name=form.theme_name.data).first()

        selected_pk_data = request.form.get('del')
        if selected_pk_data is not None:
            selected_pk_data = selected_pk_data
            selected_row = Theme.query.filter_by(theme_name=selected_pk_data).first()
            db.session.delete(selected_row)
            db.session.commit()
            select_result.remove(selected_row)
            return render_template('theme.html', data=select_result, form=form)

        selected_pk_data = request.form.get('edit')
        if selected_pk_data is not None:
            selected_pk_data_list = selected_pk_data
            selected_row = Theme.query.filter_by(theme_name=selected_pk_data).first()
            selected_row = {
                'theme_name': selected_row.theme_name,
                'theme_popularity' : selected_row.theme_popularity,
                'code': selected_row.code
            }
            session['theme_edit_pk_data'] = selected_pk_data
            return render_template("edit_theme.html", row=selected_row, form=form)

        if not form.validate():
            flash_errors(form)
            return render_template('theme.html', data=select_result, form=form)

        elif theme:
            flash("This theme_name already exists in 'theme' entity")
            return render_template('theme.html', data=select_result, form=form)

        else:
            theme_popularity = form.theme_popularity.data
            if theme_popularity == None:
                theme_popularity = 0
            theme = Theme(form.theme_name.data, theme_popularity, form.code.data)
            db.session.add(theme)
            db.session.commit()
            select_result.append(theme)

    return render_template('theme.html', data=select_result, form=form)


if __name__ == '__main__':
    app.run(debug=True)