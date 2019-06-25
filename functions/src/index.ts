import * as functions from 'firebase-functions';

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });


export const saveStockHistory = functions.database.ref('/stocks')
    .onWrite((change, context) => {
      // Grab the current value of what was written to the Realtime Database.
      const original = change;
      return ['Uppercasing', context, original];
      // const uppercase = original.toUpperCase();
      // You must return a Promise when performing asynchronous tasks inside a Functions such as
      // writing to the Firebase Realtime Database.
      // Setting an "uppercase" sibling in the Realtime Database returns a Promise.
      // return snapshot.ref.parent.child('uppercase').set(uppercase);
    });
