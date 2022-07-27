from datetime import datetime
from flask import render_template, redirect, session, flash, request, url_for
from weddingapp import app, db, csrf
from weddingapp.models import Admin,Gifts, Guests

@app.route('/admin', methods=["POST", "GET"])
@csrf.exempt
def admin_home():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    else:
        #form submitted, retrieve form data
        username = request.form.get('username')
        pwd= request.form.get('pswd')
        ad =Admin.query.filter(Admin.admin_username==username, Admin.admin_pwd==pwd).first()
        if ad:
            adminid = ad.admin_id
            admin_fullname = ad.admin_name
            session['adminid']=adminid
            session['adminname'] =admin_fullname
            return redirect('/admin/dashboard')
        else:
            flash('Invalid credentials')
            return redirect('/admin')
       
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('adminid')!= None and session.get('adminname')!= None:
        return render_template('admin/admin_dashboard.html')
    else:
       return redirect('/admin') 
@app.route('/logout')
def logout():
    session.pop('adminid', None)
    session.pop('adminname', None)
    return redirect('/admin')
@app.route('/admin/manage_gifts')
def manage_gifts():
    #protect this page for only logged in users
    if session.get('adminid')!= None and session.get('adminname')!= None:
        records = db.session.query(Gifts).order_by(Gifts.gift_name.desc()).all()
        names = db.session.query(Guests).all()
        return render_template('/admin/all_gifts.html', records=records, names=names)
    else:
        return render_template('/admin')
@app.route('/admin/add/gift', methods=['GET', 'POST'])
def add_gifts():
    if session.get('adminid')!= None and session.get('adminname')!= None:
        if request.method == 'GET':
            return render_template('admin/add_gifts.html')
        else:
            giftname =request.form.get('giftname')
            g=Gifts(gift_name=giftname)
            db.session.add(g)
            db.session.commit()
            return redirect('/admin/manage_gifts')
    else:
        flash('Invalid Credentials')
        return redirect('/admin')
@app.route('/admin/edit/<id>')
def edit(id):
    deets = Gifts.query.get(id)
    
    return render_template('admin/edit_gifts.html', deets=deets)

@app.route('/admin/delete/<id>')
def delet(id):
    x = db.session.query(Gifts).get(id)
    db.session.delete(x)
    db.session.commit()
    flash('Gift Deleted') 
    return redirect(url_for('manage_gifts'))
@app.route('/admin/all/guests')
def all_guests():
    #protect this page for only logged in users
    if session.get('adminid')!= None and session.get('adminname')!= None:
        names = db.session.query(Guests).all()
        return render_template('/admin/all_guests.html', names=names)
    else:
        return render_template('/admin')
@app.route('/admin/update', methods=["POST"])
def update_gift():
    #retrieve form data
    newname= request.form.get('giftname')
    id= request.form.get('id')
    updates = db.session.query(Gifts).get(id)
    updates.gift_name = newname
    db.session.commit()
    flash('Gift was sucessfully updated')
    return redirect(url_for('manage_gifts'))


