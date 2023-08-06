# BIOMATCHER
BioMatcher is a software that allows you to find identical seeds between human microRNA and plant microRNA, within a position of your choice.

## How to install BioMatcher
To install BioMatcher, you need to write to the console:

    pip install BioMatcher

## How to run Matcher
To start the software, you need to type the following command line string in your terminal:<br> `match -h fileh -p filep -c jsonconfig -o fileo -hid jsonidhuman -pid jsonidplant`<br>
The files to provide in input in particular are the following:
- `fileh` = This is the path of fasta file of human microRNA
- `filep` = This is the path of fasta file of plant microRNA
- `jsonconfig` = This is the JSON containing all the types of comparisons you want to make
The structure of the json file must be like this:
```
	{
		"exact_matches":[  
			{  
			"id": "h2-8p2-8",  
			"h_start": "2",  
			"h_end": "8",  
			"p_start": "2",  
			"p_end": "8",  
			"active": "True"  
			}
	}
```
In this file, the default standard comparisons will be present. Furthermore, it is possible to enter one or more comparisons to perform. To add a new comparison, you will need to add a structure similar to the one already present in the JSON file. Finally, through the "active" parameter, existing comparisons can be activated (True) or deactivated (False), without having to cancel any comparison.
- `fileo` = This is the path of output csv file
- `jsonidhuman` = This is the path to the JSON file containing all the human IDs to be considered in the process (optional). Its structure must be as in this example:
```
	{  
		"id_human":[  
			"MIMAT0000062",  
			"MIMAT0002826"  
			]  
	}
```
- `jsonidplant` = This is the path of the JSON file containing all the plant IDs to be taken into consideration in the process (optional). Its structure must be as in this example:
```
	{  
		"id_plant":[  
			"MIMAT0016317",  
			"MIMAT0016318"  
			]  
	}
```
When the software ends, you can find all the corresponding seeds in the csv output file chosen by you in the following format:

| Human ID | Plant ID | Comparison IDs |
|:--------:| --------:| -------------:|

## How to run Filter
 This component is used to filter the FASTA file with selected species. To start the Filter software, you need to type the following line of code into your terminal:

    filter –m filem –s jsonspecies –o fileo

The files to provide in input in particular are the following:
- `filem` = This is the path of the FASTA file of the microRNAs to be filtered
- `jsonspecies` = This is the path of the JSON file of the selected species to filter the FASTA file. The structure of this file will be:
```
	{  
		"selectedspecies":[  
			"Acacia auriculiformis",  
			"Arabidopsis lyrata",  
			"Acacia mangium"  
			]  
	}
```
- `fileo` = This is the path to the output FASTA file

## How to run Cleaner
This component is used to clean up the FASTA input file from errors and redundancies. To start the Cleaner software, you need to type the following line of code into your terminal:

    cleaner –m filem –o fileo –e errors –r redundancies
The files to provide in input in particular are the following:
- `filem` = This is the path of the FASTA file of the microRNAs to be cleaned up
- `fileo` = This is the path of the cleaned FASTA output file
- `errors` = This is the path to the output FASTA file containing all the microRNAs with errors
- `redundancies` = This is the path to the output CSV file with all the redundant sequence IDs. Its structure will be:

| Main ID | Redundant IDs|
|:--------:| --------:|