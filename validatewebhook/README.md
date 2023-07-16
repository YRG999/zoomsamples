# ChatGPT readme
Notes from ChatGPT.

- [Deploy to Heroku](#deploy-to-heroku)
- [Store securely in database](#store-securely-in-database)
- [Store raw in database](#store-raw-in-database)

## Deploy to Heroku

To run this on Heroku, you need to do the following steps:

1. **Install the Heroku CLI**: You can download it from the [Heroku website](https://devcenter.heroku.com/articles/heroku-cli). After installation, you can use the `heroku` command from your command shell. You will need to log in using the email address and password you used when creating your Heroku account.

2. **Prepare your application for Heroku**: Here are the steps to prepare your Flask application to be deployed on Heroku:

    a. **Create a requirements.txt file**: This file tells Heroku which Python packages it needs to install for your application. In this case, it would look like:

    ```
    Flask
    gunicorn
    Jinja2
    ```

    b. **Create a Procfile**: This file tells Heroku how to run your application. It should contain the following line:

    ```
    web: gunicorn app:app
    ```

    Here, `app` refers to the Python file (`app.py`) and the Flask web application instance (`app = Flask(__name__)`). Make sure your python script is named as `app.py`.

    c. **Configure your Secret Token as an Environment Variable**: In your python script, replace `YOUR_WEBHOOK_SECRET` with `os.getenv("YOUR_WEBHOOK_SECRET")`. Then add the following import at the top:

    ```python
    import os
    ```

    This change makes the script get your secret from the environment variable `YOUR_WEBHOOK_SECRET`. You'll set this environment variable on Heroku in the next steps.

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

4. **Open your application**: You can open your application by running `heroku open`, or by visiting the application URL that Heroku returned when you created the new app.

You have now deployed your Zoom webhook validator to Heroku. It is listening for POST requests at the path `/zoom-webhook` on your application's domain.

## Store securely in database

If you want to use a database to store your webhook data securely on Heroku, I would recommend using a PostgreSQL database due to its integration and compatibility with Heroku. You can add a PostgreSQL database to your Heroku app using the Heroku Postgres add-on.

Here's a brief guide on how to get started:

1. Provision the Heroku Postgres add-on from your app's Resources tab in the Heroku dashboard, or from the command line with `heroku addons:create heroku-postgresql:hobby-dev`, which creates a free PostgreSQL database.

2. Heroku automatically sets a `DATABASE_URL` config var for your app, which contains the database URL that SQLAlchemy will use to connect to your database.

3. Update your Flask application to use this database URL, and make sure you're using the `psycopg2` library for PostgreSQL compatibility.

4. To secure the data, you can hash or encrypt sensitive data before storing it in the database.

Here's how your Flask application might look after these changes:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
import hmac
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

YOUR_WEBHOOK_SECRET = os.getenv("YOUR_WEBHOOK_SECRET")

class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)

@app.route('/zoom-webhook', methods=['POST'])
def validate_webhook():
    # Parse the incoming JSON request
    data = request.get_json()

    # Secure the incoming webhook data: for example, here we're hashing it
    secured_data = hashlib.sha256(str(data).encode()).hexdigest()

    # Store the secured webhook data to the database
    webhook_data = WebhookData(data=secured_data)
    db.session.add(webhook_data)
    db.session.commit()

    # Ensure the request is a CRC validation
    if data['event'] != 'endpoint.url_validation':
        return 'Unexpected event type', 400

    # Get the plain token from the request
    plain_token = data['payload']['plainToken']

    # Create the HMAC SHA-256 hash
    hash_obj = hmac.new(YOUR_WEBHOOK_SECRET.encode('utf-8'), 
                        plain_token.encode('utf-8'), 
                        hashlib.sha256)
    encrypted_token = hash_obj.hexdigest()

    # Create the response JSON object
    response = {
        'plainToken': plain_token,
        'encryptedToken': encrypted_token
    }

    # Respond within 3 seconds with a 200 or 204 HTTP response code.
    return jsonify(response), 200

if __name__ == '__main__':
    db.create_all()  # create the database table
    app.run(port=8000)
```

You need to include the following in your `requirements.txt` file:

```
Flask
gunicorn
psycopg2-binary
Flask-SQLAlchemy
```

Please replace the versions above with the versions you are using or intend to use. This is just an example.

Remember to commit these changes and push them to Heroku with `git push heroku master`. Your application will automatically connect to the PostgreSQL database and store the webhook data there.

Please note that you should not store sensitive data like personal identifiable information or sensitive business information without proper security measures. If you're not sure how to handle this data, you should consult with a security expert.

## Store raw in database

If you wish to store the data in its original form, you can simply remove the hashing step and store the `data` directly. Here is how the updated Flask application might look:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
import hmac
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

YOUR_WEBHOOK_SECRET = os.getenv("YOUR_WEBHOOK_SECRET")

class WebhookData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)

@app.route('/zoom-webhook', methods=['POST'])
def validate_webhook():
    # Parse the incoming JSON request
    data = request.get_json()

    # Store the incoming webhook data to the database
    webhook_data = WebhookData(data=str(data))
    db.session.add(webhook_data)
    db.session.commit()

    # Ensure the request is a CRC validation
    if data['event'] != 'endpoint.url_validation':
        return 'Unexpected event type', 400

    # Get the plain token from the request
    plain_token = data['payload']['plainToken']

    # Create the HMAC SHA-256 hash
    hash_obj = hmac.new(YOUR_WEBHOOK_SECRET.encode('utf-8'), 
                        plain_token.encode('utf-8'), 
                        hashlib.sha256)
    encrypted_token = hash_obj.hexdigest()

    # Create the response JSON object
    response = {
        'plainToken': plain_token,
        'encryptedToken': encrypted_token
    }

    # Respond within 3 seconds with a 200 or 204 HTTP response code.
    return jsonify(response), 200

@app.route('/data', methods=['GET'])
def get_data():
    # Fetch all records from the WebhookData table
    all_data = WebhookData.query.all()

    # Prepare the data for JSON serialization
    result = [{"id": item.id, "data": item.data} for item in all_data]

    return jsonify(result)

if __name__ == '__main__':
    db.create_all()  # create the database table
    app.run(port=8000)
```

In this script, we're storing the raw data as received from the request and directly saving it into the database. The `/data` endpoint will fetch all records from the `WebhookData` table in the database and return them as a JSON response.

Please keep in mind that storing raw data, especially sensitive data like personal identifiable information or sensitive business information, should be done with proper security measures. Always ensure that your application is secure and follows all necessary data privacy laws and regulations.
