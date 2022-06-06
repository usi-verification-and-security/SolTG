// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
contract C
{
	uint a;
	function f(uint x) public {
		uint y;
		a = (y = x);
	}
	function g() public {
		f(42);
		assert(a > 1);
	}
}

contract ContractTest_1 is Test {
    function setUp() public {}
    function test1() public {
        C c1 = new C();
        c1.g();
    }
}
