#Importing the necessary libraries

import json 
import pandas as pd
import matplotlib.pyplot as plt
from flask import request, jsonify,send_from_directory,send_file
from flask import current_app as app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity
from datetime import timedelta
from sqlalchemy import and_
from sqlalchemy import func
import datetime
from application.models import *
from application.database import db 
from validate_email import validate_email
from io import StringIO
from application.cache import cache 


bcrypt = Bcrypt(app)

@app.route('/', methods = ['GET','POST']) #default route for testing purpose
def index():
    return 'API IS RUNNING...'

@app.route('/api/usersignup',methods=['POST']) #route for user signup
def user_signup():
    
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not validate_email(email): #checking whether the email entered by the user is valid or not
        return jsonify({'message': 'Invalid email format'})

    user = User.query.filter_by(username = username).first() #trying to check if any other user is present with same username
    
    if user is not None: #if same username already exists then usename needs to changed
        return jsonify({'message': 'Username already registered'})
    else:
        user = User()

    user.username = username

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') #storing the password of user in hash format
    user.password = hashed_password
    user.is_admin = 0 #differentiating btw admin and user. [ for user it is 0, for admin it is 1]

    user.email = email

    print(user.username,user.email,user.password,user.is_admin)
    
    db.session.add(user) #saving the user details to the database
    db.session.commit()
    return jsonify({'message': 'User created successfully.'})


@app.route('/login',methods=['GET','POST']) #route for login of both user and admin
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username = username).first()
    #print(user.username,user.password, password)

    if user is None:
        return{'message': 'User doesnot exist'}
    
    hashed_password = user.password
    
    if not bcrypt.check_password_hash(hashed_password, password): #checking the password entered matches from database 
        return {'message':'Incorrect password'}
    
    #creating access token and giving it a time frame 
    access_token = create_access_token(identity = user.username,expires_delta=timedelta(1)) #time framing access

    return jsonify({'status': 'success','message': 'Successfully logged in !!', 
                    'access_token': access_token, "username": username, 'is_admin':user.is_admin})


@app.route('/admin/dashboard' ,methods=['GET','POST']) #route for admin dashboard
@jwt_required()
def admin_dashboard():
    print('admindashboard')
    current_user = get_jwt_identity() #getting the current user 
    print(current_user)
    if current_user.is_admin:
        return jsonify({'message':f'Welcome,{current_user}! this is admin dashboard'})
    return jsonify({'Error':'Unauthorised access'}),505

@app.route('/user/dashboard', methods=['GET','POST']) #route for user dashboard after login
@jwt_required()
def user_dashboard():
    current_user = get_jwt_identity()
    if not(current_user.is_admin):
        return jsonify({'message':f'Welcome,{current_user}!this is user dashboard'})
    return jsonify({'Error':'Unauthorised Access'})
@app.route('/createtheatre', methods=['POST']) #route for creation of theatre via admin
@jwt_required()
def create_theatre():
    print('checkpoint')
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting the details of admin
    print(current_user)
    if(current_user.is_admin): #checking whether this feature is accessed by admin or normal user
        #if it is admin then only entry is permitted else access is denied
        theatre = Theatre()
        #creation of theatre by getting the values from the form and storing it in the table of theatre in database
        theatre.name = request.json.get('theatrename')
        theatre.place = request.json.get('place')
        theatre.location = request.json.get('location')
        theatre.capacity = request.json.get('capacity')

        if Theatre.query.filter_by(name = theatre.name).count()>0:
            #checking whether the theatre name already exists or not
            return jsonify({'error': 'theatre name already exist'}),409
        elif theatre.capacity == '0' or theatre.place==' ' or theatre.name ==' ' or theatre.location==' ':
            return jsonify({'error':'Empty field'}),409
        else:
            #if theatre name doesn't already exist then store it in the database 
            print(theatre.name)
            db.session.add(theatre)
            db.session.commit()
            cache.delete_memoized(getalltheatre)
            return jsonify({'message':'Theatre created Successfully'})
    else:
        return jsonify({'message':'Unauthorized Access'}),505
    
