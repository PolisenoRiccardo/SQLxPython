import pyodbc
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response
app = Flask(__name__)

@app.route('/', methods=['GET'])

def grafico():
    

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
    fig, ax = plt.subplots(figsize = (8,12))
    plt.subplots_adjust(bottom=0.3)
    ax.bar(labels, dati,width = 0.5, color="green")
    ax.set_ylabel('Monete')
    ax.set_xlabel('Studenti')
    ax.set_title('Totale delle monete guadagnate in tutti i giochi')

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template(table.html)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)