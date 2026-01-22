import json
from datetime import datetime
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    session,
    url_for
    )
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import JSON

# Import screen scripts
from scripts.view_profile import profile
from scripts.view_entry import view_entry
from scripts.edit_entry import edit_entry

# TODO: switch all redirects to use url_for()
# TODO: figure out something to do with the home page
# - BUG:
# - - sort buttons styles still not updating sometimes?

# - change category names and colours
# - add a collection description for a subtitle on the /collection page
# - pin entries to profile !
# - entry subtitles?
# - edit entry tags
# - figure out rich html for anchor tags and embeds in bios ?

# - ADDITIONAL WIDGETS
# - link to other entries
# - image + text together
# - location pin (map embed?)


# INFO
# ENTRIES:
# {
#     "id": int,
#     "name": str,
#     "widgets": List[Dict],
#     "icon_url": str,
#     "category": str,
#     "timeCreated": str (converted from datetime object)
# }

# WIDGETS
# {
#     "type": "text/image",
#     "content": "text content/image url",
    # "params": {
    #     "alt": "Alt Text",
    #     "align": "left/centre/right"
    # }   ^^ put these in css class names
# }


app = Flask(__name__)
app.secret_key = "MollyLouis"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookkeeper.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# pylint: disable=invalid-name

# USER STUFF
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    password_hash=db.Column(db.String(100), nullable=False)
    collection=db.Column(JSON)
    categories=db.Column(JSON)
    tags=db.Column(JSON)

    profile_info=db.Column(JSON)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# homepage
@app.route("/", methods=["POST", "GET"])
def index():
    """
    Homepage! When a user is not logged in.
    """

    if "username" in session:
        return redirect(url_for('dashboard'))

    return render_template("index.html")

@app.route("/about")
def about():
    """
    info page
    """
    user = User.query.get(session["id"])

    return render_template("about.html", user=user)

# login
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        updateSessionFromUser(user)
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")

# register
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()

    if user:
        return render_template("index.html", error="Username is already taken.")
    else:
        # create new user!
        initNewUser(username, password)

        updateUserFromSession(user)

        db.session.commit()
        return redirect(url_for('dashboard'))
    
@app.route("/dashboard")
def dashboard():
    """
    Homepage when user is logged in.
    """

    user = User.query.get(session["id"])
    if "username" in session:
        return render_template("dashboard.html", user=user)
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    updateSessionFromUser(None)
    return redirect(url_for("index"))

@app.route("/collection", methods=["POST", "GET"])
# POST and GET are both allowed
def collectionPage():
    """
    Displays the profile/collection page.
    """
    try:
        user = User.query.get(session["id"])
    except KeyError:
        print("ERROR: No active session!")
        return redirect("/")
    if 'collection' not in session:
        print("ERROR: No collection in current session.")
        return render_template("collection.html", collection=[], user=user)

    if request.method == "POST":
        if request.form["submitEntryTitle"]:
            # NEW ENTRY
            addNewEntry(request.form, user)
            updateUserFromSession(user)

            db.session.commit()
        return redirect("/collection")
    else:
        # GET
        # load default icons
        with open('static/resources/defaulticons.json', 'r') as f:
            defaultImages = json.load(f)
        # show current collection
        sorted_by="category"
        if "sorted_by" in user.profile_info:
            sorted_by = user.profile_info["sorted_by"]

        time_collection = getSortedCollection('time', user)
        alph_collection = getSortedCollection('alphabetical', user)
        category_collection = getSortedCollection('category', user)
        return render_template(
            "collection.html",
            user=user,
            defaultImages=defaultImages,
            sorted_by=sorted_by,
            sorted_collections={
                "time": time_collection,
                "alphabetical": alph_collection,
                "category": category_collection
                } 
            )

