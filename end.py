from random import shuffle
import operator
entries = {}
with open('en_US.json','r') as file:
   for line in file:
      word,phones = line[:-1].split(':')
      entries[word] = phones.split(',')
unixes = {}
with open('accumulated.txt','r',  encoding="utf8") as file:
   i = 0
   for line in file:
      word = line[:-1].split(':')[0].lower()
      if word in entries and word not in unixes:
         unixes[word] = i
         i+=1

apis =      ['o', '%', '2', '>', '(', ')', 'b', '$', 'd', '6', 'e', '&', '*', 'f', 'g', 'h', '!', 'i', '8', 'k', 'l', 'm', 'n', '=', '[', ']', 'p', 'r', 's', '1', 't', '0', '?', 'u', 'v', 'w', 'j', 'z', '3']
consonents =   ['b', '$', 'd', '6', 'f', 'g', 'h', '8', 'k', 'l', 'm', 'n', '=', 'p', 'r', 's', '1', 't', '0', 'v', 'w', 'j', 'z', '3']
vowels = ['o', '%', '2', '>', '(', ')', 'e', '&', '*', '!', 'i', '[', ']', '?', 'u']
single_con_conv = []
end_phone_convs = {'0': 'R','1': 'P', '2': 'L', '3': 'S', '4': 'B', '5': 'F', '6': 'G', '7': 'Z'}
start_phone_convs = {'0': 'R', '1': 'P','2': 'T', '3': 'S', '4': 'K', '5': 'H', '6': 'W', '7': 'G', '8': 'Z', '9': 'D'}
rest_con_conv = []
for i in range(0,8):
   # single_con_conv.append(str(i))
   rest_con_conv.append(str(i))
for i in range(0,8):
   for j in range(i+1,8):
      rest_con_conv.append(str(i)+str(j))
for i in range(0,7):
   for j in range(i+1,7):
      for k in range(j+1,7):
         rest_con_conv.append(str(i)+str(j)+str(k))
for i in range(0,8):
   for j in range(i+1,8):
      for k in range(j+1,8):
         if str(i)+str(j)+str(k) not in rest_con_conv:
            rest_con_conv.append(str(i)+str(j)+str(k))
rest_con_conv.remove('45')
rest_con_conv.remove('145')
rest_con_conv.remove('245')
rest_con_conv.remove('345')
rest_con_conv.remove('456')
rest_con_conv.remove('457')
rest_con_conv.remove('16')
rest_con_conv.remove('126')
rest_con_conv.remove('136')
rest_con_conv.remove('146')
rest_con_conv.remove('156')
rest_con_conv.remove('567')
print(rest_con_conv)
print(len(rest_con_conv))
print(len(consonents))
print(len(single_con_conv))

