import os
import threading
import time
import secrets
from PIL import Image
from flask_mail import Message
from app.extensions import mail,db
from app.models import Election
from itsdangerous import URLSafeTimedSerializer
import datetime
from app.decorators import async_call
from flask import current_app, url_for




@async_call
def start_end_election():
    elections = Election.query.all()
    for election in elections:
        if election.start_at < datetime.datetime.now() and election.status == "Building":
            election.status = "Ongoing"
            db.session.commit()
        elif election.end_at < datetime.datetime.now():
            election.status = "Ended"
            db.session.commit()
    

def save_picture(candidate_name,form_picture):
    random_hex = secrets.token_hex(3)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = candidate_name + random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/candidate_pictures', picture_fn)
    form_picture.save(picture_path)
    
    output_size = (500, 500) #minimizing the size of the image so it isn't saved so large in the database
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn


@async_call
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        

def send_mail(to, subject, template):
    app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=('Business House Junior Common Room', 'noreply@sender.com')
    )
    send_async_email(app, msg)
    
def mass_links(voter):
    unique_token = generate_confirmation_token(voter.email)
    voting_url = url_for('voters.voters_landing', token=unique_token, _external=True)
    html = "This is a notice for the Business House JCR Executives Election 21. Click on this link to vote: " + voting_url
    subject = "Vote for your BHJCR Executives"
    send_mail(voter.email, subject, html)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=864000):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email