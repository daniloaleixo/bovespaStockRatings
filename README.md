# Bovespa Stock Ratings


## Sobre 
O projeto consiste na primeira fonte de informaçôes open-source sobre análise fundamentalista das ações da Bovespa.
O objetivo é juntar informaçôes para tomadas de decisões.

## Estrutura do projeto

O projeto consiste de 3 projetos em repositórios separados:
* [Crawler](https://github.com/daniloaleixo/bovespaStockRatings): script em python que faz um scrapping em algumas páginas para colher as informações para salvar em um banco de dados Mongo.
* [Backend](https://github.com/daniloaleixo/fundamentalAnalysisHistoricalDataServer): Backend que faz a interface, usando GraphQL entre o banco e o front-end.
* [Front-end](https://github.com/daniloaleixo/fundamentalAnalysisHistoricalDataClient): Visualização de dados da aplicação feita, totalmente em Angular.



## Análise 
Estou fazendo uma análise baseada nos princípios fundamentalistas do livro [Investidor Inteligente](https://en.wikipedia.org/wiki/The_Intelligent_Investor) do Benjamin Graham:

* Tamanho Adequado 
  * Patrimônio Líquido maior que R$2bi
* Posição Financeira Forte
  * Liquidez Corrente maior que 1,5
  * Dívida Bruta / Patrimônio Líquido < 50%
* Histórico de Dividendos contínuos por, pelo menos, os últimos 20 anos.
  * Ainda não consegui pegar essa informação, estou colocando só o último DY
  * Ultimo DY maior que 2.5%
* Estabilidade nos Ganhos, Nenhum prejuízo nos últimos 10 anos.
  * Ainda não consegui verificar se teve algum prejuízo
* Crescimento nos Ganhos: 10 anos de crescimento nos lucros-por-ação de, pelo menos,
um terço.
  * Ainda não consegui colocar essa informação, mas tenho só 
  * Crescimento no últimos 5 anos maior que 5%
  * ROE > 20%
* Preço sobre Valor de Mercado: O preço da ação inferior a 1,5 x o valor dos ativos
líquidos.
  * P/VPA < 1.5
* P/L Moderado: O preço da ação inferior a 15x o lucro dos últimos 3 anos
  * P/L < 15
* Teste alternativo: Graham multiplicava o P/L pelo preço sobre o valor de mercado e
verifica se o resultado está abaixo de 22.5
  * P/L x P/VPA < 22.5

## Credits
The project was inicially a contribution to this repostory: https://github.com/phoemur/fundamentus
