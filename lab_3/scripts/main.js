const modalPath = "./modal.html";

fetch(modalPath)
    .then(r => r.text())
    .then(html => {
        document.getElementById("modal-container").innerHTML = html;
        initRegistrationForm();
    })
    .catch(e => console.error(e));


function initRegistrationForm() {
    const form = document.querySelector(".contact-form");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        const payload = {
            username: formData.get("name"),
            email: formData.get("email"),
            password: formData.get("password"),
            sex: formData.get("gender"),
            paytype: formData.getAll("interest").join(","),
            country: formData.get("country"),
            infoabout: formData.get("about")
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/api/users/register", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                alert("Ошибка регистрации!");
                return;
            }

            const data = await response.json();
            console.log("Успешно:", data);

            document.getElementById("toggleForm").checked = false;

            if (data.access_token) {
                localStorage.setItem("access_token", data.access_token);
            }

            applyUserLoggedInUI();
        } catch (error) {
            console.error("Ошибка:", error);
        }
    });
}




document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.querySelector("#login-btn");
    if (loginBtn) {
        loginBtn.addEventListener("click", loginUser);
    }

    if (localStorage.getItem("access_token")) {
        applyUserLoggedInUI();
    }
});

async function loginUser() {
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!email || !password) {
        alert("Введите логин и пароль");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/users/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Ошибка авторизации");
            return;
        }

        localStorage.setItem("access_token", data.access_token);

        applyUserLoggedInUI();

    } catch (err) {
        console.error(err);
        alert("Ошибка соединения с сервером");
    }
}


async function applyUserLoggedInUI() {
    const loginDiv = document.querySelector(".login");
    if (!loginDiv) return;

    const token = localStorage.getItem("access_token");
    if (!token) return;

    let userName = "Профиль";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/users/me", {
            headers: { "token": token }
        });

        if (response.ok) {
            const data = await response.json();
            userName = data.username || "Профиль";
        }
    } catch (e) {
        console.warn("Не удалось загрузить имя пользователя");
    }

    loginDiv.innerHTML = `
        <button id="accountButton">${userName}</button>
        <button id="logoutButton">Выйти</button>
    `;

    document.getElementById("logoutButton").addEventListener("click", logout);
    document.getElementById("accountButton").addEventListener("click", () => {
        window.location.href = "/static/pages/account.html";
    });
}




function logout() {
    localStorage.removeItem("access_token");

    const loginDiv = document.querySelector(".login");
    loginDiv.innerHTML = `
        логин: <input type="text" id="login-email"><br>
        пароль: <input type="password" id="login-password"><br>
        <label for="toggleForm" class="register_link">регистрация</label>
        <button id="login-btn">войти</button>
    `;

    document.querySelector("#login-btn").addEventListener("click", loginUser);

    if (window.location.pathname.endsWith("account.html")) {
        window.location.href = "index.html";
    }
}

