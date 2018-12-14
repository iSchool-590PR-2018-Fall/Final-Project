import json
import random
import scipy.stats

def get_info():	
	fout = open('data.json', 'w')

	personal_info = []
	first_name_male = ['Rick', 'John', 'Jack', 'Eric', 'James', 'Michael', 'David', 'Richard', 'Daniel', 'Paul', 'Mark', 'Kevin', 'Peter', 'Steven']
	first_name_female = ['Emma', 'Mary', 'Sherry', 'Taylor', 'Linda', 'Lisa', 'Elizabeth', 'Susan', 'Laura', 'Jessica', 'Rebecca', 'Michelle']
	last_name = ['Smith', 'Johnson', 'Williams', 'Green', 'Adams', 'Anderson', 'White', 'Perez', 'Hughes', 'Darch', 'Griffin', 'Lewis']
	city_list = ['Champaign', 'Chicago', 'New York', 'Los Angeles', 'San Francisco', 'Seattle', 'Boston', 'Austin', 'Houston']
	like_list = ['travelling', 'adventures', 'partying', 'pets', 'music', 'food', 'sports', 'movies', 'reading', 'programming', 'computer games', 'art']
	nationality_list = ['US', 'UK', 'China', 'India', 'Germany', 'Korea']
	personality_list = ['introvert', 'extrovert', 'ambivert']

	for i in range(200):
		person = {}

		if i < 100:
			person['gender'] = 'male'
			firt_name_index = random.randint(0, len(first_name_male) - 1)
			person['first_name'] = first_name_male[firt_name_index]
		else:
			person['gender'] = 'female'
			firt_name_index = random.randint(0, len(first_name_female) - 1)
			person['first_name'] = first_name_female[firt_name_index]

		last_name_index = random.randint(0, len(last_name) - 1)
		person['last_name'] = last_name[last_name_index]

		person['age'] = int(round(scipy.stats.norm.rvs(loc=27, scale=4)))

		city_index = random.randint(0, len(city_list) - 1)
		person['city'] = city_list[city_index]

		nationality_index = random.randint(0, len(nationality_list) - 1)
		person['nationality'] = nationality_list[nationality_index]

		personality_index = random.randint(0, len(personality_list) - 1)
		person['personality'] = personality_list[personality_index]

		expected_personality_index = random.randint(0, len(personality_list) - 1)
		person['expected_personality'] = personality_list[personality_index]

		likes_num = random.randint(2, 6)
		likes = []
		for j in range(likes_num):
			like_index = random.randint(0, len(like_list) - 1)
			while like_list[like_index] in likes:
				like_index = random.randint(0, len(like_list) - 1)
			likes.append(like_list[like_index])

		s = ""
		for t in range(len(likes)):
			s += likes[t]
			if t != len(likes) - 1:
				s += ", "

		person['likes'] = s
		personal_info.append(person)


	jsondata = json.dumps(personal_info)
	fout.write(jsondata)


get_info()