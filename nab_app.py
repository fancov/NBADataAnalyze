from datetime import datetime
import json
from flask import Flask, request, render_template
from forms import NBAStartForm, NBAqueryForm
from flask_bootstrap import Bootstrap
from db import db
from models import NBA

from crawl_data import get_best_data_player
from send_email import send_email, generate_email_file_and_data

app = Flask(__name__)

app.config.from_object('config')
bootstrap = Bootstrap(app)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def start():
    form = NBAStartForm()
    if form.validate_on_submit():
        team_name = form.team_name.data
        email = form.email.data

        all_data = get_best_data_player()
        if team_name:
            team_data = all_data.get(team_name)
            all_team = False
        else:
            team_data = all_data
            all_team = True
        team_info_json = json.dumps(team_data, ensure_ascii=False)
        now_time_str = datetime.now().strftime('%Y%m%d%H%M')
        nba = NBA(year_time='2018', store_time=now_time_str, team_info=team_info_json)
        db.session.add(nba)
        db.session.commit()

        team_data = generate_email_file_and_data(team_data, all_team=all_team, team_name=team_name)
        send_email([email])
        return render_template('start.html', form=form, team_data=team_data)

    return render_template('start.html', form=form)


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = NBAqueryForm()
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        data_list = NBA.query.filter(NBA.store_time >= start_time, NBA.store_time <= end_time).all()
        team_info_list = []
        for item in data_list:
            item_dict = {}
            item_dict['id'] = item.id
            item_dict['year_time'] = item.year_time
            item_dict['store_time'] = item.store_time
            item_dict['team_info'] = item.team_info
            team_info_list.append(item_dict)

        return render_template('query.html', form=form, team_info_list=team_info_list)
    return render_template('query.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
