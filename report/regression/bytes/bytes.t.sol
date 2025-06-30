//Generated Test by TG
//[[['Con', 'contract', 51, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender'], ['average', 23, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender', 'uint256', 'a', 'uint256', 'b'], ['Caverage', 50, 'state_type', 'state', 'uint', 'msg.value', 'address', 'msg.sender', 'uint256', 'a', 'uint256', 'b']]]
import "forge-std/Test.sol";
import "../regression/bytes.sol";

contract bytes_Test is Test {
	Con con0;
	Con con1;
	function setUp() public {
		con0 = new Con();
		con1 = new Con();
	}
	function test_bytes_0() public {
		vm.prank(0x25dcA4422c721484500000000000000000000000);
		con0.Caverage( 0, 0); //Caverage__50("address(this).balance=38", 0, 0, 0, 0)
	}
	function test_bytes_1() public {
		vm.prank(0x1695112f107848E9b00000000000000000000000);
		con1.average( 0, 0); //average__23("address(this).balance=38", 0, 0, 0, 0)
	}
}
