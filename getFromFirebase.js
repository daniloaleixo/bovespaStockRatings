console.log('bla')

var database = firebase.database();

var arrayStocksHistory = [];

database.ref().child('stocks').once('value').then(function(snapshot){
	// console.log(snapshot.val())

	Object.keys(snapshot.val()).forEach(function(key){
		// console.log(snapshot.val()[key])
		var object = JSON.parse(snapshot.val()[key]);
		arrayStocksHistory.push(object)
		// console.log(object);
	})

	// Sort by date, the first one will be the newest
	arrayStocksHistory.sort(function(a,b){
		var date1 = new Date(a.date);
		var date2 = new Date(b.date);
		return date2 - date1;
	})

	// console.log(arrayStocksHistory);
	buildTable(arrayStocksHistory[0]);
	hideLoading();

}, function(error){
	console.log("deu erro");
})


var hideLoading = function(){
	$('#loading-whell').addClass("hidden");
	$('#info').removeClass("hidden");
}

var buildTable = function(data){

	// Put the objects in an array
	arrayObjects = [];
	Object.keys(data).forEach(function(key){
		arrayObjects.push(data[key])
	});

	arrayObjects = calculateScores(arrayObjects);


	// Sort elements by score
	arrayObjects.sort(function(a, b){
		var nota1 = 0, nota2 = 0;
		Object.keys(a).forEach(function(key){
			nota1 = a[key]["nota"]
		})
		Object.keys(b).forEach(function(key){
			nota2 = b[key]["nota"]
		})
		return nota2 - nota1;
	})

	var txt = "";
	for(var i = 0; i < arrayObjects.length; i++) {
		if(typeof(arrayObjects[i]) == "object"){

			Object.keys(arrayObjects[i]).forEach(function(stock){

				var greenLine = " class='green-line'";
				// If we see a stock with score below 7.5 we turnoff green
				if(parseFloat(arrayObjects[i][stock]["nota"]) < 7.5)
					greenLine = '';

				var stockLine = "<tr" + greenLine + ">" + 
								"<td class='stock'>" + stock + "</td>" + 
				            	"<td>" + arrayObjects[i][stock]["nota"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["cotacao"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Pat.Liq"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Liq.Corr."] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["ROE"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Div.Brut/Pat."] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Cresc.5a"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/VP"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/L"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["DY"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["PSR"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/Ativo"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/Cap.Giro"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/EBIT"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["P/Ativ.Circ.Liq."] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["EV/EBIT"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["EBITDA"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Mrg.Liq."] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["ROIC"] + "</td>" +
				            	"<td>" + arrayObjects[i][stock]["Liq.2m."] + "</td>" +
				        		"</tr>";

								txt += stockLine;
			})
		}
	}
	
	$("#resultado").append(txt)




}

var calculateScores = function(stockArray){
	for(var i = 0; i < stockArray.length; i++) {
		if(typeof(stockArray[i]) == "object"){
			Object.keys(stockArray[i]).forEach(function(stock){
				var nota = 0.0;

				var patrLiq = parseFloat(stockArray[i][stock]["Pat.Liq"].replace(/\./g, '').replace(/\,/g, '.'));
				if( patrLiq > 200000000)
				    nota = nota + 1
				var liqCorr = parseFloat(stockArray[i][stock]["Liq.Corr."].replace(/\./g, '').replace(/,/g, '.'));
				if( liqCorr > 1.)
				    nota = nota + 1
				var roe = parseFloat(stockArray[i][stock]["ROE"].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( roe > 20) 
				    nota = nota + 1
				var divPat = parseFloat(stockArray[i][stock]["Div.Brut/Pat."].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( divPat < 0.5 && divPat > 0) 
				    nota = nota + 1
				var cresc = parseFloat(stockArray[i][stock]["Cresc.5a"].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( cresc > 5) 
				    nota = nota + 1
				var pvp = parseFloat(stockArray[i][stock]["P/VP"].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( pvp < 2 && pvp > 0) 
				    nota = nota + 1
				var pl = parseFloat(stockArray[i][stock]["P/L"].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( pl < 15 && pl > 0) 
				    nota = nota + 1
				var dy = parseFloat(stockArray[i][stock]["DY"].replace(/\./g, '').replace(/\,/g, '.').replace(/%/g, ''));
				if( dy > 2.5) 
				    nota = nota + 1
				if(pl * pvp < 22.5)
					nota = nota + 1;

				stockArray[i][stock]["nota"] = (parseFloat(nota) / 9.0 * 10.0).toFixed(2);

				// console.log([stock, stockArray[i][stock]["nota"], patrLiq, liqCorr, roe, divPat, cresc, pvp, pl, dy])

			});
		}
	}

	return stockArray;
}