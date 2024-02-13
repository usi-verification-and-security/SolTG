// SPDX-License-Identifier: MIT

contract  Math {

    function max(uint256 a, uint256 b) public pure returns (uint256) {
        if(a >= b){
            assert(a>=b);
            return a;
        } else {
            assert(b>a);
            return b;
        }
    }

    function min(uint256 a, uint256 b) public pure returns (uint256) {
        if(a < b){
            assert(a<b);
            return a;
        } else {
            assert(b>a);
            return b;
        }
    }

//    /**
//     * @dev Returns the average of two numbers. The result is rounded towards
//     * zero.
//     */
//    function average(uint256 a, uint256 b) public pure returns (uint256) {
//
//        assert(((a & b) + (a ^ b) / 2)*2 == a+b);
//        // (a + b) / 2 can overflow.
//        return (a & b) + (a ^ b) / 2;
//    }

    function ceilDiv(uint256 a, uint256 b) public pure returns (uint256) {
        // (a + b - 1) / b can overflow on addition, so we distribute.
        return a / b + (a % b == 0 ? 0 : 1);
    }
}
