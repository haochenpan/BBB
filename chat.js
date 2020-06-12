// geth attach ~/BBB/hosts/ethData1/geth.ipc
// geth attach ~/BBB/hosts/ethData2/geth.ipc

function checkAllBalances() {
    var i = 0;
    eth.accounts.forEach(function (e) {
        console.log("  eth.accounts[" + i + "]: " + e + " \tbalance: " + web3.fromWei(eth.getBalance(e), "ether") + " ether");
        i++;
    })
}

checkAllBalances();
web3.personal.unlockAccount(web3.personal.listAccounts[0], "1019");
web3.personal.unlockAccount(web3.personal.listAccounts[1], "1019");
var tx_hash1 = eth.sendTransaction({
    from: eth.accounts[0],
    to: eth.accounts[1],
    value: web3.toWei(1, 'wei'),
    data: web3.toHex('0 send to 1111')
});
console.log(tx_hash1);
checkAllBalances();
var tx_hash2 = eth.sendTransaction({
    from: eth.accounts[1],
    to: eth.accounts[0],
    value: web3.toWei(1, 'wei'),
    data: web3.toHex('1 send to 0000')
});
console.log(var tx_hash2 = eth.sendTransaction({
);

checkAllBalances();
web3.toAscii(eth.getTransaction(tx_hash1).input);
web3.toAscii(eth.getTransaction("0x395940f9ddfa0d7c72ac8b92bac3c7a1c482cd9c53e59f07bee7000a4b4b0d16").input);
web3.toAscii(eth.getTransaction(tx_hash2).input);
// setTimeout(function () {
//     checkAllBalances();
//     web3.toAscii(eth.getTransaction(tx_hash1).input);
//     web3.toAscii(eth.getTransaction(tx_hash2).input);
// }, 5000);


// geth --exec 'loadScript("/root/BBB/chat.js")' attach ~/BBB/hosts/ethData1/geth.ipc