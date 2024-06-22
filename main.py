from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

#
# with app.create_contect():
#     db.create_all()



@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

@app.route("/random")
def random_choice():
    with app.app_context():
        result = db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe = random.choice(result)
        # return jsonify(cafe={
        #     "id": random_cafe.id,
        #     "name": random_cafe.name,
        #     "map_url": random_cafe.map_url,
        #     "img_url": random_cafe.img_url,
        #     "location": random_cafe.location,
        #     "has_toilet": random_cafe.has_toilet,
        #     "has_wifi": random_cafe.has_wifi,
        #     "has_sockets": random_cafe.has_sockets,
        #     "can_take_calls": random_cafe.can_take_calls,
        #     "coffee_price": random_cafe.coffee_price,
        #     "seats": random_cafe.seats
        # })
        return jsonify(random_cafe.to_dict())


@app.route("/all")
def all_cafes():
    with app.app_context():
        result = db.session.execute(db.select(Cafe)).scalars().all()
        return jsonify([cafe.to_dict() for cafe in result])


@app.route("/search")
def search_cafes():
    location = request.args.get("loc")
    with app.app_context():
        result = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
        if len(result) == 0:
            return jsonify(error={
                "Not Found": "Sorry we do not have a cafe at the location."
            })
        else:
            return jsonify([cafe.to_dict() for cafe in result])


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price"),
        seats=request.form.get("seats")
    )
    db.session.add(cafe)
    db.session.commit()
    return jsonify(response={
        "success": "Successfully saved the cafe."
    })

## HTTP PUT/PATCH - Update Record
@app.route("/update/<int:cafe_id>", methods=["PATCH"])
def price_update(cafe_id):
    new_price = request.args.get("cafe_id")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(sucess = "Successfully updated price.")
    else:
        return jsonify(error={
            "Not Found": "Sorry cafe requested not found in the database."
        })


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def report_closed(cafe_id):
    key = request.args.get("key")
    if key == "TOP-SECRET":
        cafe = db.get_or_404(Cafe, cafe_id)
        print(1)
        print(cafe)
        if cafe:
            print(2)
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(messge="Successfully closed the cafe in record!")
        else:
            print(3)
            return jsonify(error={
                "Not Found": "Sorry we do not have a cafe at the location."
            })
    else:
        return jsonify(error={
            "Unauthorized": "You are not authorized to perform this action."
        })


if __name__ == '__main__':
    app.run(debug=True)
