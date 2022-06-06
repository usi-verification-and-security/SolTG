// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/Loop_1.sol";

contract ContractTest_Loop_1 is Test {
    Loop_1 l1;

    function setUp() public {
        l1 = new Loop_1();
    }
    function test_loop_1() public {
        //simple call
        l1.f(10);
        assertTrue(true);
    }

    function test_loop_2() public {
        //check results
        uint z = l1.f(1);
        assertTrue(z > 0);
    }

    function test_loop_3() public {
        //check results
        l1.example_from_article(10, 10);
        assertTrue(true);
    }
}
