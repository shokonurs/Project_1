from data_management.models import*



data=Diatomic_constant.objects.all()


molecule=raw_input("Enter the symbol of molecule (can't be blank) ")


# spin=raw_input("Enter the total electronic spin number (can be blank)")


print("Your molecule is %s " % molecule)

'''
if spin == "":
    print("You did not specify spin number")
else:
    print(" The spin number is " +spin)

'''


the_list=[]




for i in range(len(data)):
    if data[i].molecular_state.symbol==molecule:
        the_list.append(data[i].reference_publication)
'''

else :

    spin=int(spin)

    for i in range(len(data)):
        if data[i].molecular_state.symbol==molecule and data[i].molecular_state.total_electronic_spin==spin:
            the_list.append(data[i].reference_publication)


'''


print('There are total '+str(len(the_list))+' publictaions in database' )



# print(the_list[1].author)



ind=raw_input("Enter the number of publication ")

print("You chose paper of index "+str(ind))

ind=int(ind)

title=the_list[ind-1].title
journal=the_list[ind-1].journal
author=the_list[ind-1].author
year=the_list[ind-1].year


print( '\n'+ 

'The title of paper with number '+str(ind)+' is '+ '\n'

+ title+'\n' +

'\n'+ 'The name of journal is '+ journal+ '\n'

'\n'+'The author(s) of paper '+ author+ '\n'

'\n'+ 'Publish year '+str(year)
)















