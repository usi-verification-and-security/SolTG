contract A {
	uint public x;
	constructor(uint) {}

	function f() internal returns (uint) {
		x = x + 1;
		return x;
	}
}

contract C is A {
	constructor() A(f()) {
		assert(x == 1);
	}
    function test(uint a) public returns (uint) {
		x = x + 1;
        if(x > 1){
            x = a;
        }
        if(x > 5){
            x = x + 10;
        }
        if(x > 1000){
            x = 2000;
        }
		return x;
	}
}