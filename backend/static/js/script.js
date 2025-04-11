// backend/static/js/script.js

// Espera o DOM (estrutura da página HTML) ser completamente carregado antes de executar o código
document.addEventListener('DOMContentLoaded', () => {

  // Pega a referência para o formulário pelo ID
  const predictionForm = document.getElementById('prediction-form');
  // Pega a referência para a div onde os resultados serão exibidos
  const resultsDiv = document.getElementById('results');

  // Adiciona um 'ouvinte de evento' ao formulário que será acionado quando ele for submetido
  predictionForm.addEventListener('submit', async (event) => {
      // 1. Evitar o comportamento padrão do formulário de recarregar a página
      event.preventDefault();

      // Mostra uma mensagem de 'carregando' enquanto a previsão é feita
      resultsDiv.innerHTML = '<p>Calculando previsão...</p>';

      // 2. Coleta os dados dos campos do formulário
      const formData = new FormData(predictionForm); // Cria um objeto FormData a partir do formulário
      const data = {}; // Cria um objeto JavaScript vazio para armazenar os dados
      
      // Itera sobre os pares [name, value] do FormData e preenche o objeto 'data'
      // Ex: data['Q006'] = 'B', data['Q002'] = 'E', etc.
      formData.forEach((value, key) => {
          data[key] = value;
      });

      console.log('Dados a serem enviados:', data); // Mostra os dados no console do navegador (para depuração)

      // 3. Envia os dados para o backend (API Flask) usando a Fetch API
      try {
          // Faz uma requisição POST para a rota '/predict' do backend
          const response = await fetch('/predict', { // O URL é relativo à origem atual (onde o HTML foi servido)
              method: 'POST',                     // Método HTTP
              headers: {
                  'Content-Type': 'application/json' // Informa ao backend que estamos enviando JSON
              },
              body: JSON.stringify(data)          // Converte o objeto JavaScript 'data' para uma string JSON
          });

          // 4. Processa a resposta do backend
          if (response.ok) { // Verifica se a resposta HTTP foi bem-sucedida (status 2xx)
              const predictions = await response.json(); // Converte a resposta JSON do backend em um objeto JavaScript
              console.log('Previsões recebidas:', predictions); // Mostra no console

              // Formata e exibe os resultados na div 'results'
              resultsDiv.innerHTML = `
                  <h3>Notas Previstas:</h3>
                  <p>Matemática (MT): ${predictions.NU_NOTA_MT}</p>
                  <p>Ciências da Natureza (CN): ${predictions.NU_NOTA_CN}</p>
                  <p>Linguagens e Códigos (LC): ${predictions.NU_NOTA_LC}</p>
                  <p>Ciências Humanas (CH): ${predictions.NU_NOTA_CH}</p>
                  <p>Redação: ${predictions.NU_NOTA_REDACAO}</p>
              `;
          } else {
              // Se a resposta não foi 'ok' (ex: erro 400 ou 500)
              const errorData = await response.json(); // Tenta ler a mensagem de erro JSON enviada pelo Flask
              console.error('Erro do servidor:', errorData);
              // Exibe a mensagem de erro recebida do backend
              resultsDiv.innerHTML = `<p class="error">Erro na previsão: ${errorData.error || 'Ocorreu um erro desconhecido.'}</p>`;
          }
      } catch (error) {
          // Captura erros que podem ocorrer na comunicação com o backend (ex: rede offline, backend desligado)
          console.error('Erro na requisição fetch:', error);
          resultsDiv.innerHTML = `<p class="error">Erro ao conectar com o servidor de previsão. Verifique sua conexão ou tente mais tarde.</p>`;
      }
  });
});