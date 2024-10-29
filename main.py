from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
import random
from flask_wtf import CSRFProtect
from flask import jsonify
import logging



# Initialize Flask app
app = Flask(__name__)
csrf = CSRFProtect(app)

# Load environment variables from .env file
load_dotenv()




# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your-databasepass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Mail
# Looking to send emails in production? Check out our Email API/SMTP product!
app.config['MAIL_SERVER']='your-smtp-server'
app.config['MAIL_PORT'] = your-port
app.config['MAIL_USERNAME'] = '6f14520eb561ee'
app.config['MAIL_PASSWORD'] = 'ca36f8b302bd89'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Store OTP temporarily
otp_storage = {}

# Initialize SQLAlchemy
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()  # Avoid using 'session' to prevent Flask-Login confusion

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User and Blog Models
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(500), nullable=False)  # Make sure this length fits the hash
    is_admin = Column(Integer, default=0)  # 0 for normal user, 1 for admin

class BlogPost(Base):
    __tablename__ = 'blogposts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    image_path = Column(String(200))  # Added for image path
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')

Base.metadata.create_all(engine)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)  # Optional field
    message = Column(Text, nullable=False)

# Create all tables
Base.metadata.create_all(engine)


Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    comment = Column(Text, nullable=False)
    post = relationship("Post", back_populates="comments")




@app.route('/submit_message', methods=['POST'])
def submit_message():
    first_name = request.form['FirstName']
    last_name = request.form['Last Name']
    email = request.form['Email']
    phone_number = request.form['PhoneNumber']
    message = request.form['message']  # Updated to match the textarea name

    new_message = Message(first_name=first_name, last_name=last_name,
                          email=email, phone_number=phone_number,
                          message=message)

    db_session.add(new_message)
    db_session.commit()
    
    flash('Your message has been submitted successfully!', 'success')
    return redirect(url_for('about'))  # Adjust to your about page endpoint




# Check for admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access only!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))  # Use session.get() for SQLAlchemy 2.0


# bug here -------------------------1

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = db_session.query(BlogPost).all()
    return render_template('index.html', posts=posts)






@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        otp = request.form.get('otp')

        if otp:
            # Check if the OTP is valid
            if otp_storage.get(email) == otp:
                hashed_password = generate_password_hash(password)  # Hash the password

                try:
                    new_user = User(username=username, email=email, password=hashed_password)
                    db_session.add(new_user)
                    db_session.commit()
                    flash('Registration successful!', 'success')
                    otp_storage.pop(email, None)  # Remove OTP once registration is complete
                    return redirect(url_for('login'))
                except Exception as e:
                    db_session.rollback()
                    flash('Error: Username or email already exists.', 'danger')
                    print(f"Registration error: {e}")
                    return redirect(url_for('register'))
            else:
                flash('Invalid OTP!', 'danger')
                return redirect(url_for('register'))

        # If no OTP, generate and send it
        generated_otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
        otp_storage[email] = generated_otp  # Store the OTP for the email

        # Send the OTP via email
        msg = Message('Your OTP for registration', recipients=[email])
        msg.body = f'Your OTP is {generated_otp}. Please enter this OTP to complete your registration.'
        mail.send(msg)

        flash('OTP sent to your email. Please verify to complete registration.', 'info')
        return render_template('register.html', email=email)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()  # Ensure to remove whitespaces
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        
        # Try to find the user by username or email
        user = db_session.query(User).filter((User.username == username) | (User.email == email)).first()
        
        if user:
            # Check if the password matches
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!' , 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Login failed. User not found.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
@app.route('/profile')
@login_required  # Ensure only logged-in users can access
def profile():
    return render_template('profile.html')

@app.route('/destinations')
@login_required  # Ensure only logged-in users can access
def destinations():
    return render_template('destinations.html')



