//Generated Test by TG
//[[['Math', 'contract', 89, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender'], ['max', 32, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender', 'uint256', 'a', 'uint256', 'b'], ['min', 64, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender', 'uint256', 'a', 'uint256', 'b'], ['ceilDiv', 88, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender', 'uint256', 'a', 'uint256', 'b']]]
import "forge-std/Test.sol";
import "../src/Math.sol";

contract Math_Test is Test {
	Math math0;
	Math math1;
	Math math2;
	Math math3;
	Math math4;
	function setUp() public {
		math0 = new Math();
		math1 = new Math();
		math2 = new Math();
		math3 = new Math();
		math4 = new Math();
	}
	function test_Math_0() public {
		vm.prank(0x353eF8F27Dc6222b000000000000000000000000);
		math0.ceilDiv( 0, 0); //ceilDiv__88("address(this).balance=0", 0, 0, 0, 0)
		assertTrue(true);
	}
	function test_Math_1() public {
		vm.prank(0x1F1C8992D95AD3aed00000000000000000000000);
		math1.min( 0, 1); //min__64("address(this).balance=38", 0, 0, 0, 1)
		assertTrue(true);
	}
	function test_Math_2() public {
		vm.prank(0x4e8AEA9f81927803c00000000000000000000000);
		math2.min( 0, 0); //min__64("address(this).balance=38", 0, 0, 0, 0)
		assertTrue(true);
	}
	function test_Math_3() public {
		vm.prank(0xFbf4662A87c38F45000000000000000000000000);
		math3.max( 0, 0); //max__32("address(this).balance=38", 0, 0, 0, 0)
		assertTrue(true);
	}
	function test_Math_4() public {
		vm.prank(0x5475c083a1a54bdd700000000000000000000000);
		math4.max( 0, 1); //max__32("address(this).balance=38", 0, 0, 0, 1)
		assertTrue(true);
	}
}
