document.addEventListener('DOMContentLoaded', function () {
    function fetchLatestProducts() {
        fetch('/get_latest_products')
            .then(response => response.json())
            .then(data => {
                const productsContainer = document.getElementById('products-container');
                const { produits, connecter } = data;

                productsContainer.innerHTML = '';
                // Limiter le nombre de produits à 5
                const produitsLimites = produits.slice(0, 5);

                produitsLimites.forEach(p => {
                    const productDiv = document.createElement('div');
                    productDiv.className = 'col-12 col-md-6 col-lg-4 col-xl-3 d-flex justify-content-center pb-3 product-card';
                    productDiv.setAttribute('data-id', p.id_produit);
                    productDiv.innerHTML = `
                        <div class="card h-100 shadow bg-body-tertiary rounded" style="width: 18rem;">
                            <div class="card-header d-flex justify-content-center p-0">
                            <img src="/static/images/produits/produit.png" class="border-bottom img-fluid p-0" alt="Produit image" onerror="this.onerror=null;this.src='/static/images/produits/default.png';"/>
                            </div>
                            <div class="card-body">
                                <div class="d-flex align-items-start">
                                    <h3 class="card-title pt-1" style="font-size: 2rem;">${p.titre}</h3>
                                    <a class="nav-link" href="/produits/${p.id_produit}">
                                        <i class="bi bi-info-circle" style="font-size: 2rem;"></i>
                                    </a>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="d-flex justify-content-center">
                                    <p class="card-text text-danger fs-5">
                                        <b>${p.prix}$</b>
                                    </p>
                                </div>
                                ${connecter ? `
                                ${p.quantite === 0 ? `
                                    <p class="text-center fw-bold">Ce produit n'est plus en inventaire. Revenez plus tard!</p>
                                ` : `
                                    <form method="post" action="/compte/panier">
                                        <div class="d-flex justify-content-center">
                                            <div class="btn-group w-50" role="group" aria-label="Basic example">
                                                <button type="button" class="btn btn-dark" onclick="dec('amount-${p.id_produit}')">-</button>
                                                <input class="w-75 text-center text-bg-dark border border-0 user-select-none" name="amount-${p.id_produit}" type="number" value="0">
                                                <button type="button" class="btn btn-dark" onclick="inc('amount-${p.id_produit}')">+</button>
                                            </div>
                                        </div>
                                        <div>
                                            <input type="hidden" name="id" value="${p.id_produit}" class="visually-hidden">
                                        </div>
                                        <div class="d-flex justify-content-center p-1">
                                            <button type="submit" value="ajouter au panier" name="action" id="action" class="btn btn-dark">Ajoutez au panier</button>
                                        </div>
                                    </form>
                                `}
                                ` : `
                                <div class="d-flex justify-content-center text-center fw-bold">
                                    Pour commander ce produit vous devez être connecté
                                </div>
                                <div class="d-flex justify-content-between">
                                    <a class="btn btn-dark" href="/compte/connexion">Se connecter</a>
                                    <a class="btn btn-dark" href="/compte/inscription">S'inscrire</a>
                                </div>
                                `}
                            </div>
                        </div>
                    `;
                    productsContainer.appendChild(productDiv);
                });
            })
            .catch(error => console.error('Error fetching latest products:', error));
    }

    // Fetch products every 5 seconds
    setInterval(fetchLatestProducts, 5000);
    fetchLatestProducts();  // Initial fetch
});