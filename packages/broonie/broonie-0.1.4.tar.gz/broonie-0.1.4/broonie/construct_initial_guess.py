##
## A stub to identify needing an initial guess class. In this case it simply RETURN the name
## of a pre generated file that serves as our initial guess
##

###########################################################################

## Basic input file format
## CELL SEX DATE NODEID MOUSE 0610007N19Rik ........

import pandas as pd
import numpy as np
import sklearn.preprocessing
from sklearn import preprocessing

# Bens input data filename 
# /projects/sequence_analysis/vol1/prediction_work/CausalInference/CausalNetworking_forKirk/PCAProjectionImputationPipeline/MouseTumor_allMice_allGenes/mouse_allPhenotypes_regressed_data_allCells_Notscaled.tsv

##########################################################################

def getKnownGroupEffects(fulldata):
    """ Check the input file for KNOWN possible group effects
    Exclude those that may not exist such as TREATMENT. Make no
    assumptions about order or sorting. Return list in arbitrary 
    order. Independent of list provided by the user
    """
    currentPossibleColumnEffects = ['TREATMENT','MOUSE','SEX','DATE','NODEID']
    allColumns = fulldata.columns.values
    # Grab only those fulldata columns that exist inb currentPossible
    foundColumns = list(set(allColumns) & set(currentPossibleColumnEffects))
    print('Number of groupeffect columns in data is '+str(foundColumns))
    print('They are: '+str(foundColumns))
    return (foundColumns)

###############################################################################
# Start the class

class constructInitialGuess(object):
    """
    Just read in Ben's prescaled regressedData
    """

    def reportParameters(self):
        print('Infilename is '+self.inputfilename)
        print('Output metadata '+self.outputInitialGuessfilename)
        print('SPECIAL CASE: Bens data '+self.preregressedfilename)

    def __init__(self, rawinfilename, initialGuessoutputfilename):
        self.inputfilename = rawinfilename 
        self.outputInitialGuessfilename = initialGuessoutputfilename
        self.preregressedfilename = '/projects/sequence_analysis/vol1/prediction_work/CausalInference/CausalNetworking_forKirk/PCAProjectionImputationPipeline/MouseTumor_allMice_allGenes/mouse_allPhenotypes_regressed_data_allCells_Notscaled.tsv'

    def getOutputFilename(self):
        return self.outputInitialGuessfilename
    
    def runInitialGuess(self):
        inputList = self.inputfilename
        inputpreregressedList = self.preregressedfilename
        regressdata  = pd.read_csv(inputpreregressedList,delim_whitespace=True, index_col=0,header=0,low_memory=False)
        #columnEffects = getKnownGroupEffects(regressdata) 
        #df_R = regressdata.drop(columnEffects,axis=1,inplace=False)
        regressdata.to_csv(self.outputInitialGuessfilename,sep=' ') 
        print('Completed initial guess')
