'''
Prepare Data
'''
from __future__ import absolute_import, division, print_function

# tf and keras
import tensorflow as tf
#from tensorflow import keras
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
#from keras.models import model_from_json

# helper libs
import numpy as np
import matplotlib.pyplot as plt

# Blackjack import
from Blackjack import *
import Blackjack as bj

# lets make some data sets
import Blackjack as bj

#bj.gen_data_set( 200000, "blackjack4-2", 2, True )


# get the data set
data = open( "blackjack5-out.data").readlines()
tags = open( "blackjack5-out.tags").readlines()

data_clean = []
tags_clean = []

#strip whitespace
first = True
i = 0
for datum in data:
	print('Hand Number:', i)
	i = i + 1
	# skip empty line first
	if first:
		first = False
		continue
	#print('Datum', datum)
	clean_datum = datum[1:datum.index('\n')-1].strip().split(', ')
	#print( len(clean_datum) )
	#print( type(clean_datum) )
	#print( type(clean_datum[0]) )
	#print('Clean Datum', clean_datum)
	clean_datum[0] = int( clean_datum[0] )
	clean_datum[1] = int( clean_datum[1] )
#	print( clean_datum )
	data_clean = data_clean + [ clean_datum ]
	#print('Clean Data', data_clean)

first = True
for tag in tags:
	if first:
		first = False
		continue
	tag = tag[:tag.index('\n')]
	if tag == 'h':
		tags_clean = tags_clean + [ 1.0 ]
	elif tag == 's':
		tags_clean = tags_clean + [ 0.0 ]
	elif tag == 'd':
		tags_clean = tags_clean + [ 2.0 ]
	else:
		print('Error! Split not Implemented')

size = int( len(data)*(0.7) )

#print('Clean Data', data_clean)
#print('Clean Tags', tags_clean)

train_data = np.array( data_clean[1:size] )
train_tags = np.array( tags_clean[1:size] )
test_data = np.array( data_clean[size:] )
test_tags = np.array( tags_clean[size:] )

'''
Train & Test
'''
train_data2 = train_data.astype(np.float)
#print(train_data2[0])
#print('Train Data2', train_data2.shape)
#print(type(train_data2))

#print('-------------Test Data-----------')
test_data2 = test_data.astype(np.float)
#print(test_data2[0])
#print(test_data2.shape)
#print('Train Tags', train_tags)

'''
model = tf.keras.Sequential()
model.add( tf.keras.layers.Dense(2048, input_dim=2) )
model.add( tf.keras.layers.Dense(2048, input_dim=2) )
model.add( tf.keras.layers.Dense(2048, input_dim=2) )
#model.add( tf.keras.layers.Dense(2048, input_dim=54) )
#model.add( tf.keras.layers.Dense(2048, input_dim=54) )
#model.add( tf.keras.layers.Dense(1028, input_dim=54) )
#model.add( tf.keras.layers.Dense(1028, input_dim=54) )
#model.add( tf.keras.layers.Dense(1028, input_dim=54) )
model.add( tf.keras.layers.Dense(3, activation=tf.nn.softmax) )
model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data2, train_tags, epochs=10)

test_loss, test_acc = model.evaluate(test_data2, test_tags)
print('Test Loss:', test_loss)
print('Test accuracy:', test_acc)

# save model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
model_json = model.to_json()
with open( "models/blackjackmodel.4.json", "w") as json_file:
	json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("models/blackjackmodel.4.h5")
print( "Model saved" )
'''


model = tf.keras.Sequential()
#model.add( tf.keras.layers.Dense(32, input_dim=2) )
#model.add( tf.keras.layers.Dense(32, input_dim=2) )
#model.add( tf.keras.layers.Dense(64, input_dim=2) )
#model.add( tf.keras.layers.Dense(128, input_dim=2) )
#model.add( tf.keras.layers.Dense(1024, input_dim=2) )
model.add( tf.keras.layers.Dense(512, input_dim=2) )
model.add( tf.keras.layers.Dense(32, input_dim=2) )
model.add( tf.keras.layers.Dense(16, input_dim=2) )
model.add( tf.keras.layers.Dense(8, input_dim=2) )
model.add( tf.keras.layers.Dense(3, activation=tf.nn.softmax) )
model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data2, train_tags, epochs=20)
test_loss, test_acc = model.evaluate(test_data2, test_tags)
print('Test Loss:', test_loss)
print('Test accuracy:', test_acc)

# save model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
model_json = model.to_json()
with open( "blackjackmodel.5-2.json", "w") as json_file:
	json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("blackjackmodel.5-2.h5")
print( "Model saved" )


wins, losses, ties = test_model( "blackjackmodel.5", 100, False, 2, True, False )
print('Here')
total = wins + losses + ties
win_percentage = (wins/total)*100.0
loss_percentage = (losses/total)*100.0
tie_percentage = (ties/total)*100.0
print( "Percentage won:  " + str( win_percentage ) )
print( "Percentage lost: " + str( loss_percentage ) )
print( "Percentage tied: " + str( tie_percentage ) )
