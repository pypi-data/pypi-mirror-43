[![Build Status](https://travis-ci.com/Sebi2020/csemver.svg?branch=master)](https://travis-ci.com/Sebi2020/csemver)
[![Coverage Status](https://coveralls.io/repos/github/Sebi2020/csemver/badge.svg?branch=feature%2Fdep)](https://coveralls.io/github/Sebi2020/csemver?branch=feature%2Fdep)
![Version Github: v0.2.0](https://img.shields.io/github/release/sebi2020/csemver.svg?colorB=green&style=flat)
[![Version PyPi: v0.2.0](https://img.shields.io/pypi/v/csemver.svg?colorB=green&style=flat)](https://pypi.org/project/csemver/)
![Issue Count](https://img.shields.io/github/issues-raw/sebi2020/csemver.svg?style=flat)
[![License: GPL-3](https://img.shields.io/github/license/sebi2020/csemver.svg?colorB=green&style=social)](https://github.com/Sebi2020/csemver/blob/master/LICENSE.md)
# csemver
csemver is the object orientied optimized Version of semver. It is much more consistent because you only need one object for all operations.
## Installation
```bash
pip install csemver
```
## Features
- Arithmetic comprehensions with `<,<=,==,!=,>=,>`
- Arithmetic additions with `+,+=`
- Access to specific parts (major, minor, patch, prerelease, build) through index operator

## Version manipulation
### Increase Versions
To increase the different versions **csemver** provides five methods
- `incMajor(incBy=1)`
- `incMinor(incBy=1)`
- `incPatch(incBy=1)`
- `incPrerelease(incBy=1)`
- `incBuild(incBy=1)`

If needed, you can chain the first three method calls: `a.incMajor(x).incMinor(y).incPatch(y)`. Attention: The order matters because an increment of major resets minor and an minor increment resets the patch version.

```python
from csemver import csemver as Version
a = Version();
print(a)
a.incMajor();
print(a)
a.incMinor();
print(a)
a.incPatch();
print(a)
```

```console
foo@bar:~$ python test.py
0.1.0
1.0.0
1.1.0
1.1.1
```
### Adding versions
```python
from csemver import csemver as Version
a = Version("2.1.5");
b = Version("1.1.1");
print(a+b);
b += Version("0.1.1");
print(b);
```
```console
3.1.1
1.2.1
```
**Note**: The addition respects [semver rules](https://semver.org/#semantic-versioning-specification-semver). Therefore the resulting versions are *3.1.1* and *1.2.1*  rather than *3.2.6* and *1.2.2*

### Overwrite Version
To overwrite the current Version just set a new **Semver-String** for `csemver.number`
```python
from csemver import csemver as Version
a = Version();
print(a)
a.number ="1.0.0-pre+build.1";
# Python 2.7: a.setNumber("1.0.0-pre+build.1")
print(a)
```
```bash
foo@bar:~$ python test.py
0.1.0
1.0.0-pre+build.1
```

### Manipulate specific parts
```python
from csemver import csemver as Version
a = Version(); # defaults to 0.1.0
a['major'] = 2
print(a)
a['minor'] = 2
print(a)
a['patch'] = 1
print(a)
a['prerelease'] = "dev"
print(a)
a['build'] = "build0"
print(a)
a['build'] = None
print(a)
```

```bash
2.1.0
2.2.0
2.2.1
2.2.1-dev
2.2.1-dev+build0
2.2.1-dev
```
### Reset Version
Delete the `number` property to reset the Version to `0.1.0`
```python
from csemver import csemver as Version
a = Version("1.0.0");
print(a)
del a.number
# Python 2.7: a.delNumber()
print(a)
```

```bash
foo@bar:~$ python test.py
1.0.0
0.1.0
```
## Comparing versions
### Compare different versions:
You can compare **csemver** instances with `>, >=, ==, !=, <=, <`
```python
from csemver import csemver as Version

a = Version("1.1.1")
b = Version("1.1.1")
repr(a)
repr(b)
print(a<b)

b.incPatch()
print(b)
print(a<b)
print(a<"1.1.2")
```

```bash
foo@bar:~$ python test.py
Version<1.1.1> instance at 0x00000159D2061BA8
Version<1.1.1> instance at 0x00000159D2061DD8
False
1.1.2
True
True
```

### Get a dictionary view
If you wish you can retrieve a view on the different version parts with `keys()` and `values()`:

```python
from csemver import csemver as Version

a = Version("1.1.1")
vals = a.values()
print(vals)
a['major'] = 3
print(vals)
```

```bash
odict_values([1, 1, 1, None, None])
odict_values([3, 1, 1, None, None])
```

### Iterate over csemver object
Note: All code examples import csemver like this `from csemver import csemver as Version` before using `Version(...)`.

**Plain version:**
```python
a = Version("1.0.0")
for i in zip(a.keys(),a): # Use only 'for i in a' if you don't need the keys
	print(i)
```

**With prerelease:**
```python
a = Version("1.0.0-pre")
for i in zip(a.keys(),a):
	print(i)
```
**With build-tag:**<br />
Attention: *Iteration stops at first NONE-ENTRY*
```python
a = Version("1.0.0+build")
for i in zip(a.keys(),a):
	print(i)
```
**Complete string:**
```python
a = Version("1.0.0-rc0+build0")
for i in zip(a.keys(),a):
	print(i)
```

**Output:** (additional print calls were ommitted in source)
```bash
Plain version:
('major', 1)
('minor', 0)
('patch', 0)

With prerelease:
('major', 1)
('minor', 0)
('patch', 0)
('prerelease', 'pre')

ATTENTION: Iteration stops at first NONE-ENTRY
('major', 1)
('minor', 0)
('patch', 0)

Complete string:
('major', 1)
('minor', 0)
('patch', 0)
('prerelease', 'rc0')
('build', 'build0')
```