# delete an entry
@app.route("/delete/<string:username>-<int:id>")
def deleteEntry(username:str, id:int):
    """
    Deletes an entry from your collection.
    This is routed because it creates a temporary path to delete the entry,
    then returns to the collection page.
    I don't know why.... it's how the tutorial did it.
    """
    # these arguments (username + id) are just here bc of the url
    user = User.query.get(session["id"])

    entry_to_delete = None
    for entry in session['collection']:
        if entry['id'] == id:
            entry_to_delete = entry
            break
    if not entry_to_delete:
        return redirect("/collection")
    # try:
    temp = session['collection']
    temp.remove(entry_to_delete)
    session['collection'] = temp
    # user collection
    updateUserFromSession(user)
   
    db.session.commit()
    return redirect("/collection")
    # except Exception as e:
    #     return f"ERROR: {e}"

@app.route("/<string:username>", methods=["POST", "GET"])
def viewProfile(username:str):
    """ for editing your profle + categories + tags """

    user = User.query.get(session["id"])
    if not user:
        return redirect("/")
    
    if request.method == "POST":
        for form_submission in request.form:
            # Handle form submissions.
            profile.formPOST(user, request.form, form_submission)

        # Update user + session
        # this order is important! formPOST updates the user and not the session.
        updateSessionFromUser(user)
        updateUserFromSession(user)
        db.session.commit()

    # Render the page!
    profile_subtitle = profile.getProfileSubtitle(user)
    return render_template(
            "profile.html",
            user=user,
            profile_subtitle=profile_subtitle
            )
    
@app.route("/view/<string:username>-<int:id>", methods=["POST", "GET"])
def viewEntry(username:str, id:int):
    """
    the solo page for each entry
    """
    user = User.query.get(session["id"])

    current_entry = view_entry.getCurrentEntry(user, entry_id=id)
    if not current_entry:
        return redirect("/collection")

    collection = user.collection

    # INDEXES
    # for cycling through entries
    current_index = collection.index(current_entry)
    next_index = view_entry.nextIndex(current_index, collection)
    prev_index = view_entry.prevIndex(current_index, collection)

    # Render template
    try:
        time_object = datetime.strptime(current_entry['timeCreated'], '%Y-%m-%d %H:%M:%S.%f').date()

        return render_template(
            "viewentry.html",
            entry=current_entry,
            time_object=time_object,
            nextPageIndex=next_index,
            prevPageIndex=prev_index,
            user=user
            )
    except Exception as e:
        print(f"VIEWENTRY ERROR: {e}")
        return redirect("/collection")

@app.route("/edit/<string:username>-<int:id>", methods=["POST", "GET"])
def editEntry(username:str, id:int):
    """
    The edit page for individual entries
    """
    user = User.query.get(session["id"])
    current_entry = view_entry.getCurrentEntry(user, entry_id=id)
    
    if request.method == "POST":
        for form_submission in request.form:
            edit_entry.formPOST(form_submission, request.form, user, current_entry)

        updateSessionFromUser(user)
        updateUserFromSession(user)
        db.session.commit()

        return redirect(f"/edit/{user.username}-{str(id)}")

    else:
        with open('static/resources/defaulticons.json', 'r', encoding='utf-8') as f:
            defaultImages = json.load(f)
        return render_template(
            "editentry.html",
            entry=current_entry,
            user=user,
            defaultImages=defaultImages
            )

# HELPER FUNCTIONS
def addNewEntry(form, user):
    """
    Adds a new entry from the collection page
    """

    entry_name = form['submitEntryTitle']
    entry_desc = {
                "type": "text",
                "content": request.form['submitEntryDesc'],
                "params": {
                    "align": request.form['align']
                }
            }
    entry_category = form['submitEntryCategory']
    # entry_tags = form['submitEntryTags']
    entry_tags = []
    for item in form:
        if item in user.tags:
            entry_tags.append(item)

    if not entry_name:
        return


    default_icon = "https://dl.dropboxusercontent.com/scl/fi/mwutd0x3jq33ln69v6gpu/defaultIcon.png?rlkey=989wyny94j2zclzpaq2e8kvs5&st=tg9fswle&dl=0"
    # default image if there isnt one or if it fails

    entry_icon = form['submitEntryIcon']
    if entry_icon == "":
        entry_icon = default_icon
        for item in request.form.items():
            if item[0] == "defaultImage":
                entry_icon = item[1]
    
    # New entry!
    newEntry = {}

    # find unique id
    taken_ids = []
    for entry in user.collection:
        taken_ids.append(entry['id'])
    
    new_id = session['id'] + (len(session['collection']) + 1)
    while new_id in taken_ids:
        new_id += 1

    newEntry['id']=new_id
    newEntry['name'] = entry_name
    newEntry['widgets'] = [entry_desc]
    newEntry['icon_url'] = entry_icon
    newEntry['category'] = entry_category
    newEntry['tags'] = entry_tags

    currenttime = datetime.utcnow()
    newEntry['timeCreated'] = str(currenttime)

    user.collection.append(newEntry)

    updateSessionFromUser(user)

