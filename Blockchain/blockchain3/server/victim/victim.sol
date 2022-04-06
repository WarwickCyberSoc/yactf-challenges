// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.9;

contract Blockchain3 {
    mapping(address => uint64) private balances;
    
    event BalanceChange(address _account, uint64 _old, uint64 _new);

    constructor(uint64 _supply) {
        balances[msg.sender] = _supply;
    }

    function getBalance(address _account) public view returns (uint64) {
        return (balances[_account]);
    }
    
    // Transfers _amount from msg.sender to _to.
    function transfer(address _to, uint64 _amount) public {
        require(balances[msg.sender] >= _amount, "Not enough balance.");

        uint64 newFrom = balances[msg.sender] - _amount;
        uint64 newTo = balances[_to] + _amount;

        emit BalanceChange(msg.sender, balances[msg.sender], newFrom);
        emit BalanceChange(_to, balances[_to], newTo);

        balances[msg.sender] = newFrom;
        balances[_to] = newTo;
    }
}
