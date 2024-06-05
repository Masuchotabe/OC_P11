# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.8+

    * [Flask](https://flask.palletsprojects.com/en/3.0.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - You should now be ready to test the application. In the directory, type <code>python run.py</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    We're using pytest framework for testing and [coverage](https://coverage.readthedocs.io/en/7.5.1/) to see 
6. how well we're testing.  
    A HTML report is included in hmtlcov directory. 
    If you want to execute again the tests and generate a report use this command in the source directory :  
`pytest --cov=. --cov-report html`
  
6. Performance  
   Locust is the package for testing the app performance. 
7. You can start it with this if you're in the root project repository :  
   `locust -f tests/performance_tests/locustfile.py`
or navigate to the directory where the locustfile.py is and start locust :
```
cd tests/performance_tests
locust
```
   

