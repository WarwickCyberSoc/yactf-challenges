// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract Blockchain4 {
    address private owner;

    event Win();

    constructor() {
        owner = msg.sender;
    }

    modifier isOwner() {
        require(uint16(uint160(msg.sender)) == uint16(uint160(owner)), "Only the owner can call this function.");
        _;
    }

    function win() public isOwner {
        emit Win();
    }
}
