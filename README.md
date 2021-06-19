Fyyur
-----

### Introduction

Fyyur is a Coin Currency detector.


### Tech Stack

Our tech stack will include:

* **Python3** and **Flask** as our server language and server framework
* **OpenCv**  as image processing library
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
  ├── error.log
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── upload
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
  ```



### Development Setup


To start and run the local development server,


0. download weights and .cfg files from (https://drive.google.com/drive/folders/1qvLYoSDnyIeq-jR4JdLxz5j0Pw9FSl_y)

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv  env
  $ source env/bin/activate #Linux
  $ source env/Scripts/activate #Windows
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=app
  $ export FLASK_ENV=development # enables debug mode
  $ flask run
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
