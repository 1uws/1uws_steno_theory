from random import shuffle
import operator
import re
words = {}
ori_words = {}
for file_name in ['en_US.json','en_US_bonus.json']:
   with open(file_name,'r') as file:
      for line in file:
         word,phones = line[:-1].split(':')
         words[word] = [i.replace('\\','').replace('|','') for i in phones.split(',')]
         ori_words[word] = phones.split(',')
unixes = {}
with open('accumulated.txt','r',  encoding="utf8") as file:
   i = 0
   for line in file:
      word = line[:-1].split(':')[0].lower()
      if word in words and word not in unixes:
         unixes[word] = i
         i+=1

apis = ['o', '%', '2', '>', '(', ')', 'b', '$', 'd', '6', 'e', '&', '*', 'f', 'g', 'h', '!', 'i', '8', 'k', 'l', 'm', 'n', '=', '[', ']', 'p', 'r', 's', '1', 't', '0', '?', 'u', 'v', 'w', 'j', 'z', '3']
consonents = ['b', '$', 'd', '6', 'f', 'g', 'h', '8', 'k', 'l', 'm', 'n', '=', 'p', 'r', 's', '1', 't', '0', 'v', 'w', 'j', 'z', '3']
vowels = ['o', '%', '2', '>', '(', ')', 'e', '&', '*', '!', 'i', '[', ']', '?', 'u']
strokes = {}
arrays = {}
end_cons = {}
jsontxt = ''
end_convs = {'pw': 'P', 'nv': 'P', '3r': 'P', '3d': 'P', 'fw': 'P', '$p': 'P', '1dl': 'P', 'vw': 'P', 'stz': 'P', 'brw': 'P', 'ksv': 'P', '$mp': 'P', 'dls': 'P', 'dk': 'P', '=r': 'P', '1=': 'P', 'fkr': 'P', '1g': 'P', 'drt': 'P', 'lrs': 'P', 'lms': 'P', '=h': 'P', '$w': 'P', 'drst': 'P', 'dh': 'P', '8z': 'P', 'dp': 'P', 'dmz': 'P', '1=k': 'P', 'ht': 'P', '0dl': 'P', 'dhr': 'P', 'drs': 'P', 'fks': 'P', 'hjl': 'P', '=l': 'P', 'mn': 'P', 'djn': 'P', 'pz': 'P', '1f': 'P', 'jr': 'P', 'fps': 'P', 'lpst': 'P', '1d': 'P', '0j': 'P', 'fz': 'P', '0fl': 'P', '$=': 'P', '6s': 'P', '=dk': 'P', '0mr': 'P', 'jw': 'P', 'bs': 'L', '8dl': 'L', 'dlr': 'L', '=s': 'L', '0nst': 'L', 'rw': 'L', 'mrs': 'L', '0dn': 'L', 'mpz': 'L', '0lv': 'L', 'knz': 'L', '=t': 'S', '1v': 'S', '0dns': 'S', 'fmt': 'S', '1st': 'T', '1b': 'T', 'fk': 'T', 'ltz': 'T', 'frs': 'F', '=gz': 'F', '0f': 'F', '1tz': 'F', 'lrt': 'F', 'krst': 'F', 'dlp': 'F', '6d': 'B', 'ds': 'B', 'bk': 'B', '=st': 'B', 'blz': 'B', 'gst': 'B', 'tv': 'B', 'fms': 'G', '0fs': 'G', '1kr': 'G', 'dnt': 'Z', 'dlv': 'PL', 'fmp': 'PL', 'hl': 'PL', '0=': 'PL', 'lpt': 'PL', 'hm': 'PL', 'mw': 'PL', 'hn': 'PL', '$s': 'PL', '6n': 'PL', 'prst': 'PL', '8f': 'PL', 'mst': 'PL', '=kst': 'PS', 'grz': 'PS', '8j': 'PS', '0ds': 'PS', 'kmp': 'PS', '8t': 'PS', '$lt': 'PT', 'dst': 'PT', '$j': 'PT', 'frt': 'PT', 'hs': 'PT', 'w': 'PF', 'gt': 'PF', 'nrst': 'PF', 'bmz': 'PF', '6r': 'PF', '8dr': 'PB', '3w': 'PB', '$k': 'PB', '0t': 'PB', '=gst': 'PB', '0k': 'PB', '0ks': 'PB', 'bt': 'PB', 'rtz': 'PB', 'nst': 'PG', 'kz': 'PG', 'bdr': 'PG', 'dlm': 'PG', '0st': 'PG', 'jz': 'PZ', 'lrz': 'LS', 'gn': 'LS', 'ntz': 'LS', 'mrz': 'LT', '8l': 'LT', 'nw': 'LT', '0d': 'LT', 'klt': 'LT', 'drv': 'LT', '8w': 'LT', '1rt': 'LT', '$1r': 'LT', '6j': 'LT', 'pst': 'LF', '=g': 'LF', 'rvz': 'LF', 'flt': 'LF', 'j': 'BL', 'drw': 'BL', 'gj': 'LG', 'sv': 'LG', 'jst': 'LG', '0ls': 'LZ', '0p': 'LZ', 'dv': 'ST', 'lvz': 'ST', '6z': 'ST', '0=s': 'ST', 'lnz': 'ST', 'klm': 'ST', 'dnz': 'SF', 'js': 'SF', '0ps': 'SF', 'mps': 'SB', '8d': 'SG', 'kns': 'SG', 'dt': 'SG', '0ns': 'SG', '0=k': 'SG', '1t': 'SZ', '0n': 'SZ', 'km': 'SZ', 'ln': 'SZ', '0=ks': 'SZ', 'kw': 'TF', 'hj': 'TF', 'sw': 'TB', 'dj': 'TB', 'bm': 'TB', 'jv': 'TG', 'fn': 'TG', 'blw': 'TG', 'bkm': 'TG', 'mpst': 'TZ', 'ms': 'FB', 'jks': 'FB', 'jt': 'FB', '$rt': 'FB', '0w': 'FB', 'lw': 'FG', 'fnt': 'FG', 'fpr': 'FZ', 'gl': 'BG', 'brz': 'BG', 'hw': 'BZ', '0rs': 'BZ', 'mp': 'GZ', 'mt': 'GZ', '8dn': 'PLS', 'fm': 'PLS', '8r': 'PLT', '=kt': 'PLT', 'wz': 'PLT', 'hr': 'PLT', '$m': 'PLT', 'fp': 'PLF', 'krt': 'PLF', 'jl': 'PLB', '8m': 'PLB', '=z': 'PLG', 'kv': 'PLG', 'nrt': 'PLG', 'jk': 'PLZ', 'gw': 'PLZ', 'ksw': 'PLZ', 'pt': 'PST', '3': 'PSF', 'bj': 'PSF', 'dw': 'PSF', 'jm': 'PSB', 'tw': 'PSB', 'df': 'PSB', 'fj': 'PSG', '1w': 'PSG', 'jp': 'PSZ', '1n': 'PTF', 'kn': 'PTF', 'jps': 'PTF', 'kp': 'PTF', 'mr': 'PTB', 'lps': 'PTB', 'jn': 'PTB', '=ks': 'PTG', 'kls': 'PTZ', '0l': 'PTZ', '1l': 'PFB', 'rv': 'PFB', '1j': 'PFB', 'prs': 'PFG', '1m': 'PFZ', 'lv': 'PFZ', 'bw': 'PFZ', '1p': 'PFZ', 'dmr': 'PBG', 'mpt': 'PBZ', '$l': 'PBZ', 'dnr': 'PGZ', 'drz': 'LST', '1k': 'LST', 'bst': 'LSF', 'lr': 'LSB', 'fst': 'LSG', 'prt': 'LSG', 'dg': 'LSZ', '=d': 'LTF', '$r': 'LTB', '$nt': 'LTB', 'nrz': 'LTG', 'fls': 'LTZ', 'n': 'P', 'l': 'L', 'k': 'S', 's': 'T', 'm': 'F', 'r': 'B', 'd': 'G', 't': 'Z', 'z': 'PL', 'b': 'PS', 'p': 'PT', '=': 'PF', 'f': 'PB', 'h': 'PG', 'st': 'PZ', 'g': 'LS', 'v': 'LT', '1': 'LFB', '8': 'LF', 'nz': 'BL', 'ks': 'LG', '$': 'LZ', 'rt': 'ST', 'pr': 'SF', 'kr': 'SB', 'br': 'SG', 'gr': 'SZ', 'dn': 'TF', 'nt': 'TB', 'ps': 'TG', '0': 'TZ', 'lz': 'FB', 'dr': 'FG', 'kl': 'FZ', 'dl': 'BG', 'dz': 'BZ', 'fr': 'GZ', 'rst': 'PLS', 'lp': 'PLT', 'fl': 'PLF', 'ns': 'PLB', 'bl': 'PLG', 'mz': 'PLZ', 'ls': 'PST', 'rz': 'PSF', 'kt': 'PSB', '=k': 'PSG', 'lt': 'PSZ', 'nr': 'PTF', 'vz': 'PTB', '0r': 'PTG', 'krs': 'PTZ', 'ft': 'PFB', 'kst': 'PFG', 'gz': 'PFZ', 'fs': 'PBG', '1r': 'PBZ', 'bz': 'LFG', 'dm': 'PGZ', '6': 'LST', 'lst': 'LSF', '8n': 'LSB', 'rs': 'LSG', 'dlz': 'LSZ', '$n': 'LFZ', 'lm': 'LTF', '$t': 'LBG', '0s': 'LTB', 'bd': 'LTG', 'tz': 'LTZ', 'lmz': 'LBZ'}
end_order = 'FRPBLGTSDZ'
start_order = '#STKPWHRAO*EU'
start_convs = {'$r': 'R', '$l': 'R', 'dh': 'R', '0f': 'R', 'drz': 'R', 'mz': 'R', 'brw': 'P', '=j': 'P', 'lt': 'P', 'hjl': 'P', 'rw': 'T', '0j': 'S', '3j': 'S', 'dm': 'S', 'mn': 'S', 'mrs': 'S', 'vz': 'S', 'dg': 'S', 'djn': 'S', 'bs': 'S', 'dv': 'K', 'dn': 'K', '1v': 'K', 'fw': 'H', '8j': 'W', 'pw': 'W', 'lm': 'W', '$j': 'RP', '6j': 'RT', 'jr': 'RS', 'jz': 'RS', 'mw': 'RS', 'fn': 'RS', 'bz': 'RK', '8w': 'RH', 'hs': 'RH', 'km': 'RH', 'dz': 'RW', 'tv': 'RW', 'hl': 'PT', 'vw': 'PT', 'hn': 'PT', 'hm': 'PS', '8f': 'PS', '3w': 'PK', '=': 'PH', 'lv': 'PW', '1t': 'PW', 'drw': 'PW', 'js': 'TS', 'jst': 'TK', 'kls': 'TH', 'mr': 'TH', '$w': 'TH', 'gj': 'TW', 'nw': 'TW', 'bm': 'TW', 'jw': 'TW', 'sv': 'SK', 'jt': 'SH', 'lz': 'SH', 'jv': 'SW', 'blw': 'SW', 'fs': 'KH', 'hr': 'KH', 'wz': 'KW', 'kn': 'HW', 'rs': 'HW', 'dj': 'RPT', 'kv': 'RPS', '0w': 'RPS', 'gw': 'RPK', 'ksw': 'RPK', 'bw': 'RPK', '1j': 'RPH', 'lw': 'RPH', 'bj': 'RPW', 'dw': 'RPW', 'jm': 'RTS', '1r': 'RTK', 'lps': 'RTK', 'tw': 'RTH', '1n': 'RTH', 'jks': 'RTW', 'rv': 'RTW', 'prs': 'RSK', '1p': 'RSH', '1w': 'RSW', 'jps': 'RKH', 'r': 'R', 'l': 'RKW', 'd': 'RHW', 'n': 'P', 'm': 'T', '1': 'PTS', 't': 'S', 'k': 'K', 's': 'H', 'b': 'W', 'pr': 'PTK', 'p': 'RP', 'rt': 'RT', 'f': 'RS', 'h': 'RK', 'v': 'RH', 'g': 'RW', 'w': 'PT', 'z': 'PS', '8': 'PTH', 'st': 'PK', '$': 'PH', 'j': 'PW', 'br': 'TS', 'kr': 'TK', 'gr': 'TH', 'ks': 'TW', '0': 'SK', 'kl': 'SH', 'ps': 'SW', 'rst': 'KH', 'lp': 'KW', 'fr': 'PTW', 'dr': 'HW', 'kw': 'RPT', 'bl': 'RPS', 'fl': 'PSK', 'ls': 'PSH', 'gl': 'PSW', 'jk': 'RPK', 'sw': 'RPH', '3': 'RPW', '6': 'RTS', 'jn': 'RTK', 'hw': 'PKH', 'jl': 'RTH', 'ms': 'RTW', 'jp': 'RSK', 'ns': 'RSH', '0r': 'PKW', 'hj': 'RSW', 'krs': 'PHW', 'fj': 'TSK', '1l': 'RKH', '1m': 'TSH'}

