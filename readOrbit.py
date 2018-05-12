import pickle

itemlist=[]

with open ('sat1.dat', 'rb') as fp:
  itemlist2=pickle.load(fp)
  itemlist.append(itemlist2)
  
with open ('sat2.dat', 'rb') as fp2:
  itemlist2=pickle.load(fp2)
  itemlist.append(itemlist2)
  
print(itemlist2[10])
print(itemlist[0][10])
print(itemlist[1][10])