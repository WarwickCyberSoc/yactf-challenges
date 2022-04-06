// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract AbstractStorage {
    address private owner;
    mapping(bytes4 => address) public implementers;
    mapping(uint32 => bytes32) private data;

    constructor() {
        owner = msg.sender;
    }

    modifier isOwner() {
        require(msg.sender == owner, "Caller is not owner.");
        _;
    }

    // Is the given address a contract?
    function isContract(address _address) private view returns (bool) {
        uint32 size;
        assembly {
            size := extcodesize(_address)
        }
        return (size > 0);
    }

    // Sets _contract as the implementer for the function with _hash.
    function setImplementer(bytes4 _hash, address _contract) public isOwner {
        require(isContract(_contract), "Users can't implement a function.");
        
        implementers[_hash] = _contract;
    }

    // Allows a user to register interest in implementing the function with _hash.
    function registerInterest(bytes4 _hash) public {
        require(!isContract(msg.sender), "Contracts can't register interest.");
        require(implementers[_hash] == address(0), "This function is already implemented.");

        implementers[_hash] = msg.sender;
    }

    // Calls the contract implementing the function with hash.
    fallback () external {
        bytes4 hash = bytes4(msg.data[0:4]);

        address implementer = implementers[hash];

        require(implementer != address(0), "This function is not implemented.");
        require(isContract(implementer), "This function is not yet implemented.");

        assembly {
            let tmp := mload(0x40)
            calldatacopy(tmp, 0, calldatasize())
            let result := delegatecall(gas(), implementer, tmp, calldatasize(), 0, 0)
            returndatacopy(tmp, 0, returndatasize())
            switch result
            case 0 { revert(tmp, returndatasize()) }
            case 1 { return(tmp, returndatasize()) }
        }
    }
}
