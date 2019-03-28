### Code Review Checklist
## General
* Does the code work?
* Is all the code easily understood?
* Does it conform to the agreed coding conventions?.
* Is there any redundant or duplicate code?
* Is the code as modular as possible?
* Can any global variables be replaced?
* Is there any commented out code?
* Do loops have a set length and correct termination conditions?
* Do the names used in the program convey intent?
## Performance
* Are there any obvious optimizations that will improve performance?
* Can any of the code be replaced with library or built-in functions?
* Can any logging or debugging code be removed?
## Security
* Are all data inputs checked (for the correct type, length, format, and range) and encoded?
* Where third-party utilities are used, are returning errors being caught?
* Are output values checked and encoded?
* Are invalid parameter values handled?
## Documentation
* Do comments exist and describe the intent of the code?
* Are all functions commented?
* Is any unusual behavior or edge-case handling described?
* Is the use and function of third-party libraries documented?
* Are data structures and units of measurement explained?
* Is there any incomplete code? If so, should it be removed or flagged with a suitable marker like ‘TODO’?
## Testing
* Is the code testable? The code should be structured so that it doesn’t add too many or hide dependencies, is unable to initialize objects, test frameworks can use methods etc.
* Do tests exist, and are they comprehensive?
* Do unit tests actually test that the code is performing the intended functionality?
* Could any test code be replaced with the use of an existing API?


## References:
* [Code Review: Template](https://nyu-cds.github.io/effective-code-reviews/03-checklist/) (Nyu-cds docs, 2017)

[Back to Template Index](./index.md)
