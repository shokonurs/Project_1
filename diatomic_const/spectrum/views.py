# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from data_management.models import *
from django.template.defaulttags import register

from django.db.models import Q

def index(request):
    return HttpResponse("<h2> Hey! This is my first line of code! </h2>")




def files(request):

    all_data=Diatomic_constant.objects.all()

    molecule_names=[]
    count=0
    for entry in all_data:
	
        name=entry.molecular_state.symbol
        if name not in molecule_names:
            molecule_names.append(name)
	    count+=1

    
   
    variables={'molecule_names':molecule_names,'count':count }
   
    return render(request, 'spectrum/the_list_view.html',variables)


# This is main function
def molecules_list(request):
    data=Diatomic_constant.objects.all()

    names=[]
    for i in data:
        name=i.molecular_state.symbol
        if name not in names:
            names.append(name) 
    variables={'molecules_list':names}
    return render(request,'spectrum/a_molecules_list.html',variables)





def test_function(request):
    data=Diatomic_constant.objects.all()
    variables={'data':data}
    return render(request, 'spectrum/b_test.html',variables)


# This is main function
def molecule_states(request, molecule_name):
    data=Diatomic_constant.objects.all()
    all_states=[]
    for i in data:
        current_molecule=i.molecular_state.symbol
        current_state=i.molecular_state
        if current_molecule==molecule_name:
            if current_state not in all_states:
                all_states.append(current_state)

    variables={"states": all_states,
                 "name": molecule_name}
  # return render(request, 'spectrum/c_molecule_details.html', variables)
    return render(request, 'spectrum/d_molecule_states_table.html', variables)




# Testing function(to be deleted later) 
def table(request):
    #1. Find all unique molecules
    unique_molecules_source=Diatomic_constant.objects.all()
   
     # List of unique molecules
    molecules_list=[]
    for i in unique_molecules_source:
        if i.molecular_state.symbol not in molecules_list:
            molecules_list.append(i.molecular_state.symbol)
    

    # 2. Open For Loop that iterates over each molecule
    # Also make new dictioney to store all data
    main={}
    for molecule in molecules_list:
        # a) Find unique states for given molecule
        states_list=[]
        data=Diatomic_constant.objects.all()
        for i in data:
            if i.molecular_state.symbol==molecule:
                if i.molecular_state not in states_list:
                    states_list.append(i.molecular_state)
        
        
        # b) For each state find publications and constants associated with it
        # make dictionary for current state
        

        for state in states_list:
            # Make dictionary for current state
            dict_state={}
    
            # Make list of entries for a specific state
            publ_source=Diatomic_constant.objects.all().filter(molecular_state=state)
            # FInd number of papers for a given State
            papers_number=len(publ_source)
    
            # Iterate over list of entries and parse publication and constant_type and value    
            for entry in publ_source:
            
                tag=entry.reference_publication.reference_publication_tag
                constant_type=entry.constant_type
                value=entry.value
                d1={tag:{constant_type:value}}
                dict_state[state]=d1
        
        main[str(molecule)]=dict_state    







    variables={'main':main}
    return render(request, 'spectrum/b_test.html', variables)
    
    
    



def table2(request):
    # a) Find unique molecules list
    unique_molecules=Molecular_state.objects.values_list('symbol', flat=True).distinct()    
    unique_molecules=sorted(unique_molecules)
    
    # b) FInd unique states list
    unique_states=Molecular_state.objects.all()
    
    # c) Make dictionary for each state and save publications and constants
    common={}
    for state in unique_states:
        constants_of_state=Diatomic_constant.objects.filter(molecular_state=state)
             
        common[state]=constants_of_state
    
    
   
    
    # d) Now sort common dictionary according to molecules 
    main={}
    for molecule in unique_molecules:
        a=[]
        for key in common:
            if key.symbol==molecule:
                a.append({key:common[key]})
        main[str(molecule)]=a   
       
    
    # Here 'main' is the dictionary where key is the 'molecule'.
    # Value is the list of states that are linked to certain constants,papers
    

    # e) Make needed constants: equilibrium
    all_constants=Constant_type.objects.all()
    e_constants=[]
    for i in all_constants:
        if "e" in i.symbol:    
            e_constants.append(i)
    
    delete={'a':1,'b':2} 
    variables={'main': main,
               'unique_molecules': unique_molecules,
               'e_constants': e_constants}
    return render(request, 'spectrum/b_test.html', variables)
  
   


