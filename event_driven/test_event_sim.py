import unittest
import event_sim

#Test every method in event_sim file for validity
class TestCalc(unittest.TestCase):
	maxInterArrivalTime = 1164063200;
	minInterArrivalTime = 1163030800;

	#Determines if FEL is populated at the start of the simulation
	def test_getHistoricalEvents(self):
		FEL = {}
		self.assertEqual({}, FEL)
		FEL = event_sim.getHistoricalEvents();
		self.assertNotEqual({}, FEL)  #Populated Initial event list

	#Checks if the inter arrival time that is generated is reasonable based on the trajectory data
	def test_getInterArrivalTime(self):
		minInterArrivalTime = 1163030800;
		maxInterArrivalTime = 1164063200;

		x = 0;
		while x < 10000:
			self.assertGreater(event_sim.getInterArrivalTime(), minInterArrivalTime)
			self.assertLessEqual(event_sim.getInterArrivalTime(), maxInterArrivalTime)
			x = x + 1

	#Checks if the inter arrival time that is generated is reasonable based on the trajectory data
	def test_rightTurnChance(self):
		rightTurnChance = event_sim.getRightTurnChance()
		self.assertGreater(rightTurnChance, 0)
		self.assertLessEqual(rightTurnChance, 1)

	#Checks if turn was set to 1, which is a left turn, or 2 which is a right turn, or a zero which means no turn
	def test_ninthSegment(self):
		event = (1, ['TenthIntersection', .5, .5, .1, 0])
		result = event_sim.ninthSegment(event)
		self.assertGreater(result, -1)
		self.assertLess(result, 3)

	#Checks if time delayed at an intersection is a reasonable positive number
	def test_tenthIntersection(self):
		event = (1, ['TenthIntersection', .5, .5, .1, 0])
		result = event_sim.tenthIntersection(event)
		self.assertGreater(result, -1)
		self.assertIsInstance(result, int)

	#Checks if turn was set to 2 which is a right turn, or a zero which means no turn
	def test_tenthSegment(self):
		event = (1, ['EleventhIntersection', .5, .5, .1, 0])
		result = event_sim.tenthSegment(event)
		self.assertGreater(result, -1)
		self.assertLess(result, 3)

	#Checks if time delayed at an intersection is a reasonable positive number
	def test_eleventhIntersection(self):
		event = (1, ['TenthIntersection', .5, .5, .1, 0])
		result = event_sim.eleventhIntersection(event)
		self.assertGreater(result, -1)
		self.assertIsInstance(result, int)


	#Checks if turn was set to 2 which is a right turn, or a zero which means no turn
	def test_eleventhSegment(self):
		event = (1, ['TwelfthIntersection', .5, .5, .1, 0])
		result = event_sim.eleventhSegment(event)
		self.assertGreater(result, -1)
		self.assertLess(result, 3)

	#Checks if time delayed at an intersection is a reasonable positive number
	def test_twelfthIntersection(self):
		event = (1, ['TwelfthIntersection', .5, .5, .1, 0])
		result = event_sim.twelfthIntersection(event)
		self.assertGreater(result, -1)
		self.assertIsInstance(result, int)

	#Checks if turn was set to 2 which is a right turn, or a zero which means no turn
	def test_twelfthSegment(self):
		event = (1, ['TwelfthIntersection', .5, .5, .1, 0])
		result = event_sim.twelfthSegment(event)
		self.assertGreater(result, -1)
		self.assertLess(result, 3)

	#Checks if time delayed at an intersection is a reasonable positive number
	def test_fourteenthIntersection(self):
		event = (1, ['FourteenthIntersection', .5, .5, .1, 0])
		result = event_sim.fourteenthIntersection(event)
		self.assertGreater(result, -1)
		self.assertIsInstance(result, int)

	#Checks if we get a left (1), right (2), or straight(0) turn returned
	def test_checkLeftRightTurn(self):
		event = (1, ['FourteenthIntersection', .5, .5, .1, 0])
		result = event_sim.checkLeftRightTurn(event)
		self.assertGreater(result, -1)
		self.assertLess(result, 3)

	#Checks if next light scheduled is the opposite of the current light
	def test_switchTenthLights(self):
		event = (1, ['NorthSignals10', 'red'])
		result = event_sim.switchTenthLights(event)
		self.assertEqual(result, 'green')
		event = (1, ['NorthSignals10', 'green'])
		result = event_sim.switchTenthLights(event)
		self.assertEqual(result, 'red')

	#Checks if next light scheduled is the opposite of the current light
	def test_switchTenthLeftLights(self):
		event = (1, ['NorthSignals10', 'red'])
		result = event_sim.switchTenthLeftLights(event)
		self.assertEqual(result, 'green')
		event = (1, ['NorthSignals10', 'green'])
		result = event_sim.switchTenthLeftLights(event)
		self.assertEqual(result, 'red')

	#Checks if next light scheduled is the opposite of the current light
	def test_switchEleventhLights(self):
		event = (1, ['NorthSignals10', 'red'])
		result = event_sim.switchEleventhLights(event)
		self.assertEqual(result, 'green')
		event = (1, ['NorthSignals10', 'green'])
		result = event_sim.switchEleventhLights(event)
		self.assertEqual(result, 'red')

	#Checks if next light scheduled is the opposite of the current light
	def test_switchFourteenthLights(self):
		event = (1, ['NorthSignals10', 'red'])
		result = event_sim.switchFourteenthLights(event)
		self.assertEqual(result, 'green')
		event = (1, ['NorthSignals10', 'green'])
		result = event_sim.switchFourteenthLights(event)
		self.assertEqual(result, 'red')

	#Checks if next light scheduled is the opposite of the current light
	def test_switchFourteenthLeftLights(self):
		event = (1, ['NorthSignals10', 'red'])
		result = event_sim.switchFourteenthLights(event)
		self.assertEqual(result, 'green')
		event = (1, ['NorthSignals10', 'green'])
		result = event_sim.switchFourteenthLights(event)
		self.assertEqual(result, 'red')

if __name__ == '__main__':
	unittest.main()