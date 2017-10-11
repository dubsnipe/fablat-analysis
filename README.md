# FABLAT Analysis

##Description

This repo contains data mined by the data_crawler Python script from project Google Drive folders, and the resulting analysis by an R script, both included among the files. The mined data was obtained through two files:

## Files

* ```data_crawler.py```: This is the Python script used to mine data from a Google Drive folder. The folder ID can be specified within the script.
* ```<filename>.txt```: These contain a breakdown of all edits per file in a specific project folder.
* ```<filename>_err.txt```: Error file from the scripts. Despite its name, it contains all the files that don't contain file modifications, but it accounts for file creations. They are factored as edits, mostly useful for files that haven't been edited inside of the Google Drive folders, but have most likely been uploaded.
* The image files in the folder are examples of the resulting analysis by the script.

More information on the analysis used by the scripts [can be found on the RPubs file](http://rpubs.com/dbsnp/fablatanalysis-oct2017).