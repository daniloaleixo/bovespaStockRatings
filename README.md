# Bovespa Stock Ratings

Projeto de análise de dados fundamentalistas da Bovespa

**If you like this project you can support me.**  
<a href="https://www.buymeacoffee.com/daniloaleixo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-white.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>


## Sobre 
O projeto consiste na primeira fonte de informaçôes open-source sobre análise fundamentalista das ações da Bovespa.
O objetivo é juntar informaçôes para tomadas de decisões.

## Estrutura do projeto

O projeto consiste de 4 projetos em repositórios separados:
* [Crawler](https://github.com/daniloaleixo/bovespaStockRatings): script em python que faz um scrapping em algumas páginas para colher as informações para salvar em um banco de dados Mongo.
* [Backend](https://github.com/daniloaleixo/fundamentalAnalysisHistoricalDataServer): Backend que faz a interface, usando GraphQL entre o banco e o front-end.
* [Front-end](https://github.com/daniloaleixo/fundamentalAnalysisHistoricalDataClient): Visualização de dados da aplicação feita, totalmente em Angular.
* [Agente de trading](https://github.com/daniloaleixo/NeuroEvolutionMarketTrader): Agente usando neuro evolução para comprar e vender ações automaticamente


## Configurando o projeto

  
Clonar o repositório principal
```
git clone --recursive git@github.com:daniloaleixo/bovespaStockRatings.git
```

[Opcional] Se quiser clonar o subrepositórios
```
git submodule update --init --recursive
```
  
## Rodando o crawler

### Rodando da imagem docker oficial
```
docker run -e MONGO_URI=$MONGO_URI daniloaleixo/bovespa-stock-ratings-crawler
```
### Fazendo o build da imagem docker
```
docker build -t bovespa_stock_ratings .
docker run -e MONGO_URI=$MONGO_URI -t bovespa_stock_ratings
```



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
