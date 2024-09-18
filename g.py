from random import shuffle
import operator
import re
words = {}
ori_words = {}
# for file_name in ['en_US.json','en_US_bonus.json']:
for file_name in ['en_US.json']:
   with open(file_name,'r') as file:
      for line in file:
         word,phones = line[:-1].split(':')
         if word in words and len(phones) < len(words[word]):
            continue
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
end_convs = {'nv': 'F', 'pw': 'F', '3r': 'F', '3d': 'F', 'fw': 'F', '$p': 'F', '1dl': 'F', 'vw': 'F', 'brw': 'F', 'ksv': 'F', '$mp': 'F', 'dk': 'F', '=r': 'F', '1=': 'F', 'fkr': 'F', '1g': 'F', 'drt': 'F', 'lrs': 'F', 'lms': 'F', '$w': 'F', 'drst': 'F', 'dh': 'F', '8z': 'F', 'dp': 'F', '1=k': 'F', 'dls': 'F', '0dl': 'F', 'drs': 'F', 'fks': 'F', '=s': 'F', 'hjl': 'F', '=l': 'F', 'mn': 'F', 'djn': 'F', 'stz': 'F', 'pz': 'F', '1f': 'F', 'jr': 'F', 'lpst': 'F', '1d': 'F', '0j': 'F', 'fz': 'F', '0fl': 'F', '$=': 'F', '6s': 'F', '=dk': 'F', '0mr': 'F', 'jw': 'F', 'bs': 'P', '8dl': 'P', '=gz': 'P', 'dlr': 'P', '0nst': 'P', 'rw': 'P', 'mrs': 'P', '0dn': 'P', 'mpz': 'P', '0lv': 'P', 'knz': 'P', '=t': 'L', '1v': 'L', '0dns': 'L', 'fmt': 'L', '1b': 'R', 'fk': 'R', 'ltz': 'R', 'frs': 'B', '0f': 'B', '1tz': 'B', 'lrt': 'B', 'krst': 'B', '0ls': 'B', 'dlp': 'B', '6d': 'G', 'ds': 'G', 'bk': 'G', '=st': 'G', 'blz': 'G', 'gst': 'G', 'tv': 'G', 'fms': 'T', '0fs': 'T', '1kr': 'T', 'dnt': 'D', '=kst': 'FP', 'grz': 'FP', '8j': 'FP', '0ds': 'FP', 'kmp': 'FP', '8t': 'FP', 'dlv': 'FL', 'fmp': 'FL', 'hl': 'FL', '0=': 'FL', 'lpt': 'FL', 'hm': 'FL', 'mw': 'FL', 'hn': 'FL', 'prt': 'FL', '$s': 'FL', '6n': 'FL', '0st': 'FL', '8f': 'FL', 'mst': 'FL', '$lt': 'FR', 'dst': 'FR', '$j': 'FR', 'frt': 'FR', 'hs': 'FR', 'w': 'FB', 'gt': 'FB', 'nrst': 'FB', 'bmz': 'FB', 'prst': 'FB', '6r': 'FB', '8dr': 'FG', '$k': 'FG', '0t': 'FG', '3w': 'FG', '=gst': 'FG', '0k': 'FG', '0ks': 'FG', 'bt': 'FG', 'rtz': 'FG', 'nst': 'FT', 'brz': 'FT', 'kz': 'FT', 'jz': 'FD', 'sv': 'PL', 'lrz': 'PL', 'gn': 'PL', 'ntz': 'PL', 'mrz': 'PR', 'kns': 'PR', '8l': 'PR', 'nw': 'PR', '0d': 'PR', 'dlm': 'PR', '8w': 'PR', '1rt': 'PR', '$1r': 'PR', '6j': 'PR', 'pst': 'PB', '=g': 'PB', '0ns': 'PB', 'rvz': 'PB', 'bdr': 'PB', '0p': 'PB', 'gj': 'PG', 'js': 'PG', 'j': 'PT', 'drw': 'PT', 'dv': 'PD', 'lvz': 'PD', '6z': 'PD', 'klt': 'PD', '0=s': 'PD', 'klm': 'PD', '0ps': 'LR', 'dnz': 'LB', 'jst': 'LB', 'lnz': 'LB', 'mps': 'LG', '=z': 'LT', '0l': 'LT', 'mpst': 'LT', 'km': 'LT', '0=k': 'LT', 'kw': 'LD', 'hj': 'LD', 'sw': 'RB', 'dj': 'RB', 'bm': 'RB', 'drv': 'RB', '1t': 'RG', '0n': 'RG', 'ln': 'RG', '0=ks': 'RG', 'jks': 'RT', 'fn': 'RT', 'flt': 'RT', 'blw': 'RT', 'bkm': 'RT', 'mt': 'RD', 'ms': 'BG', 'jv': 'BG', 'rv': 'BG', 'jt': 'BG', '0w': 'BG', 'fnt': 'BT', 'lw': 'BT', 'dt': 'BD', '$rt': 'BD', 'fpr': 'BD', 'gl': 'GT', 'nrt': 'GT', '8r': 'GD', '=kt': 'GD', 'tz': 'GD', 'wz': 'GD', 'hr': 'GD', '$m': 'GD', 'mp': 'TD', '8m': 'TD', '0s': 'FPL', '8dn': 'FPL', 'fm': 'FPL', 'hw': 'FPR', '0rs': 'FPR', 'fp': 'FPB', 'krt': 'FPB', 'jn': 'FPG', 'df': 'FPG', 'nr': 'FPT', 'kv': 'FPT', 'pt': 'FPD', 'jk': 'FLR', 'gw': 'FLR', 'ksw': 'FLR', 'bj': 'FLB', 'tw': 'FLB', 'jl': 'FLB', 'jm': 'FLG', '1w': 'FLG', '3': 'FLT', 'dw': 'FLT', 'fj': 'FLD', 'kn': 'FLD', 'mr': 'FRB', 'jp': 'FRB', 'lps': 'FRB', '=ks': 'FRG', '1l': 'FRT', 'jps': 'FRT', 'kls': 'FRD', 'kp': 'FRD', 'prs': 'FBG', '1j': 'FBG', 'mpt': 'FBT', '$l': 'FBT', '1p': 'FBT', '1m': 'FBD', 'lv': 'FBD', 'bw': 'FBD', 'dmr': 'FGT', 'fls': 'FGT', 'dnr': 'FGD', 'drz': 'FTD', '1k': 'FTD', 'bst': 'PLR', 'rs': 'PLB', 'lr': 'PLG', 'fst': 'PLT', 'bd': 'PLD', 'dg': 'PRB', '$nt': 'PRG', '=d': 'PRT', 'n': 'F', 'l': 'P', 'k': 'L', 's': 'R', 'm': 'B', 'r': 'G', 'd': 'T', 't': 'D', 'b': 'FP', 'z': 'FL', 'p': 'FR', '=': 'FB', 'f': 'FG', 'h': 'FT', 'st': 'FD', 'g': 'PL', 'v': 'PR', '1': 'PRD', '8': 'PB', 'ks': 'PG', 'nz': 'PT', 'rt': 'PD', '$': 'LR', 'pr': 'LB', 'kr': 'LG', 'br': 'LT', 'dn': 'LD', 'nt': 'RB', 'gr': 'RG', 'ps': 'RT', '0': 'RD', 'lz': 'BG', 'dr': 'BT', 'kl': 'BD', 'dl': 'GT', 'lp': 'GD', 'fr': 'TD', 'rst': 'FPL', 'dz': 'FPR', 'fl': 'FPB', 'ns': 'FPG', 'bl': 'FPT', 'ls': 'FPD', 'mz': 'FLR', 'kt': 'FLB', '=k': 'FLG', 'rz': 'FLT', 'lt': 'FLD', 'vz': 'FRB', '0r': 'FRG', 'ft': 'FRT', 'krs': 'FRD', 'kst': 'FBG', '1r': 'FBT', 'gz': 'FBD', 'fs': 'FGT', 'bz': 'PBG', 'dm': 'FGD', '6': 'FTD', 'lst': 'PLR', '8d': 'PLB', '8n': 'PLG', '$n': 'PBT', 'lm': 'PLT', '1n': 'PLD', 'dlz': 'PRB', '$t': 'PBD', 'nrz': 'PRG', '$r': 'PRT', 'lmz': 'PGT'}
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
right_spell_units = {' ': '-BG', "'": '-PG', 'a': '-GS', 'b': '-B','c': '-FP', 'd': '-FRB', 'e': '-BS', 'f': '-RT', 'g': '-RB', 'h': '-RG', 'i': '-GTS', 'j': '-PB', 'k': '-G', 'l': '-RBG', 'm': '-L', 'n': '-P', 'o': '-TS', 'p': '-RP', 'q': '-RPL', 'r': '-R', 's': '-F', 't': '-T', 'u': '-FBS', 'v': '-FR', 'w': '-PL', 'x': '-BL', 'y': '-RPB', 'z': '-PT'}
spell_units = {' ': 'KW', "'": 'KP', 'a': 'K*', 'b': 'W','c': 'PH', 'd': 'WHR', 'e': 'W*', 'f': 'SR', 'g': 'WR', 'h': 'KR', 'i': 'SK*', 'j': 'PW', 'k': 'K', 'l': 'KWR', 'm': 'T', 'n': 'P', 'o': 'S*', 'p': 'PR', 'q': 'TPR', 'r': 'R', 's': 'H', 't': 'S', 'u': 'WH*', 'v': 'HR', 'w': 'TP', 'x': 'TW', 'y': 'PWR', 'z': 'SP', "backspace": "*", "escape": "-Z", "return": "-DZ","tab": "-D","left": "-R","right":"-S","up":"-G","down":"-B",
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

def sort_stroke(strokes):
   first_keys = []
   second_keys = []
   for stroke in strokes:
      is_first = True
      for key in stroke:
         if key == '-':
            is_first = False
            continue
         if is_first and key in start_order:
            first_keys.append(key)
         else:
            if is_first:
               is_first = False
            second_keys.append(key)
   result = ''
   if len(first_keys) != 0:
      result = ''.join(sorted(first_keys, key = lambda x: start_order.index(x)))
   if len(second_keys) != 0:
      if result == '' or result[-1] not in 'AO*EU':
         result += '-'
      result += ''.join(sorted(second_keys, key = lambda x: end_order.index(x)))
   return result

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
   return strokes

test_counter=0
phone_stenos = {}
for phone in phones:
   segments = [i for i in re.split('[\\\\|]', phone) if i != '']
   phone_json = [get_json_segment(segment, phones[phone]) for segment in segments]
   phone_json[0][0] = sort_stroke([phone_json[0][0], '*'])
   phone_json = '/'.join(['/'.join(x) for x in phone_json])
   if phone_json not in phone_stenos:
      phone_stenos[phone_json] = phones[phone]
   else:
      phone_stenos[phone_json] += phones[phone]
for phone_json in phone_stenos:
   words = phone_stenos[phone_json]
   if len(words) == 1:
      jsontxt += '"' + phone_json + '": "{^' + words[0] +' ^}",\n'
   else:
      words = sorted(words, key=lambda x: unixes[x])
      jsontxt += '"' + phone_json + '": "{^' + words[0] +' ^}",\n'
      accum_phone_json = []
      for i in range(1, len(words)):
         accum_phone_json.append({'pre': words[0], 'word': words[i], 'j': phone_json})
      accum_count = 0
      while len(accum_phone_json) != 0:
         for accum_i in range(len(accum_phone_json)):
            word = accum_phone_json[accum_i]['word']
            previous_word = accum_phone_json[accum_i]['pre']
            equal_substring = ''
            for c in previous_word:
               if len(word) - 1 < len(equal_substring):
                  from_char = c
                  to_char = ' '
                  break
               elif c == word[len(equal_substring)]: # len(equal_substring) > len(word) - 1
                  equal_substring += c
               else:
                  from_char = c
                  to_char = word[len(equal_substring)]
                  break
            else:
               if word == previous_word:
                  print('not similar right? ',words)
               from_char = ' '
               to_char = word[len(previous_word)]
            accum_phone_json[accum_i]['j'] += '/' +sort_stroke([spell_units[from_char], right_spell_units[to_char]])
         next_accum = []
         for i in range(len(accum_phone_json)):
            is_first_j = True
            for j in range(i):
               if accum_phone_json[i]['j'] == accum_phone_json[j]['j']:
                  is_first_j = False
                  break
            if is_first_j:
               jsontxt += '"' + accum_phone_json[i]['j'] + '": "{^' + accum_phone_json[i]['word'] +' ^}",\n'
               for j in range(i+1, len(accum_phone_json)):
                  accum_phone_json[j]['pre'] = accum_phone_json[i]['word']
            else:
               next_accum.append(accum_phone_json[i])
         accum_phone_json = next_accum
p = re.compile(r'([AOEU])-')
jsontxt = p.sub(r'\1',jsontxt)
with open('steno.json', 'w') as file:
   file.write('{\n'+jsontxt[:-2].replace('/U/','/#*U/').replace('/A/','/#A*/').replace('/U"','/#*U"').replace('/A"','/#A*"')+'\n}')
help_pairs = [[x for x in re.split('[":, ]', line) if x != ''] for line in jsontxt.replace('{^','').split('\n') if line != '' and re.search(r'"[A-Z\/-]*": "[a-z\']*"',line) != None]
helps = {}
for help_pair in help_pairs:
   if help_pair[1] not in helps:
      helps[help_pair[1]] = [help_pair[0]]
   else:
      helps[help_pair[1]].append(help_pair[0])
helptxt = ''
for h in helps:
   helptxt += '"SKW/' + '/'.join([spell_units[c.lower()] for c in h]) + '/SKW": "{^' + '='.join(helps[h]) + '^}",\n'
with open('help.json', 'w') as file:
   file.write('{\n'+helptxt[:-2]+'\n}')
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
      if '"DZ"' not in line and "{\n" != line and "}" != line:
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