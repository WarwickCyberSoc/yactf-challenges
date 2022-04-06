// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

abstract contract AbstractStorage {
    function registerInterest(bytes4 _hash) public virtual;
}

contract Solve {
    event Win();

    constructor (address _abstract_storage) {
        AbstractStorage(_abstract_storage).registerInterest(0x473ca96c);  // keccak256("win()")
    }

    function win() public {
        emit Win();
    }
}
