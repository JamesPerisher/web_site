from flask import Flask
from flask import render_template, redirect

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


if __name__ == '__main__':
    app.run()
