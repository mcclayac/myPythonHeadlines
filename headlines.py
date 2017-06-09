__author__ = 'anthonymcclay'
__project__ = 'myPythonHeadlines'
__date__ = '6/8/17'
__revision__ = '$'
__revision_date__ = '$'

import feedparser
import json
import urllib
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

 # RSS Feed example


BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"



WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=718e411a82db8e1a08377ef9d76a4f44"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"



RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'aws': 'http://feeds.feedburner.com/AmazonWebServicesBlog'}


DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
                   }
    return weather

def get_rate(frm, to):
    all_currency = urllib.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']




@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customised weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customised currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html", articles=articles, weather=weather,
                           currency_from=currency_from, currency_to=currency_to, rate=rate,
                           currencies=sorted(currencies))


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

