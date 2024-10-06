from random import shuffle
import operator
import re
words = {}
ori_words = {}
for file_name in ['en_US.json']:
   with open(file_name,'r') as file:
      for line in file:
         word,phones = line[:-1].split(':')
         if word in words and len(phones) < len(words[word]):
            continue
         words[word] = list(set([i.replace('\\','').replace('|','') for i in phones.split(',')]))
         ori_words[word] = phones.split(',')
unixes = {}
with open('accumulated.txt','r',  encoding="utf8") as file:
   i = 0
   for line in file:
      word = line[:-1].split(':')[0].lower()
      if word in words and word not in unixes:
         unixes[word] = i
         i+=1
consonents = {'b': 0, '$': -0.1, 'd': -0.125, '6': 0, 'f': 0, 'g': 0, 'h': -0.125, '8': 0, 'k': -0.05, 'l': 0, 'm': -0.05, 'n': 0, '=': 1, 'p': 0, 'r': 0, 's': -0.125, '1': 0, 't': 0, '0': -0.1, 'v': 0, 'w': -0.05, 'j': 0, 'z': 0, '3': 0}
vowels = {'o': -0.07, '%': -0.1, '2': -1, '>': -0.25, '(': -0.05, ')': 0, 'e': -0.5, '&': -0.4, '*': -0.05, '!': -0.75, 'i': -0.1, '[': 0, ']': 0, '?': -0.1, 'u': -0.03}
entxt = ''
for word in unixes:
   if len(words[word]) > 1:
      max_score = -9999999
      selected = []
      for word_ipa in words[word]:
         score = 0
         for ipa in word_ipa:
            if ipa in consonents:
               score += consonents[ipa]
            else:
               score += vowels[ipa]
         if score >= max_score:
            if score > max_score:
               selected = [word_ipa]
            else:
               selected.append(word_ipa)
            max_score = score
      max_word_ipa_len = -1
      temp_selected = selected
      selected = []
      for word_ipa in temp_selected:
         if len(word_ipa) >= max_word_ipa_len:
            if len(word_ipa) > max_word_ipa_len:
               selected = [word_ipa]
            else:
               selected.append(word_ipa)
            max_word_ipa_len = len(word_ipa)
      if len(selected) > 1:
         selected = [selected[0]]
      print(word, words[word], selected, max_score)
      # if len(selected) != 1:
         # exit()
      entxt += word + ':' + selected[0] + '\n'
   else:
      entxt += word + ':' + words[word][0] + '\n'
with open('en.json', 'w') as file:
   file.write(entxt[:-1])