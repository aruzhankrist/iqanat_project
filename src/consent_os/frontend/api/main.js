import {
  login,
  getAgreements,
  register
} from "./api.js";

/* =========================
   DOM INIT
========================= */
document.addEventListener("DOMContentLoaded", () => {

  /* =========================
     NAV / SECTIONS
  ========================= */

  // Переключение экранов (SPA логика)
  window.showSection = function (id) {
    document.querySelectorAll(".page-section")
      .forEach(s => s.classList.remove("active"));

    document.getElementById(id).classList.add("active");
  };

  /* =========================
     LOGIN FORM
  ========================= */

  const loginForm = document.getElementById("loginForm");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // ⚠️ ВАЖНО: ID должны совпадать с HTML
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    console.log("LOGIN DATA:", { email, password });

    const res = await login(email, password);

    console.log("LOGIN RESPONSE:", res);

    if (res.token) {
      localStorage.setItem("token", res.token);
      showSection("home");
    } else {
      alert("Ошибка входа");
    }
  });

  /* =========================
     REGISTER FORM
  ========================= */

  const registerForm = document.getElementById("registerForm");

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    console.log("REGISTER DATA:", { username, email, password });

    const res = await register(username, email, password);

    console.log("REGISTER RESPONSE:", res);

    if (res.success) {
      alert("Успешная регистрация");
      showSection("home");
    } else {
      alert("Ошибка регистрации");
    }
  });

  /* =========================
     LOAD CONTRACTS
  ========================= */

  window.loadContracts = async function () {
    const list = document.querySelector(".contract-list");

    const agreements = await getAgreements();

    console.log("AGREEMENTS:", agreements);

    if (!Array.isArray(agreements)) return;

    list.innerHTML = agreements.map(a => `
      <div class="contract-item">
        <div class="info">
          <h3>${a.title}</h3>
          <span>${a.created}</span>
        </div>
      </div>
    `).join("");
  };

  /* =========================
     TAB SWITCH (LOGIN / REGISTER)
  ========================= */

  const loginTab = document.getElementById("loginTab");
  const registerTab = document.getElementById("registerTab");

  loginTab.addEventListener("click", () => {
    loginForm.style.display = "block";
    registerForm.style.display = "none";

    loginTab.classList.add("active");
    registerTab.classList.remove("active");
  });

  registerTab.addEventListener("click", () => {
    loginForm.style.display = "none";
    registerForm.style.display = "block";

    registerTab.classList.add("active");
    loginTab.classList.remove("active");
  });

});
