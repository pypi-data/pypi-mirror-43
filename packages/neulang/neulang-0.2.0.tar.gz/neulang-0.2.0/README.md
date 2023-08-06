# Neulang
Coding for humans.

## Description
Neulang is a natural language layer embedded in Python. It takes scripts containing pseudocode in [Org](http://orgmode.org/) format and runs them.

## Why?
As the easiest programming language for anyone to learn, Python is awesome.
But there's still that curve that continues to shut many out of the coding world.
People shouldn't have to learn another language to code, esp in this age of smart devices, IoT and AI.
Let's bring coding to the people, not the people to coding.
Oh, and I have a lot of pseudocode in Org format that I'd like to make executable.

## Installing
* `pip install neulang`

## Features
* Command line mode
  * `neu [options] -c "command"`
* Interactive mode
  * `neu [options]`
  * Exit with `air_exit` or `air_quit`
* Importable as module
  * `from neulang import Neulang`
  * `n = Neulang()`
  * `script = "* air_say 'hello world'"`
  * `n.loads(script)`
  * `n.eval()`
* Run script files
  * `neu [options] /path/to/script.neu`
* Run a single node in a script file
  * `neu [options] script.neu -o "s/org/path/as/regex/or/index"`

## Usage
* For the best experience, use a text editor which supports org-mode. Preferably Emacs as it is used for the project.
* Activate org-mode on a new buffer and write a script as organized pseudocode.
* Modify your pseudocode so it adheres to the operations available in `tests/tests.neu`. The following operational categories are currently available:
  * Regular [Python expression](https://docs.python.org/3/reference/expressions.html) nodes:
    * `* print("Hello world")`
  * ASTIR (Abstract Syntax Tree Intermediate Representation) nodes as a drop-in for statements and expressions (not all are implemented as yet). It is distinguished by keywords beginning with `air_`. The rest tends to, in most cases, correspond to the Python-native name of the operation (though not in this example):
    * `* air_setv`
    * `** my_string`
    * `** This is a string`
  * Natural language nodes parsed via the [Mycroft Adapt](https://github.com/MycroftAI/adapt) intent parser:
    * The `intent_parts` section takes 1+ valid regular expressions which uses dict groups to enable parsing into an intent.
    * The `body` section is made of any of the categories, and also gets a dict `nl_ctx` containing the parsed data.
    * NB: see `tests.neu` for example usage.
* Run your script: `neu script.neu`
* Provide feedback on your experience, bugs and suggestions for improvement.

## To Do
* Implement remaining core Python features in AST
* Complete CLI functionality
* Implement fuzzy search and learning resolvers
