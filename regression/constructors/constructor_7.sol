contract A {
	uint public x;
	constructor() { x = 0; }
    function test() public virtual returns (uint) {
		if (x < 1){
			x = x + 1;
		}else{
			x = x + 2;
		}
		return x;
	}
}

contract B is A {
    A a;
	constructor() A() {
//        a = new A();
//        a.test();
	}

	function f() public returns (uint) {
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
