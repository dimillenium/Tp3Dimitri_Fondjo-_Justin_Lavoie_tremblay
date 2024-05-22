import hashlib
import re

from flask import Blueprint, render_template, request, session, make_response, redirect, url_for, flash, abort

import bd
from bd import get_achat, get_produits_from_id, buy_produit

regex_courriel = r'^[\w\.-]+@[\w\.-]+\.\w+$'
caracteres_interdits = re.compile('<|>')

compte_bp = Blueprint('compte', __name__)


@compte_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    """Affiche un formulaire de connexion"""
    if request.method == 'POST':
        courriel = request.form.get('email', default=None, type=str)
        mdp = request.form.get('password', default=None, type=str)

        if not courriel or not mdp:
            return render_template('compte/connexion.jinja',
                                   error='Veuillez remplir tous les champs.', courriel=courriel, mdp=mdp)

        if caracteres_interdits.match(courriel) or caracteres_interdits.match(mdp):
            return render_template('compte/connexion.jinja',
                                   error='Ne pas inscrire des caracteres HTML.', courriel=courriel, mdp=mdp)
        if re.match(regex_courriel, courriel):

            hashed_password = hashlib.sha512(mdp.encode()).hexdigest()

            with bd.creer_connexion() as conn:
                user = bd.verifier_user(conn, courriel, hashed_password)
            if user is not None:
                session['nom'] = user[3]
                session['connecter'] = True
                session['est_administrateur'] = user[5]
                session['id_user'] = user[0]
                flash('Vous avez été connecté avec succes', category='success')
                return redirect('/')
            else:
                return render_template('compte/connexion.jinja',
                                       error='Identifiants incorrects ou inexistants', courriel=courriel, mdp=mdp)
        else:
            return render_template('compte/connexion.jinja',
                                   error='Le courriel ne respecte pas le format exigé :xxxx@xxxmail.com',
                                   courriel=courriel, mdp=mdp)
    return render_template('compte/connexion.jinja')


@compte_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """Affiche un formulaire d'inscription"""
    if request.method == 'POST':
        courriel = request.form.get('email', default=None, type=str)
        mdp1 = request.form.get('password', default=None, type=str)
        mdp2 = request.form.get('pswConf', default=None, type=str)
        adresse = request.form.get('adresse', default=None, type=str)
        name = request.form.get('nom', default=None, type=str)

        if caracteres_interdits.match(courriel) or caracteres_interdits.match(mdp1) or caracteres_interdits.match(
                mdp2) or caracteres_interdits.match(adresse) or caracteres_interdits.match(name):
            return render_template('compte/inscription.jinja', error='Veuillez ne pas écrire des caracteres interdits.',
                                   courriel=courriel, mdp1=mdp1, mdp2=mdp2, adresse=adresse, name=name)


        if not courriel or not mdp1 or not mdp2 or not adresse or not name:
            return render_template('compte/inscription.jinja', error='Veuillez remplir les champs vides',
                                   courriel=courriel, mdp1=mdp1, mdp2=mdp2, adresse=adresse, name=name)
        with bd.creer_connexion() as conn:
            if mdp1 == mdp2:
                if re.match(regex_courriel, courriel):
                    hashed_password = hashlib.sha512(mdp1.encode()).hexdigest()
                    user_existe = bd.verify_user(conn, courriel)

                    if not user_existe:
                        bd.creeruser(conn, courriel, hashed_password, name, adresse)
                        flash("Vous avez bien été ajouté", "sucess")
                        user = bd.verify_user(conn, courriel)
                        session['nom'] = user[3]
                        session['connecter'] = True
                        session['est_administrateur'] = user[5]
                        flash('Votre compte a été créé avec succes', category='success')
                        return redirect(url_for('accueil'))
                    else:
                        return render_template('compte/inscription.jinja',
                                               error="Un utilisateur avec ce courriel existe déja.", courriel=courriel,
                                               mdp1=mdp1,
                                               mdp2=mdp2, adresse=adresse, name=name)
                else:
                    return render_template('compte/inscription.jinja',
                                           error='Le couriel ne respecte pas le format exigé :xxxx@gmail.com',
                                           courriel=courriel, mdp1=mdp1,
                                           mdp2=mdp2, adresse=adresse, name=name)
            else:
                return render_template('compte/inscription.jinja',
                                       error=' Les mots de passe ne correspondent pas', courriel=courriel, mdp1=mdp1,
                                       mdp2=mdp2, adresse=adresse, name=name)
    return render_template('compte/inscription.jinja')


@compte_bp.route("/panier", methods=["GET", "POST"])
def panier():
    """Affiche un message"""
    achats = []
    if request.method == "POST":
        produit_id = request.form.get("id")
        quantite = request.form.get("amount-" + produit_id, type=int, default="")
        with bd.creer_connexion() as conn:
            produit = get_produits_from_id(conn, produit_id)
        if not quantite == "":
            if quantite > 0:
                if produit['quantite'] >= quantite:
                    with bd.creer_connexion() as conn:
                        buy_produit(conn, produit['id_produit'], quantite, session.get("id_user", default=""))
                    flash("Le produit à bien été acheté!", category="success")
                else:
                    flash("Il n'y pas pas sufisamment de ce produit en inventaire", category="danger")

            else:
                abort(400, "Plus de stock disponible")
        else:
            flash("La quantité doit être un nombre!", category="danger")

        return redirect('/produits/' + produit_id)
    if request.method == "GET":
        with bd.creer_connexion() as conn:
            achats = get_achat(conn, session.get("id_user", default=""))
            print(achats)
        return render_template("compte/achat.jinja", achats=achats)


@compte_bp.route('/deconnexion', methods=['GET', 'POST'])
def logout():
    if session.get("connecter", default="") != "":
        session.clear()
        flash('Vous avez été deconnecté avec succes', category='success')

    return redirect(url_for('accueil'))
