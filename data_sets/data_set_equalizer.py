import random

file_tags1 = open('blackjack4-2.tags')
file_data1 = open('blackjack4-2.data')

lines_to_read = []
tags = []
datum1 = []
i = 0

for position, line in enumerate(file_tags1):
    if i > 200000:
        break
    #print(position, line[0] , len(line))
    if line[0] == 'd':
        tags = tags + [ 'd' ]
        lines_to_read = lines_to_read + [position]
    i = i + 1

#print(lines_to_read)
print('Length', len(lines_to_read))

datum = file_data1.readlines()
for i in range(max(lines_to_read)+1):
    if i in lines_to_read:
        datum1 = datum1 + [ datum[i] ]
        #print(data[i], type(data[i]))


#print(data[0])
#print(data[3])
#print(data[1200])
#print(len(data), len(tags), type(data), type(data[0]))

file_tags2 = open('blackjack5.tags')
file_data2 = open('blackjack5.data')
datum2 = file_data2.readlines()
tags2 = file_tags2.readlines()

for z in range(len(datum1)):
    datum1[z] = datum1[z][:-1]

for z in range(len(datum2)):
    datum2[z] = datum2[z][:-1]
    tags2[z] = tags2[z][:-1]
print('Length datum2', len(datum2), len(tags2))
print('Length datum1', len(datum1), len(tags))

final_data = []
final_tags = []
i = 0
j = 0

tags_over = False
tags2_over = False
while not tags_over or not tags2_over:
    if i == len(tags):
        tags_over = True
    if j == len(tags2):
        tags2_over = True
    if random.random() > 0.3333333 and not tags2_over:
        final_data = final_data + [datum2[j]]
        final_tags = final_tags + [tags2[j]]
        j = j + 1
    elif not tags_over:
        final_data = final_data + [datum1[i]]
        final_tags = final_tags + [tags[i]]
        i = i + 1

print(len(final_data), len(final_tags))


name = 'blackjack5-out'
dataf = open( name + ".data", "a" )
tagf = open( name + ".tags", "a" )


for final_datum in final_data:
    dataf.write( final_datum + "\n" )
for tag in final_tags:
    tagf.write( tag  + "\n" )
dataf.close()
tagf.close()
