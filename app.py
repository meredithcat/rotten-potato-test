from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from werkzeug.exceptions import NotFound


client = MongoClient()
db = client.rotten_potatoes
reviews = db.reviews

app = Flask(__name__)

#@app.route('/')
#def index():
#    """Return homepage."""
#    return render_template("home.html", msg="Jinja is Cool!")
#    # return "Hello, world!"

# OUR MOCK ARRAY OF PROJECTS
# reviews = [
#   { "title": "Great Review", "movieTitle": "Batman II" },
#   { "title": "Awesome Movie", "movieTitle": "Titanic" }
# ]

# INDEX
@app.route("/")
def reviews_index():
    """Show all reviews."""
    return render_template("reviews_index.html", reviews=reviews.find())

# NEW
@app.route('/reviews/new')
def reviews_new():
    """Create a new review."""
    return render_template('reviews_new.html', review={}, title='New Review')

# CREATE
@app.route("/reviews", methods=["POST"])
def reviews_submit():
    """Submit a new review."""
    review = request.form.to_dict()
    review_id = reviews.insert_one(review).inserted_id
    return redirect(url_for("reviews_show", review_id=review_id))

# SHOW
@app.route('/reviews/<review_id>')
def reviews_show(review_id):
    review = reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("reviews_show.html", review=review)

# EDIT
@app.route('/reviews/<review_id>/edit')
def reviews_edit(review_id):
    review = reviews.find_one({'_id': ObjectId(review_id)})
    return render_template('reviews_edit.html', review=review, title='Edit Review')

# UPDATE
@app.route('/reviews/<review_id>', methods=['POST'])
def reviews_update(review_id):
    if request.form.get('_method') == 'PUT':
        updated_review = {
            'title': request.form.get('title'),
            'movieTitle': request.form.get('movieTitle'),
            'description': request.form.get('description')
        }
        reviews.update_one(
            {'_id': ObjectId(review_id)},
            {'$set': updated_review})
        return redirect(url_for('reviews_show', review_id=review_id))
    else:
        raise NotFound()

@app.route('/reviews/<review_id>/delete', methods=["POST"])
def reviews_delete(review_id):
    reviews.delete_one({'_id': ObjectId(review_id)})
    return redirect(url_for('reviews_index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

