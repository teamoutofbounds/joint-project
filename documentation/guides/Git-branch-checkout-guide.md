### Git branching and checkout

When a repository is cloned into a folder, it is normally done so from the _master_ branch. More often than not, however, we require access to the files from another branch. Normally, we would use __git branch__ to list the available branches, then __git checkout |name|__ to switch to the branch. However, __git branch__ only shows the branches git knows exist.

There are multiple ways of getting access to the other branches. The easiest, and one suggested by this guide, is to add the __-a__ parameter to __git branch__, so the written command looks like this:

    git branch -a

This will list absolute paths for all the branches. Take the part of the path after _remotes/origin/_ and __git checkout__ it, and your cloned repository will switch to that branch. I.e., if __git branch -a__ shows you this:

    master*
    remotes/origin/HEAD -> origin/master    
    remotes/origin/SQAP-doc   
    remotes/origin/SQAP-hotfix
    remotes/origin/master

use the command __git checkout SQAP-doc__ to check out the _SQAP-doc_ branch. Once done, __git branch__ should confirm that you are on the _SQAP-doc_ branch by showing a * next to the branch name.
