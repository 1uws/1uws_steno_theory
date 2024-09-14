import re
p = re.compile(r'^[a-zA-Z][a-zA-Z\']*\t')
words = {}
for file_no in ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']:
# for file_no in ['23']:
   file_name = '1-000' + file_no + '-of-00024'
   with open('C:\\Users\\nguye\\Downloads\\'+file_name + '\\' + file_name,'r', encoding='utf8') as file:
      for line in file:
         m = p.match(line)
         if m != None:
            word = m[0][:-1].lower()
            if word[-2:] == '\'s':
               continue
            count = sum([int(records.split(',')[1]) for records in line.split('\t')[1:]])
            if word not in words:
               words[word] = count
            else:
               words[word] += count
wordcount = []
for word in words:
   wordcount.append(word + ':' + str(words[word]))
wordcount = sorted(wordcount, key = lambda x: int(x.split(':')[1]), reverse = True)
with open('accumulated.txt', 'w') as file:
   file.write('\n'.join(wordcount))