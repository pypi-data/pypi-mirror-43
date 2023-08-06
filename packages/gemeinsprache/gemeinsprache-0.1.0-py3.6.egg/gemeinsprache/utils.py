from __future__ import division
import  re
import bz2
import fnmatch
import gzip
import json
import os
import shlex
import subprocess
import ast
from termcolor import colored


def normalize_filepath(fp):
    return os.path.realpath(os.path.abspath(os.path.expanduser(fp)))

def run_shell_command(cmd):
  exit_code = 0
  error_msg = ""
  out = b'\n'
  try:
    out = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
  except subprocess.CalledProcessError as err:
    print(err)
    print(err.__dict__)
    exit_code = err.returncode
    error_msg = err.stderr
    out = err.stdout
  ok = exit_code is 0
  try:
    decoded = out.decode("utf-8").strip()
  except AttributeError:
    decoded = out.strip()
  return ok, decoded, exit_code, error_msg


def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1<<50, 'PB'),
        (1<<40, 'TB'),
        (1<<30, 'GB'),
        (1<<20, 'MB'),
        (1<<10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

import math


def entropy(string):
        "Calculates the Shannon entropy of a string"

        # get probability of chars in string
        prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

        # calculate the entropy
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

        return entropy


def entropy_ideal(length):
        "Calculates the ideal Shannon entropy of a string with given length"

        prob = 1.0 / length

        return -1.0 * length * prob * math.log(prob) / math.log(2.0)



class Pretty:
  def __repr__(self):
    return self.prettified()
  
  def __init__(self, obj):
    try:
      self.data = obj.__dict__
    except:
      self.data = obj
    try:
      self.serialized = json.dumps(
        self.data, default=lambda x: str(x), sort_keys=True)
    except:
      self.serialized = None
    cmd = f"echo '{self.serialized}' | jq \".\" | pygmentize -l json -O style=paraiso-dark > /tmp/pretty.out"
    self.ok, self.stdout, self.exit_code, self.error_msg = run_shell_command(
      cmd)
    with open("/tmp/pretty.out", 'r') as f:
      self.output = f.read()
  
  def prettified(self):
    if self.ok:
      return self.output
    else:
      return self.error_msg
  
  def print(self):
    print(self.prettified())


def green(s, *attrs):
  return colored(s, 'green', attrs=['bold'].extend(list(attrs)))


def cyan(s, *attrs):
  return colored(s, 'cyan', attrs=['bold'].extend(list(attrs)))


def yellow(s, *attrs):
  return colored(s, 'yellow', attrs=['bold'].extend(list(attrs)))


def blue(s, *attrs):
  return colored(s, 'blue', attrs=['bold'].extend(list(attrs)))


def white(s, *attrs):
  return colored(s, 'white', attrs=['bold'].extend(list(attrs)))


def black(s, *attrs):
  return colored(s, 'black', attrs=['bold'].extend(list(attrs)))


def grey(s, *attrs):
  return colored(s, 'grey', attrs=['bold'].extend(list(attrs)))


def magenta(s, *attrs):
  return colored(s, 'magenta', attrs=['bold'] + list(attrs))


def red(s, *attrs):
  return colored(s, 'red', attrs=['bold'] + list(attrs))


def gen_find(filepat, top=None, pred=None, feeling_lucky=False, limit=999999):
  '''
Find all filenames in a directory tree that match a shell wildcard pattern
'''
  top = top if top is not None else os.getcwd()
  limit = 1 if feeling_lucky is True else limit if limit is not None else 9999999
  n = 0
  for path, dirlist, filelist in os.walk(top):
    for name in fnmatch.filter(filelist, filepat):
      n += 1
      fp = os.path.join(path, name)
      if pred is None:
        yield fp
      else:
        if pred(fp):
          yield fp
      if n >= limit:
        break
    if n >= limit:
      break


def gen_locate(patt,
               top=None,
               pred=None,
               feeling_lucky=False,
               max_wait=30,
               limit=9999999):
  '''
Find all filenames in a directory tree that match a shell wildcard pattern
'''
  top = top if top is not None else os.environ['HOME']
  limit = 1 if feeling_lucky is True else limit if limit is not None else 9999999
  n = 0
  pred = lambda x: True if pred is None else pred
  args = shlex.split(f"locate {patt} {top}")
  try:
    p = subprocess.check_output(args, timeout=max_wait, shell=True)
    for line in p.split(b'\n'):
      n += 1
      fp = line.decode("utf-8")
      if pred(fp):
        yield fp
      if n >= limit:
        break
  except subprocess.TimeoutExpired as e:
    print(f"Timed out: {e} (Max wait={max_wait})")
  except Exception as e:
    print(f"Got an unknown error: {e}")


def gen_filter(pred, filenames):
  for filename in filenames:
    if pred(filename):
      yield filename


def gen_opener(filenames):
  '''
Open a sequence of filenames one at a time producing a file object.
The file is closed immediately when proceeding to the next iteration.
'''
  for filename in filenames:
    if filename.endswith('.gz'):
      f = gzip.open(filename, 'rt')
    elif filename.endswith('.bz2'):
      f = bz2.open(filename, 'rt')
    else:
      f = open(filename, 'rt')
    yield f
    f.close()


def gen_concatenate(iterators):
  '''
Chain a sequence of iterators together into a single sequence.
'''
  for it in iterators:
    yield from it


def gen_grep(pattern, lines):
  '''
Look for a regex pattern in a sequence of lines
'''
  pat = re.compile(pattern)
  for line in lines:
    if pat.search(line):
      yield line





def is_valid_python(code):
  try:
    ast.parse(code)
  except SyntaxError:
    return False
  return True

def load_ptpython_history():
  with open(os.path.expanduser("~/.ptpython/history"), 'r') as f:
    raw = f.read()
  entries = re.split(r'(\n\n# )', raw)
  return entries

class REPLEntry:
  session_dir = os.path.expanduser("~/.ptpython/sessions")
  def __init__(self, raw_string):
    lines = raw_string.splitlines()
    os.makedirs(self.session_dir, exist_ok=True)
    self.raw_string = raw_string
    try:
      self.timestamp, self.session_id = lines[0].split(" SESS_ID:")
      self.session_id = int(self.session_id.strip())
      self.has_session = True
    except:
      self.has_session = False
      self.session_id = None
    self.lines = [line[1:] for line in lines if line.startswith("#")]
    self.body = ''.join(self.lines)
    self.path_to_session = os.path.join(self.session_dir, f"{self.session_id}.py")
    self.curr_session = self.load_session()
    self.ok = self.is_valid_entry()
    self.update_session()
  def load_session(self):
    if self.has_session and os.path.isfile(self.path_to_session):
      with open(self.path_to_session, 'r') as f:
        return f.read()
    else:
      return ""
  def is_valid_entry(self):
    maybe_valid = '\n'.join([self.curr_session, self.body])
    if is_valid_python(maybe_valid):
      return True
    else:
      return False
  def update_session(self):
    if self.is_valid_entry():
      if not os.path.isfile(self.path_to_session):
        with open(self.path_to_session, 'w') as f:
          f.write(self.body)
      else:
        with open(self.path_to_session, 'a') as f:
          f.write(self.body)
    print("Invalid code; not updating the session")
    
    
    
    
