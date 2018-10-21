from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class NBAStartForm(FlaskForm):
    team_name = StringField('球队名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('查询并发送邮件')


class NBAqueryForm(FlaskForm):
    start_time = StringField('开始时间', validators=[DataRequired()])
    end_time = StringField('结束时间', validators=[DataRequired()])
    submit = SubmitField('开始查询')