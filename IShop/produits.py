from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash

import app
import bd
from bd import get_produits_from_id
import os
import app

ALLOWED_EXTENSIONS = {'png'}

produits_bp = Blueprint('produits', __name__)


@produits_bp.route('/<int:identifiant>', methods=['GET'])
def info(identifiant):
    """Affiche les informations d'un produit"""
    produit = []
    if identifiant:
        with bd.creer_connexion() as conn:
            produit = get_produits_from_id(conn, identifiant)
            if not produit:
                return abort(404, "Le produit n'existe pas")
            else:
                return render_template('produits/infos.jinja', produit=produit)
    else:
        return abort(400, "Paramètre 'id' manquant ou incorrect")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@produits_bp.route('/<identifiant>/uplodeImage', methods=['POST'])
def upload_image(identifiant):
    if request.method == 'POST':
        file = request.files['file[]']
        if file:
            if allowed_file(file.filename):
                app.upload_file(identifiant, file)
                flash("L'image a bien été enregistré", category="success")
            else:
                flash("Le fichier n'est pas un png", category="danger")
        else:
            flash("Le fichier n'a pas été trouvé", category="danger")
    return redirect('/produits/' + identifiant)


@produits_bp.route('/<identifiant>/modifier_image', methods=['GET', 'POST'])
def modifier_image(identifiant):
    """Modifie l'image d'un produit"""
    produit = []
    if session["est_administrateur"]:
        if request.method == 'GET':
            if identifiant.isnumeric():
                with bd.creer_connexion() as conn:
                    produit = get_produits_from_id(conn, identifiant)
                    if not produit:
                        abort(404, "Paramètre 'id' invalide")
                    else:
                        return render_template('produits/modimage.jinja', produit=produit)
            else:
                abort(400, "Paramètre 'id' manquant ou incorrect")
        if request.method == 'POST':
            file = request.files['file[]']
            if file:
                if allowed_file(file.filename):
                    if identifiant.isnumeric():
                        if file_exists('static/images/produits/produit' + identifiant + '.png'):
                            os.remove('static/images/produits/produit' + identifiant + '.png')
                            app.upload_file(identifiant, file)
                            flash("L'image a bien été modifiée", category="success")
                        else:
                            flash("L'image est image inexistante", category="danger")
                    else:
                        abort(404, "Paramètre 'id' invalide ou image inexistante")
                else:
                    flash("Le fichier n'est pas un png", category="danger")
            else:
                flash("Le fichier n'a pas été trouvé", category="danger")
    else:
        return abort(403, "Vous n'avez pas les autorisations requises.")

    return redirect('/produits/' + identifiant)


@produits_bp.route('/<int:identifiant>/supprimer_image', methods=['GET'])
def supprimer_image(identifiant):
    """supprime l'image d'un produit"""
    produit = []
    if session["est_administrateur"]:
        if identifiant:
            if file_exists('static/images/produits/produit' + str(identifiant) + '.png'):
                os.remove('static/images/produits/produit' + str(identifiant) + '.png')
                flash("L'image a bien été supprimée", category="success")
            else:
                abort(404, "Paramètre 'id' invalide ou image inexistante")
        else:
            abort(400, "Paramètre 'id' manquant ou incorrect")
    else:
        abort(403, "Vous n'avez pas les autorisations requises.")

    return redirect('/produits/' + str(identifiant))


def file_exists(file_path):
    return os.path.isfile(file_path)
