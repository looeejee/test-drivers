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