for end_conv in end_convs:
   end_convs[end_conv] = ''.join(sorted(end_convs[end_conv], key = lambda x: end_order.index(x)))
for start_conv in start_convs:
   start_convs[start_conv] = ''.join(sorted(start_convs[start_conv], key = lambda x: start_order.index(x)))

start_conv_counter = {}
for end_conv in end_convs:
   end_convs[end_conv] = '-' + end_convs[end_conv]
vowel_simple_convs = {'o': 'A', '%': 'AE', '2': 'OE', '>': 'O', '(': 'AEU', ')': 'AU', 'e': 'E', '&': 'AOEU', '*': 'AOE', '!': 'U', 'i': 'AO', '[': 'OEU', ']': 'OU', '?': 'AOU', 'u': 'EU'}
number_convs = {0: '-R', 1: 'S-R', 2: 'T-R', 3: 'P-R', 4: 'H-R', 5: 'K-R', 6: 'W-R', 7: 'R-R', 8: '-FR', 9: '-RP', 10: '-RL', 11: '-RT', 12: '-RB', 13: '-RG', 14: '-RS'}
spell_units = {"'": 'KP', 'a': 'K*', 'b': 'W','c': 'PH', 'd': 'WHR', 'e': 'W*', 'f': 'SR', 'g': 'WR', 'h': 'KR', 'i': 'SK*', 'j': 'PW', 'k': 'K', 'l': 'KWR', 'm': 'T', 'n': 'P', 'o': 'S*', 'p': 'PR', 'q': 'TPR', 'r': 'R', 's': 'H', 't': 'S', 'u': 'WH*', 'v': 'HR', 'w': 'TP', 'x': 'TW', 'y': 'PWR', 'z': 'SP', "backspace": "*","return": "-Z","tab": "-D","left": "-R","right":"-S","up":"-G","down":"-B",
   "1": "#S",
   "2":"#T",
   "3":"#P",
   "4":"#H",
   "5":"#K",
   "6":"#W",
   "7":"#R",
   "8":"#TP",
   "9":"#KW",
   "0":"#HR",
   "F1":"#SU",
   "F2":"#TU",
   "F3":"#PU",
   "F4":"#HU",
   "F5":"#KU",
   "F6":"#WU",
   "F7":"#RU",
   "F8":"#TPU",
   "F9":"#KWU",
   "F10":"#HRU",
   "F11":"#TKU",
   "F12":"#PWU",
   "home": "K-B",
   "end": "W-B"
   }

