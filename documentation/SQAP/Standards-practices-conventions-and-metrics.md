### 5. Standards, Practices, Conventions and Metrics

#### 5.1. Purpose

The purpose of this section of the SQAP is to identify the processes, product standards, and metrics used by a part
of the team OutOfBounds, called Quality Assurance Team (QAT).

#### 5.2. Content

##### 5.2.1. Process Requirements

Documentation, design and coding standards, development and maintenance processes, test standard and practices are all
described by the GPT. All these information should be available for the other team members.
The QA will take part to monitor the requirements through regularly scheduled, formally documented audits.

##### 5.2.2. Identification of the Standards, Practices, Conventions and Metrics:

The content for the developement of this project will be shown below:

##### 5.2.2.1 Standards:
 To make a good distribution of all the standard used in this project, it will be divided in these groups:

  * __Documentation standards__: To develop this project, it has been used the _IEEE Standard for Software Quality Assurance   Plans_. Also, it's used the _Volere_ standard for the requirements part.
  * __Design standards__: It has been used the _UML standard_.
  * __Coding standards:__ It has been used a _Standard python guide_ named _PEP8_.
  * __Commentary standards:__ There's no standard followed in this part.
  * __Selected software quality assurance product and processes metrics:__ There's no standard followed in this part.

##### 5.2.2.2 Practices:

This section is referenced with the templates part which contains a _Meetings_ and a _Code Review_ templates in order to streamline the task of documenting the tasks performed and to be performed.

There's a folder in the SQAP-doc brach named _templates_ which is explained in the section [12.2:Quality Assurance Repository](./Record-collections-maintenance-and-retention.md)

##### 5.2.2.3 Metrics:
Actually, the metrics of this project are not defined at all, because it's a part that will be developed as the project progresses. Some of them could be found in the part of non functional requirements of the user stories.
The metrics that we have defined are:

 * The quantity of code that must be tested is between the 70-80%.
 * The aproved tool to recolect metrics is CodeBeat.
 
Each quality report must be named after the commit hash of the project. This will serve in order to keep track of the evolution of the quality during the implementation of the product.

##### 5.2.2.4 Conventions:
During the development of the project, there has been defined some conventions/basic rules in order to make clear the way of working of the team project. Also there has been provided some guides for the Development Team (DT).

One of the conventions that the group stated are the messages for the commits, which must be write like: SQAP-_number-of-section_: message. Identical commit messages should be avoided, but if it occurs that one is unavoidable, said message must contain either a number signifying its chronological position in the commit list.

i.e., _dev:Added new models_ -> _dev:Added new models 2_

English is the language that must be used by all the team members for
the Quality Management, all the documents and the code comments.

Furthermore, commit messages should not be ambiguous or confusing.

It has been used a specific numeration depending of the document that is being treated:

&nbsp;&nbsp;&nbsp;&nbsp;__User Stories__: Related with the PUC proposed.

&nbsp;&nbsp;&nbsp;&nbsp;If we find this kind of numeration X.0 it means that is being developed
&nbsp;&nbsp;&nbsp;&nbsp;the whole PUC, but instead of this, if we find this numeration X.1, X.2 ...
&nbsp;&nbsp;&nbsp;&nbsp;it means that the PUC is divided in different sections.

&nbsp;&nbsp;&nbsp;&nbsp;The no functional requierements must be defined as: 0.X.

&nbsp;&nbsp;&nbsp;&nbsp;__Prototypes__: Related with the User Story.

&nbsp;&nbsp;&nbsp;&nbsp;For the coding part, the mock up must be named as: *name-of-mock* _
&nbsp;&nbsp;&nbsp;&nbsp;mock and for the url, there has to be
a previous meeting with all the
&nbsp;&nbsp;&nbsp;&nbsp;team members to agree the name of the url.

#### 5.3. References

##### 5.3.1. Standards:

+ [IEEE Standard for Software Quality Assurance Plans](https://ieeexplore.ieee.org/document/213705) (IEEE 730.1-1989, 1989)

+ [Volere: Volere model](http://www.volere.co.uk) (Volere Requirements Resources docs, 2018)

+ [UML standard](https://www.uml.org/) (UML docs, July 2005)

##### 5.3.2. Guides:

+ [PEP8:  Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) (Python docs, version 8, August 1 2013)



  [Back to Index](./index.md)
