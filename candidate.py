"""
IS 590PR - Programming for Analytics & Data Processing
Final Project- Finding Best Dating Match in optimal time
Authors:
Smriiti Singhal
Yue Sheng
Yazhuo Zhang
"""

import scipy.stats
import numpy as np
import math
import json
import operator
import random

class Candidates:

	def _init_(self, candidates_dic):
		self.candidates_dic = candidates_dic


	def calculate_person_score(self, candidates_list):
		"""
		This is used to determine whether a person in the candidate database is competitive or not
		We calculate the average matching score for each candidate, and get the whole average score.
		If a candidate' average matching score is greater than the whole average score, we mark him or her as 'competitive', otherwise not.
		If a candidate is competitive, then the probability of the candidate already been chosen increases, otherwise not.
		:param candidates_list: a list of candidates' personal information
		:return: a list of candidates' personal information with "is_competitive" attribute

		>>> test_candidates = Candidates()
		>>> candidates_list = [{"gender": "male", "first_name": "John", "last_name": "White", "age": 31, "city": "Boston", "nationality": "India", "personality": "extrovert", "expected_personality": "extrovert", "likes": "food, music"}, {"gender": "female", "first_name": "Helen", "last_name": "White", "age": 26, "city": "Seattle", "nationality": "US", "personality": "extrovert", "expected_personality": "extrovert", "likes": "partying, food"}]
		>>> test_candidates.calculate_person_score(candidates_list)
		[{'gender': 'male', 'first_name': 'John', 'last_name': 'White', 'age': 31, 'city': 'Boston', 'nationality': 'India', 'personality': 'extrovert', 'expected_personality': 'extrovert', 'likes': 'food, music', 'is_competitive': 1}, {'gender': 'female', 'first_name': 'Helen', 'last_name': 'White', 'age': 26, 'city': 'Seattle', 'nationality': 'US', 'personality': 'extrovert', 'expected_personality': 'extrovert', 'likes': 'partying, food', 'is_competitive': 1}]

		"""

		person_score = []
		for i in range(len(candidates_list)):
			score_sum = 0
			score_count = 0
			for j in range(len(candidates_list)):
				if i == j or candidates_list[i]['gender'].lower() == candidates_list[j]['gender'].lower():
					continue
				score_count += 1
				score_sum += self.get_base_score(candidates_list[i], candidates_list[j])
			person_score.append(score_sum / score_count)

		total_avg_score = sum(person_score) / len(person_score)

		for i in range(len(person_score)):
			if person_score[i] >= total_avg_score:
				candidates_list[i]['is_competitive'] = 1
			else:
				candidates_list[i]['is_competitive'] = 0

		return candidates_list


	def get_base_score(self, person_dic, candidate_dic):
		"""
		This is used to determine whether a person in the candidate database is competitive or not
		For a person in the candidate database, calculate the matching scores for another person in the database based on matching rules
		:param person_dic: Personal information of the person
		:param candidate_dic: Personal information of another person
		:return: The matching score for that person associated with another person

		>>> test_candidates = Candidates()
		>>> person_dic = {"gender": "male", "first_name": "John", "last_name": "White", "age": 31, "city": "Boston", "nationality": "India", "personality": "extrovert", "expected_personality": "extrovert", "likes": "food, music"}
		>>> candidate_dic = {"gender": "female", "first_name": "Helen", "last_name": "White", "age": 26, "city": "Seattle", "nationality": "US", "personality": "extrovert", "expected_personality": "extrovert", "likes": "partying, food"}
		>>> test_candidates.get_base_score(person_dic, candidate_dic)
		1

		"""

		matched_score = 0
		if person_dic['city'].lower() == candidate_dic['city'].lower():
			matched_score += 1

		if person_dic['expected_personality'].lower() == candidate_dic['personality'].lower():
			matched_score += 1

		if person_dic['nationality'].lower() == candidate_dic['nationality'].lower():
			matched_score += 1

		candidate_likes = candidate_dic['likes'].split(', ')
		for person_like in person_dic['likes']:
			for candidate_like in candidate_likes:
				if person_like == candidate_like:
					matched_score += 0.5

		return matched_score


