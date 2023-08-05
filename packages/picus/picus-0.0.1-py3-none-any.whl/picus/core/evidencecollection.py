# coding: utf-8

'''
# Criteria

## Pathogenic

### Pathogenic Very Strong
* PVS1 null variant (nonsense, frameshift, canonical ±1 or 2 splice sites, initiation codon, single or multiexon deletion) in a gene where LOF is a known mechanism of disease

### Pathogenic Strong
* PS1 Same amino acid change as a previously established pathogenic variant regardless of nucleotide change
* PS2 De novo (both maternity and paternity confirmed) in a patient with the disease and no family history
* PS3 Well-established in vitro or in vivo functional studies supportive of a damaging effect on the gene or gene product
* PS4 The prevalence of the variant in affected individuals is significantly increased compared with the prevalence in controls

### Pathogenic Moderate
* PM1 Located in a mutational hot spot and/or critical and well-established functional domain (e.g., active site of an enzyme) without benign variation
* PM2 Absent from controls (or at extremely low frequency if recessive) (Table 6) in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium
* PM3 For recessive disorders, detected in trans with a pathogenic variant
* PM4 Protein length changes as a result of in-frame deletions/insertions in a nonrepeat region or stop-loss variants
* PM5 Novel missense change at an amino acid residue where a different missense change determined to be pathogenic has been seen before
* PM6 Assumed de novo, but without confirmation of paternity and maternity

### Pathogenic Supporting
* PP1 Cosegregation with disease in multiple affected family members in a gene definitively known to cause the disease
* PP2 Missense variant in a gene that has a low rate of benign missense variation and in which missense variants are a common mechanism of disease
* PP3 Multiple lines of computational evidence support a deleterious effect on the gene or gene product (conservation, evolutionary, splicing impact, etc.)
* PP4 Patient’s phenotype or family history is highly specific for a disease with a single genetic etiology
* PP5 Reputable source recently reports variant as pathogenic, but the evidence is not available to the laboratory to perform an independent evaluation

## Benign

### Benign Stand-alone
* BA1 Allele frequency is >5% in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium

### Benign Strong
* BS1 Allele frequency is greater than expected for disorder
* BS2 Observed in a healthy adult individual for a recessive (homozygous), dominant (heterozygous), or X-linked (hemizygous) disorder, with full penetrance expected at an early age
* BS3 Well-established in vitro or in vivo functional studies show no damaging effect on protein function or splicing
* BS4 Lack of segregation in affected members of a family

### Benign Supporting
* BP1 Missense variant in a gene for which primarily truncating variants are known to cause disease
* BP2 Observed in trans with a pathogenic variant for a fully penetrant dominant gene/disorder or observed in cis with a pathogenic variant in any inheritance pattern
* BP3 In-frame deletions/insertions in a repetitive region without a known function
* BP4 Multiple lines of computational evidence suggest no impact on gene or gene product (conservation, evolutionary, splicing impact, etc.)
* BP5 Variant found in a case with an alternate molecular basis for disease
* BP6 Reputable source recently reports variant as benign, but the evidence is not available to the laboratory to perform an independent evaluation
* BP7 A synonymous (silent) variant for which splicing prediction algorithms predict no impact to the splice consensus sequence nor the creation of a new splice site AND the nucleotide is not highly conserved
'''

import pandas as pd
import json


class EvidenceCollection:
    def __init__(self):
        self.variant_info_cols = [
            'CHR', 'POS', 'GT', 'AD',
            'id', 'gene_symbol', 'transcript_id',
            'hgvsc', 'hgvsp',
            'transcript_consequence_terms', 'evidences'
        ]

    def collect_evidences(self, df):
        # To Do (evidences to collect)
        # PM1
        # PP2
        # BP1
        df['PVS1'] = df.apply(self.get_PVS1, axis=1)
        df['BA1'] = df.apply(self.get_BA1, axis=1)
        df['PM2'] = df.apply(self.get_PM2, axis=1)

        df['evidences'] = '{' + \
            '"PVS1": ' + df['PVS1'] + \
            ', "BA1": ' + df['BA1'] + \
            ', "PM2": ' + df['PM2'] + \
            '}'
        variants = json.loads(
            df[self.variant_info_cols].to_json(orient='records'))
        for variant in variants:
            variant['evidences'] = json.loads(variant['evidences'])
        return variants

    def get_PVS1(self, df):
        LOF_genes = ["ATM", "BARD1", "BLM", "BRCA1", "BRCA2", "BRIP1", "CDH1", "CFTR", "CHEK2", "EPCAM", "MEFV", "MEN1", "MLH1", "MSH2",
                     "MSH6", "MUTYH", "NBN", "PALB2", "PMS2", "PTEN", "RAD50", "RAD51C", "RAD51D", "STK11", "TP53", "XRCC2", "MRE11A", "APC", "PIK3CA"]
        null_variants = ["transcript_ablation", "splice_acceptor_variant", "splice_donor_variant", "stop_gained", "frameshift_variant", "stop_lost",
                         "start_lost", "transcript_amplification", "inframe_insertion", "inframe_insertion", "inframe_deletion", "missense_variant", "protein_altering_variant"]
        if df['gene_symbol'] in LOF_genes and df['transcript_consequence_terms'] in null_variants:
            return '1'
        else:
            return '0'

    def get_BA1(self, df):
        if df['minor_allele_freq'] > 0.05 or df['gnomad'] > 0.05:
            return '1'
        else:
            return '0'

    def get_PM1(self, df):
        pass

    def get_PM2(self, df):
        if pd.isna(df['id']):
            return '1'
        else:
            return '0'
