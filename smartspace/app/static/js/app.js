document.querySelectorAll("form[data-confirmar]").forEach(function (formulario) {
  formulario.addEventListener("submit", function (evento) {
    if (!window.confirm(formulario.dataset.confirmar)) {
      evento.preventDefault();
    }
  });
});

document.addEventListener("submit", function (evento) {
  if (evento.defaultPrevented || ["get", "dialog"].includes(evento.target.method)) {
    return;
  }
  evento.target.querySelectorAll("button[type='submit']").forEach(function (botao) {
    botao.disabled = true;
  });
});

window.addEventListener("pageshow", function (evento) {
  if (evento.persisted) {
    document.querySelectorAll("button[type='submit']").forEach(function (botao) {
      botao.disabled = false;
    });
  }
});

const formularioData = document.getElementById("form-data");
if (formularioData) {
  formularioData.querySelector("input[name='data']").addEventListener("change", function () {
    formularioData.submit();
  });
}

document.querySelectorAll("[data-alternar-senha]").forEach(function (botao) {
  botao.addEventListener("click", function () {
    const campo = botao.parentElement.querySelector("input");
    const mostrando = campo.type === "text";
    campo.type = mostrando ? "password" : "text";
    botao.textContent = mostrando ? "Mostrar" : "Ocultar";
  });
});

function fecharAviso(aviso) {
  aviso.classList.add("saindo");
  window.setTimeout(function () {
    aviso.remove();
  }, 400);
}

document.querySelectorAll("[data-fechar-aviso]").forEach(function (botao) {
  botao.addEventListener("click", function () {
    fecharAviso(botao.closest(".flash"));
  });
});

document.querySelectorAll(".flash[data-some-sozinho]").forEach(function (aviso) {
  window.setTimeout(function () {
    if (aviso.isConnected) {
      fecharAviso(aviso);
    }
  }, 6000);
});

document.querySelectorAll("dialog[data-abrir-ao-carregar]").forEach(function (janela) {
  if (typeof janela.showModal === "function") {
    janela.showModal();
  }
});
