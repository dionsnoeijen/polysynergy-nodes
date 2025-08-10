import unittest
import asyncio
from unittest.mock import MagicMock
from polysynergy_nodes.jump.list_loop import ListLoop
from polysynergy_nodes.jump.loop_end import LoopEnd

class AsyncDummyFlow:
    def __init__(self):
        self.executed_nodes = []

    async def execute_node(self, node):
        self.executed_nodes.append(node)

    def get_node(self, node_id):
        return None  # wordt niet gebruikt in deze test

    def get_driving_connections(self, node_id):
        return []

class TestListLoopIntegration(unittest.TestCase):
    def test_basic_loop_integration(self):
        loop_node = ListLoop()
        loop_end_node = LoopEnd()

        # Mock de flow
        flow = AsyncDummyFlow()
        loop_node.flow = flow

        # Zorg dat loop_end_node geschikt is voor de test
        loop_end_node.make_blocking = MagicMock()
        loop_end_node.unblock = MagicMock()

        # Mock de find_nodes_in_loop zodat het echte object wordt teruggegeven
        loop_node.find_nodes_in_loop = MagicMock(return_value=([], loop_end_node))

        loop_node.input_list = ["one", "two", "three"]
        
        async def run_test():
            await loop_node.execute()
            
        asyncio.run(run_test())

        # ✅ Assertions
        self.assertEqual(loop_node.index, 2)
        self.assertEqual(loop_node.true_path, "three")
        loop_end_node.make_blocking.assert_called_once()
        loop_end_node.unblock.assert_called_once()
        self.assertEqual(flow.executed_nodes.count(loop_node), 3)
        self.assertIn(loop_end_node, flow.executed_nodes)

if __name__ == "__main__":
    unittest.main()