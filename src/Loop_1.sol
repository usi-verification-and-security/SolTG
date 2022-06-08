// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract Loop_1 {

	function f(uint _x) public pure returns (uint) {
        require(_x < 100);
		do {
			_x = _x + 1;
		} while (_x < 10);
		assert(_x > 0);
		return _x;
	}
    

    function example_from_article(uint _y, uint _z) public pure returns (uint){
        uint _x = 0;
        uint _i = 0;
        while(true){
            if(_x >= 5){
                _y = _y + 1;
            }else{
                _x = _x + 1;
            }
            if (_y <= 5){
                _z = _z + 1;
            }else{
                if (_x > _y){
                    _y = _y + 1;
                }else{
                    _x = 0;
                }
            }
            if (_z == 0){
                return 2;
            }
            _i = _i + 1;
            if (_i > 100){return 0;}
        }
        assert(_x > 0);
        return 1;
	}
}
