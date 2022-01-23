"""
Created on January 2021

pure test-file to check if parts of new code run correctly before including it into the main code.

@author: Niko Suchowitz
"""
import pandas as pd
import main
from gap_creator import create_gaps
from interpolate_main import fill_and_valid


def versuchsCode():
    """

    :return:
    """
    # read in the file
    df_1 = pd.read_csv('data/own_data/ActualTotalLoad_edited/AT/2018_03_ActualTotalLoad_6.1.A_ATCTA.csv',
                              sep='\t', encoding='utf-8')
    #df_2 = pd.read_csv('data/own_data/ActualTotalLoad_edited/AT/2018_06_ActualTotalLoad_6.1.A_ATCTA.csv',
    #                  sep='\t', encoding='utf-8')
    #df_3 = pd.read_csv('data/own_data/ActualTotalLoad_edited/AT/2018_09_ActualTotalLoad_6.1.A_ATCTA.csv',
    #                   sep='\t', encoding='utf-8')

    #df_original = df_1.append([df_2, df_3])
    df_original = df_1

    # calc missing data in original in percent
    missing_percent_o = round(main.calc_missing_data(df_original), 2)
    print('amount of NaN in original: '+str(missing_percent_o))
    print(missing_percent_o, "Percent is missing Data of AT")

    # fill with gaps
    df_original["DateTime"] = pd.to_datetime(df_original["DateTime"])
    df_original.sort_values(by='DateTime', inplace=True)
    df_original.reset_index(drop=True, inplace=True)
    data_with_gaps = create_gaps(df_original)

    # calc missing data in modified in percent
    missing_percent_m = round(main.calc_missing_data(data_with_gaps), 2)
    print('amount of NaN in modified: '+str(missing_percent_m))
    print(missing_percent_m, "Percent is missing Data of AT")

    # interpolate
    data_with_gaps["DateTime"] = pd.to_datetime(data_with_gaps["DateTime"])
    mapcode_gapfree = 'AT'
    areatypecode = "CTA"
    save_name = '2018_05_test_ActualTotalLoad_6.1.A_'+mapcode_gapfree+'_'+areatypecode
    fill_and_valid(df_original, data_with_gaps, save_name, mapcode_gapfree, missing_percent_m)


if __name__ == '__main__':
    versuchsCode()