phones = {}
for word in words:
   if word not in unixes:
      continue
   for phone in words[word]:
      if phone not in phones:
         phones[phone] = [word]
      elif word not in phones[phone]:
         phones[phone].append(word)
keys = list(phones.keys())
for phone in keys:
   if phone not in phones:
      continue
   matching_ori_phones = []
   for word in phones[phone]:
      for ori_phone in ori_words[word]:
         if ori_phone.replace('\\','').replace('|','') == phone:
            if ori_phone not in matching_ori_phones:
               matching_ori_phones.append(ori_phone)
   selected_ori_phone = matching_ori_phones[0]
   max_seperator_count = selected_ori_phone.count('\\')+selected_ori_phone.count('|')
   for ori_phone in matching_ori_phones:
      if ori_phone.count('\\')+ ori_phone.count('|') > max_seperator_count:
         selected_ori_phone = ori_phone
         max_seperator_count = ori_phone.count('\\')+ori_phone.count('|')
   if selected_ori_phone != phone:
      phones[selected_ori_phone] = list(phones[phone])
      del phones[phone]
def get_json_segment(segment, words):
   segment_json = ''
   strokes = [segment[0]]
   for char in segment[1:]:
      if char in consonents:
         if (strokes[-1][-1] in consonents):
            strokes[-1] += char
         else:
            strokes.append(char)
      else:
         strokes.append(char)
   while True:
      no_new = True
      for i in range(1, len(strokes)-1):
         if strokes[i][0] in consonents and strokes[i-1][0] not in consonents and strokes[i+1][0] not in consonents:
            cons = strokes[i]
            if cons[-1] == 'j':
               cons = cons[:-1]
            if len(cons) > 2 and cons[:2] != 'ks' and cons[-3:] in ['str','spr']:
               cons = cons[:-3]
            elif len(cons) > 2 and cons[-3] != 'k' and cons[-2:] in ['st','sk','sl','sm','sw','sp']:
               cons = cons[:-2]
            elif len(cons) > 2 and cons[-2:] in ['bl','dr','fl','fr','gl','gw','kl','kw','0r','tr','gr','pl','pr','kr','br']:
               cons = cons[:-2]
            elif len(cons) > 1 and cons[1] in cons[:1]:
               cons = cons[:1]
            elif len(cons) > 2 and cons[2] in cons[:2]:
               cons = cons[:2]
            elif len(cons) > 3 and cons[3] in cons[:3]:
               cons = cons[:3]
            elif len(cons) > 4 and cons[4] in cons[:4]:
               cons = cons[:4]
            elif len(cons) > 0:
               cons = cons[:-1]
            
            if cons!= '' and cons != strokes[i]:
               second_half = strokes[i][len(cons):]
               strokes[i] = cons
               strokes.insert(i+1, second_half)
               no_new = False
               break
      if no_new:
         break
   for i in range(len(strokes)-1, -1, -1):
      if strokes[i][0] in consonents:
         for j in range(len(strokes[i])):
            for k in range(j+1, len(strokes[i])):
               if strokes[i][j] == strokes[i][k]:
                  strokes.insert(i+1, strokes[i][k:])
                  strokes[i] = strokes[i][:k]
   for i in range(len(strokes)-1, -1, -1):
      if strokes[i][0] not in consonents and strokes[i][0] in apis:
         stroke_json = ''
         insert_i = i
         if i+1<len(strokes) and strokes[i+1][0] in consonents:
            if ''.join(sorted(strokes[i+1])) not in end_convs:
               print(segment, words, strokes)
            stroke_json = end_convs[''.join(sorted(strokes[i+1]))]
            del strokes[i+1]
         stroke_json = vowel_simple_convs[strokes[i]] + stroke_json
         del strokes[i]
         if i>0 and strokes[i-1][0] in consonents:
            stroke_json = start_convs[''.join(sorted(strokes[i-1]))] + stroke_json
            insert_i -= 1
            del strokes[i-1]
         strokes.insert(insert_i, stroke_json)
   for i in range(len(strokes)):
      if strokes[i][0] in consonents:
         strokes[i] = start_convs[''.join(sorted(strokes[i]))]
      else:
         break
   for i in range(len(strokes)):
      if strokes[i][0] in consonents:
         strokes[i] = end_convs[''.join(sorted(strokes[i]))]
   for i in range(len(strokes)-1, -1, -1):
      if strokes[i][0] in consonents:
                  print('well ', strokes, segment, words)
   return '/'.join(strokes)

