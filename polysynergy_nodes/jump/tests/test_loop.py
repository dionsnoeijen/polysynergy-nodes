import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from polysynergy_nodes.jump.loop import Loop
from polysynergy_nodes.jump.loop_end import LoopEnd


class AsyncDummyFlow:
    def __init__(self):
        self.executed_nodes = []

    async def execute_node(self, node):
        self.executed_nodes.append(node)

    def get_node(self, node_id):
        return None

    def get_driving_connections(self, node_id):
        return []


class TestLoopNode(unittest.TestCase):

    def setUp(self):
        self.loop = Loop()
        self.loop_end = LoopEnd()
        self.flow = AsyncDummyFlow()
        self.loop.flow = self.flow

    def test_basic_loop_execution(self):
        """Test basic loop execution with 3 repeats"""
        self.loop_end.make_blocking = MagicMock()
        self.loop_end.unblock = MagicMock()
        
        self.loop.find_nodes_in_loop = MagicMock(return_value=([], self.loop_end))
        self.loop.resurrect = MagicMock()
        
        self.loop.repeats = 3
        
        async def run_test():
            await self.loop.execute()
            
        asyncio.run(run_test())

        # Should execute 3 times + loop end
        self.assertEqual(len(self.flow.executed_nodes), 4)  # 3 loop + 1 end
        self.assertEqual(self.loop.counter, 3)
        self.assertEqual(self.loop.true_path, 3)
        self.loop_end.make_blocking.assert_called_once()
        self.loop_end.unblock.assert_called_once()

    def test_loop_without_loop_end(self):
        """Test loop execution without loop end node"""
        self.loop.find_nodes_in_loop = MagicMock(return_value=([], None))
        self.loop.resurrect = MagicMock()
        
        self.loop.repeats = 2
        
        async def run_test():
            await self.loop.execute()
            
        asyncio.run(run_test())

        # Should execute 2 times (no loop end)
        self.assertEqual(len(self.flow.executed_nodes), 2)
        self.assertEqual(self.loop.counter, 2)
        self.assertEqual(self.loop.true_path, 2)

    def test_loop_break_functionality(self):
        """Test breaking out of loop early"""
        self.loop_end.make_blocking = MagicMock()
        self.loop_end.unblock = MagicMock()
        
        self.loop.find_nodes_in_loop = MagicMock(return_value=([], self.loop_end))
        self.loop.resurrect = MagicMock()
        
        self.loop.repeats = 5
        
        async def break_on_third_iteration():
            execution_count = 0
            original_execute = self.flow.execute_node
            
            async def mock_execute_node(node):
                nonlocal execution_count
                if node == self.loop:
                    execution_count += 1
                    if execution_count == 3:  # Break on 3rd iteration
                        self.loop.break_loop()
                return await original_execute(node)
            
            self.flow.execute_node = mock_execute_node
            await self.loop.execute()
            
        asyncio.run(break_on_third_iteration())

        # Should stop at iteration 3 + loop end
        self.assertEqual(self.loop.counter, 3)
        self.loop_end.unblock.assert_called_once()

    def test_loop_continue_functionality(self):
        """Test continue functionality in loop"""
        self.loop_end.make_blocking = MagicMock()
        self.loop_end.unblock = MagicMock()
        
        self.loop.find_nodes_in_loop = MagicMock(return_value=([], self.loop_end))
        self.loop.resurrect = MagicMock()
        
        self.loop.repeats = 3
        
        async def continue_on_second_iteration():
            execution_count = 0
            original_execute = self.flow.execute_node
            
            async def mock_execute_node(node):
                nonlocal execution_count
                if node == self.loop:
                    execution_count += 1
                    if execution_count == 2:  # Continue on 2nd iteration
                        self.loop.continue_loop()
                return await original_execute(node)
            
            self.flow.execute_node = mock_execute_node
            await self.loop.execute()
            
        asyncio.run(continue_on_second_iteration())

        # Should complete all 3 iterations + loop end
        self.assertEqual(self.loop.counter, 3)
        self.assertEqual(len(self.flow.executed_nodes), 4)  # 3 loop + 1 end

    def test_zero_repeats_error(self):
        """Test that zero repeats raises an error"""
        self.loop.repeats = 0
        
        async def run_test():
            with self.assertRaises(ValueError) as context:
                await self.loop.execute()
            self.assertIn("must be greater than 0", str(context.exception))
            
        asyncio.run(run_test())

    def test_negative_repeats_error(self):
        """Test that negative repeats raises an error"""
        self.loop.repeats = -1
        
        async def run_test():
            with self.assertRaises(ValueError) as context:
                await self.loop.execute()
            self.assertIn("must be greater than 0", str(context.exception))
            
        asyncio.run(run_test())

    def test_single_repeat(self):
        """Test loop with single repeat (default)"""
        self.loop.find_nodes_in_loop = MagicMock(return_value=([], None))
        self.loop.resurrect = MagicMock()
        
        # Default repeats = 1
        
        async def run_test():
            await self.loop.execute()
            
        asyncio.run(run_test())

        self.assertEqual(len(self.flow.executed_nodes), 1)
        self.assertEqual(self.loop.counter, 1)
        self.assertEqual(self.loop.true_path, 1)

    def test_node_resurrection(self):
        """Test that nodes in loop are properly resurrected"""
        mock_node_in_loop = MagicMock()
        mock_node_in_loop.resurrect = MagicMock()
        
        self.loop.find_nodes_in_loop = MagicMock(return_value=([mock_node_in_loop], None))
        self.loop.resurrect = MagicMock()
        
        self.loop.repeats = 2
        
        async def run_test():
            await self.loop.execute()
            
        asyncio.run(run_test())

        # Should resurrect nodes twice (once per iteration)
        self.assertEqual(mock_node_in_loop.resurrect.call_count, 2)
        self.assertEqual(self.loop.resurrect.call_count, 2)


if __name__ == "__main__":
    unittest.main()