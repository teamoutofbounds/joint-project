### 4. Documentation

Documentation must lay the foundation for quality, traceability, and history for both the individual document and for the entire project documentation.
It is also extremely important that the documentation is well arranged, easy to read, and adequate.
In this section all the documentation related to the development of the project is listed. This includes all those documents that manage the development of the software as well as its validation and maintenance, and also includes the user documentation.


#### 4.1 Purpose

Project documentation is a vital part of project management. It is substantiated by the two essential functions of the documentation: to ensure that the project requirements are fulfilled and to establish traceability with respect to what has been done, who has done it and when it has been done.


### 4.2 Minimum documentation requirements

### 4.2.1. Software requirements

For the elicitation of the requirements, a checklist is used to verify that both the interviews and the apprenticing cover all the important topics that have been defined previously. It also uses a sheet with a list of questions to conduct the interview or in the case of apprenticing to support the activity.
To make the summary of the day of apprenticing a template is used.Later the information obtained in the elicitation is coded as Business Use Case (BUC) and Product Use Case (PUC). All gathering requirements materials can be found in [Drive](https://www.google.com/intl/es_ALL/drive/) in folder named "1 - Anàlisi Requeriments".
Finally, the user stories are written following the template of the Volere card.


### 4.2.2. Software design

The design of the application is carried out from the [UML](https://www.uml.org/) standard.  
In addition, low fidelity prototyping, drawn on paper, is used for the first sketches. Once the prototypes of low fidelity were approved, the high fidelity prototypes were made. These are dijital and are made using the [gimp](http://www.gimp.org.es/) tool.


### 4.2.3. Verification and validation plans
The team is going to do a formal review once per sprint. [Referenced in section 6.2.1](./Software-reviews.md)  
Informal reviews are also going to be made during the development. [Referenced in section 6.2.2](./Software-reviews.md)  
The SQA personnel will assess code walkthroughs. [Referenced in section 6.2.3](./Software-reviews.md)  
There has to be a full verification of the requirements. [Referenced in section 6.2.4](./Software-reviews.md)  
The team is going to work using TDD development. [Further explanation in section 6.2.5](./Software-reviews.md)  


### 4.2.4. Verification and validation results reports

Sprint review: Esta reunión se realiza al acabar el Sprint. En esta debe realizarse el <a href="https://github.com/UdL-EPS-ProjectManagement/ProcessModelTheory/blob/master/templates/Sprint_Retrospective_Template.md" target="blank">retrospective review report.</a>


### 4.2.5 User documentation

The User documentation will not be described in this first deliverable as\
the team wants to discuss with the Users and the client which are their needs\
who does prepare it and which format would be more convinient for them (text, video...).

Once everything is discussed, this section will be prepared acordingly.

### 4.2.6. Software configuration management plan (SCMP)

In order to ensure the persistence of all materials related to the project, git will be used. This ensures that each computer that works on the project becomes a node that stores all the file history, so that if one disappears, the rest contains all the necessary information. In addition, as a remote repository, which allows synchronizing all other repositories by adding one more node, this time in the cloud, github will be used. All participants must follow this [guidelines to use git](https://github.com/teamoutofbounds/joint-project/blob/SQAP-doc/documentation/procedures/Branching-guidelines.md).

Each release of the code will be identified with a annotated tag in the following way:

```bash
<version>.<sub-version>.<fix>.<date:y/m/d>
Example: 0.2.0.20190407
```

In order to create an annotated tag, the following command will be used on git:

```bash
git tag -a <tag-name>
```

The message of the tag must contain at least:
+ A detailed explanation of the changes introduced by the version.
+ A detailed explanation of the bugs that the version corrects.


### 4.2.7. Other documentation

#### 4.2.7.1. Documentation style guide

All documentation, including this SQAP, will be developed in markdown and will be available in a hypertext format (for faster and more efficient consultation) through the [github wiki/pages/SQAP](https://github.com/teamoutofbounds/joint-project/wiki/SQAP).

+ __Titles:__ ## <number\>. <Section_Name\>  
+ __Subtitles:__ ### <number\>.<Number\>. <Subsection_ Name\>  
+ __Sub-subtitles:__ ### <number\>.<Number\>.<Number\>. <Sub-subsection_Name\>
+ __Sub-sub-subtitles:__ #### <number\>.<number\>.<Number\>.<Number\>. <Sub-sub-subsection_Name\>
+ __Lists:__ + <item / text\>
+ __Links:__ [<link_name\>] (<link\>)  

[Back to Index](./index.md)
