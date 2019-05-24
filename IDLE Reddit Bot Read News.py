import os
import re
import praw
import requests
from datetime import datetime
from newspaper import Article
from bs4 import BeautifulSoup
import nltk
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


subreddits = ['Bitcoin', 'CryptoCurrency']
banned_substances = ['i.redd.it', 'png', 'jpg', 'imgur', 'youtu', 'daily_discussion','reddit']

# Create the Reddit instance and log in
reddit = praw.Reddit(
    client_id='vhCE7aeRg4MAJg',
    client_secret='SAusJVyuClMrejHq_HrO3m1lovA',
        #password='',
        #username='',
    user_agent='L1pzBl4ckDr4g0n'
    )

mail=[]

#'Main' method. Gets hot subs, selects top 5, sends email
def get_hot(subreddit_name):

    # Get hot 15 submissions from reddit
    hot_submissions = reddit.subreddit(subreddit_name).hot(limit=20)

    #iterates hot_submissions in order to extract from server, sorts in list by descending order
    submissions_list = []
    for submission in hot_submissions:
        submissions_list.append(submission)    
    submissions_list.sort(key = lambda submission : submission.score, reverse=True )


    # Prints title of articles that don't contain banned words
    counter = 0
    for submission in submissions_list:
        score = score_submission(submission)
        if(score>0):
            counter +=1
        display_info(submission, score)
        if(counter==5):
            break
    print('\n NArcticles: ' + str(counter))


def display_info(submission, score):
    if score == 0:
        print('\nThis article has vanished for being useless')
    else:
        article = Article(submission.url)
        article.download()
        article.parse()
        article.nlp()
        text_to_print = '\n\n\n Art with score '+str(submission.score)+' : ' + article.title +'\n\n'+ article.summary + '\nlink:' + article.url
        print(text_to_print)
        mail.append(text_to_print)


def score_submission(submission):
    for substance in banned_substances:
        if(substance in submission.url):
            return 0
    return 1

def send_mail(mail):

    password_file = r'C:\Users\Augusto\Documents\projects\PetProjects\password.txt'
    file = open(password_file,'r')
    password = file.read()

    text = ''.join(mail)
    print(text)
    subject = 'Crypto daily digest'
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "augusto.m.galego@gmail.com"
    receiver_email = "augustomirandagalego@gmail.com"

    body = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
    body['From'] = sender_email
    body['To'] = receiver_email
    body['Subject'] = Header(subject, 'utf-8')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, body.as_string())
    


def main():
    
    
    for sr in subreddits:
        print('\n\nScraping /r/%s...' % sr)
        
        get_hot(sr)
    send_mail(mail)

main()
