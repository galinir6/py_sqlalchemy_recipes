from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SQLAlchemy configuration
# for using SQLite database named 'database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# for using mysql database named 'recipes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Galisql23@localhost:3306/recipes' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# secret key
app.secret_key = 'my_secret_key'


# creating a table using new Class
class Recipes(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingridients = db.Column(db.String(100))
    prepTime = db.Column(db.String(100))


# creating table for users
class Users(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))




@app.route('/register', methods=['GET', 'POST'])
def register():
    # get data from form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        # new variable for user
        new_user = Users(username=username, password=hashed_password)
        
        # adding to db table
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Users.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/')
def home():
    # select from db to new variable
    my_recipes = Recipes.query.all() 
    print(my_recipes)
    return render_template('index.html', my_recipes=my_recipes)


# add data to table
@app.route('/add', methods=['GET', 'POST'])
def add():
    # get data from form
    if request.method == 'POST':
        name = request.form['name']
        ingridients = request.form['ingridients']
        prepTime = request.form['prepTime']
        # new variable for recipe
        new_recipe = Recipes(name=name, ingridients=ingridients, prepTime=prepTime)
        # adding to db table
        db.session.add(new_recipe)
        db.session.commit()
        
        flash('Recipe added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add.html')

# edit function
@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
    recipe_to_edit = Recipes.query.get_or_404(recipe_id)

    if request.method == 'POST':
        recipe_to_edit.name = request.form['name']
        recipe_to_edit.ingredients = request.form['ingredients']
        recipe_to_edit.prepTime = request.form['prepTime']

        db.session.commit()
        flash('Recipe updated successfully', 'success')
        return redirect(url_for('home'))

    return render_template('edit.html', recipe=recipe_to_edit)


# delete function
@app.route('/delete/<int:recipe_id>', methods=['POST'])
def delete(recipe_id):
    recipe_to_delete = Recipes.query.get_or_404(recipe_id)
    db.session.delete(recipe_to_delete)
    db.session.commit()
    flash('Recipe deleted successfully', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)