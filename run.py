from app import create_app
from dotenv import load_dotenv
#from flask_mail import Mail
import os

load_dotenv()

app = create_app('config.py')
print(os.path.abspath("static/images/logo_png.png"))
if __name__ == "__main__":
    app.run(debug=True)