# Autoevaluation

##  What works and doesn't

**Works:**

**Doesn't work**

## Compare to initial objectives
1. Multi-files exchange is 

## Time spend

1. Fabian - 40 hours
2. Marco - 35 hours
3. Orhan - 30 hours
4. Kristina - 30 hours

## Particular tasks division
1. Fabian : hub functionality, peer-to-peer architecture and testing
2. Marco: file splitting system, library file generator, peer-to-peer testing.
3. Orhan: hashlib md5 coding, file sending and receiving system, setup-py.
4. Kristina: automation testing, documentation creation, task management (trello board), team management (meetings, meta-group communication).

## “Good Development Practices” section evaluation

**About documents:**

1. Write your documentation in markdown (.md) so that it is automatically nicely display in github (and check that it is displayed well)
-> **100% DONE**


**About git:**


1. Commit only source and configuration files (no generated files, no zip of your sources, ...) -> **100% DONE**
2. Use .gitignore file(s) so that git status shows up clean -> **100% DONE**
3. Do not use git just to store a zip of your project -> **100% DONE**
4. If your repository starts to reach several MB in size, there is probably an issue, -> **size of our final repository is **
5. Commit/push often, so you don't fear making changes -> **75% DONE, quite a long periods with no commits **
6. Provide good commit messages (e.g., see a post about commit messages) that describe the changes and the reason for these changes -> **85% DONE, not all commit messages are self-explanatory**
7. Use English for all commit messages, -> **100% DONE**
8. If you pair-program in front of single machine, mention in the message who contributed to the commit (you'd be surprised how fast you can forget who did what on a project) -> **we don't have such expirience**


**About your code:**

1. Write your code in English -> **100% DONE**
2. Indent/format your code properly, learn how to use your tools/editors to do it -> **85% DONE, naming convention must be improved**
3. Avoid mixing spaces and tabs (ideally, don't use tabulations) -> **100% DONE**
4. Keep your code clean: do not use global/static variables, choose your names carefully (packages, classes, functions, etc), follow some/the conventions (e.g., java convention, pep8), use constants for constant values, ...-> **65% DONE, we use global variables, name convention is not ok, not all best practises are followed**


**You're writing software, and especially networking and concurrent software, so:**


1. Test a lot and often -> **65% DONE, we could provide better and more profound testing**
2. Have automated tests -> **45% DONE, need to spend more time writing tests**
3. Have stress tests -> -> **25% DONE, only manual stress testing**
4. Have tests for "bad" behaviors from other peers (e.g., a peer connecting but not sending anything) -> **45% DONE, we could try to create and test more use-case scenarios**
5. Document how to use, compile, test and start your project -> **100% DONE**
6. Document how to understand and continue your project. -> **85% DONE**