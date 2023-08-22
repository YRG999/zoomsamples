# README
Zoom webhook validation and event logging tool created with help from ChatGPT. See [moredetails.md](moredetails.md) for details.

## Deploy to Heroku

Follow these steps to deploy and run on Heroku.

1. **Install the Heroku CLI**: Download it from the [Heroku website](https://devcenter.heroku.com/articles/heroku-cli). After installation, use the `heroku` command from your command shell. Log in using the email address and password of your Heroku account.

2. **Prepare your application for Heroku**: Prepare your Flask application to be deployed on Heroku:

    a. **Create a [requirements.txt](requirements.txt) file**: This file tells Heroku which Python packages it needs to install for your application. In this case, it would look like:

    ```
    Flask
    gunicorn
    Jinja2
    ```

    b. **Create a [Procfile](Procfile)**: This file tells Heroku how to run your application. It should contain the following line:

    ```
    web: gunicorn app:app
    ```

    Here, `app` refers to the Python file (`app.py`) and the Flask web application instance (`app = Flask(__name__)`). Make sure your python script is named `app.py`.

    c. Add the [`app.py`](app.py) file to the directory with your `requirements.txt` and `Procfile`.

3. **Deploy your application on Heroku**: Once your application is prepared, use the following commands to deploy it:

    a. Navigate to your project directory using `cd`.

    b. Initialize a new git repository with the following commands:

    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```

    c. Create a new Heroku application:

    ```bash
    heroku create
    ```

    d. Set the `YOUR_WEBHOOK_SECRET` environment variable on Heroku:

    ```bash
    heroku config:set YOUR_WEBHOOK_SECRET=youractualwebhooksecret
    ```

    e. Push your code to Heroku:

    ```bash
    git push heroku main
    ```

4. **Open your application**: You can open your application by running `heroku open`, or by visiting the application URL that Heroku returned when you created the new app (see [notes](#notes-and-troubleshooting)).

You have now deployed your Zoom webhook validator to Heroku! It is listening for POST requests at the path `/zoom-webhook` on your application's domain.

## Notes and troubleshooting

1. When you open the application, it will display the following. The app will still work.

```
Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
```

2. When you go to `/zoom-webhook`, it will display the following. The app will still work.

```
Method Not Allowed
The method is not allowed for the requested URL.
```

3. If unable to validate, be sure you correctly entered your webhook secret. Note that uppercase `I`s can look like `l`s in the Zoom app page.
 
See [moredetails.md](moredetails.md) for code and more.

4. Webhook events are displayed in the console and log.