@app.route('/edittheatre', methods=['GET','PUT','DELETE']) #route for updation/deletion of theatres
@jwt_required()
def edit_theatre():
    print('checkpoint')
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting details of user accessing the route
    print(current_user)
    if(current_user.is_admin): #checking if the user is admin or normal user
        if request.method=='GET':
            #for get request returning the details of the theatres already created by serializing them
            id = request.args.get('id') #getting the id of theatre whose details are needed
            theatre = Theatre.query.get(id)
            return jsonify({'theatre':theatre.serialize()})
        elif request.method=='DELETE':
            #if the request method is delete
            id = request.json.get('id') #getting id of theatre which has to be deleted
            #delete all bookings,show,theatre
            Theatre.query.filter_by(id = id).delete() #deleting that theatre details from theatre table
            Show.query.filter_by(theatre_id = id).delete() #deleting the shows running in that theatre from show table
            Booking.query.filter_by(theatre_id = id).delete() #deleting the bookings made in that theatre from booking table
            db.session.commit() #making the changes permanent by saving it
            return jsonify({'message': 'Theatre deleted successfully'})
        elif request.method =='PUT':
            #if the request method is of put/updation of theatre details
            id = request.json.get('id') #getting the id of theatre whose details needs to be updated
            theatre = Theatre.query.get(id)
            theatre.place = request.json.get('place')
            theatre.location = request.json.get('location')
            theatre.capacity = request.json.get('capacity')
            
            if theatre.capacity=='0' or theatre.place==' ' or theatre.location==' ':
                return jsonify({'error':'Empty Field'}),409

            db.session.commit()
            cache.delete_memoized(getalltheatre)
            return jsonify({'message':'theatre updated successfully'})

    else:
        return jsonify({'message':'Unauthorised access'}),505
    
@app.route("/getalltheatre", methods = ['GET']) #route to get the details of all the theatres created
@jwt_required()
@cache.cached(timeout=1)
def getalltheatre():
    theatre_list_ob = Theatre.query.all() #getting all the theatres created
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting the details of the current user
    theatre_list = []
    print(theatre_list_ob)
    for i in theatre_list_ob:
        theatre_list.append(i.serialize()) #serializing the details of the theatres 
    print(theatre_list)
    return jsonify({'theatre_list':theatre_list,'is_admin':current_user.is_admin, 'user_id':current_user.id})
    


@app.route('/createshow', methods=['GET','POST']) #route for creation of shows in theatres
@jwt_required()
def create_show():
    print('checkpoint')
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting the current user
    print(current_user)
    if(current_user.is_admin): #checking whether the user is admin or normal user
        show = Show()
        #getting the details of the show via form 
        show.showname = request.json.get('showname')
        show.ratings = request.json.get('ratings')
        show.tags = request.json.get('tags')
        show.price = request.json.get('price')
        show.theatre_id = request.json.get('theatre_id')
        show.time = request.json.get('time')
        show.counts = 0
        show.capacity = request.json.get('capacity')

        current_capacity = 0
        showlist = Show.query.filter_by(theatre_id = show.theatre_id).all()
        print(showlist)
        for s in showlist:
            x = s.serialize()
            current_capacity+=int(x['capacity'])
        
        #checking whether that show is already running in the current theatre
        if Show.query.filter(and_(Show.showname == show.showname, Show.theatre_id == show.theatre_id) ).count()>0:
            return jsonify({'error': 'Show already exist'}),409
        elif Theatre.query.filter_by(id=show.theatre_id).first().capacity - current_capacity < int(show.capacity):
            return jsonify({'error':'Show Capacity Exceeded'}),409
        else:
            print(show.showname)
            #storing the details of the show and saving it in the database
            db.session.add(show)
            db.session.commit()

            return jsonify({'message':'show created Successfully'})
    else:
        return jsonify({'message':'Unauthorized Access'}),505


