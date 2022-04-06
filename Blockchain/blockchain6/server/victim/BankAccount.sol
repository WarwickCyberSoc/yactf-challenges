// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.7.6;

contract BankAccount {
    mapping(address => bool) private authorised;

    constructor() {
        authorised[msg.sender] = true;
    }

    modifier isAuthorised_() {
        require(authorised[msg.sender], "Caller is not authorised.");
        _;
    }

    function authorise(address _sender) public isAuthorised_ {
        authorised[_sender] = true;
    }

    function deauthorise(address _sender) public isAuthorised_ {
        authorised[_sender] = false;
    }

    function isAuthorised(address _sender) public view returns (bool) {
        return (authorised[_sender]);
    }
}
