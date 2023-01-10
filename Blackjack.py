# blackjack.py
# an implementation of the classic card game using justinbodnar/Deck.py
from Deck import Deck
import random as rand
import tensorflow as tf
import tensorflow.keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
#from tensorflow import keras
import numpy as np
from tensorflow.keras.utils import plot_model

# instantiate deck of cards
global deck
deck = Deck()

# function to count the value of a hand
def hand_value( hand ):

	summ = 0

	for card in hand:
		# grab first character of the card
		card1 = int( card[:card.index('-')] )
		# deal with the face card
		if card1 > 10:
			card1 = 10
		summ = summ + card1

	return summ

############################
# function for split availability #
############################
def split_available( hand ):
	#print('Hand', hand)
	hand_cards = []
	for card in hand:
		# grab first character of the card
		card1 = int( card[:card.index('-')] )
		hand_cards.append(card1)

	if len(hand_cards) > 2:
		return False
	elif hand_cards[0] != hand_cards[1]:
		return False
	else:
		return True


############################
# function for double availability #
############################
def double_available( hand ):
	#print('Hand', hand)
	hand_cards = []
	for card in hand:
		# grab first character of the card
		card1 = int( card[:card.index('-')] )
		hand_cards.append(card1)

	if len(hand_cards) > 2:
		return False
	else:
		return True

############################
# function for single hand #
############################
# level 1: only gather data about the players cards
# level 2: gather level 1 AND the dealers face up card
# level 3: gather level 2 AND the history of which cards have been seen
def hand( montecarlo, level, debug ):

	# these lists are for collecting data
	data = []
	tags = []

	if level < 3:
		# get cards ready
		deck.shuffle()

	# instantiate two empty hands
	dealers_hand = [ ]
	players_hand = [ ]

	# this is for monte carlo simulations
	choices = [ 'h', 's', 'd']

	# deal the cards
	# players get two cards face-up
	# dealer gets one face-up, one face-down
	dealers_hand = [ deck.deal(), deck.deal() ]
	players_hand = [ deck.deal(), deck.deal() ]

	#print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
	#print( "Player: " + players_hand[0] + "   " + players_hand[1] )
	#print('Whatever -- ', int( dealers_hand[0][:dealers_hand[0].index('-')] ) )

	# print current game
	if debug:
		print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
		print( "Player: " + players_hand[0] + "   " + players_hand[1] )

	# check for win/loss
	summ = hand_value( players_hand )
	if summ is 21 and hand_value( dealers_hand ) is 21:
		if debug:
			print( "21 each." )
			print( "TIE" )
		return data, tags
	elif summ is 21 and hand_value( dealers_hand ) is not 21:
		if debug:
			print( "BlackJack!" )
			print( "PLAYER WINS" )
		return data, tags
	elif summ > 21:
		if debug:
			print( "Bust." )
			print( "PLAYER LOSES" )
		return data, tags
	else:
		players_summ = summ

	# hit up to 5 times
	double_played = False
	for i in range(5):
		#  hit or stay?

		'''
		if montecarlo and split_available(players_hand):
			choice = rand.choice( ["h","s","d","sp"] )
			#choice = "h"
		'''
		if montecarlo and double_available(players_hand):
			choice = rand.choice( ["h","s","d"] )
			#choice = "h"
		elif montecarlo:
			choice = rand.choice( ["h","s"] )
		else:
			print( "Hit or stay? (Enter 'h' or 's'): " )
			choice = raw_input()

		if double_played:
			choice = 's'

		# if hitting
		if choice is "h":
			# add data
			if level is 1:
				data = data + [ hand_value( players_hand ) ]
			elif level is 2:
				data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
			# hit
			players_hand = players_hand + [ deck.deal() ]
			summ = hand_value( players_hand )
			if debug:
				print( "Hitting" )
				players_hand_str = ""
				for card in players_hand:
					players_hand_str = players_hand_str + card + "   "
				print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
				print( "Player: " + players_hand_str )
			if summ > 21:
				# add tag
				tags = tags + [ 's' ]
				if debug:
					print( "Bust." )
					print( "PLAYER LOSES" )
				return data, tags
			elif summ is 21:
				# add tag
				if len(tags) == 0:
					tags = tags + [ 'd' ]
				else:
					tags = tags + [ 'h' ]
				if debug:
					print( "21" )
				return data, tags
			else:
				# add tag
				tags = tags + [ 'h' ]
				players_summ = summ

		# if staying
		elif choice is "s":
			# add data
			if level is 1:
				data = data + [ hand_value( players_hand ) ]
			elif level is 2:
				data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
			if debug:
				print( "Staying" )
				# print current game
				players_hand_str = ""
				for card in players_hand:
					players_hand_str = players_hand_str + card + "   "
			# check if dealer needs card
			while hand_value( dealers_hand ) < 17:
				dealers_hand = dealers_hand + [ deck.deal() ]
				if debug:
					print( "Dealer hits" )
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
			# check winner
			summ = hand_value( dealers_hand )
			if summ > 21:
				# add tag
				if double_played:
					tags = tags + [ 'h' ] + [ 's' ] #Does not guarantee 'd' as a good move
				else:
					tags = tags + [ 's' ]
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
					print( "Dealer busts." )
					print( "PLAYER WINS" )
				return data, tags
			elif summ is 21:
				# add tag
				if double_played:
					tags = tags + [ 'h' ] + [ 'h' ]
				else:
					tags = tags + [ 'h' ]
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " +  dealers_hand_str )
					print( "Player: " + players_hand_str )
					print( "Dealer has 21." )
					print( "PLAYER LOSES" )
				return data, tags
			else:
				if debug:
					dealers_hand_str = ""
					for card in dealers_hand:
						dealers_hand_str = dealers_hand_str + card + "   "
					print( "Dealer: " + dealers_hand_str )
					print( "Player: " + players_hand_str )
				if summ > players_summ:
					# add tag
					if double_played:
						tags = tags + [ 'h' ] + [ 'h' ]
					else:
						tags = tags + [ 'h' ]
					if debug:
						print( "PLAYER LOSES" )
					return data, tags
				else:
					# add tag
					if double_played:
						tags = tags + [ 'd' ] + [ 's' ]
					else:
						if len(tags) == 1 and tags[0] == 'h':
							tags[0] = 'd'
						tags = tags + [ 's' ]
					if debug:
						print( "PLAYER WINS" )
					return data, tags
		elif choice is "d":
			# add data
			if level is 1:
				data = data + [ hand_value( players_hand ) ]
			elif level is 2:
				data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]

			# hit Double
			players_hand = players_hand + [ deck.deal() ]
			summ = hand_value( players_hand )
			if debug:
				print( "Doubling" )
				players_hand_str = ""
				for card in players_hand:
					players_hand_str = players_hand_str + card + "   "
				print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
				print( "Player: " + players_hand_str )
			if summ > 21:
				# add tag
				tags = tags + [ 's' ]
				if debug:
					print( "Bust." )
					print( "PLAYER LOSES" )
				return data, tags
			elif summ is 21:
				#data = data + [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
				tags = tags + [ 'd' ]
				if debug:
					print( "21" )
				return data, tags
			else:
				# add tag
				double_played = True
				players_summ = summ