def initNewUser(username, password):
    """
    Initialises a new user upon registration
    """
    new_user=User(
        username=username
        )
    new_user.set_password(password)
    new_user.collection = []
    new_user.categories = {"Unsorted": "#000000"}
    new_user.tags = []
    new_user.profile_info = {}
    new_user.profile_info['bio'] = "This user doesn't have a bio yet. How mysterious!"
    db.session.add(new_user)
    db.session.flush()

    updateSessionFromUser(new_user)


def updateSessionFromUser(user=None):
    """
    Updates session information from User information.
    Mostly used when logging in/registering, as this creates a session.
    """
    if not user:
        for item in session.copy():
            session.pop(item)
        return

    session['id'] = user.id
    session['username'] = user.username
    session['collection'] = user.collection
    session['categories'] = user.categories
    session['tags'] = user.tags
    session['profile_info'] = user.profile_info

    # print("UPDATING SESSION INFO:", session)

    db.session.commit()

def updateUserFromSession(user=None):
    """
    updates user info, such as entry edits
    """
    if not user:
        return
    user.collection = session['collection']
    user.categories = session['categories']
    user.tags = session['tags']
    user.profile_info = session['profile_info']

    # print("UPDATING USER INFO:", user)

    db.session.commit()
    # does this do anythign here? idk

# SELECTION SORT BUTTONS
@app.route('/sortCollectionByCategory')
def sortCollectionByCategory():

    user = User.query.get(session["id"])
    user.profile_info["sorted_by"] = "category"

    updateSessionFromUser(user)

    return redirect("/collection")

@app.route('/sortCollectionByAlphabet')
def sortCollectionByAlphabet():

    user = User.query.get(session["id"])
    user.profile_info["sorted_by"] = "alphabetical"

    updateSessionFromUser(user)

    return redirect("/collection")

@app.route('/sortCollectionByTime')
def sortCollectionByTime():
    
    user = User.query.get(session["id"])
    user.profile_info["sorted_by"] = "time"

    updateSessionFromUser(user)

    return redirect("/collection")

@app.route("/listView")
def listView():
    user = User.query.get(session["id"])
    user.profile_info['collectionView'] = "list"
    updateSessionFromUser(user)
    updateUserFromSession(user)
    return redirect("/collection")

@app.route("/gridView")
def gridView():
    user = User.query.get(session["id"])
    user.profile_info['collectionView'] = "grid"
    updateSessionFromUser(user)
    updateUserFromSession(user)
    return redirect("/collection")

def getSortedCollection(sorted_by, user):
    collection = []
    if sorted_by == "alphabetical":
        entry_titles = [entry['name'] for entry in user.collection]
        entry_titles.sort()

        for name in entry_titles:
            for entry in user.collection:
                if entry['name'] == name:
                    collection.append(entry)
    elif sorted_by == "time":
        entry_titles = [entry['timeCreated'] for entry in user.collection]
        entry_titles.sort()
        for time in entry_titles:
            for entry in user.collection:
                if entry['timeCreated'] == time:
                    if entry not in collection:
                        collection.append(entry)
    elif sorted_by == "category":
        categories = [i for i in user.categories.keys()]
        category_index = 0
        while category_index <= len(categories) - 1:
            for entry in user.collection:
                if entry['category'] == categories[category_index]:
                    collection.append(entry)
            category_index += 1

    return collection

# keep all routes above here
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
