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
        .addEventListener("input", afficherSuggestions)
}

window.addEventListener("load", initialisation)