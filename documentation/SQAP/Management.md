
### 3.Management
#### 3.1 Joint Project Organization

##### 3.1.1 Program Organization Structure

The TeamOutOfBounds is organised and managed by three different teams:

Quality Assurance Team (QAT): this team is composed by two members are only 
involved in QA activities. \
Development Team (DT): this team is formed by two members and will only 
be involved in code related activities. \
General Purpose Team (GPT): this team has 5 members and will be assigned 
into a large variety of product related activities such as design, development,
test or quality assurance procedures.

Program Managment provides management oversight during all task life cycle 
phases and ensures that adequate support services are available for all 
tasks to include schedule tracking and quality assurance.


##### 3.1.2 Quality Assurance Organization

The Quality Assurance (QA) for the joint-project will be developed by the 
members of the QAT and the the GPT. 

The QA Manager has overall responsibility for quality assurance programs
 and will identify and direct the joint-project QAT and GPT members assisting.
 In order to ensure that no bias is applied to the QA procedures, the 
Quality Assurance Manager is elected from the QAT and all information 
concerning QA will only be reported to him. \
The QA Manager will be the only interface between the DT and QAT. In order 
to sustain good communication between between both teams a meeting between 
the Product Manager and the QA Manager will be held.


#### 3.2 Tasks

##### 3.2.1 Maintenance and Development lifecycles

TeamOutOfBounds comprises only the development activities. Modification 
requests lead to system enhancements and may involve the complete software 
development lifecycle: requirements, design, development,unit test and 
deployment and includes system, installation and operational documentation.


##### 3.2.2 Maintenance and Development Tasks

| Activity     | Entry        | Exit Criteria |
|:--------------:|:------------:|:-------------:|
| _Requirement licitation_ | _Beginning of a new Sprint_ | _Meetings held with the Stakeholders_ |
| _Writing User Stories_ | _Requirement licitation completed_ | _BUC, PUC's and User Stories written and approved_ |
| _Sprint Planning_ | _Writting User Stories Completed_ | _Tasks obtained from User Stories assigned to each member and Sprint end set to a date_ |
| _Daily Meeting_ | _Each Monday, Wednesday and Friday during a Sprint_| _20 min after starting the Meeting_|
| _Sprint Review_ | _Sprint end date day_ | _Stakeholders tell the opinion about all Software developed since the moment_ |
| _Sprint Retrospective_| _Sprint Review Completed_ | _Scrum Master says the meeting has ended_ |

##### 3.2.3 Maintenance and Engineering Support Tasks

The maintenance and support tasks are out of the scope of TeamOutOfBounds
project development and therefore will be not assessed in this document.


##### 3.2.4 Deployment Tasks

The project follows the principles of Continious Integration (CI), for each\
Sprint, the activities will be the following:

| Activity     | Entry        | Exit Criteria |
|:--------------:|:------------:|:-------------:|
| _Relese review_  | _All Software is pulled to the QA branch and a meeting is appointed_ | _The Product Owner and the Quality Assurance Manager approves the Software State_ |
| _Release integration_| _Release review is completed_| _QA branch pulls to master branch_|
|_Deploy check_|_QA branch pulled to master_|_All tests run on production environment_|



##### 3.2.5 Quality Assurance Processes

The main processes that the project will follow regarding QA will be 
described in the sections listed bellow:
* [6. Software Reviews](./Software-reviews.md)
* [7. Test](./Test.md)
* [8. Problem reporting and corrective actions](./Problem-reporting-and-corrective-actions.md)
* [12. Records Collection, Maintenance and Retention](./Records-collections-maintenance-and-retention.md)

#### 3.3 Roles and Responsibilities

##### 3.3.1 Quality Assurance Manager

The Quality Assurance organization will be led by a Quality Assurance Manager
with the responsibility to:
* QAT is staffed appropriately.
* Consensus the TeamOutOfBounds QA schedule.
* Write and conduct the QA meetings.  
* Evaluate QA staff performance, provide direction and guidance, as appropriate.
* Ensure conformance to the requirements of the standards.
* Ensure the metrics and data provided by the Quality Assurance Engineers
is correct.
* Notify the Product Owner about the state of the project in terms to 
the conformance to the SQAP.    


##### 3.3.2 Quality Assurance Engineers

Quality assurance Engineers (QAE) are members of the QAT with the responsibility 
to:

* Monitor Joint Project activities and ensure the appropriate standards,
 processes and procedures are identified and implemented by both the GPT
  and the DT.
* Perform objective evaluations of TeamOutOfBounds processes and work products, 
based on defined criteria, to ensure they are in accordance with and 
conform to specified standards, processes, and procedures.
* Record and communicate results of evaluations, which include identifying 
non conformances and documenting them following the proper template. 
* Collect and analyze QA activity metrics and report results to QA Manager 
and Program management.
* Assign, track and verify corrective actions resulting from QA procedures 
or Quality Action Requests (QAR).

##### 3.3.3 Product Owner

The Product Owner is a member of the DT or GPT and is elected every Sprint. The
Product Owner is responsible of:

* Assure that all tasks are staffed properly.
* Document the activities related to Scrum.
* Distribute the tasks amongst the DT and GPT.
* Schedule the meetings related to Scrum processes.
* Represent the interests of the client during the Sprint.

##### 3.3.4 Scrum Master

The Scrum Master is responsible to:

* Assure that every task is being developed according to the plan.
* Lead the Daily Meetings.

##### 3.3.5 Developer

Developers have the following responsibilities:

* Develop the assigned tasks.
* Follow the SQAP.
* Notify the Scrum Master during the Daily Meetings the problems he encounters.


#### 3.3.3 Quality Assurance Estimated Resources

This part of the SQAP does not apply to the first delivery and will be writen
on the second delivery.

[Back to Index](./index.md)