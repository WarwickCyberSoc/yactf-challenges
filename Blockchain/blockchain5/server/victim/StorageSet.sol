// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract StorageSet {
    address private owner;
    mapping(bytes4 => address) public implementers;
    mapping(uint32 => bytes32) private data;

    function set(uint32 _index, bytes32 _data) public {
        data[_index] = _data;
    }
}
