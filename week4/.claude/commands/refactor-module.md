# Refactor Module Command

My command input will provide an $OLD_NAME and a $NEW_NAME. (E.g., "services/extract.py services/parser.py")

Please follow these exact steps safely:
1. Rename the file `$OLD_NAME` to `$NEW_NAME`.
2. Find all Python files in the repository that import the old module name and update those import statements to use the new module name.
3. Run `make lint` to check for syntax errors.
4. Run `make test` to ensure no functionality was broken.
5. Finally, give me a checklist containing the exact list of files you modified and confirm that the verification steps passed.
