from flask import Flask
from flask import render_template, redirect
import json, sqlite3
import time, pytz
from datetime import datetime

def db_start():
    global connection, crsr
    connection = sqlite3.connect("queue.db")
    crsr = connection.cursor()

def db_close():
    global connection, crsr
    try:
        connection.commit()
    except:
        pass
    connection.close()

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/res_pack')
def res_pack():
    return render_template("res_pack.html")

@app.route('/discord_bot')
def discord_bot():
    return render_template("discord_bot.html")

@app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")

@app.route('/queue')
def queue():
    global connection, crsr

    db_start()
    sql_command = "SELECT * FROM que_history WHERE time > %s" %100#%int(time.time()-86400)
    crsr.execute(sql_command)

    queue_data = crsr.fetchall()
    db_close()

    labels = []
    data = []
    for i in queue_data:
        labels.append(str(datetime.fromtimestamp(float(i[3])).astimezone(pytz.utc)).split("+")[0])
        data.append(i[1])


    # id, que, online time  [(1, -2, 0, 1559413778), (2, 987, 1612, 1559414010)]
    chart_data = json.load(open("chart_config.json"))
    chart_data["data"] = data
    chart_data["labels"] = labels

    chart_data = json.dumps(chart_data)

    return render_template("queue.html", queue=chart_data)




if __name__ == '__main__':
    app.run()
