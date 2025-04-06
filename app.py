import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

# Charger les données CSV
associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

## Vous devez ajouter les routes ici : 
@app.route('/')
def helloworld():
    return f'hello world !'

@app.route('/api/alive',methods=['GET'])
def isalive():
    return jsonify({"message":"Alive"})

@app.route('/api/associations',methods=['GET'])
def liste_assos():
    #on convertit les données en liste car jsonify ne supporte pas les dataframes, ni les arrays
    return jsonify(list(associations_df["id"]))

@app.route('/api/association/<int:id>',methods=['GET'])
def infos_asso(id):
    if id>=1 and id<=4 :
        df_asso = associations_df.iloc[id-1]
        #le cours sur les dataframes est un peu loin, je m'en suis sorti de manière peu élégante
        array_asso = np.array(df_asso)
        return jsonify({"id":id,"nom":array_asso[1],"type":array_asso[2],"description":array_asso[3]})
    else :
        return jsonify({"error":"Association not found"})

@app.route('/api/evenements',methods=['GET'])
def liste_evenements():
    return jsonify(list(evenements_df["id"]))

@app.route('/api/evenement/<int:id>',methods=['GET'])
def infos_evenement(id):
    if id>=101 and id<=105 :
        df_eve = evenements_df.iloc[id-101]
        array_eve = np.array(df_eve)
        return jsonify({"id":str(id),"association_id":str(array_eve[1]),"nom":str(array_eve[2]),"date":str(array_eve[3]),"lieu":str(array_eve[4]),"description":str(array_eve[5])})
    else :
        return jsonify({"error":"Event not found"})
    
@app.route('/api/association/<int:id>/evenements',methods=['GET'])
def evenements_de_asso(id):
    if id>=1 and id<=4:
        df_eve_de_asso = evenements_df[evenements_df['association_id']==id]['id']
        print(df_eve_de_asso)
        #le cours sur les dataframes est un peu loin, je m'en suis sorti de manière peu élégante
        array_eve_asso = np.array(df_eve_de_asso)
        liste_eve_asso = list(array_eve_asso)
        return jsonify([str(a) for a in liste_eve_asso])
    else :
        return jsonify({"error":"Association not found"})


@app.route('/api/type/<float:type>/associations',methods=['GET'])
def assos_par_type(type):
    if type in associations_df["type"] :
        df_assos_type = associations_df[associations_df['type']==type]['id']
        array_assos_type = np.array(df_assos_type)
        liste_asso_type = list(array_assos_type)
        return jsonify([str(a) for a in liste_asso_type])
    else :
        return jsonify({"error":"Type not found"})

if __name__ == '__main__':
    app.run(debug=False)