@app.route('/editshow', methods=['GET','PUT','DELETE']) #route for updation/deletion of the shows
@jwt_required()
def edit_show():
    print('checkpoint')
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting the current user
    print(current_user)
    
    print('request method', request.method)
    if request.method=='GET':
        #if the request method is get, then all the details of the shows are being returned
        id = request.args.get('id')
        print('id', id)
        show = Show.query.get(id)
        print('edit show:',show.serialize())
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        return jsonify({'show':show.serialize(),'user_id':current_user.id})
    elif current_user.is_admin and request.method=='DELETE':
        #if the request method is delete then that show is being deleted
        id = request.json.get('id')
        Show.query.filter_by(id = id).delete()
        Booking.query.filter_by(show_id = id).delete()
        db.session.commit()
        return jsonify({'message': 'Show deleted successfully'})
    elif current_user.is_admin and request.method =='PUT':
        #if the request method is put, i.e making updates in the show details
        id = request.json.get('id')
        show = Show.query.get(id)
        show.ratings = request.json.get('rating')
        show.price = request.json.get('price')
        show.tags = request.json.get('tags')
        show.time = request.json.get('time')
        db.session.commit()
        cache.delete_memoized(get_shows)
        return jsonify({'message':'show updated successfully'})

    else:
        return jsonify({'message':'Unauthorised access'}),505


@app.route("/getshows", methods=["GET"]) #route for getting the details of all the shows
@jwt_required()
@cache.cached(timeout=1)
def get_shows():
    id = request.args.get('id') #getting the theatre id 
    time = datetime.datetime.now().time().strftime("%I%p") #checking the current time from the system
    print(time)
    all_shows = Show.query.filter_by(theatre_id = id).all()
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    print(current_user.is_admin)
    show_list = []
    for i in all_shows: #only those shows details will be sent which have not started yet on the current day
        x = i.serialize()
        print(x['time'])
        if x['time']>time:
            show_list.append(x)
        x['theatre']=Theatre.query.filter_by(id =id).first().place
        x['location']= Theatre.query.filter_by(id=id).first().location
    print(show_list)
    return jsonify({'show_list': show_list,'is_admin':current_user.is_admin, 'user_id':current_user.id})

@app.route("/myprofile", methods=["GET"]) #route to access the myprofile of the user 
@jwt_required()
def myprofile():
    id = request.args.get('id') #getting the id of the user whose details are needed
    all_bookings = Booking.query.filter_by(user_id = id).all() #getting the details of all booking made by that user
    show_list = []
    for i in all_bookings: #getting the details of the shows booked by the user
        showid = i.show_id
        ind_show = Show.query.filter_by(id = showid).all()
        show_list.append(ind_show[0].serialize())
    print(show_list)
    return jsonify({'show_list': show_list}) #returning the details of the shows booked by the user




@app.route('/bookshow', methods = ['POST']) #route for booking of the show
@jwt_required()
def bookshow():
    current_user = User.query.filter_by(username=get_jwt_identity()).first() # Getting the details of the user
    
    if current_user.is_admin == 0: # If the user is not admin then only booking of show is allowed
        book = Booking()
        
        # Getting the details of the show which has to be booked
        book.theatre_id = request.json.get('theatre_id')
        book.show_id = request.json.get('show_id')
        book.count = request.json.get('count')
        book.user_id = current_user.id  # Storing the userid who has made booking
        
        # Fetch the show's details from the database
        show_to_book = Show.query.filter_by(id=book.show_id).first()
        
        if show_to_book:
            if int(show_to_book.capacity) >= int(book.count):
                # Update the capacity of the show after booking
                show_to_book.capacity -= int(book.count)
                db.session.add(book)  # Commit the booking to the database
                db.session.commit()
                return jsonify({'message': 'Booking executed successfully'})
            else:
                return jsonify({'message': 'Not enough capacity for this booking'})
        else:
            return jsonify({'message': 'Show not found'})
    else:
        return jsonify({'message': 'Admin cannot book tickets'})


