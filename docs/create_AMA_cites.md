## Creating Valid AMA Citation(s) for Each Row

We do not implement all the APA citation rules given we have limited kinds of research in our database. Here's what we have implemented, split by type of research:  

* **Journal Articles**

    * We use rules specified here: https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf

    * We ignore:
        * Journal Supplements
        * Government Publication
        * Newspaper Article
        * Dictionary
        * Unpublished Material
        * CDROM

    * We implement rules for number of authors specified [here (pdf)](https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf) but ignore:
        - Two or More Works by the Same Author. People citing multiple retracted articles by the same author is uncommon. We leave it for later.
        - Introductions, Prefaces, Forewords, and Afterwords

    * If there is a group_author, we follow advice from https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf

    * If the article is a special issue, follow directions [here](https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf)

* **Online Articles**

    We ignore online articles because we don't have them in our data. But the general rules are phere](http://library.nymc.edu/informatics/amastyle.cfm). Add the phrase 'retrieved from' when building references. Rules for the number of authors are the same as for journal articles. 

* **Conference Papers**

    We only implement rules for Papers and Poster Sessions listed [here](https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf). If an article has both "article_title" and "conf_title", we generate two separate citations for the article---one for the conference, other for the journal article. Rules for multiple authors are the same as above.

**Verifying Work**

We verify the references we produce by comparing against [http://scholar.google.com](scholar.google.com) and some manual sifting.
