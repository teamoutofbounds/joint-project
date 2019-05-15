### 6. Software Reviews

#### 6.1 Purpose
The purpose of software reviews are to correct defects on the code as well as improve the development process of the projects. Some of the points of doing software reviews are: 
* Education of other developers. Ensure that everyone sees the modification associated with a defect fix or enhancement so that they can understand the rest of the software. This is especially useful when people are working on components that need to be integrated or on complex systems where one person may go for long periods without looking at certain modules.
* Finding defects or opportunities for improvement. Both the deliverable code as well as test code and data can be examined to find weaknesses. This ensures that the test code is robust and valid and that the design and implementation is consistent across the application. If there needs to be additional changes made, it catches the opportunity closer to the point of entry.

#### 6.2 Minimum requirements

##### 6.2.1 Formal reviews: Code-Walkthrough
At least one week before each sprint ends, a formal meeting will be made by all the team members to do a code review and explain their work to the other members as well as the reasoning about their implementations. The team will use the template ["Code review template"](../templates/code_and_design_review.md) that can be found in the templates folder. 
The team will also review every document generated during the process of the sprints and will generate the document adjunted in the annex of this SQAP. 
SQA personnel will be invited to all code walkthroughs to ensure that peer reviews of the source code are conducted. The SPM will ensure that a verifiable process is used to identify all action items generated during this review process. SQA may then audit this process to ensure that all action items have been addressed.

On this code-walkthrough the team members are going to be divided in two groups and the following tasks have to be addressed:
* Be sure all the buttons are correctly linked
* Review all the code identation
* Review if all the tests have been correctly passed
* Check refactor possibilities
This tasks have to be done for all the HTMLs, models and views.

##### 6.2.2 Informal reviews
Some of the team members are more experienced than others, in order to increase the production in the brief future, the team is going to work via pair-programming. The benefits of this are the fast-learning that the senior developer is going to induce to the less experienced developer, it will also provide a discussion about differents points of view about the implementation of a feature. This discussions can be very rich if both members discuss their ideas and the reasoning behind them. This can lead to find a very optim solution of the implementation.

##### 6.2.3 Functional audit
Prior to the software delivery, there must be a team meeting verifying that all of the requirements specified in the requirements document has been satisfied. 

##### 6.2.4 Test Reviews
This development team is going to work using a TDD (Test-driven development) methodology. This methodolohy is a software development process that relies on the repetition of a very short development cycle: requirements are turned into very specific test cases, then the software is improved to pass the new tests, only.

The development team will not commit a code requeriment onto the github repository until all the tests have been passed succesfully. This means the code that is uploaded on the repository will always be fully operational and assures us that a push won't break the already working code.

In the next section of this document it is explained in depth what type of tests the team is going to use. 

##### 6.2.5 Quality Gateway
The aim is to trap requirements-related defects as early as they can be identified. We prevent incorrect requirements from being incorporated in the design and implementation where they will be more difficult and expensive to find and correct.

To pass through the quality gateway and be included in the requirements specification, a requirement must pass a number of tests. These tests are concerned with ensuring that the requirements are accurate, and do not cause problems by being unsuitable for the design and implementation stages later in the project.

This tests are:
* Does each requirement have a fit criterion that can be used to test whether a solution meets the requirement?
* Is every requirement in the specification relevant to this system?
* Does the specification contain a definition of the meaning of essential terms within the specification? 
* Is every reference to a defined term consistent with its definition?
* Is the context of the requirements study wide enough to cover everything we need to understand?
* Does the requirement contain a rationale?
* Have we asked the stakeholders about conscious, unconscious and undreamed of requirements? 
* Does the specification contain solutions posturing as requirements?
* Is the stakeholder value defined for each requirement?
* Is each requirement uniquely identifiable?

##### 6.2.6 Software Design Review
A design review is a milestone within a product development process whereby a design is evaluated against its requirements in order to verify the outcomes of previous activities and identify issues before committing to further work.
In order to evaluate a design against its requirements the SQAP personnel will evaluate the design via examinations (walk-throughs).

##### 6.2.7 DataBase Design Review
In order to evaluate the correctness of the modalization of the database entities. The SQAP and the developer team members must have a meeting where this topic must be discussed and reach a consensus of the models used in the database.

##### 6.2.8 Test Review
The main purpose of the test review is to increase test coverage and subsequently the test script quality.
The SQAP personnell will use the following checklist. ["Test review template"](../templates/test_review.md)


[Back to Index](./index.md)
