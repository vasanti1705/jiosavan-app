from flask import Flask, request, redirect, jsonify, render_template_string
import time
import jiosaavn
import os
from traceback import print_exc
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET", 'thankyoutonystark#weloveyou3000')
CORS(app)

# HTML template for frontend
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JioSaavn Song Fetcher</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #444;
        }
        form {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        ul {
    list-style-type: none;
    padding: 0;
}

li {
    padding: 10px;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
}

li:hover {
    background-color: #f9f9f9;
}

strong {
    color: #007bff;
    font-weight: bold;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>JioSaavn Song Fetcher</h1>
        <form id="songForm">
            <input type="text" id="songQuery" placeholder="Enter JioSaavn Song URL or search query" required>
            <button type="submit">Fetch Song Info</button>
        </form>
        <div id="result"></div>
    </div>

    <script>
        document.getElementById("songForm").addEventListener("submit", function(event) {
            event.preventDefault();
            const query = document.getElementById("songQuery").value;
            const apiUrl = `/result/?query=${encodeURIComponent(query)}`;

            fetch(apiUrl)
                .then(response => response.json())
                .then(data => displayResult(data))
                .catch(error => {
                    document.getElementById("result").innerHTML = '<p>Something went wrong. Please try again.</p>';
                });
        });

function displayResult(data) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (!data || data.error) {
        resultDiv.innerHTML = `<p>${data.error || 'No data found!'}</p>`;
        return;
    }

    // Create a list to display matching songs
    const resultsList = document.createElement("ul");

    data.forEach(song => {
        const songName = song.song || song.name || 'Unknown Song';
        const albumName = song.album || 'Unknown Album';

        const songItem = document.createElement("li");
        songItem.innerHTML = `<strong>${songName}</strong> - ${albumName}`;

        // Add event listener to fetch detailed song info
        songItem.addEventListener("click", () => {
            displaySongDetails(song);
        });

        resultsList.appendChild(songItem);
    });

    resultDiv.appendChild(resultsList);
}


function displaySongDetails(song) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    // Song title
    const title = document.createElement("h3");
    title.textContent = `Title: ${song.song || 'Unknown'}`;
    resultDiv.appendChild(title);

    // Album
    if (song.album) {
        const album = document.createElement("p");
        album.textContent = `Album: ${song.album}`;
        resultDiv.appendChild(album);
    }

    // Singers
    if (song.singers) {
        const singers = document.createElement("p");
        singers.textContent = `Singers: ${song.singers}`;
        resultDiv.appendChild(singers);
    }

    // Music Director
    if (song.music) {
        const music = document.createElement("p");
        music.textContent = `Music Director: ${song.music}`;
        resultDiv.appendChild(music);
    }

    // Release Date
    if (song.release_date) {
        const releaseDate = document.createElement("p");
        releaseDate.textContent = `Release Date: ${song.release_date}`;
        resultDiv.appendChild(releaseDate);
    }

    // Starring
    if (song.starring) {
        const starring = document.createElement("p");
        starring.textContent = `Starring: ${song.starring}`;
        resultDiv.appendChild(starring);
    }

    // Lyrics Snippet
    if (song.lyrics_snippet) {
        const lyrics = document.createElement("p");
        lyrics.textContent = `Lyrics Snippet: ${song.lyrics_snippet}`;
        resultDiv.appendChild(lyrics);
    }

    // Cover Image
    if (song.image) {
        const image = document.createElement("img");
        image.src = song.image;
        image.alt = "Cover Image";
        image.style.maxWidth = "200px";
        resultDiv.appendChild(image);
    }

    // Media Preview
    if (song.media_preview_url) {
        const preview = document.createElement("audio");
        preview.controls = true;
        preview.src = song.media_preview_url;
        resultDiv.appendChild(preview);
    }

    // Permanent URL
    if (song.perma_url) {
        const link = document.createElement("a");
        link.href = song.perma_url;
        link.textContent = "Listen on JioSaavn";
        link.target = "_blank";
        resultDiv.appendChild(link);
    }
}



    </script>
</body>
</html>
'''

# Route to serve frontend
@app.route('/')
def home():
    return render_template_string(html_template)

# Song search and fetch routes remain unchanged
@app.route('/song/')
def search():
    lyrics = False
    songdata = True
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    songdata_ = request.args.get('songdata')
    if lyrics_ and lyrics_.lower() != 'false':
        lyrics = True
    if songdata_ and songdata_.lower() != 'true':
        songdata = False
    if query:
        return jsonify(jiosaavn.search_for_song(query, lyrics, songdata))
    else:
        error = {
            "status": False,
            "error": 'Query is required to search songs!'
        }
        return jsonify(error)

@app.route('/result/')
def result():
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower() != 'false':
        lyrics = True

    try:
        # Use search_for_song to get multiple matches based on the song name, include songdata
        search_results = jiosaavn.search_for_song(query, lyrics, songdata=True)

        if search_results:
            return jsonify(search_results)
        else:
            error = {"status": False, "error": "No matching songs found!"}
            return jsonify(error)

    except Exception as e:
        print_exc()
        error = {"status": False, "error": str(e)}
        return jsonify(error)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5100, use_reloader=True, threaded=True)