# This is the main function that passes sorted data into main table
def table3(request):
     # 1) Find unique molecules list
    unique_molecules=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    unique_molecules=sorted(unique_molecules)
    mol_list=[]
    for i in unique_molecules:
        mol_list.append(str(i))

    test_dictionary={}
    count=1
    for i in unique_molecules:
        test_dictionary[i]=count
        count+=1


    # 2) Find unique states list
    unique_states=Molecular_state.objects.all()
   
   
   
   
   
    # 3) For each of state find entry from Diatomic_constant
    common={}
    for state in unique_states:
        inner={}
        inner[str("state_object")]=state
        data_of_state=Diatomic_constant.objects.filter(molecular_state=state)
        inner[str("constants")]=data_of_state
        common[state]=inner
        
       
    
    
    # 4) Sort the common dictionary accriding to molecules
    main={}
    for molecule in unique_molecules:
        d1={}
        
        for key, value in common.items():
            if str(molecule) in str(key):
                d1[str(key)]=value
                 
        main[molecule]=d1
    

    # 5) Makes list of needed constants
    constant_source=Constant_type.objects.all()
    e_constants=[]
    for i in constant_source:
        if "e" in i.symbol:
            e_constants.append(i)
    
    
    variables={'unique_molecules':mol_list,       
               'test_dictionary':test_dictionary,
               'unique_states': unique_states,         
               'common':common,
               'main':main,
               'e_constants':e_constants}  
    return render(request, 'spectrum/f_main_table.html', variables)
    
    
    
    
    

# this is similar function as the previous one. This one is used only
# for visualisation.

def main_data(request):
     # 1) Find unique molecules list
    unique_molecules=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    unique_molecules=sorted(unique_molecules)
    mol_list=[]
    for i in unique_molecules:
        mol_list.append(str(i))

    test_dictionary={}
    count=1
    for i in unique_molecules:
        test_dictionary[i]=count
        count+=1


    # 2) Find unique states list
    unique_states=Molecular_state.objects.all()
   
   
  
    # 3) Makes list of needed constants
    constant_source=Constant_type.objects.all()
    e_constants=[]
    for i in constant_source:
        if "e" in i.symbol:
            e_constants.append(i)
   

 
   
   
    # 4) For each of state find entry from Diatomic_constant
    common={}
    for state in unique_states:
        inner={}
        inner[str("state_object")]=state
        # This data contains all types of constants
        # We need to filter them, so only 'equilibrium' constants are here
        data_of_state=Diatomic_constant.objects.filter(molecular_state=state)
        
        container=[]
        for i in data_of_state:
            if "e" in i.constant_type.symbol:
                container.append(i)  


        # Now we need to order the entries of the container.
        sorted_container=[]
        for const in e_constants:
            for entry in container:
                if entry.constant_type==const:
                    sorted_container.append(entry)
     
        inner[str("constants")]=sorted_container
        
        #We also have to add the length on each list for each state
        number_of_constants=len(container)
        if number_of_constants==0:
            remaining=0
            rowspan=1
        else:
            remaining=number_of_constants-1
            rowspan=number_of_constants
        inner[str("rowspan")]=rowspan
        inner[str("remaining")]=remaining
        common[state]=inner
        
       
    
    
    # 5) Sort the common dictionary accriding to molecules
    main={}
    for molecule in unique_molecules:
        d1={}
        
        for key, value in common.items():
            if str(molecule) in str(key):
                d1[str(key)]=value
                 
        main[molecule]=d1
    
    
    variables={'unique_molecules':mol_list,       
               'test_dictionary':test_dictionary,
               'unique_states': unique_states,         
               'common':common,
               'main':main,
               'e_constants':e_constants}  
    return render(request, 'spectrum/g_main_data.html', variables)
    
    
    





 
    


