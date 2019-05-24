import os
import re
import praw
import requests
from datetime import datetime
from newspaper import Article
from bs4 import BeautifulSoup
import nltk
import smtplib, ssl

# Create the Reddit instance and log in
reddit = praw.Reddit(
    client_id='vhCE7aeRg4MAJg',
    client_secret='SAusJVyuClMrejHq_HrO3m1lovA',
    #password='guto0502',
    #username='Apprehensive_Design',
    user_agent='L1pzBl4ckDr4g0n'
)


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
    #send_mail(mail)


def display_info(submission, score):
    if score == 0:
        print('\nThis article has vanished for being useless')
    else:
        article = Article(submission.url)
        article.download()
        article.parse()
        print('\n\nARC: ')
        print(article.url)
        print('\n')
        print(article.title)
        article.nlp()
        print('\n')
        print(article.summary)


def score_submission(submission):
    for substance in banned_substances:
        if(substance in submission.url):
            return 0
    return 1

#def send_mail(mail):
    

subreddits = ['Bitcoin', 'CryptoCurrency']
banned_substances = ['i.redd.it', 'png', 'jpg', 'imgur', 'youtu', 'daily_discussion','reddit']
       
for sr in subreddits:
    print('\n\nScraping /r/%s...' % sr)
    get_hot(sr)

