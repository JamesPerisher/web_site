

################################################################################
# PAULN07 WEBSITE                                                              #
#                                                                              #
#       my basic website routes importing                                      #
#       templeates from /templates, static images, js and css                  #
#       located in /static/images, /static/js and /static/css                  #
#                                                                              #
#      PAGES                                                                   #
#       Home "/", Discord Bot "/discord_bot", Queue "/queue", Resource Pack    #
#       "/res_pack", Shop "shop", Item Cart "/cart"                            #
#                                                                              #
#      API                                                                     #
#                                                                              #
#                                                          DESIGNED BY PAULN07 #
################################################################################



from flask import Flask
from flask import render_template, redirect, request, session, jsonify, g, url_for, make_response
from requests_oauthlib import OAuth2Session
from werkzeug.datastructures import ImmutableOrderedMultiDict
from collections import OrderedDict as OrderedDict_old
from decimal import *
import json, sqlite3
import time, pytz
import numpy as np
import os
import sys
import random
import requests

shopItems = OrderedDict_old()
print(getcontext())
class sale_item():
    def __init__(self, title="", description="", price=1000, coins=10, image="static/images/shop_images/error.png", iscoin=False):
        self.title = title
        self.description = description
        self.image = image
        self.price  = Decimal(price)
        self.coins = coins
        self.image = image
        self.id = -1

        if iscoin:
            self.title = "%s%s" %('{:,}'.format(self.coins), self.title)
            self.description = self.description.replace("{amt}", "$%s" %(self.price / self.coins))

    def add(self, ls):
        self.id = len(ls)+1
        ls[self.id] = self
        return self



sale_item(" Coins", "Coin purchase at about {amt} per coin", Decimal("2.50"),   20000, "static/images/shop_images/error.png", True).add(shopItems)
sale_item(" Coins", "Coin purchase at about {amt} per coin", Decimal("12.69"), 100000, "static/images/shop_images/error.png", True).add(shopItems)
sale_item(" Coins", "Coin purchase at about {amt} per coin", Decimal("20.00"), 200000, "static/images/shop_images/error.png", True).add(shopItems)


def db_start():
    global connection, crsr
    connection = sqlite3.connect("database.db")
    crsr = connection.cursor()

def db_close():
    global connection, crsr
    try:
        connection.commit()
    except:
        pass
    connection.close()

def ifRecord(user_id):
    global connection, crsr
    sql_command = "SELECT COUNT(1)\n    FROM balances\n    WHERE user_id = \"%s\";"%user_id
    crsr.execute(sql_command)
    if crsr.fetchall()[0][0] == 0:
        return False
    else:
        return True


def balance(user_id):
    if ifRecord(user_id):
        sql_command = "SELECT amount FROM balances WHERE user_id = %s" %user_id
        crsr.execute(sql_command)
        return crsr.fetchall()[0][0]
    else:
        sql_command = "INSERT INTO balances VALUES (NULL, %s, 0)" %user_id
        crsr.execute(sql_command)
        print("Added %s to coins db" %user_id)
        return 0

app = Flask(__name__, template_folder='templates')
app.debug = True

root_url = "124.179.220.50:5000"

OAUTH2_CLIENT_ID = sys.argv[1]
OAUTH2_CLIENT_SECRET = sys.argv[2]
OAUTH2_REDIRECT_URI = "https://%s/authenticate_user"%root_url
API_AUTH = sys.argv[5]

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

PAYPAL_ID = sys.argv[3]
PAYPAL_SECRET = sys.argv[4]

PORT = sys.argv[6]

app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


@app.context_processor
def utility_processor():
    def OrderedDict(*args, **kwords):
        return OrderedDict_old(*args, **kwords)
    return dict(OrderedDict=OrderedDict)



###API

def jsony(status, **kwords):
    return jsonify(data=kwords, status=status, access_ip=request.remote_addr, access_date=time.time())

@app.route("/api")
def api():
    if not request.args.get('auth') == API_AUTH:
        return jsony("Success", available_api=["/api/queue", "/api/balance", "/api/baltop"])
    return jsony("Success", available_api=["/api/queue", "/api/balance", "/api/baltop"], authorised_api=["api/send_coins", "api/create_coins"])


@app.route("/api/queue")
def api_queue():
    return jsony("ServerIssue", queue="N/A", fetch_time=time.time()-200)


@app.route("/api/balance")
def api_balance():
    user_id = request.args.get('user_id')
    if user_id == None:
        return jsony("UsageError", usage="/api/balance?user_id=<user_id>")

    return jsony("Success", user_id=user_id, user_name="name%s"%user_id, balance=0)


