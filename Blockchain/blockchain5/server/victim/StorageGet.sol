// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract StorageGet {
    address private owner;
    mapping(bytes4 => address) public implementers;
    mapping(uint32 => bytes32) private data;

    function get(uint32 _index) public view returns (bytes32) {
        return data[_index];
    }
}
