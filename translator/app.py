from flask import Flask,render_template,redirect,url_for,request
import langcodes
import language_data
from googletrans import Translator
import pymongo
app=Flask(__name__)
app.config["SECRET_KEY"] = "SECRETKEY"
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["Project"]
# Get or create collections
translator_collection = db["translator_data"]
detector_collection = db["detector_data"]
# Temporary data storage
users = []
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You can perform validation checks here
        # For example, check if the username is already taken
        users.append({'username': username, 'password': password})
        return redirect('/login')
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username and password match a user in the database
        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect('/select')
        # If no match found, show an error message
        error = 'Invalid credentials. Please try again.'
        return render_template('login.html', error=error)
    return render_template('login.html')
@app.route('/select')
def select():
    return render_template('select.html')
@app.route('/about_detect')
def about_detect():
    return render_template('about_detect.html')
@app.route('/detect' ,methods=['post'])
def detector():
    translator=Translator()
    text=request.form['content']
    detected=translator.detect(text)
    lang_code=detected.lang
    lang_name=langcodes.LanguageData(language=lang_code).language_name()
    # Store detector data in MongoDB
    detector_data = {
        "content_entered": text,
        "lang_detected": lang_name
    }
    detector_collection.insert_one(detector_data)
    return render_template('detect.html',detected=lang_name)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/translate',methods=['POST'])
def translate():
    translator=Translator()
    text=request.form['content']
    source_lang=request.form['languages']
    target_lang=request.form['language']
     # Store translator data in MongoDB
    translator_data = {
        "content": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "translated_text": translated_text
    }
    translator_collection.insert_one(translator_data)
    translated_text=translator.translate(text,src=source_lang,dest=target_lang).text
    return render_template('res.html',text=text,translated_text=translated_text)
if __name__=='__main__':
    app.run(debug=True)