from django import forms
from django.forms import ModelForm, Form

from data_management.models import Molecular_state, Reference_publication, Diatomic_constant, Preferred_set, Constant_type

def test_preferred(instance):
        if (instance.pk != None): 
                msid = instance.molecular_state.molecular_state_id 
                ctid = instance.constant_type.constant_type_id
                rpid = instance.reference_publication.reference_publication_id
                stid = instance.source_type.source_type_id
                ps = Preferred_set.objects.raw('SELECT preferred_set_id WHERE molecular_state=msid AND constant_type=ctid AND reference_publication = rpid AND source_type = stid;')
                try: 
                        psid = ps.preferred_set_id
                        print msid,rpid,ctid,stid
                        return True
                except:
                        return False
        else:
                return False

class BibTeX_entry():
  record_type=""
  title=""
  author=""
  journal=""
  volume=""
  number=0
  pages=""
  year=""
  url=""
  doi=""
  note=""


def get_uniq_symbol_idx(symbol,string,valid,errors):
  symbol_idx = string.find(symbol)
  symbol_idx2 = string.find(symbol,symbol_idx+1)
  if (symbol_idx == -1):
    print ("Malformed file. Found no %s." % (symbol))
    valid = False
  else:
    if (symbol_idx2 != -1): 
      print ("Malformed file. Found multiple %s" % (symbol))
      valid = False

  return (symbol_idx)


def parse_bibtex(text_area_value,bibtex_entries,errors):

 processed_fields = ['title','author','journal','volume','number','pages','year','url','doi','note']

 debug=True
 valid=True
 
 in_record=False
 num_records = 0
 content = text_area_value.splitlines()
 content = [x.strip() for x in content]
 content = [x.replace("`","'") for x in content]

 num_lines=len(content)

 if (debug): print ("read %s lines" % num_lines)
 for idx,line in enumerate(content):
   if (debug): print (idx,line)                  
   if (content[idx] == ''):
     if (debug): print ("Skipping empty line %d" % idx)
   elif (content[idx][:1] == '@'):
     if (in_record):
       errors.append(("Malformed file. Found \"%s\" while in record in line %d" % (line,idx)))
       valid = False
     else:
       in_record=True
       bibtex_entries.insert(num_records,BibTeX_entry())

       num_records += 1
       bracket_idx = get_uniq_symbol_idx('{',line, valid, errors)
       comma_idx = get_uniq_symbol_idx(',',line,valid,errors)
       
       record_type = content[idx][1:bracket_idx]

       if (debug): print ("Found record of type %s" % record_type) 
       bibtex_entries[num_records-1].record_type=record_type
       record_name = content[idx][bracket_idx+1:comma_idx]
       if (debug): print ("Found record name to be %s" % record_name)
 
   else:
    try:       
     if (in_record):
       equal_idx = get_uniq_symbol_idx('=',line,valid,errors)
       open_idx=line.find("{")
       close_idx=line.find("}",len(line)-2)
       field_name=content[idx][0:equal_idx]
       field_value=content[idx][open_idx+1:close_idx]
       
       setattr(bibtex_entries[num_records-1], field_name, field_value)
 
       if (debug): print ("Found field name %s" %field_name)
       if (debug): print ("Found field value %s" %field_value)
         
       if (field_name not in processed_fields):
         if (debug): print ("Ignoring field %s" % field_name)
 
       if(content[idx][len(line)-1:]!=','):
         try:
           if (content[idx+1] == "}"):
             print (content[idx+1])
             last_field = True         
             in_record = False
         except: 
           errors.append(unicode("Unsuspected end of list"))
           valid = False
     elif (not in_record and last_field and content[idx] == "}"):
       if (debug): print ("Reached end of well-formed record")
     else: 
       errors.append(unicode("Malformed file. Found \"%s\" while not in record in line %d" % (line,idx)))
       valid = False
    except: 
      valid = False
      errors.append(unicode("Malformed file. Did not find a record."))

 return valid

