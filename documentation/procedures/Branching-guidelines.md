### Branchin Guidelines (or how we will use the branching in GitHub)

In order to make it so that 9 people can use efficiently the repository that the project will be allocated in, we have created different branches in which we will base our workflow. There are 6 branches in total (the branches names may vary):

+ **Master**: the branch that will contain the result of both the code and documentation merges. This branch can only be changed when the team decides to do so in a formal meeting (documented using the meeting template). This will be the branch in which we implement the sprints and also important changes over the project.
+ **Dev**: This branch will serve as the branch in which everyone will commit their work before being revised and merged into the Master branch. i here, everyone can commit heir code in other to check for errors and such.
+ **Hotfix**: This branch will be used only when small changes may be applied to the Master branch. If something small needs to be modified in the Master branch, the Hotfix will pull the Master, commit the change and then commit said change to both the Master and the Dev branch (so that that everyone is working with the same information).
+ **Q&A**: Before merging the Dev branch with the Master, there is an intermediate step that will gather both the documentation dev and the development dev (SQAP-doc and Dev) for better merging with master. 
+ **SQAP-doc**: This branch is used for the purpose of uploading the changes over the documentation of the project before merging them into the Master branch.
+ **SQAP-hotfix**: Same use as the normal hotfix except that this branch will be used for documentation only.

#### Normal procedures within a sprint:

The normal workflow in a sprint development and deployment for the GitHub shall be:

1. Use the Dev and SQAP-doc branches in order to add and change both code and documentation fo the project.
2. When the work is considered done for the current sprint (and previously reviewed with the group), the two branches will be merged with the Q&A branch so that it can be reiviewed one last time and to check how it will look for the release of the sprint
3. Once every test and every review has passed, the Q&A branch will be merged with the master branch, deploying a new version of the project.
4. Once the master branch have been uptaded with the new version (0.# because we're still in the development via sprints, the dev and SQAP-doc branches will do a pull to master so that we all work on the latest version.
5. If an error on either code or documentation is found inside the master branch, the Hotfix and SQAP-hotfix will be used to pull the master branch, rectify the error and the merge with master andone of the two fevelopment branches (if code then marge with Dev and master, if documentation the SQAP-doc and master).
