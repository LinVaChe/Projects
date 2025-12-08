document.getElementById("send-review").addEventListener("click", async () => {
    const text = document.getElementById("review-text").value.trim();

    if (!text) {
        alert("Введите текст отзыва");
        return;
    }

    const token = localStorage.getItem("access_token");

    const response = await fetch("http://127.0.0.1:8000/api/reviews/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ text })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail);
        return;
    }

    document.getElementById("review-status").innerText = "Отзыв отправлен!";
});
