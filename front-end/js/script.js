const container = document.getElementById("salas-container");
const contador = document.getElementById("contador-salas");

const totalSalas =
document.getElementById("total-salas");

const salasLivres =
document.getElementById("salas-livres");

const elementoSalasOcupadas =
document.getElementById("salas-ocupadas");

const ultimaAtualizacao =
document.getElementById("ultima-atualizacao");

const listaHistorico =
document.getElementById("lista-historico");

async function carregarHistorico() {

    try {

        const resposta = await fetch(
            "http://localhost:5000/api/historico"
        );

        const historico =
            await resposta.json();

        listaHistorico.innerHTML = "";

        if (historico.length === 0) {

            listaHistorico.innerHTML =
                "<li>Nenhum evento registrado.</li>";

            return;
        }

        historico.forEach(evento => {

            const item =
                document.createElement("li");

            item.textContent = evento;

            listaHistorico.appendChild(item);
        });

    } catch(error) {

        console.error(
            "Erro ao carregar histórico:",
            error
        );
    }
}

async function carregarSalas() {

try {

    const resposta = await fetch(
        "http://localhost:5000/api/salas"
    );

    const salas = await resposta.json();

    container.innerHTML = "";

    let quantidadeDisponiveis = 0;
    let quantidadeOcupadas = 0;

    Object.entries(salas).forEach(
        ([id, sala]) => {

            if (sala.ocupada) {
                quantidadeOcupadas++;
            } else {
                quantidadeDisponiveis++;
            }

            const card = document.createElement("div");

            card.className = sala.ocupada
                ? "card ocupada-card"
                : "card disponivel-card";

            card.innerHTML = `
                <h2>${sala.nome}</h2>

                <p class="status ${
                    sala.ocupada
                    ? "ocupada"
                    : "disponivel"
                }">

                    ${
                        sala.ocupada
                        ? "🔴 Ocupada"
                        : "🟢 Disponível"
                    }

                </p>

                <p class="info">
                    👥 Lugares: ${sala.lugares}
                </p>

                <p class="info">
                    📺 TV: ${sala.tem_tv ? "Sim" : "Não"}
                </p>

                <p class="info ${
                    sala.luz
                    ? "luz-on"
                    : "luz-off"
                }">
                    💡 Luz:
                    ${sala.luz ? "Ligada" : "Desligada"}
                </p>
                
                <p class="info">
                    ⏳ ${
                        calcularTempoOcupacao(
                            sala.tempo_ocupacao
                        )
                    }
                </p>

                <p class="info">
                    ⏰ Última atualização:
                    ${sala.ultima_atualizacao}
                </p>

                <div class="botoes">

                    <button onclick="ocuparSala('${id}')">
                        Ocupar
                    </button>

                    <button onclick="liberarSala('${id}')">
                        Liberar
                    </button>

                </div>

            `;

            container.appendChild(card);
        }
    );

    contador.textContent =
        quantidadeDisponiveis;

    totalSalas.textContent =
        quantidadeDisponiveis + quantidadeOcupadas;

    salasLivres.textContent =
        quantidadeDisponiveis;

    elementoSalasOcupadas.textContent =
        quantidadeOcupadas;

    ultimaAtualizacao.textContent =
        "Última atualização: " +
        new Date().toLocaleTimeString();

} catch (error) {

    console.error(error);

    container.innerHTML =
        "<h2>Erro ao conectar com a API</h2>";
}

}

carregarSalas();
carregarHistorico();

setInterval(() => {
    carregarSalas();
    carregarHistorico();
}, 2000);

async function ocuparSala(id) {

    try {

        await fetch(
            `http://localhost:5000/api/ocupar/${id}`,
            {
                method: "POST"
            }
        );

        carregarSalas();

    } catch(error) {

        console.error(error);
    }
}

async function liberarSala(id) {

    try {

        await fetch(
            `http://localhost:5000/api/liberar/${id}`,
            {
                method: "POST"
            }
        );

        carregarSalas();

    } catch(error) {

        console.error(error);
    }
}

function calcularTempoOcupacao(
    tempoInicio
) {

    if (!tempoInicio) {

        return "Sala disponível";
    }

    const inicio =
        new Date(tempoInicio);

    const agora =
        new Date();

    const diferenca =
        Math.floor(
            (agora - inicio) / 1000
        );

    const minutos =
        Math.floor(
            diferenca / 60
        );

    const segundos =
        diferenca % 60;

    return `Ocupada há ${minutos} min ${segundos} s`;
}