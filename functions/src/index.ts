import { Change } from 'firebase-functions';
import { DataSnapshot } from 'firebase-functions/lib/providers/database';
import * as Mysql from 'mysql';

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

export const saveStockHistory = (change: Change<DataSnapshot>, context = null) => {
  // export const saveStockHistory = functions.database.ref('/stocks')
  //   .onWrite((change: Change<DataSnapshot>, context) => {

  const arrayStocksHistory = [];

  const val = change.after.val;


  	Object.keys(val).forEach((key) => {
      // console.log(snapshot.val()[key])
      var object = JSON.parse(val[key]);
      arrayStocksHistory.push(object)
      // console.log(object);
    })
  
    // Sort by date, the first one will be the newest
    arrayStocksHistory.sort((a,b) => {
      var date1: any = new Date(a.date);
      var date2 : any= new Date(b.date);
      return date2 - date1;
    })



  const conn: Mysql.Connection = Mysql.createConnection({
    host: process.env.DB_ENDPOINT,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DATABASE_NAME,
  });


  query(conn, "show tables", {}).then((res) => {
    console.log(res);

    conn.destroy();
  })
    .catch(err => conn.destroy());


  // Grab the current value of what was written to the Realtime Database.
  console.log('Payload:', change, "Context", context);
  return ['Uppercasing', context, change];
  // const uppercase = original.toUpperCase();
  // You must return a Promise when performing asynchronous tasks inside a Functions such as
  // writing to the Firebase Realtime Database.
  // Setting an "uppercase" sibling in the Realtime Database returns a Promise.
  // return snapshot.ref.parent.child('uppercase').set(uppercase);
  // });
};


async function query<T>(conn: Mysql.Connection, queryString: string, substituionValues: Object): Promise<T> {
  const queryOptions: Mysql.QueryOptions = transformIntoMySQLString(queryString, substituionValues);

  return new Promise<T>((resolve, reject) => {
    conn.query(
      queryOptions,
      (err: Mysql.MysqlError | null, results?: any, fields?: Mysql.FieldInfo[]) => {
        if (err) reject(err);
        else {
          console.info('Salvo objeto com sucesso no DB');
          resolve(results);
        }
      }
    );
  });
}

function transformIntoMySQLString(queryString: string, substituionValues: any): Mysql.QueryOptions {

  // Get all keys (they have a ':' in front of the name)
  const allKeys: string[] = queryString.split(' ')
    .filter((word: string) => word.indexOf(':') == 0);

  const allValuesInOrder: Array<string> = allKeys
    .map((key: string) => substituionValues[key]);

  // In case of error 
  if (allKeys.length != allValuesInOrder.length)
    throw (
      { 'queryString': queryString, subsValues: substituionValues }
    );


  // Overwrite the keys with '?'
  let MysqlQueryString: string = queryString;
  for (const key of allKeys) {
    MysqlQueryString = MysqlQueryString.replace(key, '?');
  }

  return {
    sql: MysqlQueryString,
    values: allValuesInOrder
  };
}


const change: any = null;
// {
//   before:
//     DataSnapshot: {
//       app:
//       FirebaseApp: {
//         firebaseInternals_: [],
//         services_: { },
//         isDeleted_: false,
//         name_: '__admin__',
//         options_: [],
//         INTERNAL: [] },
//   instance: 'https://bovespastockratings.firebaseio.com',
//   _path: '/stocks',
//   _data:
//     {
//       '-LiAHa0uatNefaIDZ250': ' {\n    "0": {\n        "GBIO33": {\n            "Cresc.5a": "0,00%",\n            "DY": "0,00%",\n            "Div.Brut/Pat.": "0,30",\n            "EBITDA": "23,44%",\n            "EV/EBIT": "0,00",\n            "Liq.2m.": "1.360.630,00",\n            "Liq.Corr.": "2,03",\n            "Mrg.Liq.": "7,73%",\n            "P/Ativ.Circ.Liq.": "0,00",\n            "P/Ativo": "0,000",\n            "P/Cap.Giro": "0,00",\n            "P/EBIT": "0,00",\n            "P/L": "0,00",\n            "P/VP": "0,00",\n            "PSR": "0,000",\n            "Pat.Liq": "729.236.000,00",\n            "ROE": "8,70%",\n            "ROIC": "19,69%",\n            "cotacao": "7,25"\n        }\n    },\n    "1": {\n        "STBP3": {\n            "Cresc.5a": "-2,25%",\n            "DY": "0,10%",\n            "Div.Brut/Pat.": "0,16",\n            "EBITDA": "5,32%",\n            "EV/EBIT": "58,74",\n            "Liq.2m.": "6.607.860,00",\n            "Liq.Corr.": "1,23",\n            "Mrg.Liq.": "-0,01%",\n            "P/Ativ.Circ.Liq.": "-2,58",\n            "P/Ativo": "1,024",\n            "P/Cap.Giro": "39,43",\n            "P/EBIT": "59,37",\n            "P/L": "-26.388,80",\n            "P/VP": "2,21",\n            "PSR": "3,161",\n            "Pat.Liq": "1.337.190.000,00",\n            "ROE": "-0,01%",\n            "ROIC": "1,93%",\n            "cotacao": "4,43"\n        }\n    }'
//     }
//   }
// }

saveStockHistory(change);