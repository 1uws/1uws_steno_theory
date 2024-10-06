pairs = [
   'og',
'cg',
'gf',
'od',
'co',
'fo',
'fc',
'cs',
'so',
'gs',
'sa',
'ca',
'oa',
'ga',
'at',
'ts',
'ct',
'dt',
'ot',
'tg',
'ft',
'za',
'sz',
'cz',
'zx',
'ax',
'sx',
# "x'"
]
n = len(pairs)
for i_pair in range(n):
   pair = pairs[i_pair]
   for i_pair2 in range(n):
      pair2 = pairs[i_pair2]
      if pair2 != pair:
         pairs.append(''.join(sorted(list(set(pair + pair2)))))
print(set([x for x in pairs if len(x) > 2]))
print(len(set([x for x in pairs if len(x) > 2])))
print(len(set(pairs)))