test_counter=0
phone_stenos = {}
for phone in phones:
   segments = [i for i in re.split('[\\\\|]', phone) if i != '']
   phone_json = '/'.join([get_json_segment(segment, phones[phone]) for segment in segments])
   if phone_json not in phone_stenos:
      phone_stenos[phone_json] = phones[phone]
   else:
      phone_stenos[phone_json] += phones[phone]
for phone_json in phone_stenos:
   words = phone_stenos[phone_json]
   if len(words) == 1:
      jsontxt += '"' + phone_json + '": "{^}' + words[0] +'{^ ^}",\n'
   else:
      words = sorted(words, key=lambda x: unixes[x])
      jsontxt += '"' + phone_json + '": "{^}' + words[0] +'{^ ^}",\n'
      for word in words[1]:
         word = 
      if False:
         jsontxt += '"' + phone_json + '": "{^}' + ', '.join([str(i) + '='+ words[i] for i in range(len(words))]) +'{^ ^}",\n'
         the_phone_json = phone_json
         added_R = False
         for i in range(len(the_phone_json)-1,-1,-1):
            if the_phone_json[i] in ['A', 'O', 'E', 'U', '-', 'F']:
               the_phone_json = the_phone_json[:i+1] + 'R' + the_phone_json[i+1:]
               added_R = True
               break
            elif the_phone_json[i] in ['\\', '|']:
               the_phone_json = the_phone_json[:i+1] + '-R' + the_phone_json[i+1:]
               added_R = True
               break
         if not added_R:
            the_phone_json = 'R' + the_phone_json
         jsontxt += '"' + the_phone_json + '": "{^}' + words[0] +'{^ ^}",\n'
         for i in range(len(words)):
            jsontxt += '"' + phone_json + '/'+ number_convs[i] + '": "{^}' + words[i] +'{^ ^}",\n'
