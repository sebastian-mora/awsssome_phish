const { STS } = require('aws-sdk');
const sts = new STS();

module.exports.getAccountId = async () => {
  // Checking AWS user details
  const { Account } = await sts.getCallerIdentity().promise();
  return Account;
};