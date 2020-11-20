# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 03:16:07 2020

@author: Abdelhamid
"""
import copy
import numpy as np

class MCTS():
    def __init__(self, state, br, parent=None, is_terminal=False):
        
        self.state       = state
        self.parent      = parent
        self.children    = []
        self.is_expanded = False
        self.br_factor   = br
        self.is_terminal = False
        self.n_visit     = 0
        self.Q           = 0
        self.U           = -np.NINF
    
    '''##################################### add Node Function ###########################################'''    
    def addNode(self, n_state):
        if self.state:
            if len(self.children)<self.br_factor:
                self.children.append(MCTS(n_state, self.br_factor, self.state))
            else:
                self.children[0].addNode(n_state)
                
    '''##################################### Selction Function ###########################################'''            
    def selection(self):
        self.n_visit += 1
        hist_sel      = []
        while len(self.children):
            values        = np.array([node.Q +node.U for node in self.children])
            index         = np.argmax(values)
            self          = self.children[index]
            self.n_visit += 1  
            hist_sel.append(index)
            
        return hist_sel
    
    '''#################################### simulation Function ###########################################'''
    def simulation(self, hist_sel):
        current = copy.deepcopy(self)
        for index in hist_sel:
            current = current.children[index]
        
        i  = 4
        while not self.is_terminal and i>0:
            n_state     = 4    #just the new state
            is_terminal = True #suppose it is true 
            reward      = 1
            
            current.children.append(MCTS(n_state, self.br_factor, self.state, is_terminal))
            current = current.children[0]
            i -=1
            
        return reward
    
    '''################################## backprobagation Function ##########################################'''
    def backprobagation(self, hist_sel, reward, C, N):
        
        #Update root 
        self.Q  = ((self.n_visit-1)*self.Q + reward)/self.n_visit
        self.U   = C*np.sqrt(np.log(N)/self.n_visit)
        
        #update other selected nodes
        for index in hist_sel:
            self   = self.children[index]
            self.Q = ((self.n_visit-1)*self.Q + reward)/self.n_visit  
            self.U = C*np.sqrt(np.log(N)/self.n_visit)
    

