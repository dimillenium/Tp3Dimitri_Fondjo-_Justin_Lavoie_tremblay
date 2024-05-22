"""
Connexion à la BD.
"""

import types
import contextlib
import mysql.connector
from datetime import date, datetime


@contextlib.contextmanager
def creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user="garneau",
        password="qwerty123",
        host="127.0.0.1",
        database="420_05c_magasin",
        raise_on_warnings=True
    )

    # Pour ajouter la méthode getCurseur() à l'objet connexion
    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def get_curseur(self):
    """Permet d'avoir *tous* les enregistrements dans un dictionnaire"""
    curseur = self.cursor(dictionary=True, buffered=True)
    try:
        yield curseur
    finally:
        curseur.close()


def get_produits(conn):
    "Retourne les produits"
    with conn.get_curseur() as curseur:
        curseur.execute("SELECT * FROM produit ORDER BY id_produit DESC LIMIT 5")
        return curseur.fetchall()


def creeruser(conn, email, password, name, adresse):
    with conn.get_curseur() as curseur:
        curseur.execute(
            "INSERT INTO utilisateur (courriel,mdp,nom,adresse_postale,est_administrateur) VALUES (%(email)s,%(password)s,%(name)s,%(adresse)s,1)",
            {"email": email, "password": password, "name": name, "adresse": adresse})


def get_produits_by_stock(conn):
    "Retourne les produits"
    with conn.get_curseur() as curseur:
        curseur.execute("SELECT * FROM produit ORDER BY quantite DESC")
        return curseur.fetchall()


def get_produits_from_id(conn, id):
    "Retourne les produits"
    with conn.get_curseur() as curseur:
        curseur.execute("SELECT * FROM produit WHERE id_produit = %(id)s", {"id": id})
        return curseur.fetchone()


def get_produits_by_titre(conn, mot, minprice, maxprice):
    with conn.cursor() as curseur:
        curseur.execute(
            "SELECT * FROM produit WHERE prix BETWEEN %(prix_min)s AND %(prix_max)s AND (titre LIKE %(mot)s OR description LIKE %(mot)s)",
            {'mot': '%' + mot + '%', 'prix_min': minprice, 'prix_max': maxprice})
        return curseur.fetchall()


def get_produits_by_prix(conn, minprice, maxprice):
    with conn.cursor() as curseur:
        curseur.execute(
            "SELECT * FROM produit WHERE prix BETWEEN %(prix_min)s AND %(prix_max)s",
            {'prix_min': minprice, 'prix_max': maxprice})
        return curseur.fetchall()


def get_achat(conn, id):
    with conn.cursor() as curseur:
        curseur.execute(
            "SELECT a.*, p.titre, p.prix FROM achat a " +
            "INNER JOIN produit p ON a.fk_produit = p.id_produit " +
            "WHERE a.fk_utilisateur = %(id)s ORDER BY a.date_achat DESC",
            {
                "id": id
            }
        )
        return curseur.fetchall()


def verifier_user(conn, courriel, psw):
    with conn.cursor() as curseur:
        if curseur and courriel:
            curseur.execute("SELECT * FROM utilisateur WHERE courriel LIKE %(courriel)s AND mdp LIKE %(psw)s",
                            {"courriel": '%' + courriel + '%', "psw": '%' + psw + '%'})
            return curseur.fetchone()


def buy_produit(conn, id_prod, quantite, id_user):
    with conn.cursor() as curseur:
        curseur.execute('UPDATE produit SET quantite = quantite - %(quantite)s WHERE `id_produit` = %(id)s',
                        {
                            'id': id_prod,
                            'quantite': quantite
                        }
                        )
        curseur.execute(
            'INSERT INTO achat (date_achat,quantite,fk_utilisateur,fk_produit) VALUES (%(date)s,%(quantite)s,%(user)s,%(prod)s)',
            {
                'date': datetime.now(),
                'quantite': quantite,
                'user': id_user,
                'prod': id_prod
            }
        )


def verify_user(conn, courriel):
    with conn.cursor() as curseur:
        curseur.execute('SELECT * FROM utilisateur WHERE `courriel` = %s', (courriel,))
        return curseur.fetchone()
