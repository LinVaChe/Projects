document.addEventListener("DOMContentLoaded", loadUserInfo);

async function loadUserInfo() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        document.getElementById("user-info").innerHTML =
            "Вы не авторизованы.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/users/me", {
            headers: { "token": token }
        });

        if (!response.ok) {
            document.getElementById("user-info").innerHTML =
                "Ошибка загрузки данных.";
            return;
        }

        const user = await response.json();

        document.getElementById("user-info").innerHTML = `
            <p><b>Имя:</b> ${user.username}</p>
            <p><b>Email:</b> ${user.email}</p>
            <p><b>Страна:</b> ${user.country}</p>
            <p><b>Пол:</b> ${user.sex}</p>
            <p><b>Предпочтения:</b> ${user.paytype}</p>
            <p><b>О себе:</b> ${user.infoabout}</p>
        `;

    } catch (error) {
        document.getElementById("user-info").innerHTML =
            "Ошибка соединения с сервером.";
    }
}

document.addEventListener("click", (e) => {
    if (e.target.id === "sendReview") {
        const text = document.getElementById("reviewText").value.trim();
        if (!text) { alert("Введите текст отзыва!"); return; }
        console.log("Отзыв:", text);
        alert("Спасибо за отзыв!");
    }
});
