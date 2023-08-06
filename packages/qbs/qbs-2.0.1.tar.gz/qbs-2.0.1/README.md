# [qbs - Quick (and dirty) build system](https://gitlab.com/nonnymoose/qbs)

qbs is designed for people who perform the same tasks on small programs repeatedly and in a hurry. This can be helpful when you are learning a programming language and want to build (and rebuild) a series of short sample programs.

If you need qbs to do something more, chances are it's wiser just to use [GNU Make](https://www.gnu.org/software/make/). However, if you want a small feature, submit an issue.

You can install qbs from the [Python Package Index](https://pypi.org/project/qbs/) using the command `pip install qbs` (with `sudo` / `--user` as appropriate).

# Table of Contents
 - [Configuration](#configuration)
   - [Format](#format)
   - [Command arguments](#command-arguments)
   - [Filename replacement](#filename-replacement)
   - [Language aliases](#language-aliases)
   - [Configuration file loading](#configuration-file-loading)
     - [Windows](#windows)
     - [Linux / OS X](#linux-os-x)
     - [Configuration overriding](#configuration-overriding)
 - [Command-line usage](#command-line-usage)
   - [`init`](#init)
   - [`t_auto`](#t_auto)
   - [Other commands](#other-commands)
	 - [Command shortening](#command-shortening)
	 - [Command chaining](#command-chaining)

# Configuration
## Format
qbs takes configuration files in the [JSON](https://www.json.org/) file format.
They have the following structure:
```json
{
	"language1": {
		"command1": ["arg1", "argN"],
		"commandN": ["arg1", "argN"]
	},
	"languageN": {
		"command1": ["arg1", "argN"],
		"commandN": ["arg1", "argN"]
	}
}
```

## Command arguments
Commands run by qbs will not be executed in a subshell. This means that you do not need to escape spaces, but you have to put each argument in a separate element in the array. You also cannot use shell-specific commands, such as `[[`.<sup>1</sup>

<sup>1. You can use `[` though, because that's actually a binary program.</sup>

## Filename replacement
In each command, you may use the strings `{progname}` and `{progext}`, which will be replaced by the path to the file which is being built (without the file extension) and the file extension of the file which is being built (*with* the dot), respectively.

## Language aliases
qbs supports aliasing languages so that languages with weird filename conventions can all be built in the same way. The syntax is:

```json
{
	"language": "alias"
}
```

i.e. instead of providing a map of commands, you just provide a string which holds the name of the language to actually use.

This way, if you want python files to be built even though the file extension is `.py`, you can do this:

```json
{
	"py": "python"
}
```

## Configuration file loading
qbs loads configuration files in the following orders:

### Windows
```
C:\ProgramData\qbs\qbs.json
C:\Users\{username}\AppData\Roaming\qbs\qbs.json
.\qbs.json
```

### Linux / OS X
```
/etc/qbs.json
/home/{username}/.qbs.json
/home/{username}/.config/qbs.json
./.qbs.json
./qbs.json
```

### Configuration overriding
Each of the configuration files listed is loaded (after the default configuration file provided with this package) when qbs is run. Each configuration file overrides only the languages specified within it from the previous configuration files. This allows users to override settings for various languages on a per-system, per-user, and per-directory basis.

# Command-line usage
> Note: qbs does not support being used like a library. Importing qbs is not tested.

## `init`
To use qbs, you first must initialize qbs with the file that you will be building. qbs has a built-in command to do this, `init`:

```
qbs init hello_world.cpp
```

Once you have run `init`, qbs will cache the filename and language so that you can use other qbs commands. It will retain this information until you run `init` again.

*Note:* qbs stores the cache in the current directory. If you change directories, you will have to run `init` again. This makes sense, though, because the path to the file changes when you cd as well.

`init` is also the only qbs command that supports arguments. Currently, the only arguments defined are:

```
-t <template file>
-l <language>
```

Arguments must fall between `init` and the filename, like so:

```
qbs init -l java -t java_template.java
```

The `-t` option causes qbs to copy the template file into the source file. It will also replace the same strings listed in [Filename replacement](#filename-replacement) within the template file. Here is an example template for an empty Java main class:

```java
public class {progname} {
	public static void main(String[] args) {
		// put your code here
	}
}
```

The `-l` option simply selects the language you want to use. To avoid the extra typing of having to use this option, see [Language aliases](#language-aliases).

## t_auto
The `t_auto` command provides automated testing support in qbs.
> Side note: `t_auto` stands for test_auto. Why didn't I name it test_auto? Well, I almost did. The thing is, that would mean that you wouldn't be able to run any command named test! That would have been so much worse for anyone who wanted to create their own test command. You can still shorten it to `t`, though. (see also [command chaining](#command-chaining))

`t_auto` supports providing your program with some input via a file or standard input and comparing the output (from a file or standard output) to a file containing the expected output.

`t_auto` requires some special information in your qbs.json. Namely, "t_auto" should be an object rather than a string, with keys `input`, `infiles`, `output`, `outfiles`, and optionally `begin`.

`input` and `output` are the files that the program reads from and writes to, respectively. For standard input/output, use `-`. If you really mean "a file named `-` in the current directory", use `./-`. `input` and `output` can use the strings `{progname}` and `{progext}`.

`infiles` and `outfiles` are format strings which can use the strings `{progname}` and `{progext}` and must use `{num}` (If you don't include `{num}`, qbs will test your program an indefinite number of times.), where `{num}` is the test number. qbs will run tests until it cannot open either the input or output file for that number.

`begin` is the test number at which qbs should start. This is usually either `1` or `0`, and it is assumed to be `0` if omitted.

If a test fails, qbs will stop and print out a diff between the expected output and the actual output. If the file was supposed to print to stdout, qbs will print that in full. Otherwise, qbs simply won't delete the output file.

### Example usage of t_auto
> qbs.json
```json
{
  "cpp": {
    "build": ["g++", "--std=c++14", "-g", "{progname}{progext}", "-o", "{progname}"],
    "run": ["./{progname}"],
    "t_auto": {
      "input": "-",
      "infiles": "{progname}.{num}.in",
			"output": "-",
			"outfiles": "{progname}.{num}.out",
      "begin": 0
    }
  }
}
```
> test.0.in
```
hello
```
> test.0.out
```
hello
```
> test.cpp
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
  string a;
  cin >> a;
  cout << a << endl << endl;
  // oops! I typed endl twice instead of once
  return 0;
}
```



```
$ qbs init test.cpp
$ qbs build
+ g++ --std=c++14 -g test.cpp -o test
$ qbs t_auto
Test 0:
+ ./test
Error: test 0 failed: output differs from testcase:
--- test.0.out
+++ stdout
@@ -1 +1,2 @@
 hello
+

Info: output was
\`\`\`
hello

\`\`\`
```

## Other commands
Any other command will be executed as it is defined in the last-read configuration file.

*Beware:* because configuration files override one another on a per-language basis, this means that you can unset commands!

## Command shortening
qbs allows you to only type a little bit of the command you want, and it will figure out which one you mean. For example, if `init` is the only command that starts with the letter 'i', then you can type `qbs i` instead of `qbs init`. However, if there is another command `instantiate`, you would have to type at least `ini` for `init` and `ins` for `instantiate`.

*Beware:* If you create a command that contains the full text of another command at the beginning, you will not be able to execute the shorter command! For example, if you have a command `initialize` in addition to the built-in command `init`, you will not be able to execute `init` because qbs cannot tell if you meant for it to be short for `initialize` or for it to mean just `init`. You would also only be able to execute `initialize` by typing at least `initi`, for the same reason.

## Command chaining
qbs allows you to execute multiple commands in one line. For example, if you have the functions `build` and `run` declared for the language `cpp` in addition to the built-in command `init`, the following would be a perfectly valid way to build and run the file `hello.cpp` with qbs:
```
qbs init hello.cpp
qbs build
qbs run
```

But so would this:
```
qbs i hello.cpp b r
```

Now do you see why I called it quick and dirty?