class Molecular_state_form(ModelForm):
        def __init__(self, *args, **kwargs):
                super(Molecular_state_form, self).__init__(*args, **kwargs)
                self.fields['name'].required = True

	class Meta:
		model = Molecular_state
		fields = ['name', 'symbol','excitation_index','total_electronic_spin','electronic_symmetry','projected_angular_momentum','parity']
                labels = {
                        "name": "Molecular state description, e.g. OH_X2Pi",
                        "symbol": "Molecule name",
                        "excitation_index": "Electronic state Label",
                        "total_electronic_spin": "Electronic Spin (2S+1)",
                        "projected_angular_momentum": "Projected Angular Momentum (opt.)",
                        "parity": "Parity (opt.)"
                }


class Reference_publication_form(ModelForm):
        def __init__(self, *args, **kwargs):
                super(Reference_publication_form, self).__init__(*args, **kwargs)
                self.fields['reference_publication_tag'].required = True
	class Meta:
		model = Reference_publication
		fields = ['reference_publication_tag','entry_type','author','title','journal','year','volume','doi','url','number','pages','note']


class Reference_publication_from_bib_form(Form):
        bibtex_entries=[]
        messages=[]
        messages.append(unicode("Please enter one BibTeX entry at a time"))

        def __init__(self, *args, **kwargs):
                super(Reference_publication_from_bib_form, self).__init__(*args, **kwargs)
        
        tag_field = forms.CharField(label='Reference publication tag:')
        bib_field = forms.CharField(label='BibTeX entry:',widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}))
 
        def is_valid(self):
          valid = super(Reference_publication_from_bib_form, self).is_valid()
               
          if not valid:           
            return valid

            
          valid = parse_bibtex(self.cleaned_data['bib_field'],self.bibtex_entries,self.messages)     
          if (valid):
            if self.bibtex_entries[0].title == '': 
                  self.messages.append(unicode("Please add a title"))
                  valid=False

            if self.bibtex_entries[0].author == '': 
                  self.messages.append(unicode("Please add an author"))
                  valid=False

            if self.bibtex_entries[0].year == '': 
                  self.messages.append(unicode("Please add a year"))
                  valid=False

            if self.bibtex_entries[0].journal == '': 
                  self.messages.append(unicode("Please add a journal"))
                  valid=False

            if self.bibtex_entries[0].volume == '': 
                  self.messages.append(unicode("Please add a Volume"))
                  valid=False
  
          if not valid:
            self.message = self.messages[-1]          

          return valid

        def save(self):          
          rp = Reference_publication(reference_publication_tag=self.cleaned_data['tag_field'],
                                     entry_type = self.bibtex_entries[0].record_type,
                                     title = self.bibtex_entries[0].title,
                                     author=self.bibtex_entries[0].author,
                                     journal=self.bibtex_entries[0].journal,
                                     volume=self.bibtex_entries[0].volume,
                                     number=self.bibtex_entries[0].number,
                                     pages=self.bibtex_entries[0].pages,
                                     year=self.bibtex_entries[0].year,
                                     url=self.bibtex_entries[0].url,
                                     doi=self.bibtex_entries[0].doi,
                                     note=self.bibtex_entries[0].note)
          rp.save()
            
            

class Diatomic_constant_form(ModelForm):
        molecular_state = forms.ModelChoiceField(queryset=Molecular_state.objects.order_by('name'))
        constant_type = forms.ModelChoiceField(queryset=Constant_type.objects.order_by('symbol'))

        def __init__(self, *args, **kwargs):
                super(Diatomic_constant_form, self).__init__(*args, **kwargs)                
                self.fields['is_preferred'] = forms.BooleanField(initial=test_preferred(self.instance), required=False)
                self.Meta.fields.append('is_preferred')




	class Meta:
		model = Diatomic_constant
                fields = ['molecular_state','reference_publication','source_type','constant_type','value','delta_plus','delta_minus']
                labels = {
                        "delta_plus": "Delta+ (opt.)",
                        "delta_minus": "Delta- (opt.)",
                        "is_preferred": "Is prefered (opt.)"
                        }

#form = Molecular_state_form()
#ms =  Molecular_state.objects.first()
#form = Molecular_state_form(instance=ms)

