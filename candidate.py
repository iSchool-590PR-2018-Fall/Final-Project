import scipy.stats
import numpy
import math


def candidate(candidate_num, candidate_base_score):
	success_count = [0 for x in range(candidate_num)]  # for each stop time, how many times the user gets the best candidate

	for simulation_index in range(10000):  # do monte carlo simulation 10000 times
		candidate_final_scores = [0 for x in range(candidate_num)]  # initialize the final score for each candidate to zero
		best_score = 0  # keep track of the best final score among all the candidates
		best_index = 0  # keep track of the index of best final score among all the candidates

		# get the best final score among all the candidates
		for index in range(candidate_num):
			impression_score = scipy.stats.norm.rvs(loc=20, scale=5)  # the impression score obeys normal distribution
			final_score = candidate_base_score[index] + impression_score
			candidate_final_scores[index] = final_score
			if final_score > best_score:
				best_index = index
				best_score = final_score
		
		for stop_time in range(candidate_num):  # iterate each stop time
			current_best_index = 0 
			current_best_score = 0
			# get best final score among candidates from index 0 to "stop time"
			# this represent the best candidate the user ever seen before he stops
			for index in range(stop_time + 1):
				if candidate_final_scores[index] > current_best_score:
					current_best_index = index
					current_best_score = candidate_final_scores[index]

			if current_best_index == best_index: # the user meets the best candidate in the given stop time
				time_period = stop_time - current_best_index
				failure_prob = 0.05 + 0.05 * stop_time + 0.05 * math.exp(time_period) / math.exp(candidate_num)  # the probablity of the user failing to get the best candidate
				success_prob = 1 - failure_prob
				uni = numpy.random.uniform(low=0.0, high=1.0, size=None)  # uniformly generate a number within [0, 1]
				if uni < success_prob:  # the user gets the best candidate successfully
					success_count[stop_time] += 1  # increment success counter for that stop time

	for stop_time in range(candidate_num):  # for each stop time
		prob = success_count[stop_time] / 10000  # calculate the success probablity
		print("probability for stop time " + str(stop_time) + ": " + str(prob))


candidate_base_score = [10, 9, 10, 8, 10, 9, 9, 9, 10, 8, 8, 10, 8, 10, 9]
candidate(15, candidate_base_score)