strokes = {}
arrays = {}
end_cons = {}
jsontxt = ''
for word in entries:
   if word not in unixes:
      continue
   for ori_phone in entries[word]:
      phone = ori_phone
      cons = ''
      pos = 0
      start_word = True
      # while len(phone) != 0:
      while pos < len(phone):
         end_word = False
         if phone[pos] in consonents:
            if cons == '':
               start_word = pos == 0 or phone[pos - 1] in ['|','\\']
            cons+=phone[pos]
            # phone = phone[1:]
            pos += 1
            # end_word = len(phone) == 0
            end_word = len(phone) == pos
            if not end_word:
               continue
         else:
            # end_word = phone[0] in ['|','\\']
            end_word = phone[pos] in ['|','\\']
            # phone = phone[1:]
            # pos += 1
         prev_cons = cons
         if len(cons) != 0 and not end_word and not start_word:
            if cons[-1] == 'j':
               cons = cons[:-1]

            if len(cons) > 2 and cons[:2] != 'ks' and cons[-3:] in ['str','spr']:
               cons = cons[:-3]
            elif len(cons) > 2 and cons[-3] != 'k' and cons[-2:] in ['st','sk','sl','sm','sw','sp']:
               cons = cons[:-2]
            elif len(cons) > 2 and cons[-2:] in ['bl','dr','fl','fr','gl','gw','kl','kw','0r','tr','gr','pl','pr','kr','br']:
               cons = cons[:-2]
            elif len(cons) > 0 and cons[-1] in consonents:
               cons = cons[:-1]
         if len(prev_cons) > 0:
            if end_word or start_word:
               end_con = prev_cons
            else:
               end_con = cons
            # end_con = cons
            if end_con != '':
               # hollow_phone = ori_phone[:pos - len(prev_cons)] + '_' + ori_phone[pos - len(prev_cons) + len(end_con):]
               # end_con = ''.join(sorted(list(dict.fromkeys(end_con))))
               # end_con = ''.join(sorted(end_con))
               end_pos = 0
               while end_pos < len(end_con):
                  next_pos = min(end_pos + 10, len(end_con))
                  # if len(end_con) == 2:
                  #    next_pos = 2
                  # else:
                  #    next_pos = end_pos + 1
                  for i in range(end_pos+1, next_pos):
                     if end_con[i] in end_con[end_pos:i]:
                        next_pos = i
                        break
                  part_end = end_con[end_pos:next_pos]
                  end_pos = next_pos
                  hollow_phone = ori_phone[:pos - len(prev_cons)] + '_' + ori_phone[pos - len(prev_cons) + len(part_end):]
                  # if 'g&l|frendz' in ori_phone:
                  #    print(hollow_phone, ori_phone, word, prev_cons, pos, part_end, end_con)
                  part_end = ''.join(sorted(part_end))
                  # test = ''.join(sorted(list(dict.fromkeys(part_end))))
                  # if len(test) == 0 or len(test) != len(part_end):
                  #    print('what again')
                  if part_end not in end_cons:
                     end_cons[part_end] = [hollow_phone]
                  elif hollow_phone not in end_cons[part_end]:
                     end_cons[part_end].append(hollow_phone)
         cons = ''
         pos += 1
enemies = {}
# for end_con in end_cons:
#    for end_con2 in end_cons:
#       if end_con < end_con2:
#          for hollow in end_cons[end_con2]:
#             if hollow in end_cons[end_con]:
#                if end_con not in enemies:
#                   enemies[end_con] = [end_con2]
#                else:
#                   enemies[end_con].append(end_con2)
#                break
end_cons = dict(sorted(end_cons.items(), key=lambda item: len(item[1]), reverse=True))
keys = list(end_cons.keys())
end_con_alts = {}
for end_con_i in range(len(keys)):
   end_con = keys[end_con_i]
   for end_con2_i in range(len(keys)):
      end_con2 = keys[end_con2_i]
      if end_con not in end_con_alts and end_con2 not in end_con_alts and end_con_i < end_con2_i:
         areEnemies = False
         for hollow in end_cons[end_con]:
            if hollow in end_cons[end_con2]:
               areEnemies = True
               break
         if not areEnemies:
            print(end_con, ' is not enemy with ', end_con2)
            end_cons[end_con] += end_cons[end_con2]
            if end_con2 not in end_con_alts:
               end_con_alts[end_con2] = end_con
# end_con_alts2 = dict(end_con_alts)
# end_con_alts = {}
# for end_con2 in end_con_alts2:
#    end_con = end_con_alts2[end_con2]
#    if end_con not in end_con_alts:
#       end_con_alts[end_con] = [end_con]
#    end_con_alts[end_con].append(end_con2)
for end_con in end_cons:
   if end_con not in end_con_alts:
      end_con_alts[end_con] = end_con
end_convs = {}
end_con_unique_counter = {}
i = 0
# for end_con in end_cons:
   # end_convs[''.join([end_phone_convs[x] for x in rest_con_conv[i]])] = end_con_alts[end_con]
for end_con in end_con_alts:
   if end_con_alts[end_con] not in end_con_unique_counter:
      end_con_unique_counter[end_con_alts[end_con]] = i
      i+=1
   end_convs[end_con] = ''.join([end_phone_convs[x] for x in rest_con_conv[end_con_unique_counter[end_con_alts[end_con]]]])
