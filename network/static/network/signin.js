document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".inp").forEach(input => {
        input.addEventListener('input', () => {
            if ((document.querySelector('.usrnm').value.length === 0) || (document.querySelector('.pswd').value.length === 0)) {
                document.querySelector('input[type="submit"]').disabled = true;
            }
            else {
                document.querySelector('input[type="submit"]').disabled = false;
            }
        });
    });
})


//Em resumo, esse código verifica se os campos de nome de usuário e senha estão preenchidos e habilita/desabilita o botão de envio do formulário de acordo.