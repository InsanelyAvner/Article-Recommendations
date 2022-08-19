from flask import Flask, jsonify, request
import csv

import itertools
from demographic_filtering import output
from filtering_content import get_recommendations
from storage import all_articles, liked_articles, not_liked_articles

app = Flask(__name__)

with open("articles.csv", encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]



@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })


@app.route("/liked-articles", methods=["POST"])
def liked_articles():
    article = all_articles[0]
    all_articles = all_articles[1:]
    liked_articles.apppend(article)

    return jsonify({
        "status": "success"
    }), 201


@app.route("/not-liked-articles", methods=["POST"])
def not_liked_articles():
    article = all_articles[0]
    all_articles = all_articles[1:]
    not_liked_articles.apppend(article)
    
    return jsonify({
        "status": "success"
    }), 201


# Added in P142
@app.route("/popular-articles", methods=["GET"])
def popular_articles():
    return jsonify({
        "data": output,
        "status": "success"
    }), 201


@app.route("/get-recommendations", methods=["GET"])
def recommendations():
    movie = request.args.get("movie")

    return jsonify({
        "data": get_recommendations(movie),
        "status": "Success"
    }), 201

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
            all_recommended.sort()
            all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))

            article_data = []
            for recommended in all_recommended:
                article_data.append({
                    "url": recommended[0],
                    "title": recommended[1],
                    "text": recommended[2],
                    "lang": recommended[3],
                    "total_events": recommended[4]
                })
            
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200



if __name__ == "__main__":
    app.run(port = 5000)