@app.route("/getbookings", methods = ['GET']) #route to get the details of the bookings
@jwt_required()
@cache.cached(timeout=300)
def getbookings():
    #getting all the bookings made by the specific user
    all_bookings = Booking.query.filter_by(user_id = User.query.filter_by(username = get_jwt_identity()).first().id)
    booking_list = []

    for item in all_bookings: #getting the details of shows , theatres from the booking
        ob = BookingList()
        ob.id = item.id 
        ob.show_id = item.show_id
        ob.theatre_id = item.theatre_id 
        ob.theatre_name = Theatre.query.filter_by(id = item.theatre_id).first().name
        ob.show_name = Show.query.filter_by(id = item.show_id).first().showname
        ob.timing = Show.query.filter_by(id = item.show_id).first().time

        booking_list.append(ob.serialize()) #appending the booking information after serializing it

    return jsonify({'booking_list':booking_list})


@app.route('/rateshow', methods = ['PUT']) #route for rating the show
@jwt_required()
def rateshow():
    current_user = User.query.filter_by(username=get_jwt_identity()).first() #getting the user identity
    if current_user.is_admin == 0: #checking if the user is normal user or not
        
        id= request.json.get('show_id') #getting the id of the show whose rating has to be submitted
        show = Show.query.get(id)
        total_count = float(show.counts) #getting the total ratings already submitted
        # print('************************',showid)
        total_rate = float(show.ratings)*total_count #storing the sum of ratings
        total_rate+=float(request.json.get('ratings')) #adding the current entered rating
        total_count+=1 #increasing the count of the rating
        show.counts = total_count
        show.ratings = total_rate/total_count #storing the new revised rating of the show
        
        db.session.commit()
        return jsonify({'message':'Rating submitted successfully'})
    else:
        return jsonify({'message':'Admin cannot Rate'})

@app.route('/search', methods=['GET']) #route for searching of the theatres
@jwt_required()
@cache.cached(timeout=1)
def search():
    cache.delete_memoized(getalltheatre)
    qry = request.args.get('Query') #getting what to search about theatre from the user via frontend
    print('QUERY:****',qry)
    #checking whether the search was related to theatre name/location/place
    theatre_nm=Theatre.query.filter(func.lower(Theatre.name).contains(qry)).all()
    theatre_lcn=Theatre.query.filter(func.lower(Theatre.location).contains(qry)).all()
    theatre_place=Theatre.query.filter(func.lower(Theatre.place).contains(qry)).all()
    #accordingly appending the information
    if len(theatre_lcn)>0:
        theatre_list = theatre_lcn 
    elif len(theatre_nm)>0:
        theatre_list = theatre_nm 
    elif len(theatre_place)>0:
        theatre_list = theatre_place 
    else:
        theatre_list = []
    print('THEATRE:*****',theatre_list)
    search_list_theatre = []
    for i in theatre_list:
        search_list_theatre.append(i.serialize()) #appending the information after serializing
    print(search_list_theatre)
    return jsonify({'theatre':search_list_theatre})

