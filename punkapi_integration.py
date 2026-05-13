import os

import requests

from flask import Flask, render_template_string, request



app = Flask(__name__)



def get_beer_data(beer_name):
  
    url = f"https://api.punkapi.com/v2/beers?beer_name={beer_name}"
  
    response = requests.get(url)
  
    return response.json()
  


@app.route('/', methods=['GET', 'POST'])

def index():
  
    result_html = ""
  
    if request.method == 'POST':
      
        beer = request.form.get('beer')
      
        try:
          
            data = get_beer_data(beer)
          
            if data:
              
                item = data[0]
              
                result_html = f"""
                
                    <div style="margin-top:20px; border:1px solid #ddd; padding:20px; border-radius:10px;">
                    
                        <h2>{item['name']}</h2>
                        
                        <p><b>Tagline:</b> {item['tagline']}</p>
                        
                        <p><b>ABV:</b> {item['abv']}%</p>
                        
                        <p><b>IBU:</b> {item['ibu']}</p>
                        
                        <p><b>Descrição:</b> {item['description']}</p>
                        
                        <img src="{item['image_url']}" width="100">
                        
                    </div>
                    
                """
                
            else:
            
                result_html = "<p style='color:red;'>Cerveja não encontrada.</p>"
                
        except Exception as e:
        
            result_html = f"<p style='color:red;'>Ocorreu um erro: {e}</p>"
            


    return render_template_string(f"""
    
        <html>
        
            <body style="text-align:center; font-family:sans-serif; padding:50px;">
            
                <h1>Buscador de Cervejas 🍺</h1>
                
                <form method="post">
                
                    <input type="text" name="beer" placeholder="Ex: Punk IPA" style="padding:10px; width:200px;">
                    
                    <button type="submit" style="padding:10px;">Buscar</button>
                    
                </form>
                
                {result_html}
                
            </body>
            
        </html>
        
    """)
    


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port)
    










