def new_function(request):
     # 1) Find unique molecules list
    unique_molecules=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    unique_molecules=sorted(unique_molecules)
    mol_list=[]
    for i in unique_molecules:
        mol_list.append(str(i))

    test_dictionary={}
    count=1
    for i in unique_molecules:
        test_dictionary[i]=count
        count+=1


    # 2) Find unique states list
    unique_states=Molecular_state.objects.all()
   
   
  
    # 3) Makes list of needed constants
    constant_source=Constant_type.objects.all()
    e_constants=[]
    for i in constant_source:
        if "e" in i.symbol:
            e_constants.append(i)
   

 
   
   
    # 4) For each of state find entry from Diatomic_constant
    common={}
    for state in unique_states:
        inner={}
        inner[str("state_object")]=state
        # This data contains all types of constants
        # We need to filter them, so only 'equilibrium' constants are here
        data_of_state=Diatomic_constant.objects.filter(molecular_state=state)
        
        container=[]
        for i in data_of_state:
            if "e" in i.constant_type.symbol:
                container.append(i)  


        # Now we need to order the entries of the container.
        sorted_container=[]
        for const in e_constants:
            for entry in container:
                if entry.constant_type==const:
                    sorted_container.append(entry)
     
        inner[str("constants")]=sorted_container
        
        #We also have to add the length on each list for each state
        number_of_constants=len(container)
        if number_of_constants==0:
            remaining=0
            rowspan=1
        else:
            remaining=number_of_constants-1
            rowspan=number_of_constants
        inner[str("rowspan")]=rowspan
        inner[str("remaining")]=remaining
        common[state]=inner
        
       
    
    
    # 5) Sort the common dictionary accriding to molecules
    main={}
    for molecule in unique_molecules:
        d1={}
        
        for key, value in common.items():
            if str(molecule) in str(key):
                d1[str(key)]=value
                 
        main[molecule]=d1
    
    
    variables={'unique_molecules':mol_list,       
               'test_dictionary':test_dictionary,
               'unique_states': unique_states,         
               'common':common,
               'main':main,
               'e_constants':e_constants}  
    return render(request, 'spectrum/f_main_table.html', variables)
 





# Same function as above. Can be deleted later

def debug_1(request):
     # 1) Find unique molecules list
    unique_molecules=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    unique_molecules=sorted(unique_molecules)
    mol_list=[]
    for i in unique_molecules:
        mol_list.append(str(i))

    test_dictionary={}
    count=1
    for i in unique_molecules:
        test_dictionary[i]=count
        count+=1


    # 2) Find unique states list
    unique_states=Molecular_state.objects.all()
   
   
  
    # 3) Makes list of needed constants
    constant_source=Constant_type.objects.all()
    e_constants=[]
    for i in constant_source:
        if "e" in i.symbol:
            e_constants.append(i)
   

 
   
   
    # 4) For each of state find entry from Diatomic_constant
    common={}
    for state in unique_states:
        inner={}
        inner[str("state_object")]=state
        # This data contains all types of constants
        # We need to filter them, so only 'equilibrium' constants are here
        data_of_state=Diatomic_constant.objects.filter(molecular_state=state)
        
        container=[]
        for i in data_of_state:
            if "e" in i.constant_type.symbol:
                container.append(i)  


        # Now we need to order the entries of the container.
        sorted_container=[]
        for const in e_constants:
            for entry in container:
                if entry.constant_type==const:
                    sorted_container.append(entry)
     
        inner[str("constants")]=sorted_container
        
        #We also have to add the length on each list for each state
        number_of_constants=len(container)
        if number_of_constants==0:
            remaining=0
            rowspan=1
        else:
            remaining=number_of_constants-1
            rowspan=number_of_constants
        inner[str("rowspan")]=rowspan
        inner[str("remaining")]=remaining
        common[state]=inner
        
       
    
    
    # 5) Sort the common dictionary accriding to molecules
    main={}
    for molecule in unique_molecules:
        d1={}
        
        for key, value in common.items():
            if str(molecule) in str(key):
                d1[str(key)]=value
                 
        main[molecule]=d1
    
    
    variables={'unique_molecules':mol_list,       
               'test_dictionary':test_dictionary,
               'unique_states': unique_states,         
               'common':common,
               'main':main,
               'e_constants':e_constants}  
    return render(request, 'spectrum/z_hello.html', variables)
 





