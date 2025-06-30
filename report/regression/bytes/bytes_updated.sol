


contract Con{
    function average(uint256 a, uint256 b) public pure returns (uint256) {
        return (a & b) + (a ^ b) / 2;
    }

    function Caverage(uint256 a, uint256 b) public pure returns (uint256) {
        assert(a < b || a >= b);
        return (a+b) / 2;
    }
}
