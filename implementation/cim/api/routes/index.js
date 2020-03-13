var express = require('express');
var router = express.Router();
var CIM = require('../controllers/index')

/*********** DATACENTERS ***********/

/*********** NETWORK ***********/

/*********** COMPUTE ***********/

/*********** STORAGE ***********/

/*********** OPERATING SYSTEMS ***********/

/* GET filesystem instances */
router.get('/filesystem', async function (req, res, next) {
  var data = await CIM.filesystem()
  res.jsonp(data)
});

/* GET operating system instances */
router.get('/operatingsystem', async function (req, res, next) {
  var data = await CIM.operatingsystem()
  res.jsonp(data)
});

/* GET computer system instances */
router.get('/computersystem', async function (req, res, next) {
  var data = await CIM.computersystem()
  res.jsonp(data)
});

/*********** END USER DEVICES ***********/

module.exports = router;
