import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Base de dados local com cervejarias brasileiras
CERVEJARIAS_BRASILEIRAS = [
    {
        "name": "Ambev",
        "brewery_type": "large",
        "city": "São Paulo",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.ambev.com.br",
        "phone": "(11) 2122-1200",
        "description": "Maior cervejaria do Brasil e uma das maiores do mundo. Produz marcas como Brahma, Skol, Antarctica e Bohemia."
    },
    {
        "name": "Brahma",
        "brewery_type": "large",
        "city": "São Paulo",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.brahma.com.br",
        "phone": "(11) 2122-1200",
        "description": "Uma das cervejas mais tradicionais do Brasil, fundada em 1888. Pertence ao grupo Ambev."
    },
    {
        "name": "Skol",
        "brewery_type": "large",
        "city": "São Paulo",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.skol.com.br",
        "phone": "(11) 2122-1200",
        "description": "Cerveja lager brasileira, uma das mais vendidas do país. Pertence ao grupo Ambev."
    },
    {
        "name": "Antarctica",
        "brewery_type": "large",
        "city": "São Paulo",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.antarctica.com.br",
        "phone": "(11) 2122-1200",
        "description": "Cerveja tradicional brasileira fundada em 1885 em São Paulo. Pertence ao grupo Ambev."
    },
    {
        "name": "Colorado",
        "brewery_type": "regional",
        "city": "Ribeirão Preto",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.cervejariacolorado.com.br",
        "phone": "(16) 3512-6900",
        "description": "Cervejaria artesanal fundada em 1995, conhecida por usar ingredientes brasileiros como rapadura, mel e mandioca nas suas receitas."
    },
    {
        "name": "Eisenbahn",
        "brewery_type": "regional",
        "city": "Blumenau",
        "state": "Santa Catarina",
        "country": "Brasil",
        "website_url": "https://www.eisenbahn.com.br",
        "phone": "(47) 3326-5600",
        "description": "Cervejaria artesanal fundada em 2002 em Blumenau, SC. Conhecida por cervejas de estilo alemão de alta qualidade."
    },
    {
        "name": "Wäls",
        "brewery_type": "micro",
        "city": "Belo Horizonte",
        "state": "Minas Gerais",
        "country": "Brasil",
        "website_url": "https://www.wals.com.br",
        "phone": "(31) 3337-7900",
        "description": "Cervejaria artesanal mineira fundada em 1999, premiada internacionalmente. Conhecida pela Wäls Petroleum e Wäls Quadruppel."
    },
    {
        "name": "Bodebrown",
        "brewery_type": "micro",
        "city": "Curitiba",
        "state": "Paraná",
        "country": "Brasil",
        "website_url": "https://www.bodebrown.com.br",
        "phone": "(41) 3362-4900",
        "description": "Cervejaria artesanal paranaense fundada em 2007, reconhecida por cervejas experimentais e de alta fermentação."
    },
    {
        "name": "Backer",
        "brewery_type": "micro",
        "city": "Belo Horizonte",
        "state": "Minas Gerais",
        "country": "Brasil",
        "website_url": "https://www.backer.com.br",
        "phone": "(31) 3337-7800",
        "description": "Cervejaria artesanal mineira fundada em 2007, conhecida pelas cervejas Capitão Senra e 3 Lobos."
    },
    {
        "name": "Devassa",
        "brewery_type": "regional",
        "city": "Rio de Janeiro",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "website_url": "https://www.devassa.com.br",
        "phone": "(21) 2122-1200",
        "description": "Cervejaria carioca fundada em 2007, conhecida pelas cervejas Devassa Tropical Lager e Devassa Bem Loura."
    },
    {
        "name": "Itaipava",
        "brewery_type": "large",
        "city": "Petrópolis",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "website_url": "https://www.itaipava.com.br",
        "phone": "(24) 2233-1200",
        "description": "Cerveja produzida pelo Grupo Petrópolis, fundada em 1994 em Petrópolis, RJ. Uma das mais vendidas do Brasil."
    },
    {
        "name": "Bohemia",
        "brewery_type": "regional",
        "city": "Petrópolis",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "website_url": "https://www.bohemia.com.br",
        "phone": "(24) 2233-1100",
        "description": "A cerveja mais antiga do Brasil, fundada em 1853 em Petrópolis, RJ. Pertence ao grupo Ambev."
    },
    {
        "name": "Stella Artois Brasil",
        "brewery_type": "large",
        "city": "São Paulo",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.stellaartois.com.br",
        "phone": "(11) 2122-1200",
        "description": "Versão brasileira da famosa cerveja belga, produzida pela Ambev no Brasil desde 1999."
    },
    {
        "name": "Heineken Brasil",
        "brewery_type": "large",
        "city": "Itu",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.heineken.com/br",
        "phone": "(11) 4023-5000",
        "description": "Operação brasileira da cervejaria holandesa Heineken, com fábrica em Itu, SP. Produz Heineken, Kaiser e outras marcas."
    },
    {
        "name": "Therezópolis",
        "brewery_type": "micro",
        "city": "Teresópolis",
        "state": "Rio de Janeiro",
        "country": "Brasil",
        "website_url": "https://www.cervejariatherezopolis.com.br",
        "phone": "(21) 2742-5500",
        "description": "Cervejaria artesanal fluminense fundada em 2007, conhecida por cervejas premium e especiais como a Therezópolis Gold."
    },
    {
        "name": "Dado Bier",
        "brewery_type": "brewpub",
        "city": "Porto Alegre",
        "state": "Rio Grande do Sul",
        "country": "Brasil",
        "website_url": "https://www.dadobier.com.br",
        "phone": "(51) 3330-5000",
        "description": "Cervejaria gaúcha fundada em 1995, pioneira no movimento de cervejas artesanais no Brasil."
    },
    {
        "name": "Bamberg",
        "brewery_type": "micro",
        "city": "Votorantim",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.cervejariabamberg.com.br",
        "phone": "(15) 3243-1200",
        "description": "Cervejaria artesanal paulista especializada em cervejas defumadas (Rauchbier) e de estilo alemão."
    },
    {
        "name": "Seasons",
        "brewery_type": "micro",
        "city": "Ribeirão Preto",
        "state": "São Paulo",
        "country": "Brasil",
        "website_url": "https://www.seasonsbrewing.com.br",
        "phone": "(16) 3512-7000",
        "description": "Cervejaria artesanal paulista conhecida pelas cervejas sazonais e uso de ingredientes locais."
    },
]


