async function chamarApi(metodo, url, corpo) {
  const opcoes = {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
  };
  if (corpo !== undefined) {
    opcoes.body = JSON.stringify(corpo);
  }
  const resposta = await fetch(url, opcoes);
  let json = {};
  try {
    json = await resposta.json();
  } catch (erro) {
    json = {};
  }
  if (resposta.status === 401 && !url.startsWith("/auth/login")) {
    window.location.href = "/app/login";
  }
  return { ok: resposta.ok, status: resposta.status, json: json };
}

function mostrarMensagem(texto, deuErro) {
  const elemento = document.getElementById("mensagem");
  elemento.textContent = texto;
  elemento.className = deuErro ? "erro" : "ok";
}

function mostrarResultado(resultado) {
  if (resultado.ok) {
    mostrarMensagem(resultado.json.mensagem || "Operação realizada", false);
  } else {
    mostrarMensagem(resultado.json.erro || "Erro inesperado", true);
  }
}

function montarTabela(idTabela, cabecalhos, linhas) {
  const tabela = document.getElementById(idTabela);
  tabela.replaceChildren();
  const cabecalho = tabela.insertRow();
  cabecalhos.forEach(function (titulo) {
    const celula = document.createElement("th");
    celula.textContent = titulo;
    cabecalho.appendChild(celula);
  });
  linhas.forEach(function (celulas) {
    const linha = tabela.insertRow();
    celulas.forEach(function (conteudo) {
      const celula = linha.insertCell();
      if (conteudo instanceof Node) {
        celula.appendChild(conteudo);
      } else {
        celula.textContent = conteudo === null ? "" : conteudo;
      }
    });
  });
}

function criarBotao(texto, aoClicar) {
  const botao = document.createElement("button");
  botao.type = "button";
  botao.textContent = texto;
  botao.addEventListener("click", aoClicar);
  return botao;
}

async function sair() {
  await chamarApi("POST", "/auth/logout");
  window.location.href = "/app/login";
}
