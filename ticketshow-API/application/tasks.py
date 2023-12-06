from application.models import *
from application.workers import *
from datetime import datetime 
from application.mail import send_email
from celery.schedules import crontab
from jinja2 import Template


@celery_app.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs): #it schedules the tasks on a periodic interval
    sender.add_periodic_task(10,reminder.s(),name='dailyreminder') #reminder task is being scheduled
    sender.add_periodic_task(20,monthly_reminder.s(),name = 'monthly_entertainment') #monthly_reminder task is being scheduled


@celery_app.task
def reminder(): #reminder task for sending remider mails to the users every day
    allusers = User.query.filter_by(is_admin = 0).all() #getting all users except admin
    print(allusers)
    flag = False
    for user in allusers:
        #for every user using the daily reminder template and their information and sending them mail
        with open('./templates/daily_reminder.html','r') as file_:
            template = Template(file_.read())
        flag = send_email(user.email,'TicketShow Reminder', template.render(user = user.username),user = user.username ,content = "html")

    
    return flag

@celery_app.task
def monthly_reminder(): #monthly_reminder task for sending the users their entertainment report
    allusers = User.query.filter_by(is_admin = 0).all() #all users except the admin
    for user in allusers:
        id = user.id 
        # username = user.username
        #fetching the no.of bookings made, shows watched , theatres visited
        bookings = Booking.query.filter_by(user_id = id).all()
        total_booking = len(bookings)
        shows_watched = []
        theatre_visited = []
        for book in bookings:
            shows_watched.extend(Show.query.filter_by(id=book.show_id).all())
            theatre_visited.extend(Theatre.query.filter_by(id=book.theatre_id).all())
        print(shows_watched,theatre_visited)
        #with all the information, creating and html file and storing that information in it and sending the mail to user
        with open('./templates/monthly_entertainment.html','r') as file_:
            template = Template(file_.read())
        flag = send_email(user.email,'TicketShow Entertainment Report', template.render(username = user.username, booking_count = total_booking,
                                                                            theatres = theatre_visited, shows = shows_watched),user=user.username, content = "html")


    return flag



