/**
 * Script pour l'affichage de suggestion de recherche
 */

"use strict"

const divCompletion = document.getElementById("search_completion")
let inputSearch = document.getElementById("keyword")
// Sélectionner le bouton
let searchButton = document.getElementById("search_button");

/**
 * Appelée lors d'un clic dans la fenêtre.
 */
function gererClicFenetre(evenement) {
    const clicDansDivision = divCompletion.contains(evenement.target);
    console.log("Clic dans la zone cliquable ? " + clicDansDivision)

    if (!clicDansDivision) {
        divCompletion.replaceChildren()
        divCompletion.classList.add("visually-hidden")
        document.removeEventListener("click", gererClicFenetre)
    }
}


/**
 * Pour demander les suggestions au site web.
 *
 * On devrait procéder par AJAX pour récupérer les suggestions, mais
 * elles sont "hard-codés" pour la démo.
 */
function afficherSuggestions() {
    const mot = inputSearch.value.trim();
    if (inputSearch.value.length > 2)
    {
        divCompletion.replaceChildren()

        divCompletion.classList.remove("visually-hidden")

        async function postJSON(data) {
            try {
                const response = await fetch("/suggestions", {
                    method: "POST",
                    body: JSON.stringify(data),
                });

                const result = await response.json();
                for (let i=0; i<5; i++) {
                    const div = document.createElement("div")
                    console.log(result[i])
                    div.innerHTML = `<a href="/produits/${ result[i][0] }" class="list-group-item list-group-item-action">${result[i][1]}</a>`
                    divCompletion.append(div)
                }
                console.log("Success:", result);
            } catch (error) {
                console.error("Error:", error);
            }
        }
        const data = { keyword: "mot" };
        postJSON(data);

        // Ajout d'un événement sur tout le document (la fenêtre)
        document.addEventListener("click", gererClicFenetre)
    }
    else
        divCompletion.classList.add("visually-hidden")

 }


/**
 * Appelée lors de l'initialisation de la page
 */
function initialisation() {
    document
        .getElementById("keyword")
        .addEventListener('input', afficherSuggestions)
}

document.addEventListener('DOMContentLoaded', function() {
    ajouterEmail();
});
function ajouterEmail() {
    let email = document.getElementById('email');

    email.addEventListener('blur', function () {
        // Obtenez la valeur actuelle du champ email
        const valeurRecherche = email.value.trim();

        // Vérifiez si le champ email contient du texte
        if (valeurRecherche !== '') {
            // Envoyer la requête AJAX au serveur pour vérifier l'email
            fetch('/verification_identifiant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: valeurRecherche })
            })
            .then(response => response.json())
            .then(data => {
                if (data.utilise) {
                    // Affiche un message si l'email est déjà utilisé
                    console.log('Cet email est déjà utilisé.');
                    document.getElementById('email-error').innerText = 'Cet email est déjà utilisé.';
                    email.classList.add('is-invalid');
                    email.setCustomValidity('Cet email est déjà utilisé.');
                } else {
                    // L'email n'est pas utilisé
                    console.log('Cet email est disponible.');
                    document.getElementById('email-error').innerText = '';
                    email.setCustomValidity('');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
            });
        }
    });
}

window.addEventListener("load", initialisation)
