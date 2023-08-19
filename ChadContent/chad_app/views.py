from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from .models import APITokens, User, ChadResponse, KeywordList
from . import db
import csv
from chad_app.functions.function_file import make_user_api

views = Blueprint("views", __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	return render_template("home.html", user=current_user)

@views.route('/chad_content', methods=['GET', 'POST'])
@login_required
def chad_content():
    api_list = APITokens.query.filter_by(user_id=current_user.id).first()
    api_details = [api_list.api_key, api_list.org_id]
    openai_app = make_user_api(api_details)

    if request.method == 'POST':
        if request.form["button"] == "gen_para":
            topic = request.form['topic']
            keywords = request.form['keywords']
            if request.form['content_type'] == "intro":
                current_user.last_response, current_user.last_prompt = openai_app.make_paragraph(topic, keywords, current_user.brand_voice, "intro")
                db.session.merge(current_user)
                db.session.commit()
            elif request.form['content_type'] == "para":
                response = openai_app.make_paragraph(topic, keywords, current_user.brand_voice, "para")
                current_user.last_prompt = topic
                current_user.last_response = response
                db.session.merge(current_user)
                db.session.commit()

            elif request.form['content_type'] == "headings":
                current_user.last_response, current_user.last_prompt = openai_app.generate_headings(topic, keywords)
                db.session.merge(current_user)
                db.session.commit()

            elif request.form['content_type'] == "tweet":
                current_user.last_response, current_user.last_prompt = openai_app.make_paragraph(topic, keywords, current_user.brand_voice, "tweet")
                db.session.merge(current_user)
                db.session.commit()

        if request.form["button"] == "save_response":
            chad_response = request.form["tweet_details"]
            new_response = ChadResponse(chad_response=chad_response, user_id=current_user.id)
            db.session.add(new_response)
            db.session.commit()

        if request.form["button"] == "del_prompt":
            del_prompt = ChadResponse.query.get(request.form["prompt_id"])
            db.session.delete(del_prompt)
            db.session.commit()

        if request.form["button"] == "regen":
            current_user.last_response, current_user.last_prompt = openai_app.regen(current_user.last_response)

        if request.form["button"] == "gen_question":
            current_user.last_response, current_user.last_prompt = openai_app.answer_question(question, keywords, current_user.brand_voice)
            db.session.merge(current_user)
            db.session.commit()

    return render_template("chad_content.html", user=current_user, response=current_user.last_response, prompt=current_user.last_prompt)


@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        if request.form["button"] == "add_api":
            api_key = request.form['api_key']
            org_id = request.form['org_id']

            new_api = APITokens(api_key=api_key, 
                org_id=org_id, user_id=current_user.id)

            db.session.add(new_api)
            db.session.commit()

        if request.form["button"] == "add_voice":
            user_account = User.query.get(current_user.id)
            user_account.brand_voice = request.form['brand_voice']

            db.session.merge(user_account)
            db.session.commit()

        if request.form["button"] == "add_keyword":
            new_keyword = KeywordList(keywords=request.form['keywords'], user_id=current_user.id)
            db.session.add(new_keyword)
            db.session.commit()

        if request.form["button"] == "del_keyword":
            del_keyword = KeywordList.query.get(request.form["selected_keywords"])
            db.session.delete(del_keyword)
            db.session.commit()

    return render_template("account.html", user=current_user)

@views.route('/scheduled_tweets', methods=['GET', 'POST'])
@login_required
def scheduled_tweets():
    if request.method == "POST":
        api_list = APITokens.query.filter_by(twitter_name=current_user.current_api).first()
        api_details = [api_list.consumer_key, 
                        api_list.consumer_secret, 
                        api_list.access_token, 
                        api_list.access_token_secret, 
                        api_list.api_key,
                        api_list.org_id]

        if request.form["button"] == "delete":
            del_tweet = Tweets.query.get(request.form["tweet_id"])
            db.session.delete(del_tweet)
            db.session.commit()

        if request.form["button"] == "update":
            edit_tweet = Tweets.query.get(request.form["tweet_id"])
            edit_tweet.tweet_content = request.form["tweet_main"]
            edit_tweet.reply_content = request.form["tweet_reply"]
            edit_tweet.post_time = request.form["datetime"]
            db.session.merge(edit_tweet)
            db.session.commit()

        if request.form["button"] == "gen":
            twitter_app, openai_app = make_user_api(api_details)
            tweet_quote = Tweets.query.get(request.form["tweet_id"])
            new_insight = openai_app.generate_insight(tweet_quote.tweet_content)

            tweet_quote.reply_content = new_insight
            db.session.merge(tweet_quote)
            db.session.commit()

        if request.form["button"] == "publish":
            # Update entries if there where edits
            pub_tweet = Tweets.query.get(request.form["tweet_id"])
            pub_tweet.tweet_content = request.form["tweet_main"]
            pub_tweet.reply_content = request.form["tweet_reply"]

            if pub_tweet.tweet_type == "Normal":
                # Publish normal tweet
                tweet_id, tweet_link = publish_tweet(pub_tweet.tweet_content, api_details, pub_tweet.reply_content)

            else:
                tweet_id, tweet_link = publish_point_tweet(pub_tweet.tweet_content, api_details)

            # Update the database
            pub_tweet.tweet_id = tweet_id
            pub_tweet.tweet_link = tweet_link
            pub_tweet.published_time = datetime.now()
            db.session.merge(pub_tweet)
            db.session.commit()

    return render_template("scheduled_tweets.html", user=current_user)


@views.route('/posted_tweets', methods=['GET', 'POST'])
@login_required
def posted_tweets():
    return render_template("posted_tweets.html", user=current_user)
