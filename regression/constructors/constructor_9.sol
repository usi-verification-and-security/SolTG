contract A {
   uint public x;
   constructor() { x = 0; }
   function inc() public returns (uint) {
      x = 1;
      return x;
   }
}

contract B {
   A a;
   constructor(){
     a = new A();
   }

   function f() public {
     uint y = a.inc();
     assert(y == 1);
   }

}