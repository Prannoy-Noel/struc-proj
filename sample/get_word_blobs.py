# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:59:07 2019

@author: DarshilKapadia
"""

def NMS(word_blobs,image_path):
    
    word_blobs_new=[]
    for i in range(len(word_blobs)):
        flag = True
        for j in range(len(word_blobs)):
            if i == j:
                continue
            [x1a,y1a,x2a,y2a] = word_blobs[i]['coordinates']
#            wa = x2a - x1a
#            ha = y2a - y1a
            [x1b,y1b,x2b,y2b] = word_blobs[j]['coordinates']
            wb = x2b-x1b
            hb = y2b-y1b
            if x1a >= x1b-(0.01)*(wb) and y1a >= y1b-(0.01)*(hb) and x2a <= x2b+(0.01)*(wb) and y2a <= y2b+(0.01)*(hb):              
                flag = False
                break

        if flag:
            word_blobs_new.append(word_blobs[i])
    
    return word_blobs_new

def get_word_blobs(word_dict,image_path,lines):
    
    '''
    Making blobs:
    '''
    
    word_blobs=[]
    
    active_word_flag = [True]*len(word_dict['coordinates'])
    curr_blob=[]
    
    curr_idx=0
    while(True):
    #    print(len(curr_blob))
        curr_idx+=1
    #    print(curr_idx,len(curr_blob))
        if curr_idx >= len(curr_blob):
    #        print('xxx')
            word_blobs.append(curr_blob)
            curr_idx=0
            curr_blob = [active_word_flag.index(True)]
        if active_word_flag[curr_blob[curr_idx]]:
            [x1a,y1a,x2a,y2a] = word_dict['coordinates'][curr_blob[curr_idx]]
            for w_jdx in range(len(word_dict['coordinates'])): 
                if w_jdx in curr_blob or not active_word_flag[w_jdx]:
                    continue
                [x1b,y1b,x2b,y2b] = word_dict['coordinates'][w_jdx]
                
                if (x2a-x1a) > (x2b-x1b):
                    if len(word_dict['value'][curr_blob[curr_idx]]) < 3:
                        width_to_consider = (x2a-x1a)
                    elif len(word_dict['value'][curr_blob[curr_idx]]) < 6:
                        width_to_consider = 0.5*(x2a-x1a)
                    else:
                        width_to_consider = 0.25*(x2a-x1a)
                else:
                    if len(word_dict['value'][w_jdx]) < 3:
                        width_to_consider = (x2b-x1b)
                    elif len(word_dict['value'][w_jdx]) < 6:
                        width_to_consider = 0.5*(x2b-x1b)
                    else:
                        width_to_consider = 0.25*(x2b-x1b)
                if ( ((x2a + width_to_consider) > x1b > (x1a - width_to_consider)) and ((y2a + (y2a-y1a)) > y1b > (y1a - (y2a-y1a))) ) :
                    flag_line = True
                    for line in lines:
                        [(x1l,y1l),(x2l,y2l)] = line
                        cond1 = ( min(x1a,x1b) < min(x1l,x2l) <= max(x1l,x2l) < max(x1a,x1b) ) and ( min(y1l,y2l) < min(y1a,y1b) < max(y2a,y2b) < max(y1l,y2l) )
                        cond2 = ( min(y1a,y1b) < min(y1l,y2l) <= max(y1l,y2l) < max(y1a,y1b) ) and ( min(x1l,x2l) < min(x1a,x1b) < max(x2a,x2b) < max(x1l,x2l) )
                        
                        if cond1 or cond2: 
                            flag_line = False
                            break
            #            print('*')
                    if flag_line:
                        curr_blob.append(w_jdx)
        
            active_word_flag[curr_blob[curr_idx]] = False
        if not any(active_word_flag):
            break
        
    
    word_blobs.append(curr_blob)
    word_blobs = [x for x in word_blobs if x!=[]]
    word_blob_coords = []
    for blob in word_blobs:
        blob_x1 = min([word_dict['coordinates'][x][0] for x in blob])
        blob_y1 = min([word_dict['coordinates'][x][1] for x in blob])
        blob_x2 = max([word_dict['coordinates'][x][2] for x in blob])
        blob_y2 = max([word_dict['coordinates'][x][3] for x in blob])
        word_blob_coords.append({'coordinates':[blob_x1,blob_y1,blob_x2,blob_y2],'value':' '.join([word_dict['value'][x] for x in blob])})
        
    word_blob_coords = NMS(word_blob_coords,image_path)
    
    '''
    End
    '''
    
    return word_blob_coords