// JavaScript pour activer les tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// JavaScript pour activer les modals
const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})

  // JavaScript pour activer la validation client côté navigateur de Bootstrap
  ; (function () {
    'use strict'
    window.addEventListener(
      'load',
      function () {
        // Récupère tous les formulaires qui nécessitent une validation
        var forms = document.getElementsByClassName('needs-validation')
        // Boucle sur tous les formulaires
        var validation = Array.prototype.filter.call(forms, function (form) {
          form.addEventListener(
            'submit',
            function (event) {
              if (form.checkValidity() === false) {
                event.preventDefault()
                event.stopPropagation()
              }
              form.classList.add('was-validated')
            },
            false
          )
        })
      },
      false
    )
  })()

// button |- 1 +|
function inc(element) {
  let el = document.querySelector(`[name="${element}"]`);
  el.value = parseInt(el.value) + 1;
}

function dec(element) {
  let el = document.querySelector(`[name="${element}"]`);
  if (parseInt(el.value) > 0) {
    el.value = parseInt(el.value) - 1;
  }
}

// toast display
document.getElementById("toastbtn").onclick = function () {
  var toastElList = [].slice.call(document.querySelectorAll('.toast'))
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl)
  })
  toastList.forEach(toast => toast.show())
}

// price total update
function updateTotal(id) {
  document.getElementById('send-' + id).click()
}
