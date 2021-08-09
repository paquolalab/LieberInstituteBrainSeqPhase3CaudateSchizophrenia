#!/usr/bin/python

__author__ = "KJ Benjamin"

import subprocess
import pandas as pd


def extract_positions():
    wgtlist_file = '../_m/Phase3_Caudate.list'
    with subprocess.Popen('''cut -d . -f 2 %s''' % wgtlist_file,
                          shell=True, stdout=subprocess.PIPE) as p:
        geneids = pd.read_csv(p.stdout, sep='\t', header=None,
                              names=['Geneid'])
    ## Annotate with WGT list
    wgtlist = pd.read_csv(wgtlist_file, sep='\t', header=None, names=['WGT'])
    new_wgt = pd.concat([wgtlist, geneids], axis=1)
    ## Gene annotation
    fn1 = "../../_m/junctions/jxn_annotation.tsv"
    fn2 = "../../../../inputs/counts/text_files_counts/_m/" +\
        "caudate/jxn_annotation.tsv"
    annot = pd.read_csv(fn1, sep='\t', usecols=[0,1], index_col=1)\
              .merge(pd.read_csv(fn2, sep='\t', index_col=0),
                     left_index=True, right_index=True)\
              .rename(columns={'JxnID': 'Geneid', 'start': 'P0',
                               'end': 'P1', 'Symbol': "ID"})
    df = pd.merge(geneids, annot, on='Geneid')
    df.loc[:, 'CHR'] = df.seqnames.str.replace('chr', '', regex=True)
    df.loc[:, "ID"] = df["ID"].fillna(df["Geneid"])
    new_df = new_wgt.merge(df, on='Geneid').drop(['Geneid'], axis=1)\
                                           .sort_values(['CHR', 'P0'])
    return new_df[['WGT', 'ID', 'CHR', 'P0', 'P1']]


def main():
    pos = extract_positions()
    pos.to_csv('Phase3_Caudate.pos', sep='\t', index=False, header=True)


if __name__ == '__main__':
    main()
