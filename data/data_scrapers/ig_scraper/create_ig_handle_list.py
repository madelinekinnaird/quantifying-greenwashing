import pandas as pd


def main(df, column):
    '''
    Function:
    Input:
    Output:
    '''
    f = open("batch.txt","w+")
    ## make sure column is type string
    data[column] = data[column].astype(str)
    for row in df[column]:
        ## skip rows with an x
        if row == 'x':
            pass
        else:
            print(row)
            f.write(row + '\n')

    f.close()



## import list of fortune 500 companies
data = pd.read_csv('../data/fortune_500_companies.csv')

## run function to get a text file of instagram handles
main(data,'INSTAGRAM')