@app.route("/api/baltop")
def api_baltop():
    number = request.args.get('n')
    if number == None:
        return jsony("UsageError", usage="/api/baltop?n=<number_of_results>")
    try:
        number = int(number)
    except ValueError:
        return jsony("UsageError", usage="/api/baltop?n=<number_of_results>", error="'n' must be an integer")

    if not request.args.get('auth') == API_AUTH:
        max_res = 20
        if number > max_res:
            number = max_res
            return jsony("Success", baltop={x:{"user_id":x*10000, "username":"%s_name"%x, "balance":((number-x)*10000+37712)} for x in range(number)}, warn="Maximum number of results is %s"%max_res)

    return jsony("Success", baltop={x:{"user_id":x*10000, "username":"%s_name"%x, "balance":((number-x)*10000+37712)} for x in range(number)})

@app.route("/api/send_coins")
def api_send_coins():
    if not request.args.get('auth') == API_AUTH:
        return jsony("PermissionError", error="You are not authorised to do this.")

    from_user = request.args.get('from_user')
    to_user = request.args.get('to_user')
    amount = request.args.get('amount')

    if from_user == None or to_user == None or amount == None:
        return jsony("UsageError", usage="/api/send_coins?from_user=<user_id>&to_user=<user_id&amount=<integer>")

    try:
        amount = int(amount)
    except ValueError:
        return jsony("UsageError", usage="/api/send_coins?from_user=<user_id>&to_user=<user_id&amount=<integer>", error="'amount' must be an integer")

    return jsony("Success", from_user=from_user, to_user=to_user, amount=amount)



@app.route("/api/create_coins")
def api_create_coins():
    if not request.args.get('auth') == API_AUTH:
        return jsony("PermissionError", error="You are not authorised to do this.")

    user = request.args.get('user')
    amount = request.args.get('amount')

    if user == None or amount == None:
        return jsony("UsageError", usage="/api/create_coins?user=<user_id>&amount=<integer>")

    try:
        amount = int(amount)
    except ValueError:
        return jsony("UsageError", usage="/api/create_coins?user=<user_id>&amount=<integer>", error="'amount' must be an integer")

    return jsony("Success", user=user, amount=amount)



####User pages

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/help')
def helpme():
    return render_template("helpme.html")

@app.route('/home')
def home_redirect():
    return redirect("/", code=302)

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    try:
        local_cookie = list(request.cookies.get("cart").encode())
    except AttributeError:
        local_cookie = []

    resp = make_response(redirect(url_for('.shop')))
    try:
        id = int(request.form["id"])
        shopItems[id]

        data_out = "{'method':'APPEND','item_id':%s,'username':'%s','id':%s,'previous_cart':%s,'new_cart':%s}"%(id, g.username, g.id, local_cookie, "{{replace_point}}")

        local_cookie.append(id)

        data_out = data_out.replace("{{replace_point}}",str(local_cookie))
        print(data_out)

        resp.set_cookie("cart", bytes(local_cookie))
    except KeyError or ValueError as e:
        print(e)
    return resp

@app.route('/remove', methods=['POST'])
def remove_product_from_cart():
    try:
        local_cookie = list(request.cookies.get("cart").encode())
    except AttributeError:
        local_cookie = []

    resp = make_response(redirect(url_for('.cart')))
    try:
        id = int(request.form["id"])
        shopItems[id]

        data_out = "{'method':'REMOVE','item_id':%s,'username':'%s','id':%s,'previous_cart':%s,'new_cart':%s}"%(id, g.username, g.id, local_cookie, "{{replace_point}}")

        try:
            local_cookie.remove(id)
        except ValueError:
            print("{'method':'FORM_SPAM','item_id':%s,'username':'%s','id':%s,'previous_cart':%s}"%(id, g.username, g.id, local_cookie))
            return make_response(redirect(url_for('.cart')))

        data_out = data_out.replace("{{replace_point}}",str(local_cookie))
        print(data_out)

        resp.set_cookie("cart", bytes(local_cookie))
    except KeyError or ValueError as e:
        print(e)
    return resp


@app.route('/shop')
def shop():
    global connection, crsr

    try:
        db_start()
        bal = balance(int(g.id) if not g.id == None else None)
        db_close()
    except Exception as e:
        print("Unexpeced error for balance.")
        bal = 0

    return render_template("shop.html", shopItems = shopItems, bal= bal)

@app.route('/cart')
def cart():
    if g.username == None:
        return redirect("/login", code=302)

    try:
        db_start()
        bal = balance(int(g.id if not g.id == None else None))
        db_close()
    except Exception as e:
        print(e)
        bal = 0

    try:
        local_cookie = list(request.cookies.get("cart").encode())
    except AttributeError:
        local_cookie = []

    try:
        sp = []
        t = 0
        for i in local_cookie:
            x = shopItems[int(i)]
            t +=x.price
            sp.append(x)

        resp = make_response(render_template("cart.html", cartItems = sp, cartItemIds=[x.id for x in sp], bal=bal, totalPrice=t))
    except KeyError or ValueError as e:
        resp.set_cookie("cart", bytes([]))
        print("cart error")

    return resp





