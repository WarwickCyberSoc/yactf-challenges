const Web3 = require("web3");

let web3 = new Web3("wss://ropsten.infura.io/ws/v3/63de5ca2f9ec4f1388a57a61f5309692");
web3.eth.defaultChain = "ropsten";

const mainAccount = web3.eth.accounts.privateKeyToAccount("0x39b270c88ba4831fa8fa5eb395f8d20305d28d048e3bfb7e966230e600f20c0a");
const destinationAccount = web3.eth.accounts.privateKeyToAccount("0x020d4b14a1a86b56950d6ddda52ee7f132b3729674d6ee0d0acb3d865d9923ff");

console.log(mainAccount);

web3.eth.defaultAccount = mainAccount.address;

console.log("Main Account", mainAccount);
console.log("Destination Account", destinationAccount);

console.log("Ransom 2 Account", web3.eth.accounts.create());
console.log("Ransom 2 Account Destination", web3.eth.accounts.create());

/*
Ransom 2 Account {
  address: '0x18D78efdBF3820B00Ec4E9F22A5BAE5D7Feba2Ae',
  privateKey: '0x260349f2e817faa065ffdfab6e99fefceff60b8fd0f6a37502663fadf8c6351c',
  signTransaction: [Function: signTransaction],
  sign: [Function: sign],
  encrypt: [Function: encrypt]
}
Ransom 2 Account Destination {
  address: '0x5503CCDAA5654c410AC097b2129c7574f1B85c7F',
  privateKey: '0x8d37678760be7bc79d0d18ed27d8b0d42ba60ff4a0d5b5a59c4529c46c47a476',
  signTransaction: [Function: signTransaction],
  sign: [Function: sign],
  encrypt: [Function: encrypt]
}
*/

/*
amateur neutral start shrimp about excite black dance remove pave ladder suit
*/

// (async () => {
//   // const transaction = await web3.eth.accounts.signTransaction(
//   //   {
//   //     to: destinationAccount.address,
//   //     data: web3.utils.toHex("hello world"),
//   //     gasLimit: "0x20000",
//   //     chain: "ropsten",
//   //     hardfork: "london",
//   //   },
//   //   mainAccount.privateKey
//   // );

//   console.log(await web3.eth.getBalance(mainAccount.address));

//   const Tx = require("@ethereumjs/tx").Transaction;

//   var rawTx = {
//     from: mainAccount.address,
//     nonce: (await web3.eth.getTransactionCount(mainAccount.address)) + 1,
//     gas: 266000,
//     gasPrice: "0x" + web3.utils.toWei("50", "gwei"),
//     to: destinationAccount.address,
//     value: "0x" + web3.utils.toWei("0.1", "ether"),
//     data: web3.utils.toHex("hello world"),
//     chainId: 0x3,
//   };

//   var tx = new Tx(rawTx, { chain: "ropsten" });
//   const signedTx = tx.sign(Buffer.from(mainAccount.privateKey.replace("0x", ""), "hex"));

//   var serializedTx = signedTx.serialize();

//   // console.log(serializedTx.toString('hex'));

//   web3.eth.sendSignedTransaction("0x" + serializedTx.toString("hex"), (err, hash) => {
//     if (err) console.error(err);

//     console.log(hash);
//   });
// })();
// // const fs = require("fs/promises");

// // (async () => {
// //   console.log(await web3.eth.getBalance(mainAccount.address));

// //   const ransom = (await fs.readFile("test.txt")).toString();

// //   // return;
// //   await web3.eth.sendTransaction({
// //     from: mainAccount.address,
// //     to: destinationAccount.address,
// //     value: 1,
// //     data: web3.utils.toHex(ransom),
// //     chainId: 3,
// //   });
// // })();
