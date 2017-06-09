__author__ = 'anthonymcclay'
__project__ = 'myPythonHeadlines'
__date__ = '6/8/17'
__revision__ = '$'
__revision_date__ = '$'

import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

 # RSS Feed example


BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"





RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'aws': 'http://feeds.feedburner.com/AmazonWebServicesBlog'}

@app.route("/", methods=['GET', 'POST'])
def get_news():
    # query = request.args.get("publication");
    query = request.form.get("publication");
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication]);
    return render_template("home.html",
                           articles=feed['entries']);


@app.route("/<publication>")
def get_publication(publication="bbc"):
    return get_news2(publication)

#
# @app.route("/bbc")
# def bbc():
#     return get_news2('bbc')
#
#
# @app.route("/cnn")
# def cnn():
#     return get_news2('cnn')
#
#
# @app.route("/fox")
# def fox():
#     return get_news2('fox')
#
# @app.route("/aws")
# def aws():
#     return get_news2('aws')
#

def get_news2(publication):
    feed=feedparser.parse(RSS_FEEDS[publication]);
    #first_article = feed['entries'][0]
    # return """<html>
    #        <body>
    #            <h1> RSS Headlines {3} </h1>
    #            <b>{0}</b> <br/>
    #            <i>{1}</i> <br/>
    #            <p>{2}</p> <br/>
    #        </body>
    #    </html>
    #    """.format(first_article.get("title"), first_article.get("published"),
    #               first_article.get("summary"), publication);
    return render_template("home.html",
                           articles=feed['entries']);



# def get_news():
#     feed = feedparser.parse(BBC_FEED)
#     first_article = feed['entries'][0]
#     return """<html>
#         <body>
#             <h1> BBC Headlines </h1>
#             <b>{0}</b> <br/>
#             <i>{1}</i> <br/>
#             <p>{2}</p> <br/>
#         </body>
#     </html>
#     """.format(first_article.get("title"), first_article.get("published"),first_article.get("summary"))


if __name__ == '__main__':
  app.run(port=5000, debug=True)

