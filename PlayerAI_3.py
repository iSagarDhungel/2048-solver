from BaseAI_3 import BaseAI
import time

MAX_TIME = 0.19

class PlayerAI(BaseAI):
	def __init__(self):
		self.direction = None

	def utilityValue(self, grid):
	    w = 4

	    # horizontal and vertical snake heuristic
	    sbh1 = grid.map[3][0] + grid.map[3][1] * w
	    sbh1 += grid.map[3][2] * pow(w,2) + grid.map[3][3] * pow(w,3)
	    sbh1 += grid.map[2][3] * pow(w,4) + grid.map[2][2] * pow(w,5) + grid.map[2][1] * pow(w,6)
	    sbh1 += grid.map[2][0] * pow(w,7) + grid.map[1][0] * pow(w,8) + grid.map[1][1] * pow(w,9)
	    sbh1 += grid.map[1][2] * pow(w,10) + grid.map[1][3] * pow(w,11) +grid.map[0][3] * pow(w,12)
	    sbh1 += grid.map[0][2] * pow(w,13) + grid.map[0][1] * pow(w,14) + grid.map[0][0] * pow(w,15)
	    

	    maxTile = grid.getMaxTile()
	    totalAvailableCells = len(grid.getAvailableCells())

	    util_value = maxTile + 7 * sbh1 + 3 * totalAvailableCells
	    return util_value


	def alphabeta_search(self, grid, alpha, beta, depth, maxTurn):
		# print("alpha: %s, beta: %s, depth:%s, maxTurn:%s, direction:%s" %(alpha, beta, depth, maxTurn, direction))
		global initial_time
		running_Time = time.clock() - initial_time
		#print(running_Time)

		if((running_Time >= MAX_TIME) or (depth >=4)):
			return self.utilityValue(grid), None

		if (maxTurn == True):
			maxUtility, max_direction =  -float("inf"), None
			available_moves = grid.getAvailableMoves()

			for m in available_moves:
				new_grid = grid.clone()
				new_grid.move(m)

				utility, _ = self.alphabeta_search(new_grid, alpha, beta, depth+1, False)

				if(utility > maxUtility):
					max_direction = m
					maxUtility = utility	

				if (maxUtility>=beta):
					break

				alpha = max(maxUtility, alpha)

			return maxUtility, max_direction

		else:
			minUtility, min_direction = float("inf"), None
			cells = grid.getAvailableCells()

			for cell in cells:
				for tile in [2,4]:
					new_grid = grid.clone()
					new_grid.setCellValue(cell, tile)
					utility, _ = self.alphabeta_search(new_grid, alpha, beta, depth+1, True)

					if(utility < minUtility):
						min_direction = (cell, tile)
						minUtility = utility

					if(minUtility <= alpha):
						break

					beta = min(beta, minUtility)

			return minUtility, min_direction


	def getMove(self, grid):
		global initial_time
		initial_time = time.clock()


		maxUtility = -float("inf")
		available_moves = grid.getAvailableMoves()

		if(len(available_moves) == 0):
			return None
		max_direction = available_moves[0]

		utility, direction = self.alphabeta_search(grid, -float("inf"), float("inf"), 1, True)
		
		if(utility > maxUtility):
			maxUtility = utility
			max_direction = direction
			
		if(max_direction == None):
			max_direction = available_moves[0]

		return max_direction
