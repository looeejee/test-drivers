var neo4j = require('neo4j-driver');

(async () => {
  // URI examples: 'neo4j://localhost', 'neo4j+s://xxx.databases.neo4j.io'
  const URL = process.env.NEO4J_URL;
  const USER = process.env.NEO4J_USERNAME;
  const PASSWORD = process.env.NEO4J_PASSWORD;
  let driver

  try {
    driver = neo4j.driver(URL, neo4j.auth.basic(USER, PASSWORD))
    const serverInfo = await driver.getServerInfo()
    console.log('Connection established')
    console.log(serverInfo)
  } catch(err) {
    console.log(`Connection error\n${err}\nCause: ${err.cause}`)
  }
})();

// Get the name of all 42 year-olds
const { records, summary, keys } = await driver.executeQuery(
    'MATCH (p:Person {age: $age}) RETURN p.name AS name',
    { age: 42 },
    { database: 'neo4j' }
  )
  
  // Summary information
  console.log(
    `>> The query ${summary.query.text} ` +
    `returned ${records.length} records ` +
    `in ${summary.resultAvailableAfter} ms.`
  )
  
  // Loop through results and do something with them
  console.log('>> Results')
  for(record of records) {
    console.log(record.get('name'))
  }