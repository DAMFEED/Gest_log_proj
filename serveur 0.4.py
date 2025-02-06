from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

Mot_de_passe = "mdp"
Mot_de_passe_admin = "mdpa"


def inserer_donnees(ip, level, date):
    """Insère les données dans la base MySQL."""
    try:
        connection = mysql.connector.connect(
            host='10.78.5.239',
            user='userlog',
            password='userlog',
            database='data_log'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = "INSERT INTO logs (ip, level, date) VALUES (%s, %s, %s)"
            cursor.execute(sql_query, (ip, level, date))
            connection.commit()
            print("Données insérées avec succès.")
    except Error as e:
        print(f"Erreur lors de l'insertion dans MySQL : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def recuperer_logs(ip=None):
    """Récupère les logs avec filtre optionnel par IP."""
    logs = []
    try:
        connection = mysql.connector.connect(
            host='10.78.5.239',
            user='userlog',
            password='userlog',
            database='data_log'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = "SELECT ip, level, date FROM logs"
            if ip:
                sql_query += " WHERE ip = %s"
                cursor.execute(sql_query, (ip,))
            else:
                cursor.execute(sql_query)

            rows = cursor.fetchall()
            for row in rows:
                logs.append({'IP': row[0], 'Niveau de sévérité': row[1], 'Date': str(row[2])})

    except Error as e:
        print(f"Erreur lors de la récupération des logs : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return logs


@app.route('/upload', methods=['POST'])
def recevoir_logs():
    """Route pour recevoir les logs."""
    mdp = request.json.get('mdp')
    logs_data = request.json.get('logs')

    if mdp != Mot_de_passe:
        return jsonify({'message': 'Mot de passe incorrect'}), 401

    if not logs_data:
        return jsonify({'message': 'Aucun log fourni'}), 400

    try:
        for log in logs_data:
            ip = log.get("IP")
            date = log.get("Date")
            level = log.get("Niveau de sévérité")
            inserer_donnees(ip, level, date)
        return jsonify({'message': 'Envoi effectué avec succès'}), 200
    except Exception as e:
        return jsonify({'message': f'Erreur lors du traitement des données : {e}'}), 500


@app.route('/renvoyer/<ip>/<mdp>', methods=['GET'])
def renvoyer_logs(ip, mdp):
    """Route pour renvoyer les logs selon l'IP et le mot de passe"""
    if mdp != Mot_de_passe:
        return jsonify({'message': 'Mot de passe incorrect'}), 401

    logs = recuperer_logs(ip=ip)
    if logs:
        return jsonify({'message': 'Renvoi effectué', 'logs': logs}), 200
    return jsonify({'message': 'Aucun log trouvé'}), 404


@app.route('/renvoyer_tout_les_logs/<mdpa>', methods=['GET'])
def renvoyer_tout_les_logs(mdpa):
    """Route pour renvoyer tous les logs avec mot de passe admin"""
    if mdpa != Mot_de_passe_admin:
        return jsonify({'message': 'Mot de passe administrateur incorrect'}), 401

    logs = recuperer_logs()
    if logs:
        return jsonify({'message': 'Renvoi effectué', 'logs': logs}), 200
    return jsonify({'message': 'Aucun log trouvé'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
