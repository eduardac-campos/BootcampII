import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)


def get_beer_data(beer_name):
    url = f"https://api.openbrewerydb.org/v1/breweries?by_name={beer_name}&per_page=1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ""

    if request.method == 'POST':
        beer = request.form.get('beer')

        try:
            data = get_beer_data(beer)

            if data and len(data) > 0:
                brewery = data[0]

                website = brewery.get('website_url') or 'N/A'
                website_link = f'<a href="{website}" target="_blank">{website}</a>' if brewery.get('website_url') else 'N/A'

                result_html = f"""
                <div style="margin-top:20px; border:1px solid #ddd; padding:20px; border-radius:10px; text-align:left; max-width:500px; margin-left:auto; margin-right:auto;">
                    <h2>{brewery.get('name', 'N/A')}</h2>
                    <p><b>Tipo:</b> {brewery.get('brewery_type', 'N/A')}</p>
                    <p><b>Cidade:</b> {brewery.get('city', 'N/A')}, {brewery.get('state', 'N/A')}</p>
                    <p><b>País:</b> {brewery.get('country', 'N/A')}</p>
                    <p><b>Website:</b> {website_link}</p>
                    <p><b>Telefone:</b> {brewery.get('phone', 'N/A')}</p>
                </div>
                """
            else:
                result_html = "<p style='color:red;'>Cervejaria não encontrada.</p>"

        except Exception as e:
            result_html = f"<p style='color:red;'>Ocorreu um erro: {str(e)}</p>"

    return render_template_string("""
    <html>
    <head>
        <style>
            body {
                text-align: center;
                font-family: sans-serif;
                padding: 50px;
                background-color: #f5f5f5;
            }
            input {
                padding: 10px;
                width: 250px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #FFB81C;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #FFA500;
            }
        </style>
    </head>
    <body>
        <h1>Buscador de Cervejarias 🍺</h1>
        <p style="color:#666;">Powered by Open Brewery DB</p>
        <form method="post">
            <input type="text" name="beer" placeholder="Ex: BrewDog, Stone Brewing" required>
            <button type="submit">Buscar</button>
        </form>
        {{ result_html | safe }}
    </body>
    </html>
    """, result_html=result_html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