p = re.compile(r'([AOEU])-')
jsontxt = p.sub(r'\1',jsontxt)
help_pairs = [[x for x in re.split('[":, ]', line) if x != ''] for line in jsontxt.replace('{^}','').split('\n') if line != '' and re.search(r'"[A-Z\/-]*": "[a-z\']*"',line) != None]
helps = {}
for help_pair in help_pairs:
   if help_pair[1] not in helps:
      helps[help_pair[1]] = [help_pair[0]]
   else:
      helps[help_pair[1]].append(help_pair[0])
helptxt = ''
for h in helps:
   helptxt += '"SKW/' + '/'.join([spell_units[c.lower()] for c in h]) + '/SKW": "{^}' + '='.join(helps[h]) + '{^ ^}",\n'
with open('steno.json', 'w') as file:
   file.write('{\n'+jsontxt[:-2]+'\n}')
with open('help.json', 'w') as file:
   file.write('{\n'+helptxt[:-2]+'\n}')
def sort_stroke(strokes):
   first_keys = []
   second_keys = []
   for stroke in strokes:
      is_first = True
      for key in stroke:
         if key == '-':
            is_first = False
            continue
         if is_first:
            first_keys.append(key)
         else:
            second_keys.append(key)
   result = ''
   if len(first_keys) != 0:
      result = ''.join(sorted(first_keys, key = lambda x: start_order.index(x)))
   if len(second_keys) != 0:
      if result == '' or result[-1] not in 'AO*EU':
         result += '-'
      result += ''.join(sorted(second_keys, key = lambda x: end_order.index(x)))
   return result