class User:
	user_dic = {}

	def set_attributes(self, user_dic):
		"""
		Set user's personal information
		:return: None
		"""

		self.user_dic = user_dic

	def real_dating(self, candidate_num, top_candidates_list):
		"""
		Simulate the real dating scenario where the user meets the selected candidates one by one.
		Apply monte carlo simulation to get the optimal time to stop and make a decision to get the best candidate.
		Print the probability of getting the best candidate for each stop time, and finally print the optimal stop time.

		:param candidate_num: The number of candidates user selected to meet
		:param top_candidates_list: A list of selected candidates' personal information
		:return: None

		>>> np.random.seed(1)
		>>> test_user = User()
		>>> user_dic = {"gender": "male", "first_name": "John", "last_name": "White", "age": 31, "city": "Boston", "nationality": "India", "personality": "extrovert", "expected_personality": "extrovert", "likes": "food, music"}
		>>> test_user.set_attributes(user_dic)
		>>> top_candidates_list = [{"gender": "female", "first_name": "Rebecca", "last_name": "Griffin", "age": 24, "city": "Boston", "nationality": "Korea", "personality": "ambivert", "expected_personality": "ambivert", "likes": "movies, computer games, travelling, pets, music", "score": 1.5, "is_competitive": 0}, {"gender": "female", "first_name": "Elizabeth", "last_name": "Green", "age": 20, "city": "Champaign", "nationality": "Germany", "personality": "ambivert", "expected_personality": "ambivert", "likes": "art, movies, sports, partying", "score": 3, "is_competitive": 0}]
		>>> test_user.real_dating(2, top_candidates_list)
		probability for stop time 0: 0.13
		probability for stop time 1: 0.5863
		To find the best dating match, the optimal time recommended for you is: 1

		"""

		success_count = [0 for x in
						 range(candidate_num)]  # for each stop time, how many times the user gets the best candidate

		score_sum = 0
		for i in range(len(top_candidates_list)):
			score_sum += top_candidates_list[i]['score']
		score_avg = score_sum / len(top_candidates_list)

		candidate_base_score = []
		for i in range(candidate_num):
			candidate_base_score.append(top_candidates_list[i]['score'])

		# do monte carlo simulation 10000 times
		for simulation_index in range(10000):  
			candidate_final_scores = [0 for x in
									  range(candidate_num)]  # initialize the final score for each candidate to zero
			best_score = 0  # keep track of the best final score among all the candidates
			best_index = 0  # keep track of the index of best final score among all the candidates

			# get the best final score among all the candidates
			for index in range(candidate_num):
				impression_score = scipy.stats.norm.rvs(loc=score_avg, scale=1)  # the impression score obeys normal distribution
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

				if current_best_index == best_index:  # the user meets the best candidate in the given stop time

					# failure_prob = prob of user failing to get the best candidate even if he/she already met the candidate in the given stop time
	                # failure_prob= 'prob. the candidate refuses to meet the user before setting up the meeting -> constant value'
	                #                                                     +
	                #                 'prob of person chosen by someone else; if the candidate has other good matches also within the database- increases prob by 10% -> linear pattern'
	                #                                                     +
	                #                 'prob. of rejecting by best candidate because tired of waiting/loose interest-> exponential pattern'
					failure_prob = 0.05 + (0.5 + 0.1 * top_candidates_list[current_best_index]['is_competitive']) * stop_time / candidate_num + 0.3 * math.exp(stop_time) / math.exp(
						candidate_num)  # the probablity of the user failing to get the best candidate
					success_prob = 1 - failure_prob
					uni = np.random.uniform(low=0.0, high=1.0, size=None)  # uniformly generate a number within [0, 1]
					if uni < success_prob:  # the user gets the best candidate successfully
						success_count[stop_time] += 1  # increment success counter for that stop time

		best_stop_time = 0
		best_stop_prob = 0
		for stop_time in range(candidate_num):  # for each stop time
			prob = success_count[stop_time] / 10000  # calculate the success probablity
			if prob > best_stop_prob:
				best_stop_time = stop_time
				best_stop_prob = prob
			print("probability for stop time " + str(stop_time) + ": " + str(prob))

		print("To find the best dating match, the optimal time recommended for you is: {}".format(best_stop_time))


	def generate_candidates(self, user_dic, candidates_list, candidate_num):
		"""
		For a specific user, get the matching scores for all candidates in the candidate database based on matching rules
		Select top candidates with higher matching scores, and the number of candidates is user defined
		:param user_dic: Personal information of the user
		:param candidates_list: Personal information of all candidates
		:param candidate_num: The number of candidates the user wants to meet in real dating
		:return: A list of selected candidates' personal information

		>>> test_user = User()
		>>> user_dic = {"gender": "male", "first_name": "John", "last_name": "White", "age": 31, "city": "Boston", "nationality": "India", "personality": "extrovert", "expected_personality": "extrovert", "likes": "food, music", "preferences": ["city", "food", "personality"], "is_random_order": "no"}
		>>> candidates_list = [{"gender": "female", "first_name": "Rebecca", "last_name": "Griffin", "age": 24, "city": "Boston", "nationality": "Korea", "personality": "ambivert", "expected_personality": "ambivert", "likes": "movies, computer games, travelling, pets, music", "score": 1.5, "is_competitive": 0}, {"gender": "female", "first_name": "Elizabeth", "last_name": "Green", "age": 20, "city": "Champaign", "nationality": "Germany", "personality": "ambivert", "expected_personality": "ambivert", "likes": "art, movies, sports, partying", "score": 3, "is_competitive": 0}]
		>>> test_user.generate_candidates(user_dic, candidates_list, 1)
		[{'gender': 'female', 'first_name': 'Rebecca', 'last_name': 'Griffin', 'age': 24, 'city': 'Boston', 'nationality': 'Korea', 'personality': 'ambivert', 'expected_personality': 'ambivert', 'likes': 'movies, computer games, travelling, pets, music', 'score': 1.75, 'is_competitive': 0}]

		"""

		candidate_matched_scores = {}

		for i in range(len(candidates_list)):
			if user_dic['gender'].lower() == candidates_list[i]['gender'].lower():
				candidate_matched_scores[i] = 0
			else:
				candidate_matched_scores[i] = self.get_matched_score(user_dic, candidates_list[i])

		sorted_candidate_indexes = sorted(candidate_matched_scores.items(), key=operator.itemgetter(1), reverse=True)
		top_candidates_dic = {}
		for i in range(candidate_num):
			candidate_index = sorted_candidate_indexes[i][0]
			top_candidates_dic[i] = candidates_list[candidate_index]
			top_candidates_dic[i]['score'] = sorted_candidate_indexes[i][1]

		top_candidates_list = []
		if user_dic['is_random_order'].lower() == 'no':  # with ranking order
			for k, v in top_candidates_dic.items():
				top_candidates_list.append(v)
		else:  # with random order
			for k, v in sorted(top_candidates_dic.items(), key=lambda x: random.random()):
				top_candidates_list.append(v)


		return top_candidates_list


	def get_matched_score(self, user_dic, candidate_dic):
		"""
		For a specific user, calculate the matching scores for a candidate in the candidate database based on matching rules
		For example, if they live in the same city, then add 1 score to the matching score.
		If 'city' is one of the user's preferences, then add another 0.75 score to the matching score.
		:param user_dic: Personal information of the user
		:param candidate_dic: Personal information of the candidate
		:return: Matching score of the user and the candidate

		>>> test_user = User()
		>>> user_dic = {"gender": "male", "first_name": "John", "last_name": "White", "age": 31, "city": "Boston", "nationality": "India", "personality": "extrovert", "expected_personality": "extrovert", "likes": "food, music", "preferences": ["city", "food", "personality"], "is_random_order": "no"}
		>>> candidate_dic = {"gender": "female", "first_name": "Rebecca", "last_name": "Griffin", "age": 24, "city": "Boston", "nationality": "Korea", "personality": "ambivert", "expected_personality": "ambivert", "likes": "movies, computer games, travelling, pets, music", "score": 1.5, "is_competitive": 0}
		>>> test_user.get_matched_score(user_dic, candidate_dic)
		1.75
		"""

		matched_score = 0
		if user_dic['city'].lower() == candidate_dic['city'].lower():
			matched_score += 1
			if 'city' in user_dic['preferences']:
				matched_score += 0.75

		if user_dic['expected_personality'].lower() == candidate_dic['personality'].lower():
			matched_score += 1
			if 'personality' in user_dic['preferences']:
				matched_score += 0.75

		if user_dic['nationality'].lower() == candidate_dic['nationality'].lower():
			matched_score += 1
			if 'nationality' in user_dic['preferences']:
				matched_score += 0.75

		candidate_likes = candidate_dic['likes'].split(', ')
		for user_like in user_dic['likes']:
			for candidate_like in candidate_likes:
				if user_like == candidate_like:
					matched_score += 0.5
					if user_like in user_dic['preferences']:
						matched_score += 0.375

		return matched_score


	def print_top_candidates(self, top_candidates_list):
		print("{:<8} {:<8} {:<15} {:<10} {:<10} {:<10} {:<10} {:<20} {:<15} {:<20}".format('No.', 'Score', 'isCompetitive',
																						   'First_Name', 'Last_Name',
																						   'Gender', 'Age', 'City',
																						   'Nationality', 'Personality',
																						   'likes'))
		for i in range(len(top_candidates_list)):
			v = top_candidates_list[i]
			is_competitive = 'Yes'
			if v['is_competitive'] == 0:
				is_competitive = 'No'
			print(
				"{:<8} {:<8} {:<15} {:<10} {:<10} {:<10} {:<10} {:<20} {:<15} {:<20}".format(i, v['score'], is_competitive,
																							 v['first_name'],
																							 v['last_name'], v['gender'],
																							 v['age'], v['city'],
																							 v['nationality'],
																							 v['personality'], v['likes']))


