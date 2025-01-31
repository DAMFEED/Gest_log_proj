from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
import json

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition des mots de passe pour sécuriser les endpoints
Mot_de_passe = "tsiris"
Mot_de_passe_admin = "sirist"

# Fonction pour insérer des logs dans la base de données MySQL
def inserer_donnees(ip, level, date):
    connection = None
    cursor = None
    try:
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host='10.78.5.239',  # Adresse de l'hôte MySQL
            user='userlog',      # Nom d'utilisateur MySQL
            password='userlog',  # Mot de passe MySQL
            database='data_log'  # Nom de la base de données
        )
        if connection.is_connected():
            # Requête SQL pour insérer les données dans la table 'logs'
            sql_query = """
            INSERT INTO logs (ip, level, date)
            VALUES (%s, %s, %s)
            """
            valeurs = (ip, level, date)  # Données à insérer
            cursor = connection.cursor()
            cursor.execute(sql_query, valeurs)  # Exécution de la requête
            connection.commit()  # Validation de l'insertion
            print("Données insérées avec succès.")

    except Error as e:
        # Gestion des erreurs de connexion ou d'insertion
        print(f"Erreur lors de la connexion ou de l'insertion dans MySQL : {e}")
    finally:
        # Fermeture des ressources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")

# Fonction pour récupérer les logs depuis la base de données MySQL
def recuperer_logs(ip=None):
    connection = None
    cursor = None
    logs = []
    try:
        # Connexion à la base de données MySQL
        connection = mysql.connector.connect(
            host='10.78.5.239',
            user='userlog',
            password='userlog',
            database='data_log'
        )
        if connection.is_connected():
            # Requête SQL pour récupérer les logs
            sql_query = "SELECT ip, level, date FROM logs"
            if ip:
                sql_query += " WHERE ip = %s"  # Filtre par IP si fourni
            cursor = connection.cursor()
            cursor.execute(sql_query, (ip,) if ip else None)  # Exécution de la requête
            rows = cursor.fetchall()  # Récupération des résultats
            for row in rows:
                date_str = str(row[2])  # Conversion de la date en chaîne
                logs.append({
                    'IP': row[0],
                    'Date': date_str,
                    'Niveau de sévérité': row[1]
                })
            return logs

    except Error as e:
        # Gestion des erreurs de récupération des logs
        print(f"Erreur lors de la récupération des logs : {e}")
        return None
    finally:
        # Fermeture des ressources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")

# Endpoint pour recevoir des logs et les insérer dans la base de données
@app.route('/upload/<mdp>/<logs>', methods=['GET'])
def recevoir_logs(mdp, logs):
    if mdp == Mot_de_passe:  # Vérification du mot de passe
        try:
            logs_data = json.loads(logs)  # Conversion des logs JSON en objet Python
            # Insertion de chaque log dans la base de données
            for log in logs_data:
                ip = log.get("IP")
                date = log.get("Date")
                level = log.get("Niveau de sévérité")
                inserer_donnees(ip, level, date)
            return jsonify({'message': 'Envoi effectué avec succès', 'logs': logs_data}), 200
        except json.JSONDecodeError as e:
            # Gestion des erreurs de format JSON
            return jsonify({'message': f'Erreur de format JSON : {e}'}), 400
        except Exception as e:
            # Gestion des autres erreurs
            return jsonify({'message': f'Erreur lors du traitement des données : {e}'}), 500
    else:
        # Si le mot de passe est incorrect
        return jsonify({'message': 'Mot de passe incorrect'}), 401

# Endpoint pour récupérer les logs filtrés par IP
@app.route('/renvoyer/<mdp>/<ip>', methods=['GET'])
def renvoyer_logs(mdp, ip):
    if mdp == Mot_de_passe:  # Vérification du mot de passe
        logs = recuperer_logs(ip=ip)  # Récupération des logs pour l'IP donnée
        if logs is not None:
            return jsonify({'message': 'Renvoi effectué', 'logs': logs}), 200
        else:
            return jsonify({'message': 'Erreur lors de la récupération des logs'}), 500
    return jsonify({'message': 'Mot de passe incorrect'}), 399

# Endpoint pour récupérer tous les logs pour les administrateurs
@app.route('/renvoyer_tout_les_logs/<mdpa>', methods=['GET'])
def renvoyer_tout_les_logs(mdpa):
    if mdpa == Mot_de_passe_admin:  # Vérification du mot de passe administrateur
        logs = recuperer_logs()  # Récupération de tous les logs
        if logs is not None:
            # Simplification des logs pour les afficher de manière lisible
            logs_simplified = [f"IP: {log['IP']} | Niveau: {log['Niveau de sévérité']} | Date: {log['Date']}" for log in logs]
            return jsonify({'message': 'Renvoi effectué', 'logs': logs_simplified}), 200
        else:
            return jsonify({'message': 'Erreur lors de la récupération des logs'}), 500
    return jsonify({'message': 'Mot de passe incorrect'}), 399

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
