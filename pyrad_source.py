from radiomics import featureextractor
from typing import Tuple
import pathlib
from fnmatch import fnmatch
import os
from collections import OrderedDict
import pandas as pd
from handle_csv import split_csv, combine_csv, combine_csv_column_wise

def extract_path_label_cells(dataframe: pd.DataFrame, index: int) -> Tuple[str, str, int]:
    return dataframe.iloc[index]['Image'], dataframe.iloc[index]['Mask'], dataframe.iloc[index]['Label']

def dict_to_df(dict: OrderedDict) -> pd.DataFrame:
    return pd.DataFrame.from_dict(dict, orient='index').transpose()

def calcute_and_export_rad_features(
    file_path: str, 
    featureClass: dict = {}, 
    settings: dict = {}, 
    ) -> bool:
    extractor = featureextractor.RadiomicsFeatureExtractor(**settings, **featureClass)
    extractor.disableAllFeatures()
    extractor.enableFeaturesByName(**featureClass)
    df = pd.read_csv(file_path)
    imagePath, maskPath, Label = extract_path_label_cells(df, 0)
    try:
        result = extractor.execute(imagePath, maskPath, Label)
        df_results = dict_to_df(result)
        df_results.to_csv(f'{os.path.basename(file_path)}', index=False)
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    settings = {}
    settings['binWidth'] = 30 # Only have it for debugging
    settings['sigma'] = [1, 2, 3] # Only have it for debugging
    
    featureClass = {}
    featureClass['firstorder'] =[]
    featureClass['shape'] = []
    featureClass['glcm'] = []
    featureClass['glrlm'] = []
    featureClass['gldm'] = []
    #featureClass['glszm'] =[]
    
    inputFile = pathlib.Path('/Users/dighvijaygiri/Codes/pyrad/csvs/test_eyes.csv')
    split_csv_dir = pathlib.Path('output_csv_files_eyes')
    split_csv(input_csv=inputFile, output_dir=split_csv_dir)
    
    for file_name in os.listdir(split_csv_dir):
        if fnmatch(file_name, '*.csv'):
            file_path = split_csv_dir / file_name
            calcute_and_export_rad_features(file_path=file_path, featureClass=featureClass, settings=settings)

    intermediate_results_path = 'results.csv'
    final_results_path = 'final_results.csv'
    combine_csv(input_dir=os.curdir, output_csv=intermediate_results_path)
    combine_csv_column_wise(inputFile, intermediate_results_path, final_results_path)
    
    
    
    
