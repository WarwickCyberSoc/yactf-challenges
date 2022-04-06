// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract Blockchain2 {
    event Win();

    function win(int8 answer) public {
        if (answer == 42) {
            emit Win();
        }
    }
}
