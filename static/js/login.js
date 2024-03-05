document.addEventListener('DOMContentLoaded', function () {
    const getUsuario = (event) => {
        return document.getElementById('email').value;
    }

    const redirectToHome = () => {
        window.location.href = '/';
    }

    const redirectToVerificationCode = () => {
        window.location.href = '/codigo_verificacao';
    }

    const validaUsuario = (event) => {
        event.preventDefault();
        const usuario = getUsuario(event);

        fetch('/cadastro_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: usuario
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na solicitação: ${response.status}`);
            }
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                throw new Error('Resposta do servidor não está no formato JSON');
            }
        })
        .then(data => {
            if (data.error === 'E-mail já cadastrado') {
                console.log('E-mail já cadastrado');
                redirectToHome(); 
            } else if (data.message === 'Cadastro realizado com sucesso') {
                console.log('Cadastro realizado com sucesso');
                redirectToVerificationCode(); 
            } else {
                
            }
        })
        .catch(error => {
            console.error(error);
        });
    }

    document.getElementById('registrationForm').addEventListener('submit', validaUsuario);
});
