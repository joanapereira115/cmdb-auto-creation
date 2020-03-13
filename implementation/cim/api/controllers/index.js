const CIM = module.exports

const pgp = require('pg-promise')();

var cn = 'postgresql://localhost/cim_operating_systems';

const db = pgp(cn);

async function execQuery(query, type) {
    try {
        const response = await db.any(query)
        return response
    }
    catch (e) {
        return ('ERRO em \'' + query + '\': ' + erro + '\n')
    }
}

/*********** DATACENTERS ***********/

/*********** NETWORK ***********/

/*********** COMPUTE ***********/

/*********** STORAGE ***********/

/*********** OPERATING SYSTEMS ***********/

/* Return all instances of 'filesystem' */
CIM.filesystem = async () => {
    const query = 'SELECT * FROM filesystem'
    var res = await execQuery(query, 'SELECT')
    return res
}

/* Return all instances of 'operatingsystem' */
CIM.operatingsystem = async () => {
    const query = 'SELECT * FROM operatingsystem'
    var res = await execQuery(query, 'SELECT')
    return res
}

/* Return all instances of 'computersystem' */
CIM.computersystem = async () => {
    const query = 'SELECT * FROM computersystem'
    var res = await execQuery(query, 'SELECT')
    return res
}

/*********** END USER DEVICES ***********/