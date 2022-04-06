// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.7.6;

abstract contract BankAccount {
    function isAuthorised(address _sender) public virtual returns (bool);
}

contract Bank {
    address private owner;
    mapping(address => uint64) private balances;

    constructor() {
        owner = msg.sender;
    }

    modifier isOwner() {
        require(msg.sender == owner, "Caller is not owner.");
        _;
    }

    function getBalance(address _account) public view returns (uint64) {
        return (balances[_account]);
    }

    function setBalance(address _account, uint64 _amount) public isOwner {
        balances[_account] = _amount;
    }

    function transfer(address _from, address _to, uint64 _amount) public {
        require(balances[_from] >= _amount, "Not enough balance.");
        require(BankAccount(_from).isAuthorised(msg.sender), "Sender not authorised.");

        balances[_from] -= _amount;
        balances[_to] += _amount;
    }
}
