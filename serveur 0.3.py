from flask import Flask, request, jsonify, Response
import mysql.connector
from mysql.connector import Error
import json  # Pour le traitement du format JSON


app = Flask(__name__)

Mot_de_passe = "mdp"  # Mot de passe utilisateur (à modifier)
Mot_de_passe_admin = "mdpa"  # Mot de passe administrateur (à modifier)


def inserer_donnees(ip, level, date):
    """Insère les données dans la base MySQL"""
    connection = None
    cursor = None  # Initialisation du curseur
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='10.78.5.239',    # Adresse IP du serveur
            user='userlog',        # Nom d'utilisateur MySQL
            password='userlog',    # Mot de passe de l'utilisateur
            database='data_log'    # Nom de la base de données
        )

        if connection.is_connected():
            print("Connexion réussie au serveur MySQL")

            # Requête SQL pour insérer les données
            sql_query = """
            INSERT INTO logs (ip, level, date)
            VALUES (%s, %s, %s)
            """

            # Les valeurs à insérer
            valeurs = (ip, level, date)

            # Création d'un curseur pour exécuter la requête
            cursor = connection.cursor()
            cursor.execute(sql_query, valeurs)

            # Validation des changements
            connection.commit()
            print("Données insérées avec succès.")

    except Error as e:
        print(f"Erreur lors de la connexion ou de l'insertion dans MySQL : {e}")

    finally:
        # Fermer la connexion et le curseur seulement si nécessaires
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")


def recuperer_logs(ip=None):
    """Récupère les logs depuis la base de données, avec un filtre optionnel sur l'IP"""
    connection = None
    cursor = None
    logs = []  # Liste pour stocker les logs récupérés
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='10.78.5.239',    # Adresse IP du serveur
            user='userlog',        # Nom d'utilisateur MySQL
            password='userlog',    # Mot de passe de l'utilisateur
            database='data_log'    # Nom de la base de données
        )

        if connection.is_connected():
            print("Connexion réussie au serveur MySQL")

            # Requête SQL pour récupérer les logs
            sql_query = "SELECT ip, level, date FROM logs"
            if ip:
                sql_query += " WHERE ip = %s"  # Ajout du filtre par IP si fourni

            # Création d'un curseur pour exécuter la requête
            cursor = connection.cursor()
            if ip:
                cursor.execute(sql_query, (ip,))
            else:
                cursor.execute(sql_query)

            # Récupérer toutes les lignes de la requête
            rows = cursor.fetchall()

            # Convertir les résultats en une liste de dictionnaires
            for row in rows:
                date_str = str(row[2])  # Conversion de la date en chaîne de caractères
                logs.append({
                    'IP': row[0],
                    'Date': date_str,  # Simple affichage de la date
                    'Niveau de sévérité': row[1]
                })

            return logs  # Retourne les logs sous forme de liste de dictionnaires

    except Error as e:
        print(f"Erreur lors de la récupération des logs : {e}")
        return None

    finally:
        # Fermer la connexion et le curseur seulement si nécessaires
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Connexion MySQL fermée.")


@app.route('/upload/<logs>', methods=['GET'])
def recevoir_logs(logs):
    """Route pour recevoir les logs"""
    mdp = request.args.get('mdp')  # Récupération du mot de passe
    if mdp == Mot_de_passe:
        try:
            # Décodage des logs encodés dans l'URL
            logs_data = json.loads(logs)

            # Parcourir chaque entrée dans le JSON pour extraire les informations
            for log in logs_data:
                ip = log.get("IP")
                date = log.get("Date")
                level = log.get("Niveau de sévérité")

                print(f"IP: {ip}, Level: {level}, Date: {date}")

                # Insertion des données dans la base MySQL
                inserer_donnees(ip, level, date)

            return jsonify({'message': 'Envoi effectué avec succès', 'logs': logs_data}), 200
        except json.JSONDecodeError as e:
            return jsonify({'message': f'Erreur de format JSON : {e}'}), 400
        except Exception as e:
            return jsonify({'message': f'Erreur lors du traitement des données : {e}'}), 500
    else:
        return jsonify({'message': 'Mot de passe incorrect'}), 401


@app.route('/renvoyer', methods=['GET'])
def renvoyer_logs():
    """Route pour renvoyer les logs au client"""
    mdp = request.args.get('mdp')
    ip = request.args.get('ip')  # Récupération de l'IP demandée par le client
    if mdp == Mot_de_passe:
        # Si une IP est fournie, on récupère les logs pour cette IP
        if ip:
            logs = recuperer_logs(ip=ip)
            if logs is not None:
                return jsonify({'message': 'Renvoi effectué', 'logs': logs}), 200
            else:
                return jsonify({'message': 'Erreur lors de la récupération des logs'}), 500
        else:
            # Si aucune IP n'est fournie, on vérifie si l'utilisateur a les privilèges administrateur
            mdpa = request.args.get('mdpa')  # Mot de passe administrateur
            if mdpa == Mot_de_passe_admin:
                # Si l'utilisateur est administrateur, on renvoie tous les logs
                logs = recuperer_logs()
                if logs is not None:
                    return jsonify({'message': 'Renvoi effectué', 'logs': logs}), 200
                else:
                    return jsonify({'message': 'Erreur lors de la récupération des logs'}), 500
            else:
                # Si l'utilisateur n'a pas de privilèges administrateur, on renvoie une erreur
                return jsonify({'message': 'Vous n\'avez pas les privilèges administrateur pour cette action.'}), 403
    else:
        return jsonify({'message': 'Mot de passe incorrect'}), 399


@app.route('/renvoyer_tout_les_logs', methods=['GET'])
def renvoyer_tout_les_logs():
    """Route pour renvoyer tous les logs au client avec un affichage simple"""
    mdpa = request.args.get('mdpa')
    if mdpa == Mot_de_passe_admin:
        logs = recuperer_logs()  # Appel à la fonction pour récupérer tous les logs
        if logs is not None:
            # Simple affichage des logs avec un saut de ligne après la date
            logs_simplified = []
            for log in logs:
                logs_simplified.append(f"IP: {log['IP']} | Niveau: {log['Niveau de sévérité']} | Date: {log['Date']} ")

            # Retourner les logs simplifiés au client
            return jsonify({'message': 'Renvoi effectué', 'logs': logs_simplified}), 200
        else:
            return jsonify({'message': 'Erreur lors de la récupération des logs'}), 500
    return jsonify({'message': 'Mot de passe incorrect'}), 399



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
