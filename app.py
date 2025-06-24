from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "YOUR_PAGESPEED_API_KEY"  # Replace with your actual API key

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            result = {
                'url': url,
                'performance': data['lighthouseResult']['categories']['performance']['score'] * 100,
                'first_contentful_paint': data['lighthouseResult']['audits']['first-contentful-paint']['displayValue'],
                'speed_index': data['lighthouseResult']['audits']['speed-index']['displayValue'],
                'interactive': data['lighthouseResult']['audits']['interactive']['displayValue']
            }
        else:
            result = {'error': 'Could not retrieve data. Please check the URL or try again later.'}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
  
