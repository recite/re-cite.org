## Creating Valid AMA Citation(s) for Each Row

We do not implement all the APA citation rules given we have limited kinds of research in our database. Here's what we have implemented, split by type of research:

* **Journal Articles**

    * We use rules (e.g handling multiple authors) specified [here](https://med.fsu.edu/sites/default/files/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf)
      Additional Resource that we refer to:
        * [University of Waterloo AMA Style Guide](http://subjectguides.uwaterloo.ca/c.php?g=695555&p=4931907)
        * [University of Illinois at Chicago AMA Guide](https://researchguides.uic.edu/ld.php?content_id=10003294)
        * [BCIT AMA Style Guide](https://www.bcit.ca/files/library/pdf/bcit-ama_citation_guide.pdf)

    * We ignore:
        * Journal Supplements
        * Government Publication
        * Newspaper Article
        * Dictionary
        * Unpublished Material
        * CDROM

	* Abbreviated journal names are available from Web of Science Journal Title Abbreviations [here](https://images.webofknowledge.com/images/help/WOS/A_abrvjt.html)

    * We implement organization/group plus author and special issue rules according to the guide linked to above


* **Online Articles**

    We ignore online articles because we don't have them in our data but the general rules are provided in the guide linked to above.

* **Conference Papers**

    We only implement rules for Papers and Poster Sessions listed [here](https://med.fsu.edu/userFiles/file/AmericanMedicalAssociationStyleJAMA.pdf). If an article has both "article_title" and "conf_title", we generate two separate citations for the article---one for the conference, other for the journal article. Rules for multiple authors are the same as above.

**Verifying Work**

We verify the references we produce by comparing against [http://scholar.google.com](scholar.google.com) and some manual sifting.
