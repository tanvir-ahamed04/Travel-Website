[![image.png](https://i.postimg.cc/mgR07Fsx/image.png)](https://postimg.cc/MvPPSHHt)

# Travel Guide Web Application

This project is a full-featured travel guide web application developed using Python Flask as the server-side framework and JavaScript for dynamic front-end design. The application helps users explore various destinations worldwide, manage travel information, and navigate a user-friendly interface that includes destination highlights, trip planning features, and more.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [License](#license)

---

## Features

- **Destination Guide**: Offers information on global destinations, highlighting key attractions.
- **User Profile Management**: Allows users to register, log in, and manage their profiles.
- **Post Management**: Users can view, create, and edit blog posts about destinations.
- **3D Earth Visualization**: An interactive Earth view using Three.js for an immersive experience.
- **Responsive Design**: Works smoothly on various devices with a focus on user experience.
- **Email Verification**: Includes OTP verification for secure registration.
- **Real-time Form Validation**: Interactive form validation using JavaScript.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **3D Graphics**: Three.js for the 3D Earth path visualization
- **Database**: MySQL for user data and post management
- **Styling**: CSS, with custom styles for responsive design
- **Mail Integration**: Mailtrap for handling email and OTP verification

## Installation

To set up and run the application on your local machine, follow these steps:

1. **Clone the Repository**:
   git clone [(https://github.com/tanvir-ahamed04/Travel-Website.git)]

2. **Navigate to the Project Directory**:
   cd Project-travel-guide

3. **Install Dependencies**:
   Make sure you have Python and pip installed, then run:

         pip install -r Requirements.txt

4. **Database Setup**:
   Import the `dump.sql` file into your MySQL database:
   ```
   mysql -u [username] -p < dump.sql
   ```

5. **Configure Environment Variables**:
   Create a `.env` file in the project directory and add the following:
   ```
   FLASK_APP=main.py
   FLASK_ENV=development
   MAIL_SERVER=sandbox.smtp.mailtrap.io
   MAIL_PORT=2525
   MAIL_USERNAME=your-mailtrap-username
   MAIL_PASSWORD=your-mailtrap-password
   MAIL_USE_TLS=True
   MAIL_USE_SSL=False
   ```

6. **Run the Application**:
                 python main.py
   The application should now be running on `http://localhost:5000`.

## Usage

- **Home Page**: Explore popular destinations and travel information.
- **User Profiles**: Register or log in to access personalized features.
- **Blog**: Read, create, and edit blog posts about various travel destinations.
- **3D Earth View**: Interact with the globe to explore different regions.
- **Contact Form**: Reach out for additional support or information.

## Folder Structure

```
Project-travel-guide/
│
├── main.py               # Main Flask application file
├── dump.sql              # SQL dump file for setting up the database
├── Requirements.txt      # Python dependencies
│
├── /templates            # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── destination.html
│   ├── new_blog.html
│   ├── post_blog.html
│   ├── edit_post.html
│   ├── readmore.html
│   ├── profile.html
│   ├── register.html
│   ├── login.html
│   └── reset_password.html
│
├── /static               # Static files
│   ├── /img              # Images
│   ├── /uploads          # Uploaded files
│   ├── style.css         # Main CSS file
│   └── Script.js         # JavaScript file for navigation, typing effect, etc.
│
└── .env                  # Environment variables (not included in repo for security)

## License

This project is licensed under the MIT License.

---

This README provides a comprehensive guide for anyone who wants to understand, install, and run the travel guide web application on their local machine.