def read_user_info():
	user_dic = {}
	like_list = ['travelling', 'adventures', 'partying', 'pets', 'music', 'food', 'sports', 'movies', 'reading',
				 'programming', 'computer games', 'art']

	user_gender = input("Please enter your gender (options: male, female, other): ")
	user_dic['gender'] = user_gender

	expected_gender = input("Which gender you are looking for (options: male, female, other): ")
	user_dic['expected_gender'] = expected_gender

	user_age = input("Please enter your age: ")
	user_dic['age'] = user_age

	user_nationality = input("Please enter your nationality (e.g. US, UK, China, India): ")
	user_dic['nationality'] = user_nationality

	user_city = input("Please enter the city you currently live in (e.g. Champaign, Chicago, New York, Los Angeles): ")
	user_dic['city'] = user_city

	user_personality = input("Please enter your personality (options: introvert, extrovert, ambivert): ")
	user_dic['personality'] = user_personality

	expected_personality = input("Which personality do you prefer (options: introvert, extrovert, ambivert): ")
	user_dic['expected_personality'] = expected_personality

	user_likes = []
	print(
		"\nPlease enter what you are interested. Below are the options you can choose:\n\ntravelling\nadventures\npartying\npets\nmusic\nfood\nsports\nmovies\nreading\nprogramming\ncomputer games\nart\n\nOnce you've finished, input \"quit\" to exit this section\n")
	like = input('choose one of these you are interested: ')
	while (like != 'quit'):
		if like not in like_list:
			raise Exception("the hobby you entered is not in our list ")

		user_likes.append(like)
		like = input('choose one of these you are interested: ')
	user_dic['likes'] = user_likes

	user_preferences = []
	num_list = ['first', 'second', 'third']
	print("\nPlease enter your three preferences. Options: age, city, nationality, personality, music, pets, food, ...")
	for i in range(3):
		preference = input('enter the {} preference: '.format(num_list[i]))
		user_preferences.append(preference)
	user_dic['preferences'] = user_preferences

	return user_dic


if __name__ == '__main__':

	candidates = Candidates()
	candidates_list = json.load(open('data.json'))
	candidates_list = candidates.calculate_person_score(candidates_list)

	user = User()
	user_dic = read_user_info()
	user.set_attributes(user_dic)

	while True:
		candidate_num = int(input("\nHow many candidates do you want to meet in real life: "))

		is_random_order = input(
			"\nBy default you'll meet them in ranking order. Do you want to meet them in random instead (yes or no)? ")
		user_dic['is_random_order'] = is_random_order

		top_candidates_list = user.generate_candidates(user_dic, candidates_list, candidate_num)
		user.print_top_candidates(top_candidates_list)
		user.real_dating(candidate_num, top_candidates_list)