####################################
# function for testing an AI model #
####################################
# takes as input a model name string, a number of games to preform,
# a boolean where True implies we use a fresh deck for each hand,
# an integer representing which level we should be testing at,
# and a boolean for debugging/verbosity
# prints win/loss ratio
def test_model( model_name, num_of_tests, fresh_deck, level, betting, debug ):

	# statistics
	wins = 0
	losses = 0
	ties = 0
	win_doubles, loss_doubles = 0, 0
	money = 1000
	balance = money
	flat_bet = 10

	# deserialize model
	json_file = open('models/'+model_name+'.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = tf.keras.models.model_from_json( loaded_model_json, custom_objects={"GlorotUniform": tf.keras.initializers.glorot_uniform} )
	model.load_weights( "models/"+model_name+".h5" )
	print( "Model " + model_name + " loaded from disk" )

	#plot_model(model, to_file=model_name+'.png')

	# get deck ready
	deck = Deck()

	# random choices
	choices = [ 'h', 's', 'd' ]

	results = []

	#########################
	### Baseline Strategy ###
	#########################
	for i in range(0,17):
		results = results + [ "" ]
		for j in range(0,9):
			prediction = model.predict( np.array([ [i+5,j+2] ] ) )
			print('Prediction', prediction)
			ind_choice = np.argmax(prediction)
			py_ind_choice = ind_choice.item()
			if py_ind_choice is 0:
				results[i] = results[i] + "s"
			elif py_ind_choice is 1:
				results[i] = results[i] + "h"
			elif py_ind_choice is 2:
				results[i] = results[i] + "d"

	print( "  ", end="" )
	for x in range( len(results[0]) ):
		print( " " + str( (x+4)%10 ), end="" )
	print( )
	for i in range( len(results) ):
		print( i+5, end="" )
		if i+5 < 10:
			print( "  ", end="" )
		else:
			print( " ", end="" )
		for j in range( len(results[i] ) ):
			print( results[i][j], end=" " )
		print( )


	# loop through the number of tests parameter
	for i in range( num_of_tests ):

		if i%10 == 1:
			print('---------------------------', i, 'th Hand going')
			print('Cardinality', deck.cardinality())
		# prepare data for eventual input to model
		data = []

		# check if we need to shuffle
		if fresh_deck or deck.cardinality() < 15:
			deck.shuffle()

		# instantiate two empty hands
		dealers_hand = [ ]
		players_hand = [ ]

		if betting:
			if balance < 20:
				print('You are out of luck and money')
				authorization = input('Authorizre more funds? (y/n)')
				if authorization is 'y' or authorization is 'Y':
					balance = balance + 1000
					money = money + 1000
				elif authorization is 'n' or authorization is 'N':
					print('Authorization rejected! Thanks for your money! :P')
					print('Wins | Losses | Ties', wins, losses, ties)
					print('Started With - ', money)
					print('Now - ', balance)
					print(f'Wins D - {win_doubles} | Losses D - {loss_doubles}')
					return float(wins), float(losses), float(ties)
				else:
					print('Authorization Failed! Sorry your judgement seems off today!')
					print('Please exit the premises. Thank you!')
					print('Wins | Losses | Ties', wins, losses, ties)
					print('Started With - ', money)
					print('Now - ', balance)
					print(f'Wins D - {win_doubles} | Losses D - {loss_doubles}')
					return float(wins), float(losses), float(ties)


		# deal the cards
		# players get two cards face-up
		# dealer gets one face-up, one face-down
		dealers_hand = [ deck.deal(), deck.deal() ]
		players_hand = [ deck.deal(), deck.deal() ]
		balance = balance - flat_bet
		double_played = False

		# print current game
		if debug:
			print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
			print( "Player: " + players_hand[0] + "   " + players_hand[1] )

		# check for win/loss
		summ = hand_value( players_hand )
		if summ is 21 and hand_value( dealers_hand ) is 21:
			if debug:
				print( "21 each." )
				print( "TIE" )
			ties = ties + 1
			balance = balance + flat_bet
			continue
		elif summ is 21 and hand_value( dealers_hand ) is not 21:
			if debug:
				print( "BlackJack!" )
				print( "PLAYER WINS" )
			wins = wins + 1
			balance = balance + 2*flat_bet
			continue
		elif summ > 21:
			if debug:
				print( "Bust." )
				print( "PLAYER LOSES" )
			losses = losses + 1
			continue
		else:
			players_summ = summ

		# hit up to 5 times
		for j in range(5):
			#print(j)
			# add data
			if level is 1:
				data = [ hand_value( players_hand ) ]
			elif level is 2:
				data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
			elif level is 3:
				 data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]


			prediction = model.predict( np.array( data ) )
			#print('----------Here---------')
			#print('Prediction', prediction)
			#print(type(prediction))

			ind_choice = np.argmax(prediction)
			py_ind_choice = ind_choice.item()
			#print('Ind Choice', ind_choice)
			if py_ind_choice == 0:
				choice = 's'
			elif py_ind_choice == 1:
				choice = 'h'
			elif py_ind_choice == 2:
				choice = 'd'
			else:
				print('Error in Prediction')

			# temp code to generate random choice
