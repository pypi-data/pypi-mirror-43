# Lock
Encrypt and decrypt files with a single password

## Usage
```sh
$ python lock.py <file>
```
You will then be prompted to enter a password(never saved).

## Key extension
Keys are extended by repetively multiplying the ASCII value of the last 2 characters and modding in to the lowercase ASCII range

## Note
Will upload to PyPi when it becomes stable.
