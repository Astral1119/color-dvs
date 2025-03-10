# Color DVs
This project uses Selenium to add hex codes as dropdown options.

This project has two scripts:
1. from_scratch.py
Generates colors from scratch. Can only generate a couple due to Google Sheets limitations (only 500 manual DV rules)
2. add_colors.py
If an option is a hex code, `add_colors.py` will change that option's color to its code.

## Usage
Start a venv with
```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

Then replace the URL in whichever script you use. Make sure the sheet is set to `Anyone can edit`.
When you run the script, it will pause and ask you to hit enter. First, navigate to the validation menu and select the rule you're working with. Then, hit enter.

## Color Pairs
If you want to color pairs you need to set up the Google Sheets API.
To do this, do the following:
1. Open the Google Cloud console and make a new project.
2. Enable the Google Sheets API.
3. Go to credentials and set up OAuth.
4. Make some OAuth credentials for a desktop application.
5. Download the file as 'credentials.json' in the working directory.
6. Add yourself as a test user.
You'll need to authorize the script when you run it. From there, you should be all set.