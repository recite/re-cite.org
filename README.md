## Find Citations to Retracted Articles

[http://re-cite.org](http://re-cite.org) highlights citations to retracted articles. 

Paste citations in APA format, click 'check citations', and voila!

### How Does it Work?

We start by ingesting the [database of retracted articles](https://github.com/recite/retracted_article_database). We then use the APA rules to create valid APA references for each article in the database. (There can be more than one valid reference per article. For instance, if an article is presented at a conference before it is published, where we have the information, we will produce two citations---one for the published piece and one for the conference. We are assuming that when the published article is retracted, the conference paper is technically retracted as well.) At the front-end, the web application parses the pasted text into a list of citations, normalizes the text (converting unicode to ascii and nuking extra spaces), and then highlights any citations that are an exact match based on the DOI or the complete reference, or any citations with a maximum Levenshtein edit distance of 3.  

### Code

* [Code organization](code_structure.md)

* [Directions for installing, configuring, and running the application](install_run_configure.md)

* [Create Database and valid APA References](freshdb.py)
    - Implements the logic discussed [here](create_apa_cites.md)

* Export the final database with APA references to a CSV to check the correctness of references, etc. using [export.py](export.py)

### Authors

Ken Cor, Gaurav Sood, and Khanh Tran

### Contributor Code of Conduct

The project welcomes contributions from everyone! In fact, it depends on it. To maintain this welcoming atmosphere, and to collaborate in a fun and productive way, we expect contributors to the project to abide by the [Contributor Code of Conduct](https://www.contributor-covenant.org/version/1/4/code-of-conduct).

### License

The code is released under the [MIT License](https://opensource.org/licenses/MIT).
