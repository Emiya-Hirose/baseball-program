from flask import Flask, render_template, request, flash
from wtforms import Form, FloatField, SubmitField, validators, ValidationError
import numpy as np
import joblib

def predict(parameters):
    # ニューラルネットワークのモデルを読み込み
    reg = joblib.load("./nn.pkl")
    params = parameters.reshape(1,-1)
    pred = reg.predict(params)
    return pred

def getScore(bat):
    print(bat)
    if bat >= 0.300:
        return "首位打者狙える", bat
    elif bat <= 0.300 and bat >= 0.250:
        return "チームの主軸", bat
    elif bat <= 0.250 and bat >= 0.200:
        return "守備や走塁で貢献しよう", bat
    elif bat <= 0.200:
        return "二軍で調整", bat
    else:
        return "error"

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'zJe09C5c3tMf5FnNL09C5d6SAzZoY'

class BaseballForm(Form):
    hit = FloatField("hit(安打数) ",
            [validators.InputRequired("この項目は入力必須です"),
            validators.NumberRange(min=0, max=250)])

    basehit = FloatField("basehit(塁打数)",
                [validators.InputRequired("この項目は入力必須です"),
                validators.NumberRange(min=0, max=350)])

    OnBasePercentage = FloatField("OnBasePercentage(出塁率)",
                [validators.InputRequired("この項目は入力必須です"),
                validators.NumberRange(min=0, max=0.500)])

    OPS = FloatField("OPS(OPS)",
                [validators.InputRequired("この項目は入力必須です"),
                validators.NumberRange(min=0, max=1.3)])

    ScoringPositionBattingAverage = FloatField("ScoringPositionBattingAverage(得点圏打率)",
                [validators.InputRequired("この項目は入力必須です"),
                validators.NumberRange(min=0, max=0.500)])

    submit = SubmitField("判定")

@app.route('/', methods = ['GET', 'POST'])
def predicts():
    form = BaseballForm(request.form)
    if request.method =='POST':
        if form.validate() == False:
            flash("すべて入力する必要があります。")
            return render_template('index.html', form=form)
        else:
            hit = float(request.form["hit"])
            basehit = float(request.form["basehit"])
            OnBasePercentage = float(request.form["OnBasePercentage"])
            OPS = float(request.form["OPS"])
            ScoringPositionBattingAverage = float(request.form["ScoringPositionBattingAverage"])

            x = np.array([hit, basehit, OnBasePercentage, OPS, ScoringPositionBattingAverage])
            pred = predict(x)
            BattingScore = getScore(pred)
            return render_template('result.html', BattingScore = BattingScore)
    elif request.method == "GET":
        return render_template('index.html', form=form)
    else:
        return "error"


if __name__ == "__main__":
        app.run()
