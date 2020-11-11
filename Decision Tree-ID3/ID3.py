# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:17:06 2020

@author: joseb
"""
"""
testing dataset

"""
trainingTags=["Stream","Slope","Elevation"]
trainingSet=[["false","true","true","false","false","true","true"],
             ["steep","moderate","steep","steep","flat","steep","steep"], 
             ["high","low","medium","medium","high","highest","high"]]

targetSet=["chapparal","riparian","riparian","chapparal","conifer","conifer","chapparal"]
classet=["chapparal","chapparal","chapparal","chapparal","chapparal","chapparal","chapparal"]


import math

"""
Auxiliary functions
Auxiliary functions are used to perform repetitive tasks such as calculate the
entropy and remaining entropy of a set  
"""
#Calculates the entropy of a single feature 
def entropy (feature):
    frecuencies={}
    categories=[]
    prob_distribution={}
    feature_entropy=0
    #The feature is classfied according to its possible instances
    for i in feature:
        if i  not in  categories:
            categories.append(i)
            frecuencies[i]=1
            prob_distribution[i]=0
        else:
            frecuencies[i]+=1
    #We calculate the probability distribution of the feature 
    #and the feature entropy
    for i in frecuencies:
        prob_i=frecuencies[i]/len(feature)
        prob_distribution[i]=prob_i
        feature_entropy+=-(prob_distribution[i]*math.log(prob_distribution[i],2))
    return feature_entropy       

#The partitions method will split the data set for each descriptive feature into
#subsets to be analyzed indivudally for entropy 
def partition(feature,target):
    categories=[]
    partitions=[]
    #we evaluate how many partitions can be based on the values of the 
    #descriptive feature, and then we create subsets of as many partitions as we need
    for i in feature:
        if i not in categories:
            categories.append(i)
    for i in categories:
        partitions.append([])        
    #We poputalte the subsets with the extracted data
    for i in range(len(feature)):
        partition_set=categories.index(feature[i])
        partitions[partition_set].append(target[i])
        
    return partitions

#Calculates the remaining entropy of a given descriptive feature
def rem_entropy(feature,partitions):
    categories=[]
    frequencies={}
    prob_distribution=[]
    for i in feature:
        if i not in categories:
            categories.append(i)
            frequencies[i]=1
        else:
            frequencies[i]+=1
    for i in frequencies:
        prob_distribution.append(frequencies[i]/len(feature))
    total_entropy=0
    for i in range(len(partitions)):
        total_entropy+=entropy(partitions[i])*prob_distribution[i]
    
    return total_entropy
#The function traverse tree will travel the decision tree with a given query
#and will return a prediction based on it , it requires that the tree is built
def traverseTree():
    pass
#the function create set will load the data set into a node:

def createNode(trainingData,targetData,dataTags):
    node=Node()
    node.TrainingSet=trainingData
    node.TargetData=targetData
    node.TrainingTags=dataTags
    return node 
"""
Data Structures

Partition: Will store the training and target data
Node: will store the partition data and will perform operations on it (entropy etc.)
Tree: Will store nodes and  create the decision path 
"""
"""
Partition
"""
class Partition():
    def __init__(self):
        self.Feature=""
        self.Training=[]
        self.Target=[]
        self.TrainingTags=[]
        self.Entropy=0
    def getTraining(self):
        return self.Training
    def getTarget(self):
        return self.Target
    def getTrainingTags(self):
        return self.TrainingTags
    def getFeature(self):
        return self.Feature
    

"""
DataSet Class

"""

#The DataSet class will handle all the partition and entropy calculation opeartions
#Each it will store , not only the information of a given data set but also its partitions
#And descriptive values 
class DataSet():
    def __init__(self):
        self.Parent=None
        self.Partitions=[]
        self.Children={}
        self.TrainingSet=[]
        self.TargetData=[]
        self.TrainingTags=[]
        self.PartitionFeature=""
        self.leaf=False
        self.isEmpty=False
        self.classified=False
    def selectPartitionFeature(self,setEntropy):
        training=self.TrainingSet
        target=self.TargetData
        selectedIndex=0
        highestInfoGain=0
        for i in training:
            setPartition=partition(i,target)
            partitionEntropy=rem_entropy(i,setPartition)
            infoGain=setEntropy-partitionEntropy
            if infoGain>highestInfoGain:
                highestInfoGain=infoGain
                selectedIndex=training.index(i)
        self.PartitionFeature=self.TrainingTags[selectedIndex]
        return self.PartitionFeature
    
    def createChildren(self):
        for i in self.Partitions:
            child=DataSet()
            child.Parent=self
            child.TrainingSet=i.Training
            child.TargetData=i.Target
            child.TrainingTags=i.TrainingTags
            child.Feature=i.Feature
            self.Children[i.Feature]=child
        return self.Children
    def createPartitions(self):
        if self.PartitionFeature!="":
            partitionIndex=self.TrainingTags.index(self.PartitionFeature)
        else:
            partitionIndex=0
        categories=[]
        #Creates partition objects based on the number of instances 
        #in the selected feature 
        for i in self.TrainingSet[partitionIndex]:
            if i not in categories:
                categories.append(i)
                new_partition=Partition()
                new_partition.Feature=i
                self.Partitions.append(new_partition)
        #Populates the partitions training and target data based on the feature 
        #Variable subsets serves as storage for the partition subsets
        #appends individual lists for each feature in the training set 
        #not counting the feature already removed 
        featureData=self.TrainingSet[partitionIndex]
        filteredData=self.TrainingSet
        filteredTags=self.TrainingTags
        del filteredData[partitionIndex]
        del filteredTags[partitionIndex]
        
        for i in self.Partitions:
            i.TrainingTags=filteredTags
            feature=i.Feature
            k=0
            for m in filteredData:
                i.Training.append([])
                
            while k<len(featureData):
                if featureData[k]==feature:
                    for j in range(len(filteredData)):
                        trainingValue=filteredData[j][k]
                        i.Training[j].append(trainingValue)
                    targetValue=self.TargetData[k]
                    i.Target.append(targetValue)
                k+=1
        return self.Partitions
    def Empty(self):
        if self.TrainingSet==[]:
            self.isEmpty=True
        return self.isEmpty
    def isClassified(self):
        targetInstances=len(self.TargetData)
        if targetInstances>0:
            i=0
            while i<targetInstances-1:
                if self.TargetData[i]==self.TargetData[i+1]:
                    self.classified=True
                else:
                    self.classified=False
                i+=1
        return self.classified
        
        
    def getFeature(self):
        return self.DFeature
    def getPartitions(self):
        return self.Partitions
    def getChildren(self):
        return self.Children
 
    

"""
ID3 Function
"""

def ID3(dataSet,setEntropy,Tags,tree=None):
    dataSet.selectPartitionFeature(setEntropy)
    node=dataSet.PartitionFeature
    dataSet.createPartitions()
    children=dataSet.createChildren()
    if tree is None:
        tree={}
        tree[node]={}
    for i in children:
        if len (children[i].TargetData)==1:
               tree[node][i]=children[i].TargetData
        else:
            children[i].TrainingTags=Tags 
            tree[node][i]=ID3(children[i],setEntropy,Tags)

    return tree
    

        
        
    
    
    
                
    
   
        
    
    
"""
Testing Code
"""

dataSet=DataSet()
dataSet.TrainingSet=trainingSet
dataSet.TargetData=targetSet
dataSet.TrainingTags=trainingTags
setEntropy=entropy(targetSet)
tags=["Stream","Slope","Elevation"]
decisionTree=ID3(dataSet,setEntropy,tags)
print(decisionTree)