print(end_convs)
# enemies = dict(sorted(enemies.items(), key=operator.itemgetter(0)))
# keys = list(enemies.keys())
# for enemy in keys:
#    for enemy2 in keys:
#       if enemy in enemies and enemy2 in enemies and enemy < enemy2:
#          areEnemies = False
#          for hollow in end_cons[enemy]:
#             if hollow in end_cons[enemy2]:
#                areEnemies = True
#                break
#          if not areEnemies:
#             print(enemy, ' is not enemy with ', enemy2)
#             del enemies[enemy2]
# print(enemies)
# end_convs = {'pw': 'P', 'nv': 'P', '3r': 'P', '3d': 'P', 'fw': 'P', '$p': 'P', '1dl': 'P', 'vw': 'P', 'stz': 'P', 'brw': 'P', 'ksv': 'P', '$mp': 'P', 'dls': 'P', 'dk': 'P', '=r': 'P', '1=': 'P', 'fkr': 'P', '1g': 'P', 'drt': 'P', 'lrs': 'P', 'lms': 'P', '=h': 'P', '$w': 'P', 'drst': 'P', 'dh': 'P', '8z': 'P', 'dp': 'P', 'dmz': 'P', '1=k': 'P', 'ht': 'P', '0dl': 'P', 'dhr': 'P', 'drs': 'P', 'fks': 'P', 'hjl': 'P', '=l': 'P', 'mn': 'P', 'djn': 'P', 'pz': 'P', '1f': 'P', 'jr': 'P', 'fps': 'P', 'lpst': 'P', '1d': 'P', '0j': 'P', 'fz': 'P', '0fl': 'P', '$=': 'P', '6s': 'P', '=dk': 'P', '0mr': 'P', 'jw': 'P', 'bs': 'L', '8dl': 'L', 'dlr': 'L', '=s': 'L', '0nst': 'L', 'rw': 'L', 'mrs': 'L', '0dn': 'L', 'mpz': 'L', '0lv': 'L', 'knz': 'L', '=t': 'S', '1v': 'S', '0dns': 'S', 'fmt': 'S', '1st': 'T', '1b': 'T', 'fk': 'T', 'ltz': 'T', 'frs': 'F', '=gz': 'F', '0f': 'F', '1tz': 'F', 'lrt': 'F', 'krst': 'F', 'dlp': 'F', '6d': 'B', 'ds': 'B', 'bk': 'B', '=st': 'B', 'blz': 'B', 'gst': 'B', 'tv': 'B', 'fms': 'G', '0fs': 'G', '1kr': 'G', 'dnt': 'Z', 'dlv': 'PL', 'fmp': 'PL', 'hl': 'PL', '0=': 'PL', 'lpt': 'PL', 'hm': 'PL', 'mw': 'PL', 'hn': 'PL', '$s': 'PL', '6n': 'PL', 'prst': 'PL', '8f': 'PL', 'mst': 'PL', '=kst': 'PS', 'grz': 'PS', '8j': 'PS', '0ds': 'PS', 'kmp': 'PS', '8t': 'PS', '$lt': 'PT', 'dst': 'PT', '$j': 'PT', 'frt': 'PT', 'hs': 'PT', 'w': 'PF', 'gt': 'PF', 'nrst': 'PF', 'bmz': 'PF', '6r': 'PF', '8dr': 'PB', '3w': 'PB', '$k': 'PB', '0t': 'PB', '=gst': 'PB', '0k': 'PB', '0ks': 'PB', 'bt': 'PB', 'rtz': 'PB', 'nst': 'PG', 'kz': 'PG', 'bdr': 'PG', 'dlm': 'PG', '0st': 'PG', 'jz': 'PZ', 'lrz': 'LS', 'gn': 'LS', 'ntz': 'LS', 'mrz': 'LT', '8l': 'LT', 'nw': 'LT', '0d': 'LT', 'klt': 'LT', 'drv': 'LT', '8w': 'LT', '1rt': 'LT', '$1r': 'LT', '6j': 'LT', 'pst': 'LF', '=g': 'LF', 'rvz': 'LF', 'flt': 'LF', 'j': 'LB', 'drw': 'LB', 'gj': 'LG', 'sv': 'LG', 'jst': 'LG', '0ls': 'LZ', '0p': 'LZ', 'dv': 'ST', 'lvz': 'ST', '6z': 'ST', '0=s': 'ST', 'lnz': 'ST', 'klm': 'ST', 'dnz': 'SF', 'js': 'SF', '0ps': 'SF', 'mps': 'SB', '8d': 'SG', 'kns': 'SG', 'dt': 'SG', '0ns': 'SG', '0=k': 'SG', '1t': 'SZ', '0n': 'SZ', 'km': 'SZ', 'ln': 'SZ', '0=ks': 'SZ', 'kw': 'TF', 'hj': 'TF', 'sw': 'TB', 'dj': 'TB', 'bm': 'TB', 'jv': 'TG', 'fn': 'TG', 'blw': 'TG', 'bkm': 'TG', 'mpst': 'TZ', 'ms': 'FB', 'jks': 'FB', 'jt': 'FB', '$rt': 'FB', '0w': 'FB', 'lw': 'FG', 'fnt': 'FG', 'fpr': 'FZ', 'gl': 'BG', 'brz': 'BG', 'hw': 'BZ', '0rs': 'BZ', 'mp': 'GZ', 'mt': 'GZ', '8dn': 'PLS', 'fm': 'PLS', '8r': 'PLT', '=kt': 'PLT', 'wz': 'PLT', 'hr': 'PLT', '$m': 'PLT', 'fp': 'PLF', 'krt': 'PLF', 'jl': 'PLB', '8m': 'PLB', '=z': 'PLG', 'kv': 'PLG', 'nrt': 'PLG', 'jk': 'PLZ', 'gw': 'PLZ', 'ksw': 'PLZ', 'pt': 'PST', '3': 'PSF', 'bj': 'PSF', 'dw': 'PSF', 'jm': 'PSB', 'tw': 'PSB', 'df': 'PSB', 'fj': 'PSG', '1w': 'PSG', 'jp': 'PSZ', '1n': 'PTF', 'kn': 'PTF', 'jps': 'PTF', 'kp': 'PTF', 'mr': 'PTB', 'lps': 'PTB', 'jn': 'PTB', '=ks': 'PTG', 'kls': 'PTZ', '0l': 'PTZ', '1l': 'PFB', 'rv': 'PFB', '1j': 'PFB', 'prs': 'PFG', '1m': 'PFZ', 'lv': 'PFZ', 'bw': 'PFZ', '1p': 'PFZ', 'dmr': 'PBG', 'mpt': 'PBZ', '$l': 'PBZ', 'dnr': 'PGZ', 'drz': 'LST', '1k': 'LST', 'bst': 'LSF', 'lr': 'LSB', 'fst': 'LSG', 'prt': 'LSG', 'dg': 'LSZ', '=d': 'LTF', '$r': 'LTB', '$nt': 'LTB', 'nrz': 'LTG', 'fls': 'LTZ', 'n': 'P', 'l': 'L', 'k': 'S', 's': 'T', 'm': 'F', 'r': 'B', 'd': 'G', 't': 'Z', 'z': 'PL', 'b': 'PS', 'p': 'PT', '=': 'PF', 'f': 'PB', 'h': 'PG', 'st': 'PZ', 'g': 'LS', 'v': 'LT', '1': 'LFB', '8': 'LF', 'nz': 'LB', 'ks': 'LG', '$': 'LZ', 'rt': 'ST', 'pr': 'SF', 'kr': 'SB', 'br': 'SG', 'gr': 'SZ', 'dn': 'TF', 'nt': 'TB', 'ps': 'TG', '0': 'TZ', 'lz': 'FB', 'dr': 'FG', 'kl': 'FZ', 'dl': 'BG', 'dz': 'BZ', 'fr': 'GZ', 'rst': 'PLS', 'lp': 'PLT', 'fl': 'PLF', 'ns': 'PLB', 'bl': 'PLG', 'mz': 'PLZ', 'ls': 'PST', 'rz': 'PSF', 'kt': 'PSB', '=k': 'PSG', 'lt': 'PSZ', 'nr': 'PTF', 'vz': 'PTB', '0r': 'PTG', 'krs': 'PTZ', 'ft': 'PFB', 'kst': 'PFG', 'gz': 'PFZ', 'fs': 'PBG', '1r': 'PBZ', 'bz': 'LFG', 'dm': 'PGZ', '6': 'LST', 'lst': 'LSF', '8n': 'LSB', 'rs': 'LSG', 'dlz': 'LSZ', '$n': 'LFZ', 'lm': 'LTF', '$t': 'LBG', '0s': 'LTB', 'bd': 'LTG', 'tz': 'LTZ', 'lmz': 'LBZ'}
print('done')
with open('ends.txt', 'w') as file:
   file.write(str(end_convs))