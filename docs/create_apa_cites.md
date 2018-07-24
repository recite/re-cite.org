## Creating Valid APA Citation(s) for Each Row

[freshdb.py](freshdb.py) creates valid APA references based on the database.

We do not implement all the APA citation rules given we have limited kinds of research in our database. Here's what we have implemented, split by type of research:  

* **Journal Articles**

* We use rules specified here: https://owl.english.purdue.edu/owl/resource/560/07/

* We ignore:
  - Article in a Magazine
  - Article in a Newspaper
  - Letter to the Editor

* We implement rules for number of authors specified [here](https://owl.english.purdue.edu/owl/resource/560/06/) but ignore:
  - Two or More Works by the Same Author
    + People citing multiple retracted articles by the same author is uncommon. We leave it for later.
  - Introductions, Prefaces, Forewords, and Afterwords

* If there is a group_author, do follow advice from [here](http://blog.apastyle.org/apastyle/2011/09/group-authors.html). For instance,

```
Jamal, S. A., Swan, V. J., Brown, J. P., Hanley, D. A., Prior, J. C., Papaioannou, A., ... & Canadian Multicentre Osteoporosis Study Research Group. (2010). RETRACTED: Kidney Function and Rate of Bone Loss at the Hip and Spine: The Canadian Multicentre Osteoporosis Study.
```

* If the article is a special issue, follow directions [here]( http://blog.apastyle.org/apastyle/2012/05/citing-a-special-issue-or-special-section-in-apa-style.html)

* **Online Articles**

We ignore online articles because we don't have them in our data. But the general rules are [here](https://owl.english.purdue.edu/owl/resource/560/10/). (We can probably safely ignore everything on the page after "Article from a Database") Add the phrase 'retrieved from' when building references. Rules for the number of authors are the same as for journal articles. 

* **Conference Papers**

We only implement rules for [Papers and Poster Sessions listed [here](http://blog.apastyle.org/apastyle/2012/08/how-to-cite-materials-from-meetings-and-symposia.html). We prepend "paper presented at" when mentioning location. If an article has both "article_title" and "conf_title", we generate two separate citations for the article---one for the conference, other for the journal article. Rules for multiple authors are the same as above.

* **Verifying Work**

We verify the references we produce by comparing against [scholar.google.com](http://scholar.google.com) and some manual sifting. We find that google scholar gets APA citations to work with 7 or more authors incorrect.
