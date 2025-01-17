import unittest
from ..StrategyBridge import StrategyBridge

class StrategyBridgeTestCase(unittest.TestCase):
  def test_initialize(self):
    sample_prism_model = f'/Users/bo40/workspace/python/mc_exp_sample.prism'
    sample_prism_adv = f'/Users/bo40/workspace/python/adv_sample.tra'
    sb = StrategyBridge(sample_prism_adv, sample_prism_model)

    self.assertEqual(sb.initial_state, 0)
    self.assertEqual(sb.observation_map[0], "____start")
    self.assertEqual(sb.observation_map[5], 'c1_heads__c2_tails__eight')
    self.assertEqual(sb.observation_map[10], 'c1_tails__c2_heads__eight')
    self.assertEqual(sb.observation_map[15], 'agree__c1_tails__c2_tails__six')
    self.assertEqual(sb.observation_map[20], 'agree__c1_tails__c2_tails__seven')
    self.assertEqual(sb.strategy[0], "go2")
    self.assertEqual(sb.strategy[4], "go2")
    self.assertEqual(sb.strategy[12], "go2")
    self.assertEqual(sb.strategy[16], "go2")
    self.assertEqual(sb.strategy[20], "go2")
    self.assertEqual(sb.strategy[25], "go1")
    self.assertEqual(sb.next_state[(0, 'go2', 'agree__c1_tails__c2_tails__six')], {42: 1.0})


  def test_next(self):
    sample_prism_model = f'/Users/bo40/workspace/python/mc_exp_sample.prism'
    sample_prism_adv = f'/Users/bo40/workspace/python/adv_sample.tra'
    sb = StrategyBridge(sample_prism_adv, sample_prism_model)

    self.assertEqual(sb.next_action(), "go2")
    sb.update_state("go2", 'agree__c1_tails__c2_tails__six')
    self.assertEqual(sb.current_state[42], 1.0)
    self.assertEqual(sb.next_action(), "go2")
    sb.update_state("go2", 'agree__c1_tails__c2_tails__five')
    self.assertEqual(sb.current_state[47], 1.0)
    # self.assertEqual(sb.history, [("go2", 'agree__c1_tails__c2_tails__six'), ("go2", 'agree__c1_tails__c2_tails__five')])

  def test_reset(self):
    sample_prism_model = f'/Users/bo40/workspace/python/mc_exp_sample.prism'
    sample_prism_adv = f'/Users/bo40/workspace/python/adv_sample.tra'
    sb = StrategyBridge(sample_prism_adv, sample_prism_model)

    sb.update_state("go2", 'agree__c1_tails__c2_tails__six')
    self.assertEqual(sb.current_state[42], 1.0)
    # self.assertEqual(sb.history, [("go2", 'agree__c1_tails__c2_tails__six')])

    sb.reset()

    self.assertEqual(sb.current_state[42], 0)
    # self.assertEqual(sb.history, [])

  def test_update_state_false(self):
    sample_prism_model = f'/Users/bo40/workspace/python/mc_exp_sample.prism'
    sample_prism_adv = f'/Users/bo40/workspace/python/adv_sample.tra'
    sb = StrategyBridge(sample_prism_adv, sample_prism_model)

    # TODO : implement this test
    self.assertEqual(sb.next_action(), "go2")
    sb.update_state("go2", 'agree__c1_tails__c2_tails__six')
    self.assertEqual(sb.current_state[42], 1.0)
    self.assertEqual(sb.next_action(), "go2")
    sb.update_state("go2", 'agree__c1_tails__c2_tails__five')
    self.assertEqual(sb.current_state[47], 1.0)
    # self.assertEqual(sb.history, [("go2", 'agree__c1_tails__c2_tails__six'), ("go2", 'agree__c1_tails__c2_tails__five')])


if __name__ == '__main__':
    unittest.main()