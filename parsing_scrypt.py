import requests

BASE = "http://127.0.0.1:5000/"

result = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')

for i in result.json()['items']:
	id = i['id']
	title = i['volumeInfo']['title']
	author = i['volumeInfo']['authors'][0]
	published_date = i['volumeInfo']['publishedDate']
	if len(published_date) > 4:
		published_date = published_date.split('-')
		published_date = published_date[0]

	response = requests.put(BASE  + "new_book/" + id, {"title": title, "authors":author, "published_date": int(published_date)})

result = requests.get('https://www.googleapis.com/books/v1/volumes?q=war')

for i in result.json()['items']:
	id = i['id']
	title = i['volumeInfo']['title']
	try:
		author = i['volumeInfo']['authors'][0]
	except KeyError:
		author = 'Unknown'
	published_date = i['volumeInfo']['publishedDate']

	if len(published_date) > 4:
		published_date = published_date.split('-')
		published_date = published_date[0]
	response = requests.put(BASE  + "new_book/" + id, {"title": title, "authors":author, "published_date": int(published_date)})
