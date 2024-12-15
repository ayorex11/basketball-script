import requests
import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = 'smtp.gmail.com'  
SMTP_PORT = 2525  
EMAIL_ADDRESS = 'your email address'
EMAIL_PASSWORD = 'your password'


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def check_basketball_matches():
    url = "https://sofascore.p.rapidapi.com/tournaments/get-live-events"


    querystring = {"sport":"basketball"}

    headers = {
        "x-rapidapi-key": "api key",
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    matches = response.json()
    print(matches["events"][0]["homeTeam"]["name"])
    

    for match in matches['events']:
        
        if 'lastPeriod' in match and match['lastPeriod'] == 'period2':  # Check if it's halftime (2nd quarter finished)
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            home_score = match['homeScore']['current']
            away_score = match['awayScore']['current']
            score_difference = abs(home_score - away_score)

            if score_difference <= 6:
                subject = f"Halftime Alert: {home_team} vs {away_team}"
                body = f"Halftime Score:\n{home_team}: {home_score}\n{away_team}: {away_score}\nScore Difference: {score_difference}"
                send_email(subject, body)
                print(body)
                print(f"Email sent for match: {home_team} vs {away_team}")

                

        


check_basketball_matches()
