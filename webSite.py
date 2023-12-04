import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])

def sign_in():
    return render_template("log.html") 



@app.route('/grafico', methods=['GET'])

def grafico():
    user, password = request.args.get('user'), request.args.get('pasw')
    
    if  user == 'admin' and password == 'xxx123#':
      server = '192.168.40.16'
      database = 'zhao.filippo'
      username = 'zhao.filippo'
      password = 'xxx123##'
      driver= '{SQL Server}'
                
      connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
      conn = pyodbc.connect(connectionString) 
      
      sql_query = """
      select  Studente.Nome, Studente.Cognome, sum(monete.Numero_Monete) as Totale_Monete from poliseno.Studente
      INNER JOIN poliseno.Monete
      on Studente.ID = monete.IDStud
      INNER JOIN poliseno.Iscrizione
      on Studente.ID = Iscrizione.IDStudente
      GROUP BY Studente.Nome, Studente.Cognome
      ORDER by sum(poliseno.monete.Numero_Monete) desc
      """
  
      df = pd.read_sql(sql_query, conn)
      
      labels = df.Nome
      dati = df.Totale_Monete
      fig, ax = plt.subplots(figsize = (12,12))
      plt.subplots_adjust(bottom=0.3)
      ax.bar(labels, dati,width = 0.5, color="green")
      ax.set_ylabel('Monete')
      ax.set_xlabel('Studenti')
      ax.set_title('Totale delle monete guadagnate in tutti i giochi')
      fig.savefig('static\image\grafico.png')
      
      return render_template("table.html", user = user) 
    else:
      return render_template("errore.html") 

@app.route('/registrazione', methods=['GET'])

def sign_up():
    
    server = '192.168.40.16'
    database = 'zhao.filippo'
    username = 'zhao.filippo'
    password = 'xxx123##'
    driver= '{SQL Server}'
              
    connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connectionString) 

    return render_template("registrazione.html") 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)