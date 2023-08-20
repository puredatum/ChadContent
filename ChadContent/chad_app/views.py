from flask import Blueprint, render_template, request, jsonify
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


@views.route('/saved_responses', methods=['GET', 'POST'])
@login_required
def saved_responses():
    display_content = ChadResponse.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        if request.form["button"] == "edit_response":
            current_user.last_edit_response = request.form["edit_response_hist"]
            current_user.last_edit_prompt = request.form["edit_prompt_hist"]

            db.session.merge(current_user)
            db.session.commit()

        if request.form["button"] == "del_response":
            del_entry = ChadResponse.query.get(request.form["edit_id"])
            db.session.delete(del_entry)
            db.session.commit()


    return render_template("saved_responses.html", user=current_user, display_content=display_content)


@views.route('/edit_last', methods=['GET', 'POST'])
@login_required
def edit_last():
    if request.method == "POST":
        if request.form["button"] == "regen":
            api_list = APITokens.query.filter_by(user_id=current_user.id).first()
            api_details = [api_list.api_key, api_list.org_id]
            openai_app = make_user_api(api_details)

            last_response = request.form['response_new']
            keyword_list = request.form['new_keywords']
            new_length = request.form['new_length']
            additional_prompt = request.form['add_prompt']

            current_user.last_edit_response, current_user.last_edit_prompt = openai_app.reword_response(
                last_response, 
                keyword_list, 
                new_length, 
                additional_prompt)

            db.session.merge(current_user)
            db.session.commit()

        if request.form["button"] == "save_response":
            chad_response = request.form["edit_response"]
            chad_prompt = request.form["edit_prompt"]
            new_response = ChadResponse(chad_response=chad_response, chad_prompt=chad_prompt, user_id=current_user.id)
            db.session.add(new_response)
            db.session.commit()

    return render_template("edit_last.html", user=current_user)


@views.route('/chad_content', methods=['GET', 'POST'])
@login_required
def chad_content():
    if request.method == 'POST' and request.form["button"] != "edit_response":
        api_list = APITokens.query.filter_by(user_id=current_user.id).first()
        api_details = [api_list.api_key, api_list.org_id]
        openai_app = make_user_api(api_details)

        if request.form["button"] == "gen_para":
            topic = request.form['topic']
            keywords = request.form['keywords']

            if request.form['content_type'] == "intro":
                current_user.last_response, current_user.last_prompt = openai_app.post_functions(topic, keywords, current_user.brand_voice, "intro")
                db.session.merge(current_user)
                db.session.commit()

            elif request.form['content_type'] == "para":
                current_user.last_response, current_user.last_prompt = openai_app.post_functions(topic, keywords, current_user.brand_voice, "para")
                db.session.merge(current_user)
                db.session.commit()

            elif request.form['content_type'] == "headings":
                current_user.last_response, current_user.last_prompt = openai_app.generate_headings(topic, keywords)
                db.session.merge(current_user)
                db.session.commit()

            elif request.form['content_type'] == "tweet":
                current_user.last_response, current_user.last_prompt = openai_app.post_functions(topic, keywords, current_user.brand_voice, "tweet")
                db.session.merge(current_user)
                db.session.commit()

        if request.form["button"] == "save_response":
            chad_response = current_user.last_response
            chad_prompt = current_user.last_prompt
            new_response = ChadResponse(chad_response=chad_response, chad_prompt=chad_prompt, user_id=current_user.id)
            db.session.add(new_response)
            db.session.commit()

        if request.form["button"] == "regen":
            current_user.last_response, current_user.last_prompt = openai_app.regen(current_user.last_response)

        if request.form["button"] == "gen_question":
            if request.form['question_size'] == "long":
                length_response = "long form"
            elif request.form['question_size'] == "1":
                length_response = "1 sentence"
            elif request.form['question_size'] == "3":
                length_response = "3 sentences"
            elif request.form['question_size'] == "6":
                length_response = "6 sentence"

            question = request.form["question"]
            keywords = request.form['q_keywords']

            current_user.last_response, current_user.last_prompt = openai_app.answer_question(question, keywords, current_user.brand_voice, length_response)
            db.session.merge(current_user)
            db.session.commit()

    if request.method == 'POST' and request.form["button"] == "edit_response":
        current_user.last_edit_response, current_user.last_edit_prompt = current_user.last_response, current_user.last_prompt
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
