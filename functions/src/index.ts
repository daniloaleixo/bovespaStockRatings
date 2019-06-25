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



  const conn: Mysql.Connection = Mysql.createConnection({
    host: process.env.DB_ENDPOINT,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DATABASE_NAME,
  });


  query(conn, "show tables", {}).then((res) => console.log(res));


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

saveStockHistory(change);