@app.route('/paypal/ipn',methods=['POST'])
def paypal_ipn():
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        print(values)
        for x, y in values.items():
            arg += "&{x}={y}".format(x=x,y=y)

        print(arg)

        validate_url = 'https://www.sandbox.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
                       .format(arg=arg)
        r = requests.get(validate_url)
        print(r)
        if r.text == 'VERIFIED':
            try:
                payer_email =  request.form.get('payer_email')
                unix = int(time.time())
                payment_date = request.form.get('payment_date')
                user_id_name = request.form.get('custom')
                item_name = request.form.get('item_name')
                last_name = request.form.get('last_name')
                payment_gross = request.form.get('payment_gross')
                payment_fee = request.form.get('payment_fee')
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = request.form.get('payment_status')
                txn_id = request.form.get('txn_id')
            except Exception as e:
                with open('ipnout.txt','a') as f:
                    data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
                    print(data)
                    f.write(data)


            totalcoins = 0
            for i in item_name.replace("[", "").replace("]", "").split(","):
                try:
                    current_item = shopItems[int(i.strip())]
                    totalcoins += current_item.coins
                except ValueError:
                    pass

            totalprice = 0
            for i in item_name.replace("[", "").replace("]", "").split(","):
                try:
                    totalprice += current_item.price
                except ValueError:
                    pass

            if totalprice > Decimal(payment_gross):
                raise ValueError("Spoofed payment", "Actual price: %s, Paid price was: %s."%(totalprice, payment_gross))

            with open('ipnout.txt','a') as f:
                data = 'SUCCESS\n'+str(values)+'\n'
                print(data)
                print("\n\nTODO: add %s from items with ids %s coin to %s's account"%(totalcoins, item_name, user_id_name))
                f.write(data)

            print("Update coins for:", unix, payment_date, user_id_name, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id)


        else:
            with open('/tmp/ipnout.txt','a') as f:
                data = 'FAILURE\n%s\n'%str(values)
                print(data)
                f.write(data)

        return r.text
    except Exception as e:
        raise e
        return str(e)





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
    reason = request.args.get('reason')
    h = "There seems to be an error with this page!"
    p = "Request argument was not provided contact @PaulN07#2596 via discord to report a bug."
    if reason == "donate":
        h = "Thank you for donating!"
        p = "Your donation is appreciated and will help support the future of this page and my projects."

    if reason == "purchase":
        h = "Thank you for purchasing items!"
        p = "Your transaction was successful."

        x = make_response(render_template("thank_you.html", h=h, p=p))
        x.delete_cookie("cart")

        return x
    return render_template("thank_you.html", h=h, p=p)


def que24(data):
    if len(data) == 0:
        return None
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
    sql_command = "SELECT * FROM que_history WHERE time > %s" %int(time.time()-86400)
    crsr.execute(sql_command)

    queue_data = crsr.fetchall() # id, que, online time  [(1, -2, 0, 1559413778), (2, 987, 1612, 1559414010)]
    db_close()

    data = que24(queue_data)
    chart_data = json.load(open("chart_config.json"))

    if data == None:
        data = {"time":None}

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


# ====login=====

@app.before_request
def before_request_func():
    try:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)


        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        try:
            user["code"]
        except KeyError:
            g.username = "%s#%s" %(user["username"], user["discriminator"])
            g.id = user["id"]
        else:
            g.username = None
            g.id = None
    except Exception as e:
        g.username = None
        g.id = None
        raise e

def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@app.route('/login')
def login():
    scope = request.args.get(
        'scope',
        'identify email')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@app.route('/authenticate_user')
def authenticate_user():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect("/shop")


@app.route('/me')
def me():
    global connection, crsr

    try:
        db_start()
        bal = balance(int(g.id if not g.id == None else None))
        db_close()
    except Exception as e:
        print(e)
        bal = 0

    try:
        db_start()
        sql_command = "SELECT therank FROM (SELECT balances.*, RANK() OVER (ORDER BY SCORE DESC) AS therank FROM TABLE balances) balances WHERE user_id = %s" %g.id
        crsr.execute(sql_command)
        print(crsr.fetchall())

        db_close()
    except Exception as e:
        print(e)
        bal = 0


    try:
        discord = make_session(token=session.get('oauth2_token'))
        user = discord.get(API_BASE_URL + '/users/@me').json()
        print(user)

        image = "https://cdn.discordapp.com/avatars/%s/%s.png?size=1024" %(user["id"], user["avatar"])
    except KeyError:
        return redirect("/login")
    else:
        return render_template("profile_page.html", img = image, bal=bal, user=user)



if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=PORT, ssl_context='adhoc')
