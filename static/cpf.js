function formatarCpf(input) {
    var v = input.value.replace(/\D/g, "").slice(0, 11);
    var out = "";
    if (v.length > 0) { out = v.substring(0, 3); }
    if (v.length >= 4) { out += "." + v.substring(3, 6); }
    if (v.length >= 7) { out += "." + v.substring(6, 9); }
    if (v.length >= 10) { out += "-" + v.substring(9, 11); }
    input.value = out;

    // Validacao visual: vermelho quando CPF estiver completo e invalido.
    if (v.length === 0) {
        input.style.borderColor = "";
    } else if (v.length === 11 && !cpfValido(v)) {
        input.style.borderColor = "#e74c3c";
    } else {
        input.style.borderColor = "";
    }
}

function cpfValido(cpf) {
    if (!cpf || cpf.length !== 11) {
        return false;
    }
    if (/^(\d)\1{10}$/.test(cpf)) {
        return false;
    }

    var i;
    var soma = 0;
    for (i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i), 10) * (10 - i);
    }
    var digito = (soma * 10) % 11;
    if (digito === 10) {
        digito = 0;
    }
    if (digito !== parseInt(cpf.charAt(9), 10)) {
        return false;
    }

    soma = 0;
    for (i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i), 10) * (11 - i);
    }
    digito = (soma * 10) % 11;
    if (digito === 10) {
        digito = 0;
    }
    return digito === parseInt(cpf.charAt(10), 10);
}
