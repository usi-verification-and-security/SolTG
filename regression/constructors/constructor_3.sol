contract A {
	uint public x;
	constructor(uint a) { x = a; }
    function f() public virtual returns (uint) {
		x = x + 1;
		return x;
	}
}

contract B is A {
	constructor(uint b) A(b) {
	}

	function f() public override returns (uint) {
		if(x > 10){
			x = x + 10;
		}
		if(x > 2){
			x = x + 10;
		}
		x = x + 1;
		return x;
	}

	function g() public returns (uint) {
		x = 42;
		assert(x > 0);
		return x;
	}
}
