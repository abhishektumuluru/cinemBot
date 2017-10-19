#Cinemabot
import praw
import requests
import json
from time import sleep
import sys
import re
import cinemabotCredentials

imdb_req_url = "http://theapache64.xyz:8080/movie_db/search?keyword="
_client_id = cinemabotCredentials.client_id
_client_secret = cinemabotCredentials.client_secret
_user_agent = "test"
_username = "AutoCinemaBot"
_password = "cinemabot"

pronouns = ['this', 'that', 'those', 'there']

def get_instance():
	try:
		reddit = praw.Reddit(username=_username,
						 password=_password,
						 client_id=_client_id,
	                     client_secret=_client_secret,
	                     user_agent=_user_agent)
	except Exception as e:
		print("Reddit Login failed" + repr(e))
		return None
	print("Reddit login success!")
	return reddit

def get_title_or_not(comment):
	if "cinemabot" in comment.body.lower():
		return True
	return False

def parse_comment(reddit_instance):
	if reddit_instance is None:
		pass
	subreddit = reddit_instance.subreddit('test')
	for comment in subreddit.comments(limit=20):
		if "cinemabot" in comment.body.lower():
			reply(reddit_instance, comment)

def reply(reddit_instance, comment):
	if reddit_instance.user.me() == comment.author:
		title = "shutter island"
		title = title.replace(" ", "+")
		botreply = get_movie_info(title)
		comment.reply(botreply)
		print("replied")

def delete_reply():
	pass

def get_movie_info(movie_title):
	botreply = ""
	try:
		request = requests.get(imdb_req_url + movie_title)
		if request.status_code == requests.codes.ok:
			response = request.json()
			if response['message'] != "Movie found":
				print("movie not found " + response['message'])
			else:
				data = response['data']
				heading = "##" + data['name'] + ", " + data['year'] + "##\n\n" 
				genre = "**Genre**: " + data['genre'] + "\n"
				rating = "**IMDB**: " + data['rating']
				spacing = "\n\n"
				plot = ">*" + data['plot'] + "*\n\n"
				stars = "**Starring**: " + data['stars']
				iamabot = "\n\n>*I am a bot, and this was done automatically. I will remove myself if my score is low!*"
				botreply = heading + genre + rating + spacing + plot + stars + iamabot
	except requests.exceptions.RequestException as error:
		print(repr(error))
		sys.exit(0)
	return botreply

reddit_instance = get_instance()
def main():
	while True:
		parse_comment(reddit_instance)
		sleep(10)
if __name__ == "__main__":
	main()