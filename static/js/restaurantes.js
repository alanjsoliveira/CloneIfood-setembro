fetch('static/js/restaurantes.json')
    .then(response => {
        return response.json();
    })
    .then(dados => {
        var nomes = dados.map(d => d.Nome)

        $("#nav_pesquisa").autocomplete({
            source: nomes,
            select: function(event, ui) {
                if(ui.item.value === "Mc Donalds") {
                    window.location.href = '/mcdonalds';
                } else if(ui.item.value === "KFC") {
                    window.location.href = '/kfc';
                } else if(ui.item.value === "Burger King") {
                    window.location.href = '/burguerking';
                }
            },
            response: function(event, ui) {
                console.log('Resposta do autocomplete recebida');
                ui.content.length = 0;

                for (let i = 0; i < nomes.length; i++) {
                    ui.content.push({
                        label: nomes[i],
                        value: nomes[i]
                    });
                }

                console.log('Opções de autocomplete atualizadas');
                $(this).autocomplete('instance')._suggest(ui.content);
            }
        });
    })
    .catch(error => {
        console.error('Erro:', error);
    });
