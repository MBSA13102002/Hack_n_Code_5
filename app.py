from flask import Flask,render_template,request,make_response,redirect,url_for
import random as rd
from datetime import date


app = Flask(__name__)
month_number = {"1":"January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}
def rand_pass(len):
    pass_data = "qwertyuiopasdfgjklzxcvbnm1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    password = "".join(rd.sample(pass_data, len))
    return password


@app.route('/',methods= ['GET','POST'])
def start():
    if request.method == 'POST':
        uid_for_user = request.form.get("roll__no")
        resp = make_response(render_template('index.html',UID =uid_for_user))
        resp.set_cookie('__user__',uid_for_user,max_age = 60*60*24)
        resp.set_cookie('__registered__',"0",max_age = 60*60*24)
        return resp
        
    if (request.cookies.get('__user__')==None):
        return render_template("login.html")



    else:
        uid_for_user = request.cookies.get('__user__')
        return render_template('index.html',UID =uid_for_user)


@app.route('/mess',methods = ['GET','POST'])
def mess():
    print(f"request.cookies.get('__registered__') = {request.cookies.get('__registered__')}")
    if (request.cookies.get('__registered__') == "0"):
        return render_template('mess_detail.html',resp_code = 540,new_mess="")
    else:
        new_mess = request.cookies.get('__mess_name__')
        return render_template('mess_detail.html',resp_code = 541,new_mess=new_mess)


@app.route('/mess/dues',methods = ['GET','POST'])
def mess_dues():
    return render_template('mess_detail_dues.html')

@app.route('/mess/card',methods = ['GET','POST'])
def mess_card():
    if(request.cookies.get('__registered__')=='0'):
        return redirect(url_for('start'))
    return render_template('mess_card.html',mess_card_number=request.cookies.get('__mess_card_number__'),mess_name =request.cookies.get('__mess_name__'),date = request.cookies.get('__issuedate__'))

@app.route('/mess/change',methods = ['GET','POST'])
def mess_change():
    if request.method =="POST":
        new_mess_name = request.form.get("New_Mess_Name") 
        __resp__ = make_response(redirect(url_for('mess')))
        __resp__.set_cookie('__mess_name__',new_mess_name,max_age = 60*60*24)  
        return __resp__ 
    mess_name = request.cookies.get("__mess_name__")
    return render_template('mess_detail_change.html',mess_name = mess_name)

@app.route('/mess/invoice',methods = ['GET','POST'])
def mess_invoice():
    if(request.cookies.get('__registered__')=='0'):
        return redirect(url_for('start'))
    else:
        global today,mess_card_number
        today = date.today()
        mess_card_number = rd.randint(10000, 99999) 
        resp = make_response(render_template('mess_invoice.html'))
        resp.set_cookie('__issuedate__',str(today),max_age = 60*60*24)
        resp.set_cookie('__mess_card_number__',str(mess_card_number),max_age = 60*60*24)
        return resp

@app.route('/mess/payments',methods = ['POST'])             
def mess_payments():
    if request.method == 'POST':
        resp__ = make_response(redirect(url_for('mess_invoice')))
        resp__.set_cookie('__registered__',"1",max_age = 60*60*24)
        return resp__


@app.route('/mess/registration',methods = ['GET','POST'])
def mess_registration():
    if request.method == 'POST':
        global mess_name
        mess_name = request.form.get('Mess_Name')
        resp_ = make_response(render_template('mess_detail_payment.html',mess_name = mess_name))
        resp_.set_cookie('__mess_name__',mess_name)
        return resp_
    return render_template('mess_detail_registration.html',rollno = request.cookies.get('__user__'))

@app.route('/hostel/registration',methods = ['GET','POST'])
def hostel_registration():
    if request.method == 'POST':
        global Hostel_Name
        Hostel_Name = request.form.get('Hostel_Name')
        resp_ = make_response(render_template('inside_hostel.html',Hostel_Name = Hostel_Name))
        resp_.set_cookie('__hostel_name__',Hostel_Name)
        return resp_
    # return render_template('mess_detail_registration.html',rollno = request.cookies.get('__user__'))
@app.route("/room-allot",methods = ['GET','POST'])
def room_allot():
    if request.method == 'POST':
        room_no = request.form.get('Room_No')
        Hostel_Name = request.cookies.get("__hostel_name__")
        resp_ = make_response(render_template('room_slip.html',Hostel_Name = Hostel_Name,room_no = room_no))
        resp_.set_cookie('__room_number__',str(room_no))
        return resp_
# @app.route('/mess/delete',methods = ['GET','POST'])
# def mess_delete():
#     if request.method == 'POST':
#         resp = make_response(redirect(url_for('start')))
#         resp.set_cookie('__user__','',max_age=0)
#         resp.set_cookie('__mess_name__','',max_age=0)
#         resp.set_cookie('__registered__','',max_age=0)
#         resp.set_cookie('__mess_card_number__','',max_age=0)
#         resp.set_cookie('__issuedate__','',max_age=0)
#         return resp

@app.route('/hostel',methods = ['GET','POST'])
def hostel():
    rollno = request.cookies.get('__user__')
    return render_template('hostel.html',rollno =rollno)



if __name__ == '__main__':
    app.run(debug = True)
