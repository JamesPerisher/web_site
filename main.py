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

@app.route('/queue')
def queue():
    global connection, crsr

    db_start()
    sql_command = "SELECT * FROM que_history WHERE time > %s" %100#%int(time.time()-86400)
    crsr.execute(sql_command)

    queue_data = crsr.fetchall() # id, que, online time  [(1, -2, 0, 1559413778), (2, 987, 1612, 1559414010)]
    db_close()

    labels = []
    data = []
    for i in queue_data:
        labels.append(str(datetime.fromtimestamp(float(i[3])).astimezone(pytz.utc)).split("+")[0])
        data.append(i[1])

    chart_data = json.load(open("chart_config.json"))
    chart_data["data"] = data
    chart_data["labels"] = labels

    chart_data = json.dumps(chart_data)

    return render_template("queue.html", queue=chart_data)




if __name__ == '__main__':
    app.run()
