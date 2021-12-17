import os
import sys
import glob

result_file=sys.argv[1]
cwd=os.getcwd()
fileexp=cwd+'/'+result_file+'*.txt'

dict={}
for file in glob.glob(fileexp):
    print(file)
    data=[]
    line_num=0
    with open (file,'r') as rf:
        for line in rf:
            starting_char=line[0]
            if(not starting_char.isalpha()):
                data.append(int(line))
            elif((line_num%3==1) and starting_char.isalpha()):
                line_num-=1                
            elif((line_num%3==2) and starting_char.isalpha()):
                prev_val=data[-1]
                data.append(prev_val)
                line_num+=1
            line_num+=1    
    i=0
    print('Total number of placement: %s'%str(len(data)/2))
    while(i<len(data)):
        a=data[i]
        i+=1
        b=data[i]
        i+=1
        delta=a-b
        if delta in dict:
            dict[delta]=dict[delta]+1
        else:
            dict[delta]=1

print("Final counts:-->")
print(dict)
total=0
for k in dict:
    total+=dict[k]


percent=[]
keys=[]
for k,val in sorted(dict.items()):
    percent.append(float(val)/total)
    keys.append(k)    
print(total)
print(keys)
print(percent)
print("CDF:-->")
res=0
cdf=[]
for k in percent:
    res+=k
    cdf.append(res)
print(cdf)

extended_percent=[]
        
max_key=max(keys)
for i in range(max_key+1):
    if i in dict:
        extended_percent.append(float(dict[i]/total))    
    else:
        extended_percent.append(0.0)

print("Extended percent")
print(extended_percent)

