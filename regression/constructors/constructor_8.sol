contract A {
	uint public x;
	constructor() { x = 1; }
    function get() public returns (uint) {
		return x;
	}
    function set(uint _x) public{
		x = _x;
	}
}

contract B {
    A a;
    uint y;
	constructor(){
        a = new A();
        a.set(2);
	}

	function f() public {
        uint tmp = a.get();
        y = 0;
		if(tmp > 2){
			y = y + 10;
		}else{y = y +1;}
		assert(y > 0);
	}

}
