document.addEventListener("DOMContentLoaded", loadReviews);

async function loadReviews() {
    const box = document.getElementById("reviews-box");

    const response = await fetch("http://127.0.0.1:8000/api/reviews/random");
    const reviews = await response.json();

    if (reviews.length === 0) {
        box.innerHTML = "<p>Пока нет отзывов</p>";
        return;
    }

    box.innerHTML = reviews
        .map(r => `
            <div class="review">
                <b>${r.username}</b><br>
                <p>${r.text}</p>
            </div>
        `)
        .join("");
}
