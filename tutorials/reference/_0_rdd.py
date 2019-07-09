import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


print('\n[*] RDD.PLAYER.values:')
for v in RDD.PLAYER.values:
    print(v)


print('\n[*] RDD.PLAYER.keys:')
for k in RDD.PLAYER.keys:
    print(k)


print('\n[*] RDD.PLAYER.items:')
for v, k in RDD.PLAYER.items:
    print(v, k)


print(RDD.PLAYER['M1'])
print(RDD.PLAYER['M1'].keys)
print(RDD.PLAYER['M1'].values)
print(RDD.PLAYER['M1']['METAL'])
print(RDD.PLAYER['M1']['METAL'].process)
print(RDD.PLAYER['M1']['METAL'].purpose)


print('\nMetal players:')
for m in RDD.get_physical_layers_by_purpose(purposes='METAL'):
    print(m)

print('\nMetal players:')
for m in RDD.get_physical_layers_by_process(processes='M1'):
    print(m)
# for p in RDD.PLAYER['M1'].values:
#     if p.purpose.symbol == 'METAL':
#         print(p)

# print('\nMetal players:')
# for key in RDD.PLAYER.keys:
#     for value in RDD.PLAYER[key].values:
#         if value.purpose.symbol == 'METAL':
#             print(value)

# print('\nProcess Layers:')
# for p in RDD.PLAYER.M1.get_process_layers():
#     print(p)


# print('\nRDD.PLAYER.find_item_key')
# print(RDD.PLAYER.find )
