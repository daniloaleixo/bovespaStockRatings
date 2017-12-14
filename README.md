# Bovespa Stock Ratings
Uma plataforma para analisar dados fundamentalistas das ações da BOVESPA utilizando um crawler em python e um database em firebase.
Acesso: https://daniloaleixo.github.io/bovespaStockRatings/index.html


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

## Instalação
```bash
sudo pip install requests==1.1.0
sudo pip3 install python-firebase
sudo pip3 install lxml
```

## Créditos

O projeto foi inicialmente uma contribuição para o repositório https://github.com/phoemur/fundamentus
