from fileinput import filename
import random, os
from flask import render_template, redirect, session, flash,request,jsonify
from weddingapp import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from weddingapp.forms import ContactForm, SignupForm
from weddingapp.models import Contact, Guest_gift, Guests,Gifts, Comment, State,Lga
@app.route('/')
def home():
    return render_template('user/index.html')
@app.route('/message')
def message():
    cform=ContactForm()
    return render_template('user/contact.html', cform=cform)
@app.route('/submission', methods=['POST'])
def submission():
    cform=ContactForm()
    if cform.validate_on_submit():
        fname = request.form.get('fullname')
        email= request.form.get('email')
        msg = request.form.get('message')
        #insert to db
        contact = Contact(con_fullname=fname, con_email=email, con_message=msg)
        db.session.add(contact)
        db.session.commit()
        flash('Message sent!')
        return 'Got here'
    else:
        return render_template('user/contact.html', cform=cform)
@app.route('/signup', methods=["POST", "GET"])
def signup():
    sform=SignupForm()
    if request.method == "GET":
         return render_template('user/signup.html', sform=sform)
    else:
        if sform.validate_on_submit():
            firstname = sform.firstname.data
            #firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            password = request.form.get('password')
            email= request.form.get('useremail')
            hashed=generate_password_hash(password)
        #insert to db
            user = Guests(guest_fname=firstname,guest_lname=lastname, guest_email=email, guest_image='', guest_pwd=hashed)
            db.session.add(user)
            db.session.commit()
            #retireve the guest id
            guestid= user.guest_id
            #save the id in session so that it can be used else where
            session['guest']=guestid
            flash('Sign up complete')
            return redirect('/profile')
        else:
            return render_template('user/signup.html', sform=sform)
@app.route('/login', methods=["POST", "GET"] )
def login():
    if request.method =='GET':
        return render_template('user/login.html')
    else:
        email = request.form.get('email')
        password= request.form.get('password')
        #retrieve the hashed password belonging to this user 
        userdeets=Guests.query.filter(Guests.guest_email==email).first()
        if userdeets and check_password_hash(userdeets.guest_pwd, password):
            session['guest'] = userdeets.guest_id
            return redirect('/profile')
        else:
            flash('Invalid')
            return redirect('/login')
@app.route('/update', methods=["POST", "GET"])
def updates():
    loggedin= session.get('guest')
    if loggedin != None:
        if request.method == "GET":
            return render_template('user/edit.html')
        else:
        
            guest_deets= db.session.query(Guests).filter(Guests.guest_id ==loggedin).first()
            #retrieve form data
            fname= request.form.get('fname')
            lname= request.form.get('lname')
            address= request.form.get('address')
            update= db.session.query(Guests).get(loggedin)
            update.guest_fname = fname
            update.guest_lname = lname
            update.guest_address = address
            db.session.commit()
            flash(' updated')
            return redirect('/profile')
    else:
        return redirect('/login')
                
@app.route('/profile')
def profile():
    loggedin= session.get('guest')
    if loggedin != None:
        guest_deets= db.session.query(Guests).filter(Guests.guest_id ==loggedin).first()
        return render_template('user/profile.html', guest_deets=guest_deets)

@app.route('/user/logout/')
def user_logout():
    session.pop('guest', None)
    return redirect('/login')
@app.route('/user/upload')
def upload_pix():
    loggedin= session.get('guest')
    guest_deets= db.session.query(Guests).filter(Guests.guest_id ==loggedin).first()
    if loggedin != None:
        return render_template('user/upload_profile.html', guest_deets= guest_deets)
    else:
       return redirect('/login')
                 
@app.route('/submit/upload', methods=["POST"])
def submit_pix():
    loggedin= session.get('guest')
    if loggedin != None:
        #retrieve for data and upload
        if request.files !='':
            allowed = ['.jpg', '.png','.jpeg']
            fileobj = request.files.get('profilepix')
            filename=fileobj.filename#don't use this, it can clash
            newname=random.random()*1000000000
            picturename, ext =os.path.splitext(filename)#splits file into 2 parts on the extension
            if ext in allowed:
                path= 'weddingapp/static/uploads/'+str(newname)+ext
                fileobj.save(f'{path}')
                picture=db.session.query(Guests).get(loggedin)
                picture.guest_image = str(newname)+ext
                db.session.commit()
                flash('upload Done')
                return redirect('/profile' )
            else:
                flash('Invalid format')
                return redirect('/user/upload')
        else:
            flash('please select valid image')
            return redirect('/user/upload')
    else:
       return redirect('/login') 
@app.route('/registry')
def registry():
    loggedin= session.get('guest')
    guest_deets= db.session.query(Guests).filter(Guests.guest_id ==loggedin).first()
    if loggedin != None:
        promised_gifts =[]
        promised=db.session.query(Guest_gift).filter(Guest_gift.g_guestid==loggedin).all()
        
        if promised:
            for p in promised:
                promised_gifts.append(p.g_giftid)
        gift_select= db.session.query(Gifts).all()
        return render_template('user/gift_registry.html', gifts=gift_select, promised_gifts=promised_gifts)
    else:
        return redirect('/login')
@app.route('/submit/registry', methods=['POST', "GET"] )
def submit_registry():
    loggedin= session.get('guest')
    guest_deets= db.session.query(Guests).filter(Guests.guest_id ==loggedin).first()
    if loggedin != None:
        selected = request.form.getlist('gifts')
        db.session.execute(f'DELETE FROM guest_gift WHERE g_guestid="{loggedin}"')
        db.session.commit()
        for s in selected:
            guestgift=Guest_gift()
            db.session.add(guestgift)
            guestgift.g_giftid = s
            guestgift.g_guestid = loggedin
            db.session.commit()
        flash('Thank you, Gifts recorded')
        return redirect("/registry")
    else:
        return redirect('/login')
@app.route('/forum')
def forum():
    return render_template('user/forum.html')
@app.route('/send/forum', methods=['POST','GET'])
def sendforum():
    loggedin= session.get('guest')
    if loggedin != None:
        content= request.args.get('suggestion')
        messages=Comment()
        messages.comment_content = content
        messages.comment_guestid = loggedin
        db.session.add(messages)
        db.session.commit()
        if messages.comment_id > 0 and messages.comment_content !='':
            return "your suggestion has been added"
        else:
            return 'Please try again'
    else:
        return redirect('/login')
@app.route('/ajaxtest')
def ajaxtest():
    states= db.session.query(State).all()
    return render_template('user/testing.html', states=states)
@app.route('/ajaxtest/state')
def ajaxtest_state():
    selected=request.args.get('stateid')
    lgas= db.session.query(Lga).filter(Lga.state_id == selected).all()
    retstr=''
    for i in lgas:
        retstr= retstr + f"<option value='{i.lga_id}'>{i.lga_name}</option>"
    return retstr


@app.route('/ajaxtest/check', methods=['POST', 'GET'])
def ajaxtest_submit():
    user=request.values.get('username') #used for both post and get
    chck=db.session.query(Guests).filter(Guests.guest_email ==user).first()
    if chck != None:
        return 'Username has been taken'
    else:
        return 'Username is available'
@app.route('/ajaxtest/final', methods=['POST'])
def ajaxtest_final():
    appended_data = request.form.get('missing')
    firstname=request.form.get('firstname')
    lastname= request.form.get('lastname')
    #retrieve the file here
    fileobj= request.files.get('image')
    original_filename =fileobj.filename
    fileobj.save(f'weddingapp/static/images/{original_filename}')
    #insert into db
    return jsonify(firstname=firstname, lastname=lastname, appended_data=appended_data, filename=original_filename)
   