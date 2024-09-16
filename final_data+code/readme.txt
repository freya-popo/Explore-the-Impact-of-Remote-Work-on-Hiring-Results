This is code built by Freya Xinran Zhang pre-processing Glassdoor data.

Data from three sectors: manufacturing, retailing, and finance.

built with
	python
	sklearn
	numpy
	autogluon
	pandas


data and code
	1. plans: crawler steps for 3 steps
    	2. step1: code and data used in step1
		a. code
			i. 3 python files for 3 industries
			ii. 12 folders of results of autogluon models
		b. input
			i. initial: raw data from the outsourcing company
			ii. 3 combined dataset of 3 industries
		c. output
			processed dataset of 3 industries
	3. step2: code and data used in step2
		a. jobs
			i. code
			ii. input: information of opening jobs in different locations
		b. remote jobs
			i. code
			ii. input: information of available remote jos in different locations
		c. ratings from diff groups
			i. code
			ii. input:  information of ratings from different user groups
	  in step2, there is no output files. the output is some tables in latex mode from the running codes.
	  also, the code in each sub-step is universal for different industries
	4. step3:
		a. C&P
			i. code: codes for 3 industries respectively
			ii.input: raw data
			iii.output: for each industry, there are 3 files: ' processed data', 'word frequency of cons' and 'word frequency of pros'
		b. reviews
			i. code: one python file universal for 3 industries to process data of reviews
			ii. input: raw data of reviews
			iii. output: for each industry, there are 4 files: word frequency of cons of group1; word frequency of cons of group2; word frequency of pros of group1; word frequency of pros of group2
