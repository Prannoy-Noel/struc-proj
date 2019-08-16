# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 15:25:58 2019

@author: VinitaKumari
"""
#from unidecode import unidecode as u
#import codecs
def document_finder(input_path)  :
    f = open(input_path,errors='ignore')

    lines = f.read()
    f.close()
    if lines == '':
       return False

    all_words =[]
    for i in lines:
        words = i.split(" ");
        print(words)
        all_words.append(words)
#        if all_words == []:
#            print('Document is empty')
        class_dict ={'Invoice': 0 ,'Credit': 0,'Purchase_order':0}
        Credit = 0
        Invoice = 0
        Purchase_order = 0
        some_words = all_words[0:23]

    for a in some_words:

        for b in a:
            if b.lower() == 'invoice':
    #            print('class is invoice for',b )
                Invoice = Invoice + 1
                class_dict['Invoice'] = Invoice
            elif b.lower() == 'credit':
                Credit = Credit + 1
                class_dict['Credit'] = Credit
#                print
#            else:
#                Others = Others +1
#                class_dict['Others'] = Others

            elif b.lower() == 'purchase':
                 Purchase_order = Purchase_order + 1
                 class_dict['Purchase_order'] = Purchase_order


#print("all words are captured here", all_words)
#    print(class_dict)
    sorted_dict = sorted(class_dict.items(), key=lambda x: x[1], reverse=True )
    final_class = list(sorted_dict[0])
    Document_type = final_class[0]
    return Document_type
#    final_class_info = " The Class of Document is" + " " +  final_class[0]
#    print('final_class',final_class_info)

def remove_non_ascii_1(text):
#    return u(text)
    return ''.join(i for i in text if ord(i)<128)

def document_classifier(input_path):

    #try:
    #    f = open(input_path,"r",encoding="utf8",errors='ignore');
    #except:
    removed_text = remove_non_ascii_1(input_path)
#    print(removed_text)
    Document_type =[]
    f = open(input_path, errors='ignore')
    text = f.read()
    f.close()
    if 'CREDIT NOTE' in text:
        Document_type = ['Credit']
    elif 'CREDIT INVOICE' in text:
         Document_type = ['Credit']
    elif 'CREDIT MEMO' in text:
         Document_type = ['Credit']
    else:
         Document_type = document_finder(removed_text)


    if document_finder(removed_text) == ['Purchase_order']:
        Document_type == ['Other - Type Purchase Copy']

    if Document_type == 'Invoice':
        return {'Credit_Note': ['No'],'confidence_score':[1]}
    elif Document_type == 'Credit':
        return {'Credit_Note':['Yes'],'confidence_score':[1]}
    else:
        return False
#    elif Document_type == ['Other - Type Purchase Copy']:

#    print('the final result is ',Document_type)

#document_classifier(r'C:/Users/PrachiRani/Documents/RICOH/merged first time on 5th/source/6/6_000001.txt')
