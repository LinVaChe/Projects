function getProductId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function loadProduct() {
    const id = getProductId();
    const response = await fetch(`http://127.0.0.1:8000/products/${id}`);
    const data = await response.json();

    document.getElementById("product-name").textContent = data.product.productname;
    document.getElementById("product-image").src = data.product.image;
    document.getElementById("product-description").textContent = data.product.description;
    document.getElementById("product-price").textContent = "Цена: " +data.product.price + " ₽";


    const props = document.getElementById("product-properties");
    props.innerHTML = "";

    data.properties.forEach(p => {
        props.innerHTML += `<li><b>${p.property_name}:</b> ${p.property_value}</li>`;
    });

    document.getElementById("add-to-cart-btn").addEventListener("click", () => {
    alert("Функция пока не реализована");
    });

}

loadProduct();
