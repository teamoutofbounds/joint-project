### Software Reviews

#### 6.1 Formal reviews
At least one week before each sprint ends, a formal meeting will be made by all the team members to do a code review and explain their work to the other members as well as the reasoning about their implementations. The team will also review every document generated during the process of the sprints and will generate the document adjunted in the annex of this SQAP. 

#### 6.2 Informal reviews
Some of the team members are more experienced than others, in order to increase the production in the brief future, the team is going to work via pair-programming. The benefits of this are the fast-learning that the senior developer is going to induce to the less experienced developer, it will also provide a discussion about differents points of view about the implementation of a feature. This discussions can be very rich if both members discuss their ideas and the reasoning behind them. This can lead to find a very optim solution of the implementation.

#### 6.3 Code Walkthroughs
SQA personnel will be invited to all code walkthroughs to ensure that peer reviews of the source code are conducted. The SPM will ensure that a verifiable process is used to identify all action items generated during this review process. SQA may then audit this process to ensure that all action items have been addressed.

#### 6.4 Functional audit
Prior to the software delivery, there must be a team meeting verifying that all of the requirements specified in the requirements document has been satisfied. 

#### 6.5 Test Reviews
This developer team is going to work using a TDD (Test-driven development) methodology. This methodolohy is a software development process that relies on the repetition of a very short development cycle: requirements are turned into very specific test cases, then the software is improved to pass the new tests, only.

The development team will not commit a code requeriment onto the github repository until all the tests have been passed succesfully. This means the code that is uploaded on the repository will always be fully operational and assures us that a push won't break the already working code.

In the next section of this document it is explained in depth what type of tests the team is going to use. 