#			choice = rand.choice( [ 'h', 's' ] )
#			choice = "s"

			#print( i, choice )

			if double_played:
				choice = 's'

			# if hitting
			if choice is "h":

				# hit
				players_hand = players_hand + [ deck.deal() ]
				summ = hand_value( players_hand )
				if debug:
					print( "Hitting" )
					players_hand_str = ""
					for card in players_hand:
						players_hand_str = players_hand_str + card + "   "
					print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
					print( "Player: " + players_hand_str )
				if summ > 21:
					# add tag
					if debug:
						print( "Bust." )
						print( "PLAYER LOSES" )
					losses = losses + 1
					break
				elif summ is 21:
					# add tag
					if debug:
						print( "21" )
					wins = wins + 1
					balance = balance + 2*flat_bet
					break
				else:
					# add tag
					players_summ = summ

			# if staying
			elif choice is "s":
				# add data
				if level is 1:
					data = [ hand_value( players_hand ) ]
				elif level is 2:
					data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] ]
				elif level is 3:
					 data = [ [ hand_value( players_hand ), int( dealers_hand[0][:dealers_hand[0].index('-')] ) ] + deck.negation() ]
				if debug:
					print( "Staying" )
					# print current game
					players_hand_str = ""
					for card in players_hand:
						players_hand_str = players_hand_str + card + "   "
				# check if dealer needs card
				while hand_value( dealers_hand ) < 17:
					dealers_hand = dealers_hand + [ deck.deal() ]
					if debug:
						print( "Dealer hits" )
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " + dealers_hand_str )
						print( "Player: " + players_hand_str )
				# check winner
				summ = hand_value( dealers_hand )
				if summ > 21:
					# add tag
					if debug:
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " + dealers_hand_str )
						print( "Player: " + players_hand_str )
						print( "Dealer busts." )
						print( "PLAYER WINS" )
					wins = wins + 1
					if double_played:
						win_doubles = win_doubles + 1
						balance = balance + 4*flat_bet
					else:
						balance = balance + 2*flat_bet
					break

				elif summ is 21:
					# add tag
					if debug:
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " +  dealers_hand_str )
						print( "Player: " + players_hand_str )
						print( "Dealer has 21." )
						print( "PLAYER LOSES" )
					losses = losses + 1
					if double_played:
						loss_doubles = loss_doubles + 1
					break
				else:
					if debug:
						dealers_hand_str = ""
						for card in dealers_hand:
							dealers_hand_str = dealers_hand_str + card + "   "
						print( "Dealer: " + dealers_hand_str )
						print( "Player: " + players_hand_str )
					if summ > players_summ:
						# add tag
						if debug:
							print( "PLAYER LOSES" )
						losses = losses + 1
						if double_played:
							loss_doubles = loss_doubles + 1
						break
					else:
						# add tag
						if debug:
							print( "PLAYER WINS" )
						wins = wins + 1
						if double_played:
							win_doubles = win_doubles + 1
							balance = balance + 4*flat_bet
						else:
							balance = balance + 2*flat_bet
						break

			elif choice is 'd' and not double_played:
				# Double
				players_hand = players_hand + [ deck.deal() ]
				balance = balance - flat_bet
				double_played = True
				summ = hand_value( players_hand )

				if debug:
					print( "Doubling" )
					players_hand_str = ""
					for card in players_hand:
						players_hand_str = players_hand_str + card + "   "
					print( "Dealer: " + dealers_hand[0] + "   " + "x-x")
					print( "Player: " + players_hand_str )
				if summ > 21:
					# add tag
					if debug:
						print( "Bust." )
						print( "PLAYER LOSES" )
					losses = losses + 1
					loss_doubles = loss_doubles + 1
					break
				elif summ is 21:
					# add tag
					if debug:
						print( "21" )
					wins = wins + 1
					win_doubles = win_doubles + 1
					balance = balance + 4*flat_bet
					break
				else:
					# add tag
					players_summ = summ


	# return stats
	print('Wins | Losses | Ties', wins, losses, ties)
	if betting:
		print('Started With - ', money)
		print('Now - ', balance)
		print(f'Wins D - {win_doubles} | Losses D - {loss_doubles}')
	return float(wins), float(losses), float(ties)

# function to add some number of
# data points to the blackjack data set
def gen_data_set( num_of_games, name, level, shuffle ):
	# loop through simulations
	for i in range( num_of_games ):
		print( i )
		try:
			data, tags = hand( True, level,  False )
			print('Data', data)

			if len(data) < len(tags) or len(data) > len(tags):
				print( "ERROR" )
				print( data )
				print( tags )



			dataf = open( "data_sets/" + str(name) + ".data", "a" )
			tagf = open( "data_sets/" + str(name) + ".tags", "a" )
			for datum in data:
				dataf.write( str( datum ) + "\n" )
			for tag in tags:
				tagf.write( tag  + "\n" )
			dataf.close()
			tagf.close()
			# check if we need to reshuffle the deck
			# only needed for data set level 3
#			print( deck.cardinality() )
			if shuffle:
				deck.shuffle()
		except Exception as e:
			print( e )
			deck.shuffle()
