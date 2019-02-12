from api import create_app
import logging
import requests
import json
from utils import Configuration
from flask import render_template, request, redirect, url_for
logger = Configuration.get_logger()
app = create_app()


@app.route('/search', methods=['GET', 'POST'])
def search():
    topic = request.form.get('topic')
    if request.method == 'POST':
        if topic:
            return redirect(url_for('search_topic', query=topic))
        else:
            return redirect(url_for('search'))
    return render_template('search.html')


@app.route('/search/topic/<query>', methods=['GET', 'POST'])
def search_topic(query):
    topic = request.form.get('topic')
    popular_songs = requests.get("http://localhost:5000/songs/popular").json()
    recent_songs = requests.get("http://localhost:5000/songs/recent").json()
    if request.method == 'POST':
        if topic:
            return redirect(url_for('search_topic', query=topic))
        else:
            return redirect(url_for('search'))
    songs = requests.get("http://localhost:5000/songs/" + query).json()
    return render_template('search_topic.html', songs=songs, number_of_results=len(songs), query=query, popular_songs=popular_songs, recent_songs=recent_songs)


@app.route('/search/topic/<query>/song/<song_id>/<mode>')
def song(query, song_id, mode):
    song = requests.get("http://localhost:5000/song/" + str(song_id)).json()
    return render_template('song.html', artist=song["artist"], title=song["name"], lyrics=song["lyrics"].split("\n"), query=query, mode=mode)


if __name__ == "__main__":
    logger.info("Application starting")
    app.run()
