"""
Une application Flask des plus simples !
"""
import os

import re
from venv import logger

from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash, jsonify
import psycopg2
from produits import produits_bp
from compte import compte_bp
import bd
from bd import get_produits, get_produits_by_stock, get_produits_by_titre, get_produits_from_id, buy_produit, \
    get_produits_by_prix

UPLOAD_FOLDER = os.path.join('static', 'images', 'produits')

caracteres_interdits = re.compile('<|>')

app = Flask(__name__)
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 1}
app.secret_key = "eb5f2509bd5f07f9df8054fcda25c45f64df246b6bf56fdb182c41bfd3ccda24"
app.register_blueprint(produits_bp, url_prefix='/produits')
app.register_blueprint(compte_bp, url_prefix='/compte')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.template_filter('file_exists')
def file_exists(file_path):
    return os.path.isfile(file_path)


@app.route("/")
def accueil():
    """Affiche les produits sur la route / """
    with bd.creer_connexion() as conn:
        produits = get_produits(conn)
    connecter = session.get('connecter', False)
    return render_template("accueil.jinja", produits=produits, connecter=connecter)


@app.route("/get_latest_products")
def get_latest_products_route():
    with bd.creer_connexion() as conn:
        produits = get_produits(conn)
    connecter = session.get('connecter', False)
    return jsonify({'produits': produits, 'connecter': connecter})


@app.route("/recherche", methods=["GET", "POST"])
def rechercher():
    keyword = ""
    produits = []
    """Affiche produits sur la route /recherche"""
    if request.method == "GET":
        keyword = request.args.get("keyword", type=str, default="")
        prix_min = request.args.get("minPrice", type=float, default=0)
        prix_max = request.args.get("maxPrice", type=float, default=5000)
        if caracteres_interdits.match(keyword) or caracteres_interdits.match(
                str(prix_min)) or caracteres_interdits.match(str(prix_max)):
            flash("Certains caracteres ne sont pas valide.", category="danger")
            return redirect(url_for('accueil'))
        else:
            with bd.creer_connexion() as conn:
                if keyword == "":
                    produits = get_produits_by_prix(conn, prix_min, prix_max)
                else:
                    produits = get_produits_by_titre(conn, keyword, prix_min, prix_max)

        return render_template("accueil.jinja", produits=produits)


def upload_file(identifiant, file):
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "produit" + identifiant + ".png"))


@app.errorhandler(400)
def bad_request(e):
    """Pour les erreurs 400"""

    # On verra dans le log les infos et le message laissé par abort(400, "le message")
    logger.exception(e)

    return render_template(
        'error.jinja',
        message="Parametres manquants"
    ), 400


@app.errorhandler(403)
def bad_request(e):
    """Pour les erreurs 400"""

    # On verra dans le log les infos et le message laissé par abort(400, "le message")
    logger.exception(e)

    return render_template(
        'error.jinja',
        message="vous n'avez pas acces à cette page "
    ), 403


@app.errorhandler(404)
def bad_request(e):
    """Pour les erreurs 400"""

    # On verra dans le log les infos et le message laissé par abort(400, "le message")
    logger.exception(e)

    return render_template(
        'error.jinja',
        message="Vous voulez acceder à une route inexistante ou un produit inexistant"
    ), 404


@app.errorhandler(500)
def bad_request(e):
    """Pour les erreurs 400"""

    # On verra dans le log les infos et le message laissé par abort(400, "le message")
    logger.exception(e)

    return render_template(
        'error.jinja',
        message="Probleme avec la bd "
    ), 500


@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    keyword = request.args.get("keyword", type=str, default="")
    prix_min = request.args.get("minPrice", type=float, default=0)
    prix_max = request.args.get("maxPrice", type=float, default=5000)
    # Connexion à la base de données
    with bd.creer_connexion() as conn:
        suggestions = get_produits_by_titre(conn, keyword, prix_min, prix_max)

    return jsonify(suggestions)


@app.route('/verification_identifiant', methods=['POST'])
def verification_identifiant():
    email = request.json.get('email')
    email_used = False
    with bd.creer_connexion() as conn:
        email_used = bd.verify_user(conn, email)

    return jsonify({'utilise': email_used})
