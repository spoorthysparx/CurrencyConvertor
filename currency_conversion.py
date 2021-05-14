import requests
from flask import Flask,render_template,request

app = Flask(__name__,
 template_folder="temp",
    static_folder="static")


def get_converted(inp,from_curr,to_curr):
    url="https://free.currconv.com/api/v7/convert?q="+from_curr+"_"+to_curr+"&compact=ultra&apiKey=1fe9341c819ea079e640"
    currency_value=requests.get(url).json()
    return currency_value[f"{from_curr}_{to_curr}"]*float(inp)

def get_currencies_list():
    url = "https://free.currconv.com/api/v7/currencies?apiKey=1fe9341c819ea079e640"
    currencies_list = requests.get(url).json()
    return currencies_list['results']

currencies = list(get_currencies_list().keys())

def getSymbols(id):
    symbols = get_currencies_list()[id]
    return symbols['currencySymbol']

@app.route('/',methods=['GET',"POST"])
@app.route('/home',methods=['GET',"POST"])
def homePage():
    if request.method == "POST":
        inp = request.form["from_currency"]
        from_curr=request.form["currency"]
        to_curr=request.form["currency_"]
        symbol = getSymbols(to_curr)
        converted = get_converted(inp,from_curr,to_curr)
        return render_template("index.html",converted = converted,currencies=currencies,symbol= symbol)
    else:
        return render_template("index.html",currencies=currencies)

get_currencies_list()

if __name__ == "__main__":
    app.run()