contract A {
	uint public x;
	constructor() { x = 1; }
    function f() public virtual returns (uint) {
		x = x + 1;
		return x;
	}
}

contract B is A {
	constructor() A() {
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
