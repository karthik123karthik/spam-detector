from flask import Flask, request;
from flask_wtf import FlaskForm;
from wtforms import StringField, SubmitField;
app = Flask(__name__);
import joblib;

app.config['SECRET_KEY'] = 'your_secret_key'

class MyForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    submit = SubmitField('Submit')

@app.route('/submit', methods=['POST'])
def submit_form():
    email = request.form.get('email')    
    if email:
        model = joblib.load("model");
        feature_extraction = joblib.load("feature_extraction");
        # modify the email you got
        transform_email = feature_extraction.transform([email]);
        prediction = model.predict(transform_email);
        if prediction:
            return f'''
            <div style="background-color: #f2f2f2; padding:10px; font-family: Arial, sans-serif; width:100%;">
            <h1 style="text-align:center;">Result</h1>
            <h1 style="text-align:center; font-family: Arial, sans-serif;">{email} </h1>
            <h1 style="background-color:red; text-align:center; font-family: Arial, sans-serif;"> it is the spam email </h1>
            </div>
            '''
        else:
            return  f'''
             <div style="background-color: #f2f2f2; padding:10px; font-family: Arial, sans-serif; width:100%;">
             <h1 style="text-align:center;">Result</h1>
            <h1 style="text-align:center; font-family: Arial, sans-serif;">{email} </h1>
            <h1 style="background-color:green; font-family: Arial, sans-serif; text-align:center;"> it is  not the spam email </h1>
             </div>
            '''
    else:
        return "Form data is missing."


@app.route('/', methods=['GET'])
def render_form():
    return '''
    <!DOCTYPE html>
<html>
<head>
    <title>Email form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }

        .container{
           width:60%;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .form-input {
            width: 90%;
            padding: 10px;
            border-radius: 3px;
            border: 1px solid #ccc;
        }

        .form-button {
            background-color: #4CAF50;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 3px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>EMail Spam detector</h1>
        <form action="/submit" method=POST>
            <div class="form-group">
                <label for="name" class="form-label">Email</label>
                <input type="text" id="name" name=email class="form-input" required autocomplete="off" placeholder="Enter the Email">
            </div>
            <button type="submit" class="form-button">Submit</button>
        </form>
    </div>
</body>
</html>
    '''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True);



