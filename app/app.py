from api import create_app
import logging
import requests
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
    if request.method == 'POST':
        if topic:
            return redirect(url_for('search_topic', query=topic))
        else:
            return redirect(url_for('search'))
    songs = requests.get("http://localhost:5000/songs/" + query).json()
    return render_template('search_topic.html', songs=songs, number_of_results=len(songs), query=query)


@app.route('/search/topic/<query>/not-found', methods=['GET', 'POST'])
def search_not_found(query):
    topic = request.form.get('topic')
    if request.method == 'POST':
        if topic:
            return redirect(url_for('search_topic', query=topic))
        else:
            return redirect(url_for('search'))
    return render_template('search_not_found.html', query=query)


@app.route('/search/topic/<query>/song/<song_id>')
def song(query, song_id):
    song = requests.get("http://localhost:5000/song/" + str(song_id)).json()
    return render_template('song.html', artist=song["artist"], title=song["name"], lyrics=song["lyrics"].split("\n"), query=query)


if __name__ == "__main__":
    logger.info("Application starting")
    app.run()
