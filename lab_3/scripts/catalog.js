async function loadCategory(category, containerId) 
{
const container = document.getElementById(containerId);
container.innerHTML = "Загрузка...";


try {
    const response = await fetch(`http://127.0.0.1:8000/products/category/${category}`);
    if (!response.ok) throw new Error(`Ошибка загрузки категории ${category}`);

    const products = await response.json();
    container.innerHTML = "";

    if (products.length === 0) {
        container.innerHTML = "<p>Товаров нет</p>";
        return;
    }

    products.forEach(item => {
        const div = document.createElement("div");
        div.className = "catalog-item";
        div.innerHTML = `
            <img src="${item.image}">
            <p><strong>${item.productname || ""}</strong></p>
            <p>${item.short_description || ""}</p>
            <a href="product.html?id=${item.productid}">Подробнее о товаре</a>
        `;
        container.appendChild(div);
    });
} catch (err) {
    container.innerHTML = `<p>Не удалось загрузить категорию ${category}</p>`;
    console.error(err);
}


}

loadCategory("hall", "category-hall");
loadCategory("sofa", "category-sofa");
loadCategory("wardrobe", "category-wardrobe");
loadCategory("bed", "category-bed");
