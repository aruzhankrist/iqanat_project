document.addEventListener("DOMContentLoaded", () => {

  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  const loginTab = document.getElementById("loginTab");
  const registerTab = document.getElementById("registerTab");

  // LOGIN
  loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const res = await login(email, password);

    if (res.token) {
      localStorage.setItem("token", res.token);
      showSection("home");
    } else {
      alert("Ошибка входа");
    }
  });

  // REGISTER
  registerForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    const res = await register(username, email, password);

    console.log("REGISTER:", res);

    if (res.success) {
      showSection("home");
      alert("Успешная регистрация");
    } else {
      alert(res.message || "Ошибка регистрации");
    }
  });

  // TAB SWITCH
  loginTab?.addEventListener("click", () => {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
  });

  registerTab?.addEventListener("click", () => {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
  });

});
