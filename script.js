// JavaScript para controlar a exibição dos formulários
document.getElementById("cellPhoneButton").addEventListener("click", function() {
    document.getElementById("cellPhoneForm").style.display = "block";
    document.getElementById("emailForm").style.display = "none";
});

document.getElementById("emailButton").addEventListener("click", function() {
    document.getElementById("cellPhoneForm").style.display = "none";
    document.getElementById("emailForm").style.display = "block";
});

// Funções para lidar com o envio dos dados
function enviarCelular() {
    var celular = document.getElementById("cellPhoneInput").value;
}

function enviarEmail() {
    var email = document.getElementById("emailInput").value;
}



// JavaScript para controlar a exibição do formulário do WhatsApp
document.getElementById("whatsappButton").addEventListener("click", function() {
    document.getElementById("cellPhoneForm").style.display = "none";
    document.getElementById("emailForm").style.display = "none";
    document.getElementById("whatsappForm").style.display = "block";
});

// Função para lidar com o envio do número do WhatsApp
function enviarWhatsApp() {
    var whatsapp = document.getElementById("whatsappInput").value;
    // Faça algo com o número do WhatsApp, como enviar para o servidor
}