@app.route('/searchshows', methods=['GET']) #route for searching of the shows
@jwt_required()
@cache.cached(timeout=1)
def searchshows():
    cache.delete_memoized(get_shows)
    qry = request.args.get('Query') #getting the search query from the user 
    id = request.args.get('id') 
    print('QUERY:****',qry)
    show_nm=Show.query.filter(func.lower(Show.showname).contains(qry)).all()
    show_tgs=Show.query.filter(func.lower(Show.tags).contains(qry)).all()
    show_rtn=Show.query.filter(func.lower(Show.ratings).contains(qry)).all()
    show_prc=Show.query.filter(func.lower(Show.price).contains(qry)).all()
    show_time=Show.query.filter(func.lower(Show.time).contains(qry)).all()
    if len(show_nm)>0:
        show_list = show_nm 
    elif len(show_tgs)>0:
        show_list = show_tgs 
    elif len(show_rtn)>0:
        show_list = show_rtn
    elif len(show_prc)>0:
        show_list = show_prc 
    elif len(show_time)>0:
        show_list = show_time 
    else:
        show_list = []
    print('THEATRE:*****',show_list)
    print(id)
    time = datetime.datetime.now().time().strftime("%I%p") #checking the current time from the system
    search_list_shows = []
    for i in show_list:
        x = i.serialize()
        # print(x,x['theatre_id'],type(x['theatre_id']),type(id))
        # if x['theatre_id']==int(id):
        theatreid = x['theatre_id']
        x['theatre']=Theatre.query.filter_by(id=theatreid).first().place
        x['location'] = Theatre.query.filter_by(id=theatreid).first().location
        
        if x['time']>time:
            search_list_shows.append(x)
    print(search_list_shows)
    return jsonify({'shows':search_list_shows})

@app.route('/summary',methods = ['GET']) #route for generating the summary 
@jwt_required()
def summary():
    #getting all information of current theatres and shows
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if current_user.is_admin:
        theatres = Theatre.query.all() 
        shows = Show.query.all()
        theatre_name = []
        show_name = []
        theatre_book_count = []
        show_book_count = []
        for theatre in theatres:
            theatre_name.append(theatre.name)
            l = len(Booking.query.filter_by(theatre_id = theatre.id).all()) #getting the no. of bookings in current theatre
            theatre_book_count.append(l)
        for show in shows:
            show_name.append(show.showname)
            l = len(Booking.query.filter_by(show_id = show.id).all()) #getting the no.of bookings in current show
            show_book_count.append(l)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6)) #plotting two charts

        # First chart (bar chart)
        ax1.bar(theatre_name, theatre_book_count, align="center")
        ax1.set_xlabel("Theatres")
        ax1.set_ylabel("No. of Bookings")
        ax1.set_title("Summary of Theatres")
        
        # Second chart (bar chart)
        ax2.bar(show_name, show_book_count, align="center")
        ax2.set_xlabel("Shows")
        ax2.set_ylabel("No. of Bookings")
        ax2.set_title("Summary of Shows")
        plt.bar(show_name,show_book_count,align="center")
        
        plt.savefig(r"./static/summary.png") #saving the chart in static folder
        # plt.ion()
        # plt.show()
        plt.close()

        
    
    return jsonify({'Error':'Unauthorised Access'}),505

@app.route('/export',methods=['POST']) #route for generating the csv which contains info about theatres, bookings,shows
@jwt_required()
def export():
    current_user = User.query.filter_by(username = get_jwt_identity()).first()
    if current_user.is_admin:
        data = request.get_json()
        print(data['id'])
        theatre_id = data['id'] #getting the theatre id whose csv has to be generated
        print("theatreId",theatre_id)
        #getting the no.of shows running , bookings made in the current theatre
        shows_count = len(Show.query.filter_by(theatre_id=theatre_id).all())
        bookings_count = len(Booking.query.filter_by(theatre_id = theatre_id).all())
        theatre_name = Theatre.query.filter_by(id = theatre_id).first().name

        with open(f"./static/theatre_report.csv","w") as list_csv: #creation of csv file for the respective theatre
            list_csv.write("TheatreId, TheatreName, No.of Shows Running, No.of Booking Made\n")
            list_csv.write(f"{theatre_id},{theatre_name},{shows_count},{bookings_count}\n")

        return send_from_directory("./static",f'theatre_report.csv')
    
    return jsonify({'Error':'Unauthorized Access'}),505