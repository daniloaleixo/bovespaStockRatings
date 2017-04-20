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
	arrayObjects = []
	Object.keys(data).forEach(function(key){
		arrayObjects.push(data[key])
	})


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
	console.log(arrayObjects[arrayObjects.length - 1])

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