# can delete later
def debug_2(request):
    states=Molecular_state.objects.filter(symbol="11BO")
    
    main={}
    for state in states:
        constants=Diatomic_constant.objects.filter(molecular_state=state)
        main[str(state)]=constants 
    
    variables={'main':main}
    return render(request, 'spectrum/z_hello.html', variables)



################################# BLOCK 1 #####################################
# This block with the following scheme:
# Molecules_list/Molecule/Paper_name

# FUNCTION 1. 
# THis function produces the list of unique molecules.
# Excluding isotopologs with numbers.

def unique_molecules(request):
    with_numbers=Molecular_state.objects.values_list('symbol', flat=True).distinct()
    without_numbers=[]
    for string in with_numbers:
        result=''.join([i for i in string if not i.isdigit()])
        without_numbers.append(result)
    
    without_numbers=set(without_numbers)
    without_numbers=sorted(without_numbers)
    variables={'molecules_list':without_numbers}
    return render(request, 'spectrum/a_molecules_list.html', variables)
    




# FUNCTION 2.
# This function produces table of isotopologs, states, and constants

def table_for_molecule(request,molecule_name):
    # Make list of e_constants types
    constant_source=Constant_type.objects.all()
    equilibrium_types=[]
    for i in constant_source:
        if "e" in i.symbol:
            equilibrium_types.append(i)




    data=Molecular_state.objects.all()
    
    states_list=[]
    for state in data:
        name_with_numbers=state.symbol 
        no_numbers=''.join([i for i in name_with_numbers if not i.isdigit()])
        
        if str(no_numbers) == str(molecule_name):
            states_list.append(state)
    
    # Now find all isotopologs. Even if there is only one
    isotopologs=[]

    for entry in states_list:
        name=entry.symbol
        if name not in isotopologs:
            isotopologs.append(name)
    isotopologs=sorted(isotopologs)

    # FOr each isotopolog find the list of states
    main={}
    for isotopolog in isotopologs:
        d1={}
        states_of_isotopolog=[]
        for state in states_list:
            if state.symbol==isotopolog:
                states_of_isotopolog.append(state)
    
        # FOr each of the state, find ALL constans
        for state in states_of_isotopolog:
            inner={}
            all_constants_of_state=Diatomic_constant.objects.filter(molecular_state=state)
            
            # Filter those with 'e' them
            e_constants=[]
            for const in all_constants_of_state:
                if "e" in const.constant_type.symbol:
                    e_constants.append(const)
            

            # Now e_constants list must be sorted according to order of equilibrium_types
            sorted_e_constants=[]
            for const_th in equilibrium_types:
                for const in e_constants:
                    if const_th.symbol==const.constant_type.symbol:
                        sorted_e_constants.append(const)

            # a) First find unique_papers and make list
            unique_papers=[]
            for entry in sorted_e_constants:
                if entry.reference_publication.reference_publication_tag not in unique_papers:
                    unique_papers.append(str(entry.reference_publication.reference_publication_tag))
            
            # b) Find constants for each paper and put into list for each paper
            '''
            papers_and_values={}
            for paper in unique_papers:
                constants_of_paper=[]
                for const in sorted_e_constants:
                    if const.reference_publication.reference_publication_tag==paper:
                        constants_of_paper.append(const)
                papers_and_values[str(paper)]=constants_of_paper
           '''
            ############### NEW ATTEMPT ##############################################
            papers_and_values={}
            for paper in unique_papers:
                all_const_of_paper={}
                for e_type in equilibrium_types:
                    the_list=[]
                    for const in sorted_e_constants:
                        if const.reference_publication.reference_publication_tag==paper:
                            if const.constant_type.symbol==e_type.symbol:
                                the_list.append(const)
                        all_const_of_paper[str(e_type)]=the_list

                papers_and_values[str(paper)]=all_const_of_paper
                    

            ###########################################################################
 

            #inner[str("constants")]=sorted_constants
            inner[str("state_object")]=state
            inner[str("ordered_papers")]=unique_papers  
            inner[str("papers_and_values")]=papers_and_values        
            

            # Here is the difference.
            # ROWSPAN must be the number of unique papers, but
            # not the number of available constants

            number_of_papers=len(unique_papers)
            if number_of_papers==0:
                remaining=0 
                rowspan=1
            else:
                remaining=number_of_papers-1
                rowspan=number_of_papers
            inner[str("rowspan")]=rowspan
            inner[str("remaining")]=remaining
            d1[str(state)]=inner
        
        main[isotopolog]=d1
        
    


    # Prepare descriptions for each symbol in equilibrium_types#
    # This is because in HTML for loop is used, hence we need
    # to preliminarily prepare them
    
    descriptions=[ 
                    "Minimum electronic energy (1/cm)" ,
                    "internuclear distance (Angstrom)",
                    "rotational constant in equilibrium position (1/cm)",
                    "vibrational constant - first term (1/cm)",
                    "vibrational constant - second term (1/cm)",
                    "vibrational constant - third term (1/cm)",
                    "rotational constant - first term  (1/cm)",
                    "rotational constant - first term, centrifugal force (1/cm)",
                    "rotation-vibration interaction constant (1/cm)",
                    "centrifugal distortion constant (1/cm)",
                    "UNKNOWN H_E (1/cm)"

                ]
      
    symbols_dictionary={}
    counter=0
    for symbol in equilibrium_types:
        symbols_dictionary[str(symbol)]=descriptions[counter]
        counter+=1

    
    variables={'states':states_list,
               'name':molecule_name,
               'isotopologs':isotopologs,
               'main':main,
               'equilibrium_types':equilibrium_types,
               'symbols_dictionary':symbols_dictionary}
                                
    return render(request, 'spectrum/d_molecule_states_table.html',variables)
    
  
# FUNCTION 3. 
# This function shows the info about specific paper for specific ISOTOPOLOG

def paper_info(request, isotopolog, paper):
    paper_object=Reference_publication.objects.filter(reference_publication_tag=paper)    

  
    # Now let's find all states and constants mentioned in this paper
    # a) All constants
    all_constants=Diatomic_constant.objects.all()
    
    # b) Loop over all constants and find those with given paper
    constants_of_paper=[]
    for entry in all_constants:
       
        if entry.reference_publication.reference_publication_tag == paper:
            constants_of_paper.append(entry)
        
    # c) Find number of constants for this paper
    number_of_constants=len(constants_of_paper) 

    # d) Find number of states mentioned in this paper
    states_of_paper=[]
    for entry in all_constants:
        if entry.reference_publication.reference_publication_tag == paper:
            if entry.molecular_state not in states_of_paper:
                states_of_paper.append(entry.molecular_state)

    number_of_states=len(states_of_paper)

    variables={ 'paper_object':paper_object[0],
                'paper_name':paper,
              # 'constants_of_paper':constants_of_paper
                'number_of_constants':number_of_constants,
                'number_of_states':number_of_states
              } 




    return render(request, 'spectrum/e_paper_info.html', variables)








