# LINESCREEN

# Introduction

If your script has more than a set number of lines, your code lines are leaking :).

LineScreen counts the lines of code in a script, and 'yells' if the limit is exceeded.
The 'yelling' behaviour can be silenced. The default limit of 500 can be overridden.
Finally, limits can be applied to physical or logical lines.

# Usage 

```
linescreen.py [-h] [-l LIMIT] [-s] [-p] filename
```

It requires just the filename to run with default settings.
<p> Optional arguments may change limit, override limit enforcement or differentiate 
between logical and physical lines.

```
positional arguments:
  filename              The name of the file to lint.

optional arguments:
  -h, --help            Shows help.
  
  -l LIMIT, --limit LIMIT
                        Sets the line limit.
  
  -s, --silence         Overrides limit enforcement, 
                        and returns just the number of lines in the script.
                        
  -p, --physical        Enforces limit on physical lines instead of logical lines. 
                        It is only useful if limit is enforced.

```

# Illustration

#### Help
```
> D:\>python linescreen.py -h
  usage: linescreen.py [-h] [-l LIMIT] [-s] [-p] filename

  positional arguments:
    filename              The name of the file to lint.

  optional arguments:
    -h, --help            show this help message and exit
    -l LIMIT, --limit LIMIT
                          Sets the line limit.
    -s, --silence         Overrides limit enforcement, and returns just the
                          number of lines in the script.
    -p, --physical        Enforces limit on physical lines instead of logical
                          lines. It is only useful if limit is enforced

```

#### Default - without optional parameters
```
> D:\>python linescreen.py lineleak.py
  NUMBER OF LINES WITHIN LIMIT.
        lineleak.py has:
        128 physical lines
        94 logical lines.
```

#### Override line count limit - default: 500
```
> D:\>python linescreen.py lineleak.py -l 30
  WARNING:root:
        | 30-LINE LOGICAL LIMIT EXCEEDED!
        | lineleak.py has 94 logical lines.
        | Limit was exceeded at line [81].

```

#### Apply limit enforcement to physical lines - default: logical lines
```
> D:\>python linescreen.py lineleak.py -l 30 -p
  WARNING:root:
        | 30-LINE PHYSICAL LIMIT EXCEEDED!
        | lineleak.py has 128 physical lines.
        | Limit was exceeded at line [73].
```

#### Ignore limit enforcement.
The second part illustrates silence even when the limit and physical 
optional arguments have been passed
```
> D:\>python linescreen.py lineleak.py -s

        lineleak.py has:
        128 physical lines
        94 logical lines.
        
        
> D:\>python linescreen.py lineleak.py -l 30 -p -s

        lineleak.py has:
        128 physical lines
        94 logical lines.
        
```

# Environment
- Shell

# Dependencies
- Best suited for Python 3+
- No external libraries required currently

# Software Cycle Stage
- Development (Pre-testing)

# Targeted Deployment
- Possible plugin for flake8
