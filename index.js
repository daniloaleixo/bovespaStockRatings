const express = require('express')
const app = express()
const port = process.env.PORT || 3000

app.get('/', (request, response) => {
  response.send('Hello from Express!');
  console.log('Someone is here');
})

app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on ${port}`)
})