# CRUD routes for admin
@app.route('/admin/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    posts = db_session.query(BlogPost).all()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Handle the uploaded image
        img_file = request.files.get('img_file')
        image_path = None

        if img_file:
            # Create a secure filename and save the file
            filename = secure_filename(img_file.filename)
            image_path = 'static/uploads/' + filename
            img_file.save(image_path)

        # Save the post to the database
        post = BlogPost(title=title, content=content, image_path=image_path, author=current_user)
        db_session.add(post)
        db_session.commit()
        
        flash('New post created!', 'success')
        return redirect(url_for('index'))
    return render_template('new_post.html', posts=posts)

@app.route('/admin/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(post_id):
    post = db_session.query(BlogPost).get(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Handle the uploaded image
        img_file = request.files.get('img_file')
        image_path = None

        if img_file:
            # Create a secure filename and save the file
            filename = secure_filename(img_file.filename)
            image_path = 'uploads/' + filename
            img_file.save(image_path)

        # Save the post to the database
        post = BlogPost(title=title, content=content, image_path=image_path, author=current_user)
        db_session.add(post)
        db_session.commit()
        
        flash('New post created!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_post.html')


@app.route('/admin/delete_post/<int:post_id>')
@login_required
@admin_required
def delete_post(post_id):
    post = db_session.query(BlogPost).get(post_id)
    db_session.delete(post)
    db_session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('index'))







# for create new post - connect with post_blog.html

@app.route('/post_blog', methods=['GET', 'POST'])
@login_required
def post_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        img_file = request.files.get('img_file')  # Get the uploaded file

        # Define the upload directory
        upload_directory = 'uploads/'
        
        # Create the directory if it doesn't exist
        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        image_path = None  # Initialize image_path

        if img_file:
            # Create a secure filename and save the file
            filename = secure_filename(img_file.filename)
            image_path = os.path.join(upload_directory, filename)
            img_file.save(image_path)

        # Save the post to the database
        post = BlogPost(title=title, content=content, image_path=image_path, author=current_user)
        db_session.add(post)
        db_session.commit()
        # Debugging line

        flash('Post created successfully!', 'success')
        return redirect(url_for('new_post'))

    return render_template('post_blog.html')







# for read admins post and blog - connect with new_post.html user only

@app.route('/post/<int:post_id>')
@login_required
def view_post(post_id):
    post = db_session.query(BlogPost).get(post_id)
    comments = db_session.query(Comment).filter(Comment.post_id == post_id).all()
    if post:
        return render_template('new_blog.html', post=post, comments=comments)
    return "Post not found", 404



# otp
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return {'success': False, 'message': 'Email is required'}, 400

    # Generate OTP
    generated_otp = str(random.randint(100000, 999999))
    otp_storage[email] = generated_otp

    # Create message
    msg = Message('Your OTP for registration', recipients=[email])
    msg.body = f'Your OTP is {generated_otp}. Please enter this OTP to complete your registration.'

    try:
        mail.send(msg)
        return {'success': True, 'message': 'OTP sent successfully'}, 200
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return {'success': False, 'message': 'Failed to send OTP'}, 500




@app.route('/change_username', methods=['POST'])
@login_required
def change_username():
    new_username = request.form['new_username']

    # Check if the username is unique
    if db_session.query(User).filter_by(username=new_username).first():
        flash("Username already exists. Choose another one.", 'danger')
        return redirect(url_for('profile'))

    # Update username
    current_user.username = new_username
    db_session.commit()
    flash("Username updated successfully!", 'success')
    return redirect(url_for('profile'))



@app.route('/change_email', methods=['POST'])
@login_required
def change_email():
    new_email = request.form['new_email']

    # Check if the email is unique
    if db_session.query(User).filter_by(email=new_email).first():
        flash("Email already in use. Choose another one.", 'danger')
        return redirect(url_for('profile'))

    # Update email
    current_user.email = new_email
    db_session.commit()
    flash("Email updated successfully!", 'success')
    return redirect(url_for('profile'))


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_new_password = request.form['confirm_new_password']

    # Check if current password is correct
    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", 'danger')
        return redirect(url_for('profile'))

    # Check if new passwords match
    if new_password != confirm_new_password:
        flash("New passwords do not match.", 'danger')
        return redirect(url_for('profile'))

    # Update password
    current_user.password = generate_password_hash(new_password)
    db_session.commit()
    flash("Password updated successfully!", 'success')
    return redirect(url_for('profile'))




# Define the route for the About page
@app.route('/about')
def about():
    return render_template('about.html')


# like and cmt
logging.basicConfig(level=logging.DEBUG)

@app.route('/toggle_like', methods=['POST'])
def toggle_like():
    post_id = request.form.get('post_id')
    
    if post_id is None:
        app.logger.error("Post ID is required.")
        return jsonify({'success': False, 'message': 'Post ID is required.'}), 400

    post = db_session.query(Post).get(post_id)
    if post:
        post.likes += 1
        db_session.commit()
        return jsonify({'success': True, 'likes': post.likes})
    
    return jsonify({'success': False, 'message': 'Post not found.'}), 404



@app.route('/add_comment', methods=['POST'])
@login_required  # Ensure the user is logged in
def add_comment():
    data = request.get_json()
    post_id = data.get('post_id')
    comment_text = data.get('comment')

    if post_id and comment_text:
        new_comment = Comment(post_id=post_id, comment=comment_text)
        session.add(new_comment)
        session.commit()

        return jsonify({'success': True, 'comment': comment_text})
    
    return jsonify({'success': False, 'message': 'Invalid input'}), 400



if __name__ == '__main__':
    app.run(debug=True)
