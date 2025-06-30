// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// regression/bytes.sol

// OpenZeppelin Contracts (last updated v5.0.0) (token/ERC721/ERC721.sol)

contract Con{
    function average(uint256 a, uint256 b) public pure returns (uint256) {
        // (a + b) / 2 can overflow.
        return (a & b) + (a ^ b) / 2;
    }

    function Caverage(uint256 a, uint256 b) public pure returns (uint256) {
        assert(a < b || a >= b);
        // (a + b) / 2 can overflow.
        return (a+b) / 2;
    }
}
