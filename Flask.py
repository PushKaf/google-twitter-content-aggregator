from flask import Flask, request, render_template, redirect
import Search
import googleT as gt
import whitelistUtil as wu


app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/homepage/")

@app.route("/homepage/")
def form():

    google = wu.readGoogleWhitelist()
    twitter = wu.readTwitterWhitelist()

    jointWhitelistData = [google] + [twitter]
    # print(jointWhitelistData)

    return render_template("index.html", data=jointWhitelistData)

@app.route('/addGoogleWhitelistModal/', methods=['POST'])
def whitelistGoogleStuff():
    googleWhitelist = request.form["googleWhitelistAdd"]
    wu.writeGoogleWhitelist(googleWhitelist)
    
    return redirect("/homepage/")


@app.route('/addTwitterWhitelistModal/', methods=['POST'])
def whitelistTwitterStuff():
    twitterWhitelist = request.form["twitterWhitelistAdd"]
    wu.writeTwitterWhitelist(twitterWhitelist)
    
    return redirect("/")

@app.route('/deleteWhitelists', methods=['POST'])
def deleteWhitelists():
    information= request.data.decode('utf-8')
    wu.deleteGoogleWhitelist(information)
    wu.deleteTwitterWhitelist(information)

    return redirect("form")

    
@app.route("/homepage/", methods=["POST"])
def main():
    try:
        searchQuery = request.form["searchQuery"]
        whitelistChoice = request.form["whitelistQuery"]
        timeQuery = request.form["timeQuery"]
    except:
        return "Enter all input"
    
    twitterSearch = Search.twitter(whitelistChoice, searchQuery)
    googleSearch = gt.google(whitelistChoice, searchQuery, timeQuery)

    if twitterSearch == None or twitterSearch.isspace():
        if googleSearch == None or googleSearch.isspace():
            return f"No Data found :("
    if twitterSearch == "oof":
        finalData = f"<strong>GOOGLE:</strong> </br></br> {googleSearch} <strong> TWITTER: </strong> </br></br><h1><strong>ENTER TWITTER AUTH CODES TO GET TWITTER RESULTS!!! :D <3</strong></h1>"
    else:
        finalData = finalData = f"<strong>GOOGLE:</strong> </br></br> {googleSearch} <strong> TWITTER: </strong> </br></br> {twitterSearch}"

    return render_template('items.html', data=finalData)
        
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
