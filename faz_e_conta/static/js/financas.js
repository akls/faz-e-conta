function syncAndConfirm() {
    document.getElementById('hidden_nome').value = document.getElementById('input_nome').value;
    document.getElementById('hidden_sala').value = document.getElementById('select_sala').value;
    document.getElementById('hidden_mes').value = document.getElementById('select_mes').value;
    document.getElementById('hidden_ano').value = document.getElementById('select_ano').value;

    const mes = document.getElementById('select_mes').value || "atual";
    const ano = document.getElementById('select_ano').value || "atual";

    return confirm(`Calcular mensalidades para o período ${mes}/${ano}?`);
}

setTimeout(function() {
    var msg = document.getElementById('message-container');
    if (msg) {
        msg.style.transition = "opacity 0.6s";
        msg.style.opacity = "0";
        setTimeout(function() { msg.style.display = "none"; }, 600);
    }
}, 5000);