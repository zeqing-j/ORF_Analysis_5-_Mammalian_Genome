# ORF_Analysis_5-_Mammalian_Genome
Data Base 
Multiz470way alignment and conservation data of 470 mammalian species from UCSC Genome Browser was extracted in MAF format using UCSC tools bigBedToBed to convert the data from bigMAF format to MAF format; The exact sequences of 5’ UTRs for each genome in MAF format is obtained based on BED coordinates to extract indexes form original MAF files from UCSC.

Format Conversion
After obtaining MAF format files, a script was generated to modify the format of MAF files to multi-FASTA format, which combines each block of alignment for each species to make a whole UTR alignment for each species.

Feature Detection
uORFs, oORFs, and NTEs were identified in the human 5’ UTR sequences, which was located at first line of every transcript in FASTA file, based on specific criteria. uORF: Contains an AUG start codon and an in-frame stop codon. oORF: Contains an AUG start codon without stop codon but is out-of-frame with the main coding sequence. NTE: Contains an AUG start codon without a stop codon and is in-frame with the main coding sequence. The specific ORF sequences, indexes with dash in multi-FASTA file is stored in excel files. 

ORF Conservation Analysis
ORF regions was aligned across species and calculated percentages of conservation in three ways to account for any mutation in evolution:
1.	Species with exact sequence and location conservation as human ORF.
2.	Species with exact sequence conservation with differing locations due to mutation in other location of the genome 5’ UTR.
3.	Species with In-frame mutations (3-codon deletion/insertion and substitution) that preserving ORF functionality
The 5’ UTR transcripts with sum of three species percentage conservation > 75% were filtered and continue for translation analysis. Those ORFs are translated to amino acid sequences aligned these to species-specific protein sequences. 
Assigned priority scores = length of ORF sequences × conservation percentage 
Transcripts with priority scores the top 30% and only contain NTE and uORFs were submitted to Gene Ontology for enrichment analysis.