shortutstxt = ''
shortutstxt += '"-F": "{}{#shift}",\n'
shortutstxt += '"-P": "{}{#control}",\n'
shortutstxt += '"-L": "{}{#command}",\n'
shortutstxt += '"-T": "{}{#option}",\n'
for char in spell_units:
   shortutstxt += '"' + sort_stroke([spell_units[char], '-F'])+'": "{}{#shift(' + char + ')}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-P']) + '": "{}{#control(' + char + ')}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-L']) + '": "{}{#command(' + char + ')}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-T']) + '": "{}{#option(' + char + ')}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-FP']) + '": "{}{#control(shift(' + char + '))}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-PT']) + '": "{}{#control(option(' + char + '))}",\n'
   shortutstxt += '"' + sort_stroke([spell_units[char], '-FT']) + '": "{}{#shift(option(' + char + '))}",\n'
with open('shortcuts.json', 'w') as file:
   file.write('{\n'+shortutstxt[:-2]+'\n}')

spelltxt = ''
with open('spell.json', 'r') as file:
   lines = []
   for line in file:
      if '"D"' not in line and "{\n" != line and "}" != line:
         beau = line[:-1]
         if beau == '':
            continue
         if beau[-1] != ',':
            beau += ','
         beau += '\n'
         lines.append(beau)
   hint = '"DZ": "' + ''.join([line[:-1] for line in lines]).replace('\\""', '\'\'').replace('^ ^','space').replace('^,','comma').replace('"^"','caret').replace('"', '').replace('&','').replace('#','').replace(' ','').replace('{','').replace('}','').replace('^','').replace(',',' ').replace('\\','\\\\') +'",\n'
   spelltxt = ''.join(lines) + hint
with open('spell.json', 'w') as file:
   file.write('{\n'+spelltxt[:-2]+'\n}')