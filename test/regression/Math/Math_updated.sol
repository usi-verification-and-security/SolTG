
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


    function ceilDiv(uint256 a, uint256 b) public pure returns (uint256) {
        return a / b + (a % b == 0 ? 0 : 1);
    }
}