def buscar_brasileira(nome):
    """Busca cervejaria na base de dados local brasileira."""
    nome_lower = nome.lower().strip()
    for c in CERVEJARIAS_BRASILEIRAS:
        if nome_lower in c["name"].lower():
            return c
    return None


def get_beer_data(beer_name):
    """Busca cervejaria na Open Brewery DB (internacional)."""
    url = f"https://api.openbrewerydb.org/v1/breweries?by_name={beer_name}&per_page=1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ""

    if request.method == 'POST':
        beer = request.form.get('beer', '').strip()

        try:
            # Primeiro tenta a base de dados brasileira
            brasileira = buscar_brasileira(beer)

            if brasileira:
                website = brasileira.get('website_url') or 'N/A'
                website_link = f'<a href="{website}" target="_blank">{website}</a>' if brasileira.get('website_url') else 'N/A'
                descricao = brasileira.get('description', '')
                result_html = f"""
                <div style="margin-top:20px; border:2px solid #009C3B; padding:20px; border-radius:10px; text-align:left; max-width:550px; margin-left:auto; margin-right:auto; background:#f9fff9;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                        <span style="font-size:24px;">🇧🇷</span>
                        <h2 style="margin:0;">{brasileira.get('name', 'N/A')}</h2>
                    </div>
                    <p><b>Tipo:</b> {brasileira.get('brewery_type', 'N/A')}</p>
                    <p><b>Cidade:</b> {brasileira.get('city', 'N/A')}, {brasileira.get('state', 'N/A')}</p>
                    <p><b>País:</b> {brasileira.get('country', 'N/A')}</p>
                    <p><b>Website:</b> {website_link}</p>
                    <p><b>Telefone:</b> {brasileira.get('phone', 'N/A')}</p>
                    {f'<p><b>Sobre:</b> {descricao}</p>' if descricao else ''}
                </div>
                """
            else:
                # Se não encontrou no Brasil, busca na API internacional
                data = get_beer_data(beer)

                if data and len(data) > 0:
                    brewery = data[0]
                    website = brewery.get('website_url') or 'N/A'
                    website_link = f'<a href="{website}" target="_blank">{website}</a>' if brewery.get('website_url') else 'N/A'
                    result_html = f"""
                    <div style="margin-top:20px; border:1px solid #ddd; padding:20px; border-radius:10px; text-align:left; max-width:550px; margin-left:auto; margin-right:auto;">
                        <h2>{brewery.get('name', 'N/A')}</h2>
                        <p><b>Tipo:</b> {brewery.get('brewery_type', 'N/A')}</p>
                        <p><b>Cidade:</b> {brewery.get('city', 'N/A')}, {brewery.get('state', 'N/A')}</p>
                        <p><b>País:</b> {brewery.get('country', 'N/A')}</p>
                        <p><b>Website:</b> {website_link}</p>
                        <p><b>Telefone:</b> {brewery.get('phone', 'N/A')}</p>
                    </div>
                    """
                else:
                    result_html = "<p style='color:red; margin-top:20px;'>Cervejaria não encontrada. Tente outro nome.</p>"

        except Exception as e:
            result_html = f"<p style='color:red;'>Ocorreu um erro: {str(e)}</p>"

    # Lista de cervejarias brasileiras para exibir como sugestão
    sugestoes_br = ", ".join([c["name"] for c in CERVEJARIAS_BRASILEIRAS[:8]])

    return render_template_string("""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Buscador de Cervejarias</title>
        <style>
            body {
                text-align: center;
                font-family: sans-serif;
                padding: 50px;
                background-color: #f5f5f5;
            }
            input {
                padding: 10px;
                width: 280px;
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
            .hint {
                color: #888;
                font-size: 13px;
                margin-top: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Buscador de Cervejarias 🍺</h1>
        <p style="color:#666;">Cervejas brasileiras 🇧🇷 e internacionais 🌍</p>
        <form method="post">
            <input type="text" name="beer" placeholder="Ex: Brahma, Colorado, Eisenbahn" required>
            <button type="submit">Buscar</button>
        </form>
        <p class="hint">Brasileiras: {{ sugestoes_br }}</p>
        {{ result_html | safe }}
    </body>
    </html>
    """, result_html=result_html, sugestoes_br=sugestoes_br)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
