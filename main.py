from flask import Flask
from flask import render_template, redirect
import json, sqlite3
import time, pytz
import numpy as np
import os

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

@app.route('/help')
def helpme():
    return render_template("helpme.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/hidden_page')
def hidden_page():
    return redirect("help", code=302)

@app.route('/res_pack')
def res_pack():
    download_name = "download.zip"
    dd = []
    for i in os.listdir("data/res_pack")[-6::]:
        with open("data/res_pack/%s/changelog"%i, "r") as f:
            dd.append([i, "data/res_pack/%s/%s"%(i, download_name), f.read().split("\n")])
            f.close()
    return render_template("res_pack.html", download_data=dd[::-1])

@app.route('/discord_bot')
def discord_bot():
    help_res = """```
    Information:
      help         Shows this message.
      ping         Get a test response
      info         Get info on user
      server       Minecrft Server Information
      player       Minecrft Player Information
      about        My creator

    Utilities:
      math         do math
      random       generate random numbers
      que          server queue
      queue        server queue graph
      admin-help   admin commands help

    Spam:
      genocide     Whatch the snappening
      Penis        Display Penis
      yodish       Yoda speak Yes, hmmm.

    Coins:
      bal          Your balance
      send         Send coins
      baltop       The richest peeps

    Fun:
      eight-ball   Ask the 8-ball
      fact         Weird facts!
      food         In case you get hungry
      knock        Knock knock

    Type ?help command for more info on a command.
    You can also type ?help category for more info on a category.
    ```""".replace("`", "")
    help_res = help_res.split("\n\n")
    for i in range(len(help_res)):
        help_res[i] = [[[e for e in v.strip().split("  ") if e != ""] for v in x.strip().split("\n")] for x in help_res[i].split(":")]
    help_res = help_res[0:-1]

    return render_template("discord_bot.html", table_data=help_res)

@app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")


def que24(data):
    x  = [] # time
    y0 = [] # queue
    y1 = [] # online
    y2 = [] # online - queue (difference)
    y3 = [] # queue/online percent
    y4 = [] # prio queue

    data_len = len(data)
    maxonline = max([x[2] for x in data if type(x[2])==type(1)])

    for i in range(data_len):
        x.append(data[i][3])
        try:
            y0.append(data[i][1]+0.1)
            if y0[-1] <= 0:
                y0[-1] = np.nan
        except:
            y0.append(np.nan)
        try:
            y1.append(data[i][2]+0.1)
            if y1[-1] <= 1:
                y1[-1] = np.nan
        except:
            y1.append(np.nan)
        try:
            y2.append((data[i][2]+0.1) - (data[i][1]+0.1))
            if y2[-1] <= 0:
                y2[-1] = np.nan
        except:
            y2.append(np.nan)

        try:
            y4.append((data[i][2]+0.1) - (data[i][1]+200+0.1))
            if y4[-1] <= 0:
                y4[-1] = np.nan
        except:
            y4.append(np.nan)

        try:
            relperc = ((data[i][1]+0.1) / (data[i][2]+0.1)) * maxonline
            relperc = np.nan if relperc > maxonline else relperc
            relperc = np.nan if relperc < 0 else relperc
            y3.append(relperc)
        except:
            y3.append(np.nan)
    return {"time":x,"queue":y0,"online":y1,"online queue difference":y2,"queue/online relative percent":y3,"priority queue":y4}

@app.route('/queue')
def queue():
    global connection, crsr

    db_start()
    sql_command = "SELECT * FROM que_history WHERE time > %s" %int(1563106276-(86400*20))# %int(time.time()-86400)
    crsr.execute(sql_command)

    queue_data = crsr.fetchall() # id, que, online time  [(1, -2, 0, 1559413778), (2, 987, 1612, 1559414010)]
    db_close()

    data = que24(queue_data)
    chart_data = json.load(open("chart_config.json"))

    chart_data["data"]["labels"] = data["time"]
    del data["time"]

    colours = ["#003f5c","#58508d","#bc5090","#ff6361","#ffa600"]
    count = 0

    for i in data:
        colour = colours[count]
        chart_data["data"]["datasets"].append({
            "fill": False,
            "label": i,
            "data": data[i],
            "borderColor": colour,
            "backgroundColor": colour,
            "lineTension": 0})
        count += 1

    chart_data = json.dumps(chart_data).replace("NaN", "\"NaN\"")
    return render_template("queue.html", queue=chart_data)




if __name__ == '__main__':
    app.run()
