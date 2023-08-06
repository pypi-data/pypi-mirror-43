# [qbs - Quick (and dirty) build system](https://gitlab.com/nonnymoose/qbs)

qbs is designed for people who perform the same tasks on small programs repeatedly and in a hurry. This can be helpful when you are learning a programming language and want to build (and rebuild) a series of short sample programs.

If you need qbs to do something more, chances are it's wiser just to use [GNU Make](https://www.gnu.org/software/make/). However, if you want a small feature (besides automated tests, which are a work in progress), submit an issue.

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

## Other commands
Any other command will be executed as it is defined in the last-read configuration file.

*Beware:* because configuration files override one another on a per-language basis, this means that you can unset commands!

## Command shortening
qbs allows you to only type a little bit of the command you want, and it will figure out which one you mean. For example, if `init` is the only command that starts with the letter 'i', then you can type `qbs i` instead of `qbs init`. However, if there is another command `instantiate`, you would have to type at lease `ini` for `init` and `ins` for `instantiate`.

*Beware:* If you create a command that contains the full text of another command at the beginning, you will not be able to execute the shorter command! For example, if you have a command `initialize` in addition to the built-in command `init`, you will not be able to execute `init` because qbs cannot tell if you meant for it to be short for `initialize` or for it to mean just `init`. You would also only be able to execute `initialize` by typing at least `initi`, for the same reason.

## Command chaining
qbs allows you to execute multiple commands in one line. For example, if you have the functions `build` and `run` declared for the language `cpp` in addition to the built-in command `init`, the following would be a perfectly valid way to build and run the file `hello.cpp` with qbs:

```
qbs i hello.cpp b r
```

Now do you see why I called it quick and dirty?
