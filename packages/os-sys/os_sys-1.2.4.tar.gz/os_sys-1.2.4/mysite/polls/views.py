from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("""
<!DOCTYPE html>

<html lang="eng" lang="eng">
<head>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
   <meta name="description" content="beschrijving van de webpagina" />
   <meta name="keywords" content="trefwoorden, gescheiden, door, komma's" />
   <title>os_sys docs index</title>
   <style type='text/css'>
   a { color: rgb(0,0,255); }
   </style>
</head>
<body>
<h1>index</h1>
<p>welcome at the os_sys docs.</p>
<h2>index:</h2>
<a href="#first">first</a><br>
<a href="#getting started">getting started with os_sys</a><br>
<a href="#process bars">process bars</a><br>
<a href="#discription">discription</a><br>
<a href="#help">help</a>
<hr>
<div id='first'>
<h2>first</h2>
<p>first there are somethings you need to know:<br>
1. this docs are under devlopment.<br>
2. if you want to add somethings to this docs go to os_sys github and post a what you want to add and i will ad it.<br>
3. have fun with this package.</p>
</div>
<hr>
<div id="getting started">
<p>
thanks for downloading os_sys. i hope you will enjoy using it this. this is a doc to help you getting started with os_sys.
os_sys is my first big package. again i hope you will enjoy using it so. lets get started.<br>
typ:<br>
import os_sys<br>
print(os_sys.msg)
if the installation was a succes you wil se in the shell:<br>
installation succes<br>
else you will get a error. so now you have installed os_sys you are ready to use it
</p>
</div>
<div id="progress bars">
<h1>loading_bars:
Easy progress reporting for Python</h1>
<p>|pypi|</p>
<h2>Bars</h2>
<p>There are 7 progress bars to choose from:</p>
<ul>
<li><code>Bar</code></li>
<li><code>ChargingBar</code></li>
<li><code>FillingSquaresBar</code></li>
<li><code>FillingCirclesBar</code></li>
<li><code>IncrementalBar</code></li>
<li><code>PixelBar</code></li>
<li><code>ShadyBar</code></li>
</ul>
<p>To use them, just call <code>next</code> to advance and <code>finish</code> to finish:</p>
<p>.. code-block:: python</p>
<pre><code>from os_sys.progress import bar

bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    bar.next()
bar.finish()
</code></pre>
<p>or use any bar of this class as a context manager:</p>
<p>.. code-block:: python</p>
<pre><code>from os_sys.progress import bar

with Bar('Processing', max=20) as bar:
    for i in range(20):
        # Do some work
        bar.next()
</code></pre>
<p>The result will be a bar like the following: ::</p>
<pre><code>Processing |#############                   | 42/100
</code></pre>
<p>To simplify the common case where the work is done in an iterator, you can
use the <code>iter</code> method:</p>
<p>.. code-block:: python</p>
<pre><code>for i in Bar('Processing').iter(it):
    # Do some work
</code></pre>
<p>Progress bars are very customizable, you can change their width, their fill
character, their suffix and more:</p>
<p>.. code-block:: python</p>
<pre><code>bar = Bar('Loading', fill='@', suffix='%(percent)d%%')
</code></pre>
<p>This will produce a bar like the following: ::</p>
<pre><code>Loading |@@@@@@@@@@@@@                   | 42%
</code></pre>
<p>You can use a number of template arguments in <code>message</code> and <code>suffix</code>:</p>
<p>==========  ================================
Name        Value
==========  ================================
index       current value
max         maximum value
remaining   max - index
progress    index / max
percent     progress * 100
avg         simple moving average time per item (in seconds)
elapsed     elapsed time in seconds
elapsed_td  elapsed as a timedelta (useful for printing as a string)
eta         avg * remaining
eta_td      eta as a timedelta (useful for printing as a string)
==========  ================================</p>
<p>Instead of passing all configuration options on instatiation, you can create
your custom subclass:</p>
<p>.. code-block:: python</p>
<pre><code>class FancyBar(Bar):
    message = 'Loading'
    fill = '*'
    suffix = '%(percent).1f%% - %(eta)ds'
</code></pre>
<p>You can also override any of the arguments or create your own:</p>
<p>.. code-block:: python</p>
<pre><code>class SlowBar(Bar):
    suffix = '%(remaining_hours)d hours remaining'
    @property
    def remaining_hours(self):
        return self.eta // 3600
</code></pre>
<h1>Spinners</h1>
<p>For actions with an unknown number of steps you can use a spinner:</p>
<p>.. code-block:: python</p>
<pre><code>from os_sys.progress import spinner

spinner = Spinner('Loading ')
while state != 'FINISHED':
    # Do some work
    spinner.next()
</code></pre>
<p>There are 5 predefined spinners:</p>
<ul>
<li><code>Spinner</code></li>
<li><code>PieSpinner</code></li>
<li><code>MoonSpinner</code></li>
<li><code>LineSpinner</code></li>
<li><code>PixelSpinner</code></li>
</ul>

</div>
<div id="discription">
<h1>include:</h1>
<pre><code>introduction


description                                                                                                                                                                    

license(at the end)
home
loading_bars
</code></pre>
<h1>introduction:</h1>
<pre><code>to install os_sys you type: pip install os_sys                                                                                  
to upgrade os_sys you type: pip install --upgrade os_sys                                                                                  
so lets get start to install os_sys                                                                                  
</code></pre>
<h1>discription:</h1>
<pre><code>os_sys is a extra package for python(3)                                                                                  
it's a extra to have a more easy use of the normal python libs                                                                                  
plz look sometimes to my packages becuse i am making more own libs(extra is not that own lib)                                                                                  
if i have more info i while show it here                                                                                   
plz read the license                                                                                  
</code></pre>
<h1>license:</h1>
<pre><code>Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</code></pre>
</div>
<div id="help">
<p>
'
Help on package os_sys:<br><br>NAME<br>    os_sys<br><br>PACKAGE CONTENTS<br>    _progress<br>    commands (package)<br>    discription<br>
errors<br>    fail<br>    html_text (package)<br>    modules<br>    os_sys<br>    programs (package)<br>    progress_bars<br>    py_install (package)<br>
system<br>    test (package)<br>    upload<br>    wifi<br><br>CLASSES<br>    builtins.object<br>        progress_types<br>    threading.Thread(builtins.object)<br>
progress_bar_loading<br>        tqdm<br>    tqdm._tqdm.tqdm(tqdm._utils.Comparable)<br>        tqdm._tqdm_gui.tqdm_gui<br><br>    gui_bar = class tqdm_gui(tqdm




._tqdm.tqdm)<br>     |  gui_bar(*args, **kwargs)<br>     |<br>     |  Experimental GUI version of tqdm!<br>     |<br>     |  Method resolution order:<b
r>     |      tqdm_gui<br>     |      tqdm._tqdm.tqdm<br>     |      tqdm._utils.Comparable<br>     |      builtins.object<br>     |<br>     |  Methods
defined here:<br>     |<br>     |  __init__(self, *args, **kwargs)<br>     |      Parameters<br>     |      ----------<br>     |      iterable  : iter
able, optional<br>     |          Iterable to decorate with a progressbar.<br>     |          Leave blank to manually manage the updates.<br>     |
desc  : str, optional<br>     |          Prefix for the progressbar.<br>     |      total  : int, optional<br>     |          The number of expected i
terations. If unspecified,<br>     |          len(iterable) is used if possible. If float("inf") or as a last<br>     |          resort, only basic pr
ogress statistics are displayed<br>     |          (no ETA, no progressbar).<br>     |          If `gui` is True and this parameter needs subsequent u
pdating,<br>     |          specify an initial arbitrary large positive integer,<br>     |          e.g. int(9e9).<br>     |      leave  : bool, optio
nal<br>     |          If [default: True], keeps all traces of the progressbar<br>     |          upon termination of iteration.<br>     |      file
: `io.TextIOWrapper` or `io.StringIO`, optional<br>     |          Specifies where to output the progress messages<br>     |          (default: sys.std
err). Uses `file.write(str)` and `file.flush()`<br>     |          methods.<br>     |      ncols  : int, optional<br>     |          The width of the
entire output message. If specified,<br>     |          dynamically resizes the progressbar to stay within this bound.<br>     |          If unspecifi
ed, attempts to use environment width. The<br>     |          fallback is a meter width of 10 and no limit for the counter and<br>     |          stat
istics. If 0, will not print any meter (only stats).<br>     |      mininterval  : float, optional<br>     |          Minimum progress display update
interval [default: 0.1] seconds.<br>     |      maxinterval  : float, optional<br>     |          Maximum progress display update interval [default: 1
0] seconds.<br>     |          Automatically adjusts `miniters` to correspond to `mininterval`<br>     |          after long display update lag. Only
works if `dynamic_miniters`<br>     |          or monitor thread is enabled.<br>     |      miniters  : int, optional<br>     |          Minimum progr
ess display update interval, in iterations.<br>     |          If 0 and `dynamic_miniters`, will automatically adjust to equal<br>     |          `min
interval` (more CPU efficient, good for tight loops).<br>     |          If > 0, will skip display of specified number of iterations.<br>     |
Tweak this and `mininterval` to get very efficient loops.<br>     |          If your progress is erratic with both fast and slow iterations<br>     |
(network, skipping items, etc) you should set miniters=1.<br>     |      ascii  : bool, optional<br>     |          If unspecified or False, use unicod
e (smooth blocks) to fill<br>     |          the meter. The fallback is to use ASCII characters `1-9 #`.<br>     |      disable  : bool, optional<br>
|          Whether to disable the entire progressbar wrapper<br>     |          [default: False]. If set to None, disable on non-TTY.<br>     |      un
it  : str, optional<br>     |          String that will be used to define the unit of each iteration<br>     |          [default: it].<br>     |      u
nit_scale  : bool or int or float, optional<br>     |          If 1 or True, the number of iterations will be reduced/scaled<br>     |          a
utomatically and a metric prefix following the<br>     |          International System of Units standard will be added<br>     |          (kilo, mega,
etc.) [default: False]. If any other non-zero<br>     |          number, will scale `total` and `n`.<br>     |      dynamic_ncols  : bool, optional<br>
|          If set, constantly alters `ncols` to the environment (allowing<br>     |          for window resizes) [default: False].<br>     |      smoothi
ng  : float, optional<br>     |          Exponential moving average smoothing factor for speed estimates<br>     |          (ignored in GUI mode). Range
s from 0 (average speed) to 1<br>     |          (current/instantaneous speed) [default: 0.3].<br>     |      bar_format  : str, optional<br>     |
Specify a custom bar string formatting. May impact performance.<br>     |          [default: \'{l_bar}{bar}{r_bar}\'], where<br>     |          l_bar=\'
{desc}: {percentage:3.0f}%|\' and<br>     |          r_bar=\'| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, \'<br>     |            \'{rate_fmt}{postfix
}]\'<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_
noinv_fmt,<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.<br>     |          Note that a trailing ": " is automatically
removed after {desc}<br>     |          if the latter is empty.<br>     |      initial  : int, optional<br>     |          The initial counter value. Usef
ul when restarting a progress<br>     |          bar [default: 0].<br>     |      position  : int, optional<br>     |          Specify the line offset to
print this bar (starting from 0)<br>     |          Automatic if unspecified.<br>     |          Useful to manage multiple bars at once (eg, from threads)
.<br>     |      postfix  : dict or *, optional<br>     |          Specify additional stats to display at the end of the bar.<br>     |          Calls `se
t_postfix(**postfix)` if possible (dict).<br>     |      unit_divisor  : float, optional<br>     |          [default: 1000], ignored unless `unit_scale` i
s True.<br>     |      gui  : bool, optional<br>     |          WARNING: internal parameter - do not use.<br>     |          Use tqdm_gui(...) instead. I
f set, will attempt to use<br>     |          matplotlib animations for a graphical output [default: False].<br>     |<br>     |      Returns<br>     |
-------<br>     |      out  : decorated iterator.<br>     |<br>     |  __iter__(self)<br>     |      Backward-compatibility to use: for x in tqdm(iterabl
e)<br>     |<br>     |  close(self)<br>     |      Cleanup and (if leave=False) close the progressbar.<br>     |<br>     |  update(self, n=1)<br>     |
Manually update the progress bar, useful for streams<br>     |      such as reading files.<br>     |      E.g.:<br>     |      >>> t = tqdm(total=filesize)
# Initialise<br>     |      >>> for current_buffer in stream:<br>     |      ...    ...<br>     |      ...    t.update(len(current_buffer))<br>     |      >
>> t.close()<br>     |      The last line is highly recommended, but possibly not necessary if<br>     |      `t.update()` will be called in such a way that
`filesize` will be<br>     |      exactly reached and printed.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      n  : int, option
al<br>     |          Increment to add to the internal counter of iterations<br>     |          [default: 1].<br>     |<br>     |  --------------------------
--------------------------------------------<br>     |  Methods inherited from tqdm._tqdm.tqdm:<br>     |<br>     |  __del__(self)<br>     |<br>     |  __ent
er__(self)<br>     |<br>     |  __exit__(self, *exc)<br>     |<br>     |  __hash__(self)<br>     |      Return hash(self).<br>     |<br>     |  __len__(self)
<br>     |<br>     |  __repr__(self)<br>     |      Return repr(self).<br>     |<br>     |  clear(self, nolock=False)<br>     |      Clear current bar displa
y<br>     |<br>     |  display(self, msg=None, pos=None)<br>     |      Use `self.sp` and to display `msg` in the specified `pos`.<br>     |<br>     |      P
arameters<br>     |      ----------<br>     |      msg  : what to display (default: repr(self))<br>     |      pos  : position to display in. (default: abs(s
elf.pos))<br>     |<br>     |  moveto(self, n)<br>     |<br>     |  refresh(self, nolock=False)<br>     |      Force refresh the display of this bar<br>
|<br>     |  set_description(self, desc=None, refresh=True)<br>     |      Set/modify description of the progress bar.<br>     |<br>     |      Parameters<br
|      ----------<br>     |      desc  : str, optional<br>     |      refresh  : bool, optional<br>     |          Forces refresh [default: True].<br>     |<b
r>     |  set_description_str(self, desc=None, refresh=True)<br>     |      Set/modify description without \': \' appended.<br>     |<br>     |  set_postfix(se
lf, ordered_dict=None, refresh=True, **kwargs)<br>     |      Set/modify postfix (additional stats)<br>     |      with automatic formatting based on datatype
.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      ordered_dict  : dict or OrderedDict, optional<br>     |      refresh  : bool, o
ptional<br>     |          Forces refresh [default: True].<br>     |      kwargs  : dict, optional<br>     |<br>     |  set_postfix_str(self, s=\'\', refresh=
True)<br>     |      Postfix without dictionary expansion, similar to prefix handling.<br>     |<br>     |  unpause(self)<br>     |      Restart tqdm timer fr
om last print time.<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Class methods inherited from tqdm._
tqdm.tqdm:<br>     |<br>     |  external_write_mode(file=None, nolock=False) from builtins.type<br>     |      Disable tqdm within context and refresh tqdm whe
n exits.<br>     |      Useful when writing to standard output stream<br>     |<br>     |  get_lock() from builtins.type<br>     |      Get the global lock. Con
struct it if it does not exist.<br>     |<br>     |  pandas(*targs, **tkwargs) from builtins.type<br>     |      Registers the given `tqdm` class with<br>     |
pandas.core.<br>     |          ( frame.DataFrame<br>     |          | series.Series<br>     |          | groupby.DataFrameGroupBy<br>     |          | groupby.
SeriesGroupBy<br>     |          ).progress_apply<br>     |<br>     |      A new instance will be create every time `progress_apply` is called,<br>     |      a
nd each instance will automatically close() upon completion.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      targs, tkwargs  : argum
ents for the tqdm instance<br>     |<br>     |      Examples<br>     |      --------<br>     |      >>> import pandas as pd<br>     |      >>> import numpy as np
<br>     |      >>> from tqdm import tqdm, tqdm_gui<br>     |      >>><br>     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))<br>     |
>>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc<br>     |      >>> # Now you can use `progress_apply` instead of `apply`<br>     |      >>> df
.groupby(0).progress_apply(lambda x: x**2)<br>     |<br>     |      References<br>     |      ----------<br>     |      https://stackoverflow.com/questions/186032
70/<br>     |      progress-indicator-during-pandas-operations-python<br>     |<br>     |  set_lock(lock) from builtins.type<br>     |      Set the global lock.<br
>     |<br>     |  write(s, file=None, end=\'<br>\', nolock=False) from builtins.type<br>     |      Print a message via tqdm (without overlap with bars)<br>     |<b
r>     |  ----------------------------------------------------------------------<br>     |  Static methods inherited from tqdm._tqdm.tqdm:<br>     |<br>     |  __ne
w__(cls, *args, **kwargs)<br>     |      Create and return a new object.  See help(type) for accurate signature.<br>     |<br>     |  ema(x, mu=None, alpha=0.3)<br>
|      Exponential moving average: smoothing to give progressively lower<br>     |      weights to older values.<br>     |<br>     |      Parameters<br>     |
----------<br>     |      x  : float<br>     |          New value to include in EMA.<br>     |      mu  : float, optional<br>     |          Previous EMA value.<br
>     |      alpha  : float, optional<br>     |          Smoothing factor in range [0, 1], [default: 0.3].<br>     |          Increase to give more weight to recent
values.<br>     |          Ranges from 0 (yields mu) to 1 (yields x).<br>     |<br>     |  format_interval(t)<br>     |      Formats a number of seconds as a clock
time, [H:]MM:SS<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      t  : int<br>     |          Number of seconds.<br>     |<br>     |
Returns<br>     |      -------<br>     |      out  : str<br>     |          [H:]MM:SS<br>     |<br>     |  format_meter(n, total, elapsed, ncols=None, prefix=\'\',
ascii=False, unit=\'it\', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000, **extra_kwargs)<br>     |      Return a string-based progr
ess bar given some parameters<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      n  : int<br>     |          Number of finished iteration
s.<br>     |      total  : int<br>     |          The expected total number of iterations. If meaningless (), only<br>     |          basic progress statistics ar
e displayed (no ETA).<br>     |      elapsed  : float<br>     |          Number of seconds passed since start.<br>     |      ncols  : int, optional<br>     |
The width of the entire output message. If specified,<br>     |          dynamically resizes the progress meter to stay within this bound<br>     |          [defau
lt: None]. The fallback meter width is 10 for the progress<br>     |          bar + no limit for the iterations counter and statistics. If 0,<br>     |          w
ill not print any meter (only stats).<br>     |      prefix  : str, optional<br>     |          Prefix message (included in total width) [default: \'\'].<br>
|          Use as {desc} in bar_format string.<br>     |      ascii  : bool, optional<br>     |          If not set, use unicode (smooth blocks) to fill the mete
r<br>     |          [default: False]. The fallback is to use ASCII characters<br>     |          (1-9 #).<br>     |      unit  : str, optional<br>     |
The iteration unit [default: \'it\'].<br>     |      unit_scale  : bool or int or float, optional<br>     |          If 1 or True, the number of iterations will
be printed with an<br>     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)<br>     |          [default: False]. If any other non-zero number,
will scale<br>     |          `total` and `n`.<br>     |      rate  : float, optional<br>     |          Manual override for iteration rate.<br>     |
If [default: None], uses n/elapsed.<br>     |      bar_format  : str, optional<br>     |          Specify a custom bar string formatting. May impact performanc
e.<br>     |          [default: \'{l_bar}{bar}{r_bar}\'], where<br>     |          l_bar=\'{desc}: {percentage:3.0f}%|\' and<br>     |          r_bar=\'| {n_fm
t}/{total_fmt} [{elapsed}<{remaining}, \'<br>     |            \'{rate_fmt}{postfix}]\'<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, t
otal_fmt,<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, p
ostfix.<br>     |          Note that a trailing ": " is automatically removed after {desc}<br>     |          if the latter is empty.<br>     |      postfix  :
*, optional<br>     |          Similar to `prefix`, but placed at the end<br>     |          (e.g. for additional stats).<br>     |          Note: postfix is u
sually a string (not a dict) for this method,<br>     |          and will if possible be set to postfix = \', \' + postfix.<br>     |          However other ty
pes are supported (#382).<br>     |      unit_divisor  : float, optional<br>     |          [default: 1000], ignored unless `unit_scale` is True.<br>     |<br>
|      Returns<br>     |      -------<br>     |      out  : Formatted meter and stats, ready to display.<br>     |<br>     |  format_num(n)<br>     |      Inte
lligent scientific notation (.3g).<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      n  : int or float or Numeric<br>     |
A Number.<br>     |<br>     |      Returns<br>     |      -------<br>     |      out  : str<br>     |          Formatted number.<br>     |<br>     |  format_si
zeof(num, suffix=\'\', divisor=1000)<br>     |      Formats a number (greater than unity) with SI Order of Magnitude<br>     |      prefixes.<br>     |<br>
|      Parameters<br>     |      ----------<br>     |      num  : float<br>     |          Number ( >= 1) to format.<br>     |      suffix  : str, optional<br>
|          Post-postfix [default: \'\'].<br>     |      divisor  : float, optionl<br>     |          Divisor between prefixes [default: 1000].<br>     |<br>
|      Returns<br>     |      -------<br>     |      out  : str<br>     |          Number with Order of Magnitude SI unit postfix.<br>     |<br>     |  status_p
rinter(file)<br>     |      Manage the printing and in-place updating of a line of characters.<br>     |      Note that if the string is longer than a line, the
n in-place<br>     |      updating may not work (it will print a new line at each refresh).<br>     |<br>     |  -----------------------------------------------
-----------------------<br>     |  Data descriptors inherited from tqdm._tqdm.tqdm:<br>     |<br>     |  format_dict<br>     |      Public API for read-only mem
ber access<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data and other attributes inherited from tqdm.
_tqdm.tqdm:<br>     |<br>     |  monitor = None<br>     |<br>     |  monitor_interval = 10<br>     |<br>     |  ------------------------------------------------

----------------------<br>     |  Methods inherited from tqdm._utils.Comparable:<br>     |<br>     |  __eq__(self, other)<br>     |      Return self==value.<br>
|<br>     |  __ge__(self, other)<br>     |      Return self>=value.<br>     |<br>     |  __gt__(self, other)<br>     |      Return self>value.<br>     |<br>
|  __le__(self, other)<br>     |      Return self<=value.<br>     |<br>     |  __lt__(self, other)<br>     |      Return self<value.<br>     |<br>     |  __ne__
(self, other)<br>     |      Return self!=value.<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data des
criptors inherited from tqdm._utils.Comparable:<br>     |<br>     |  __dict__<br>     |      dictionary for instance variables (if defined)<br>     |<br>     |
__weakref__<br>     |      list of weak references to the object (if defined)<br><br>    class progress_bar_loading(threading.Thread)<br>     |  progress_bar_lo
ading(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None)<br>     |<br>     |  A class that represents a thread of control.<br>     |<br>
|  This class can be safely subclassed in a limited fashion. There are two ways<br>     |  to specify the activity: by passing a callable object to the construc
tor, or<br>     |  by overriding the run() method in a subclass.<br>     |<br>     |  Method resolution order:<br>     |      progress_bar_loading<br>     |
threading.Thread<br>     |      builtins.object<br>     |<br>     |  Methods defined here:<br>     |<br>     |  kill(self)<br>     |<br>     |  run(self)<br>
|      Method representing the thread\'s activity.<br>     |<br>     |      You may override this method in a subclass. The standard run() method<br>     |
invokes the callable object passed to the object\'s constructor as the<br>     |      target argument, if any, with sequential and keyword arguments taken<br>
|      from the args and kwargs arguments, respectively.<br>     |<br>     |  ----------------------------------------------------------------------<br>     |
Data and other attributes defined here:<br>     |<br>     |  __all__ = [\'run\', \'kill\']<br>     |<br>     |  ------------------------------------------------
----------------------<br>     |  Methods inherited from threading.Thread:<br>     |<br>     |  __init__(self, group=None, target=None, name=None, args=(), kwar
gs=None, *, daemon=None)<br>     |      This constructor should always be called with keyword arguments. Arguments are:<br>     |<br>     |      *group* should
be None; reserved for future extension when a ThreadGroup<br>     |      class is implemented.<br>     |<br>     |      *target* is the callable object to be in
voked by the run()<br>     |      method. Defaults to None, meaning nothing is called.<br>     |<br>     |      *name* is the thread name. By default, a unique

name is constructed of<br>     |      the form "Thread-N" where N is a small decimal number.<br>     |<br>     |      *args* is the argument tuple for the targe
t invocation. Defaults to ().<br>     |<br>     |      *kwargs* is a dictionary of keyword arguments for the target<br>     |      invocation. Defaults to {}.<b
r>     |<br>     |      If a subclass overrides the constructor, it must make sure to invoke<br>     |      the base class constructor (Thread.__init__()) befor
e doing anything<br>     |      else to the thread.<br>     |<br>     |  __repr__(self)<br>     |      Return repr(self).<br>     |<br>     |  getName(self)<br>
|<br>     |  isAlive = is_alive(self)<br>     |      Return whether the thread is alive.<br>     |<br>     |      This method returns True just before the run()
method starts until just<br>     |      after the run() method terminates. The module function enumerate()<br>     |      returns a list of all alive threads.<b

r>     |<br>     |  isDaemon(self)<br>     |<br>     |  is_alive(self)<br>     |      Return whether the thread is alive.<br>     |<br>     |      This method r
eturns True just before the run() method starts until just<br>     |      after the run() method terminates. The module function enumerate()<br>     |      retu

rns a list of all alive threads.<br>     |<br>     |  join(self, timeout=None)<br>     |      Wait until the thread terminates.<br>     |<br>     |      This bl
ocks the calling thread until the thread whose join() method is<br>     |      called terminates -- either normally or through an unhandled exception<br>     |
or until the optional timeout occurs.<br>     |<br>     |      When the timeout argument is present and not None, it should be a<br>     |      floating point n
umber specifying a timeout for the operation in seconds<br>     |      (or fractions thereof). As join() always returns None, you must call<br>     |      isAli
ve() after join() to decide whether a timeout happened -- if the<br>     |      thread is still alive, the join() call timed out.<br>     |<br>     |      When
the timeout argument is not present or None, the operation will<br>     |      block until the thread terminates.<br>     |<br>     |      A thread can be join(
)ed many times.<br>     |<br>     |      join() raises a RuntimeError if an attempt is made to join the current<br>     |      thread as that would cause a dead
lock. It is also an error to join() a<br>     |      thread before it has been started and attempts to do so raises the same<br>     |      exception.<br>     |
<br>     |  setDaemon(self, daemonic)<br>     |<br>     |  setName(self, name)<br>     |<br>     |  start(self)<br>     |      Start the thread\'s activity.<br>
|<br>     |      It must be called at most once per thread object. It arranges for the<br>     |      object\'s run() method to be invoked in a separate thread
of control.<br>     |<br>     |      This method will raise a RuntimeError if called more than once on the<br>     |      same thread object.<br>     |<br>
|  ----------------------------------------------------------------------<br>     |  Data descriptors inherited from threading.Thread:<br>     |<br>     |  __di
ct__<br>     |      dictionary for instance variables (if defined)<br>     |<br>     |  __weakref__<br>     |      list of weak references to the object (if def
ined)<br>     |<br>     |  daemon<br>     |      A boolean value indicating whether this thread is a daemon thread.<br>     |<br>     |      This must be set be
fore start() is called, otherwise RuntimeError is<br>     |      raised. Its initial value is inherited from the creating thread; the<br>     |      main thread
is not a daemon thread and therefore all threads created in<br>     |      the main thread default to daemon = False.<br>     |<br>     |      The entire Python
program exits when no alive non-daemon threads are<br>     |      left.<br>     |<br>     |  ident<br>     |      Thread identifier of this thread or None if it
has not been started.<br>     |<br>     |      This is a nonzero integer. See the get_ident() function. Thread<br>     |      identifiers may be recycled when a
thread exits and another thread is<br>     |      created. The identifier is available even after the thread has exited.<br>     |<br>     |  name<br>     |

A string used for identification purposes only.<br>     |<br>     |      It has no semantics. Multiple threads may be given the same name. The<br>     |      in
itial name is set by the constructor.<br><br>    class progress_types(builtins.object)<br>     |  Data descriptors defined here:<br>     |<br>     |  __dict__<b
r>     |      dictionary for instance variables (if defined)<br>     |<br>     |  __weakref__<br>     |      list of weak references to the object (if defined)<
br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data and other attributes defined here:<br>     |<br>
|  __all__ = [\'bar\', \'charging_bar\', \'filling_sqares_bar\', \'filling_circl...<br>     |<br>     |  bar = <class \'progress.bar.Bar\'><br>     |<br>     |<
br>     |  charging_bar = <class \'progress.bar.ChargingBar\'><br>     |<br>     |<br>     |  countdown = <class \'progress.counter.Countdown\'><br>     |<br>
|<br>     |  counter = <class \'progress.counter.Counter\'><br>     |<br>     |<br>     |  filling_circles_bar = <class \'progress.bar.FillingCirclesBar\'><br>
|<br>     |<br>     |  filling_sqares_bar = <class \'progress.bar.FillingSquaresBar\'><br>     |<br>     |<br>     |  incremental_bar = <class \'progress.bar.In
crementalBar\'><br>     |<br>     |<br>     |  line_spinner = <class \'progress.spinner.LineSpinner\'><br>     |<br>     |<br>     |  moon_spinner = <class \'pr
ogress.spinner.MoonSpinner\'><br>     |<br>     |<br>     |  pie = <class \'progress.counter.Pie\'><br>     |<br>     |<br>     |  pie_spinner = <class \'progre
ss.spinner.PieSpinner\'><br>     |<br>     |<br>     |  pixel_bar = <class \'progress.bar.PixelBar\'><br>     |<br>     |<br>     |  pixel_spinner = <class \'pr
ogress.spinner.PixelSpinner\'><br>     |<br>     |<br>     |  shady_bar = <class \'progress.bar.ShadyBar\'><br>     |<br>     |<br>     |  spinner = <class \'pr
ogress.spinner.Spinner\'><br>     |<br>     |<br>     |  stack = <class \'progress.counter.Stack\'><br><br>    class tqdm(threading.Thread)<br>     |  tqdm(args
)<br>     |<br>     |  tqdm help<br>     |    <br>     |    Decorate an iterable object, returning an iterator which acts exactly<br>     |    like the origi

                        nal iterable, but prints a dynamically updating<br>     |    progressbar every time a value is requested.<br>     |    <br>     |<br>
|    def __init__(self, iterable=None, desc=None, total=None, leave=True,<br>     |                 file=None, ncols=None, mininterval=0.1,<br>     |
maxinterval=10.0, miniters=None, ascii=None, disable=False,<br>     |                 unit=\'it\', unit_scale=False, dynamic_ncols=False,<br>     |
smoothing=0.3, bar_format=None, initial=0, position=None,<br>     |                 postfix=None, unit_divisor=1000 total=100):<br>     |<br>     |  Method resoluti
on order:<br>     |      tqdm<br>     |      threading.Thread<br>     |      builtins.object<br>     |<br>     |  Methods defined here:<br>     |<br>     |  __init_
_(self, args)<br>     |      This constructor should always be called with keyword arguments. Arguments are:<br>     |<br>     |      *group* should be None; reserv
ed for future extension when a ThreadGroup<br>     |      class is implemented.<br>     |<br>     |      *target* is the callable object to be invoked by the run()<
br>     |      method. Defaults to None, meaning nothing is called.<br>     |<br>     |      *name* is the thread name. By default, a unique name is constructed of<

br>     |      the form "Thread-N" where N is a small decimal number.<br>     |<br>     |      *args* is the argument tuple for the target invocation. Defaults to (

).<br>     |<br>     |      *kwargs* is a dictionary of keyword arguments for the target<br>     |      invocation. Defaults to {}.<br>     |<br>     |      If a su
bclass overrides the constructor, it must make sure to invoke<br>     |      the base class constructor (Thread.__init__()) before doing anything<br>     |      els
e to the thread.<br>     |<br>     |  close()<br>     |<br>     |  run(self, between)<br>     |      Method representing the thread\'s activity.<br>     |<br>     |
You may override this method in a subclass. The standard run() method<br>     |      invokes the callable object passed to the object\'s constructor as the<br>

|      target argument, if any, with sequential and keyword arguments taken<br>     |      from the args and kwargs arguments, respectively.<br>     |<br>     |  up
date(self, n=1)<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data and other attributes defined here:<br>
|<br>     |  __all__ = [\'run\']<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Methods inherited from threa

ding.Thread:<br>     |<br>     |  __repr__(self)<br>     |      Return repr(self).<br>     |<br>     |  getName(self)<br>     |<br>     |  isAlive = is_alive(self)<b
r>     |      Return whether the thread is alive.<br>     |<br>     |      This method returns True just before the run() method starts until just<br>     |      aft
er the run() method terminates. The module function enumerate()<br>     |      returns a list of all alive threads.<br>     |<br>     |  isDaemon(self)<br>     |<br>

|  is_alive(self)<br>     |      Return whether the thread is alive.<br>     |<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()<br>     |      returns a list of all alive threads.<br>     |<br>     |  join(self
, timeout=None)<br>     |      Wait until the thread terminates.<br>     |<br>     |      This blocks the calling thread until the thread whose join() method is<br>
|      called terminates -- either normally or through an unhandled exception<br>     |      or until the optional timeout occurs.<br>     |<br>     |      When the

timeout argument is present and not None, it should be a<br>     |      floating point number specifying a timeout for the operation in seconds<br>     |      (or fr
actions thereof). As join() always returns None, you must call<br>     |      isAlive() after join() to decide whether a timeout happened -- if the<br>     |      th
read is still alive, the join() call timed out.<br>     |<br>     |      When the timeout argument is not present or None, the operation will<br>     |      block un

til the thread terminates.<br>     |<br>     |      A thread can be join()ed many times.<br>     |<br>     |      join() raises a RuntimeError if an attempt is made
to join the current<br>     |      thread as that would cause a deadlock. It is also an error to join() a<br>     |      thread before it has been started and attemp

ts to do so raises the same<br>     |      exception.<br>     |<br>     |  setDaemon(self, daemonic)<br>     |<br>     |  setName(self, name)<br>     |<br>     |  st
art(self)<br>     |      Start the thread\'s activity.<br>     |<br>     |      It must be called at most once per thread object. It arranges for the<br>     |
object\'s run() method to be invoked in a separate thread of control.<br>     |<br>     |      This method will raise a RuntimeError if called more than once on the<
br>     |      same thread object.<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data descriptors inherited
from threading.Thread:<br>     |<br>     |  __dict__<br>     |      dictionary for instance variables (if defined)<br>     |<br>     |  __weakref__<br>     |      li

st of weak references to the object (if defined)<br>     |<br>     |  daemon<br>     |      A boolean value indicating whether this thread is a daemon thread.<br>
|<br>     |      This must be set before start() is called, otherwise RuntimeError is<br>     |      raised. Its initial value is inherited from the creating thread;
the<br>     |      main thread is not a daemon thread and therefore all threads created in<br>     |      the main thread default to daemon = False.<br>     |<br>
|      The entire Python program exits when no alive non-daemon threads are<br>     |      left.<br>     |<br>     |  ident<br>     |      Thread identifier of this
thread or None if it has not been started.<br>     |<br>     |      This is a nonzero integer. See the get_ident() function. Thread<br>     |      identifiers may be
recycled when a thread exits and another thread is<br>     |      created. The identifier is available even after the thread has exited.<br>     |<br>     |  name<br
>     |      A string used for identification purposes only.<br>     |<br>     |      It has no semantics. Multiple threads may be given the same name. The<br>     |

initial name is set by the constructor.<br><br>    class tqdm_gui(tqdm._tqdm.tqdm)<br>     |  tqdm_gui(*args, **kwargs)<br>     |<br>     |  Experimental GUI version
of tqdm!<br>     |<br>     |  Method resolution order:<br>     |      tqdm_gui<br>     |      tqdm._tqdm.tqdm<br>     |      tqdm._utils.Comparable<br>     |      bu
iltins.object<br>     |<br>     |  Methods defined here:<br>     |<br>     |  __init__(self, *args, **kwargs)<br>     |      Parameters<br>     |      ----------<br>
|      iterable  : iterable, optional<br>     |          Iterable to decorate with a progressbar.<br>     |          Leave blank to manually manage the updates.<br>
|      desc  : str, optional<br>     |          Prefix for the progressbar.<br>     |      total  : int, optional<br>     |          The number is expected iteration
s. If unspecified,<br>     |          len(iterable) is used if possible. If float("inf") or as a last<br>     |          resort, only basic progress statistics are d
isplayed<br>     |          (no ETA, no progressbar).<br>     |          If `gui` is True and this parameter needs subsequent updating,<br>     |          specify an

initial arbitrary large positive integer,<br>     |          e.g. int(9e9).<br>     |      leave  : bool, optional<br>     |          If [default: True], keeps all t
races of the progressbar<br>     |          upon termination of iteration.<br>     |      file  : `io.TextIOWrapper` or `io.StringIO`, optional<br>     |          Sp
ecifies where to output the progress messages<br>     |          (default: sys.stderr). Uses `file.write(str)` and `file.flush()`<br>     |          methods.<br>
|      ncols  : int, optional<br>     |          The width of the entire output message. If specified,<br>     |          dynamically resizes the progressbar to stay
within this bound.<br>     |          If unspecified, attempts to use environment width. The<br>     |          fallback is a meter width of 10 and no limit for the
counter and<br>     |          statistics. If 0, will not print any meter (only stats).<br>     |      mininterval  : float, optional<br>     |          Minimum prog
ress display update interval [default: 0.1] seconds.<br>     |      maxinterval  : float, optional<br>     |          Maximum progress display update interval [defau
lt: 10] seconds.<br>     |          Automatically adjusts `miniters` to correspond to `mininterval`<br>     |          after long display update lag. Only works if `
dynamic_miniters`<br>     |          or monitor thread is enabled.<br>     |      miniters  : int, optional<br>     |          Minimum progress display update interv
al, in iterations.<br>     |          If 0 and `dynamic_miniters`, will automatically adjust to equal<br>     |          `mininterval` (more CPU efficient, good for
tight loops).<br>     |          If > 0, will skip display of specified number of iterations.<br>     |          Tweak this and `mininterval` to get very efficient l
oops.<br>     |          If your progress is erratic with both fast and slow iterations<br>     |          (network, skipping items, etc) you should set miniters=1.<
br>     |      ascii  : bool, optional<br>     |          If unspecified or False, use unicode (smooth blocks) to fill<br>     |          the meter. The fallback is
to use ASCII characters `1-9 #`.<br>     |      disable  : bool, optional<br>     |          Whether to disable the entire progressbar wrapper<br>     |          [de

fault: False]. If set to None, disable on non-TTY.<br>     |      unit  : str, optional<br>     |          String that will be used to define the unit of each iterat
ion<br>     |          [default: it].<br>     |      unit_scale  : bool or int or float, optional<br>     |          If 1 or True, the number of iterations will be r
educed/scaled<br>     |          automatically and a metric prefix following the<br>     |          International System of Units standard will be added<br>     |
(kilo, mega, etc.) [default: False]. If any other non-zero<br>     |          number, will scale `total` and `n`.<br>     |      dynamic_ncols  : bool, optional<br>

|          If set, constantly alters `ncols` to the environment (allowing<br>     |          for window resizes) [default: False].<br>     |      smoothing  : float,
optional<br>     |          Exponential moving average smoothing factor for speed estimates<br>     |          (ignored in GUI mode). Ranges from 0 (average speed) t
o 1<br>     |          (current/instantaneous speed) [default: 0.3].<br>     |      bar_format  : str, optional<br>     |          Specify a custom bar string format
ting. May impact performance.<br>     |          [default: \'{l_bar}{bar}{r_bar}\'], where<br>     |          l_bar=\'{desc}: {percentage:3.0f}%|\' and<br>     |
r_bar=\'| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, \'<br>     |            \'{rate_fmt}{postfix}]\'<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt,
total, total_fmt,<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc,
postfix.<br>     |          Note that a trailing ": " is automatically removed after {desc}<br>     |          if the latter is empty.<br>     |      initial  : int,

optional<br>     |          The initial counter value. Useful when restarting a progress<br>     |          bar [default: 0].<br>     |      position  : int, optiona
l<br>     |          Specify the line offset to print this bar (starting from 0)<br>     |          Automatic if unspecified.<br>     |          Useful to manage mul
tiple bars at once (eg, from threads).<br>     |      postfix  : dict or *, optional<br>     |          Specify additional stats to display at the end of the bar.<br
>     |          Calls `set_postfix(**postfix)` if possible (dict).<br>     |      unit_divisor  : float, optional<br>     |          [default: 1000], ignored unless
`unit_scale` is True.<br>     |      gui  : bool, optional<br>     |          WARNING: internal parameter - do not use.<br>     |          Use tqdm_gui(...) instead.
If set, will attempt to use<br>     |          matplotlib animations for a graphical output [default: False].<br>     |<br>     |      Returns<br>     |      -------
<br>     |      out  : decorated iterator.<br>     |<br>     |  __iter__(self)<br>     |      Backward-compatibility to use: for x in tqdm(iterable)<br>     |<br>

|  close(self)<br>     |      Cleanup and (if leave=False) close the progressbar.<br>     |<br>     |  update(self, n=1)<br>     |      Manually update the progress

bar, useful for streams<br>     |      such as reading files.<br>     |      E.g.:<br>     |      >>> t = tqdm(total=filesize) # Initialise<br>     |      >>> for cu
rrent_buffer in stream:<br>     |      ...    ...<br>     |      ...    t.update(len(current_buffer))<br>     |      >>> t.close()<br>     |      The last line is hi
ghly recommended, but possibly not necessary if<br>     |      `t.update()` will be called in such a way that `filesize` will be<br>     |      exactly reached and p

rinted.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      n  : int, optional<br>     |          Increment to add to the internal counter o
f iterations<br>     |          [default: 1].<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Methods inherite
d from tqdm._tqdm.tqdm:<br>     |<br>     |  __del__(self)<br>     |<br>     |  __enter__(self)<br>     |<br>     |  __exit__(self, *exc)<br>     |<br>     |  __hash
__(self)<br>     |      Return hash(self).<br>     |<br>     |  __len__(self)<br>     |<br>     |  __repr__(self)<br>     |      Return repr(self).<br>     |<br>
|  clear(self, nolock=False)<br>     |      Clear current bar display<br>     |<br>     |  display(self, msg=None, pos=None)<br>     |      Use `self.sp` and to disp
lay `msg` in the specified `pos`.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      msg  : what to display (default: repr(self))<br>     |
pos  : position to display in. (default: abs(self.pos))<br>     |<br>     |  moveto(self, n)<br>     |<br>     |  refresh(self, nolock=False)<br>     |      Force re
fresh the display of this bar<br>     |<br>     |  set_description(self, desc=None, refresh=True)<br>     |      Set/modify description of the progress bar.<br>
|<br>     |      Parameters<br>     |      ----------<br>     |      desc  : str, optional<br>     |      refresh  : bool, optional<br>     |          Forces refresh
[default: True].<br>     |<br>     |  set_description_str(self, desc=None, refresh=True)<br>     |      Set/modify description without \': \' appended.<br>     |<br>
|  set_postfix(self, ordered_dict=None, refresh=True, **kwargs)<br>     |      Set/modify postfix (additional stats)<br>     |      with automatic formatting based o
n datatype.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      ordered_dict  : dict or OrderedDict, optional<br>     |      refresh  : bool
, optional<br>     |          Forces refresh [default: True].<br>     |      kwargs  : dict, optional<br>     |<br>     |  set_postfix_str(self, s=\'\', refresh=True

)<br>     |      Postfix without dictionary expansion, similar to prefix handling.<br>     |<br>     |  unpause(self)<br>     |      Restart tqdm timer from last pri
nt time.<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Class methods inherited from tqdm._tqdm.tqdm:<br>
|<br>     |  external_write_mode(file=None, nolock=False) from builtins.type<br>     |      Disable tqdm within context and refresh tqdm when exits.<br>     |      U
seful when writing to standard output stream<br>     |<br>     |  get_lock() from builtins.type<br>     |      Get the global lock. Construct it if it does not exist
.<br>     |<br>     |  pandas(*targs, **tkwargs) from builtins.type<br>     |      Registers the given `tqdm` class with<br>     |          pandas.core.<br>     |
( frame.DataFrame<br>     |          | series.Series<br>     |          | groupby.DataFrameGroupBy<br>     |          | groupby.SeriesGroupBy<br>     |          ).pr
ogress_apply<br>     |<br>     |      A new instance will be create every time `progress_apply` is called,<br>     |      and each instance will automatically close(
) upon completion.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      targs, tkwargs  : arguments for the tqdm instance<br>     |<br>     |
Examples<br>     |      --------<br>     |      >>> import pandas as pd<br>     |      >>> import numpy as np<br>     |      >>> from tqdm import tqdm, tqdm_gui<br>
|      >>><br>     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))<br>     |      >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs
, etc<br>     |      >>> # Now you can use `progress_apply` instead of `apply`<br>     |      >>> df.groupby(0).progress_apply(lambda x: x**2)<br>     |<br>     |
References<br>     |      ----------<br>     |      https://stackoverflow.com/questions/18603270/<br>     |      progress-indicator-during-pandas operations-python<b
r>     |<br>     |  set_lock(lock) from builtins.type<br>     |      Set the global lock.<br>     |<br>     |  write(s, file=None, end=\'<br>\', nolock=False) from b
uiltins.type<br>     |      Print a message via tqdm (without overlap with bars)<br>     |<br>     |  ---------------------------------------------------------------
-------<br>     |  Static methods inherited from tqdm._tqdm.tqdm:<br>     |<br>     |  __new__(cls, *args, **kwargs)<br>     |      Create and return a new object.
See help(type) for accurate signature.<br>     |<br>     |  ema(x, mu=None, alpha=0.3)<br>     |      Exponential moving average: smoothing to give progressively low
er<br>     |      weights to older values.<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      x  : float<br>     |          New value to in

clude in EMA.<br>     |      mu  : float, optional<br>     |          Previous EMA value.<br>     |      alpha  : float, optional<br>     |          Smoothing factor

in range [0, 1], [default: 0.3].<br>     |          Increase to give more weight to recent values.<br>     |          Ranges from 0 (yields mu) to 1 (yields x).<br>

|<br>     |  format_interval(t)<br>     |      Formats a number of seconds as a clock time, [H:]MM:SS<br>     |<br>     |      Parameters<br>     |      ----------<b
r>     |      t  : int<br>     |          Number of seconds.<br>     |<br>     |      Returns<br>     |      -------<br>     |      out  : str<br>     |          [H:
]MM:SS<br>     |<br>     |  format_meter(n, total, elapsed, ncols=None, prefix=\'\', ascii=False, unit=\'it\', unit_scale=False, rate=None, bar_format=None, postfix=
None, unit_divisor=1000, **extra_kwargs)<br>     |      Return a string-based progress bar given some parameters<br>     |<br>     |      Parameters<br>     |      -
---------<br>     |      n  : int<br>     |          Number of finished iterations.<br>     |      total  : int<br>     |          The expected total number of itera
tions. If meaningless (), only<br>     |          basic progress statistics are displayed (no ETA).<br>     |      elapsed  : float<br>     |          Number of seco
nds passed since start.<br>     |      ncols  : int, optional<br>     |          The width of the entire output message. If specified,<br>     |          dynamically
resizes the progress meter to stay within this bound<br>     |          [default: None]. The fallback meter width is 10 for the progress<br>     |          bar + no
limit for the iterations counter and statistics. If 0,<br>     |          will not print any meter (only stats).<br>     |      prefix  : str, optional<br>     |
Prefix message (included in total width) [default: \'\'].<br>     |          Use as {desc} in bar_format string.<br>     |      ascii  : bool, optional<br>     |
If not set, use unicode (smooth blocks) to fill the meter<br>     |          [default: False]. The fallback is to use ASCII characters<br>     |          (1-9 #).<br
>     |      unit  : str, optional<br>     |          The iteration unit [default: \'it\'].<br>     |      unit_scale  : bool or int or float, optional<br>     |

If 1 or True, the number of iterations will be printed with an<br>     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)<br>     |          [default
: False]. If any other non-zero number, will scale<br>     |          `total` and `n`.<br>     |      rate  : float, optional<br>     |          Manual override for
iteration rate.<br>     |          If [default: None], uses n/elapsed.<br>     |      bar_format  : str, optional<br>     |          Specify a custom bar string form
atting. May impact performance.<br>     |          [default: \'{l_bar}{bar}{r_bar}\'], where<br>     |          l_bar=\'{desc}: {percentage:3.0f}%|\' and<br>     |
r_bar=\'| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, \'<br>     |            \'{rate_fmt}{postfix}]\'<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt,
total, total_fmt,<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc,

postfix.<br>     |          Note that a trailing ": " is automatically removed after {desc}<br>     |          if the latter is empty.<br>     |      postfix  : *, o
ptional<br>     |          Similar to `prefix`, but placed at the end<br>     |          (e.g. for additional stats).<br>     |          Note: postfix is usually a s
tring (not a dict) for this method,<br>     |          and will if possible be set to postfix = \', \' + postfix.<br>     |          However other types are supporte
d (#382).<br>     |      unit_divisor  : float, optional<br>     |          [default: 1000], ignored unless `unit_scale` is True.<br>     |<br>     |      Returns<br
>     |      -------<br>     |      out  : Formatted meter and stats, ready to display.<br>     |<br>     |  format_num(n)<br>     |      Intelligent scientific nota
tion (.3g).<br>     |<br>     |      Parameters<br>     |      ----------<br>     |      n  : int or float or Numeric<br>     |          A Number.<br>     |<br>

|      Returns<br>     |      -------<br>     |      out  : str<br>     |          Formatted number.<br>     |<br>     |  format_sizeof(num, suffix=\'\', divisor=100
0)<br>     |      Formats a number (greater than unity) with SI Order of Magnitude<br>     |      prefixes.<br>     |<br>     |      Parameters<br>     |      ------
----<br>     |      num  : float<br>     |          Number ( >= 1) to format.<br>     |      suffix  : str, optional<br>     |          Post-postfix [default: \'\'].
<br>     |      divisor  : float, optionl<br>     |          Divisor between prefixes [default: 1000].<br>     |<br>     |      Returns<br>     |      -------<br>
|      out  : str<br>     |          Number with Order of Magnitude SI unit postfix.<br>     |<br>     |  status_printer(file)<br>     |      Manage the printing and
in-place updating of a line of characters.<br>     |      Note that if the string is longer than a line, then in-place<br>     |      updating may not work (it will
print a new line at each refresh).<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Data descriptors inherited
from tqdm._tqdm.tqdm:<br>     |<br>     |  format_dict<br>     |      Public API for read-only member access<br>     |<br>     |  -----------------------------------
-----------------------------------<br>     |  Data and other attributes inherited from tqdm._tqdm.tqdm:<br>     |<br>     |  monitor = None<br>     |<br>     |  mon
itor_interval = 10<br>     |<br>     |  ----------------------------------------------------------------------<br>     |  Methods inherited from tqdm._utils.Comparab
le:<br>     |<br>     |  __eq__(self, other)<br>     |      Return self==value.<br>     |<br>     |  __ge__(self, other)<br>     |      Return self>=value.<br>     |

<br>     |  __gt__(self, other)<br>     |      Return self>value.<br>     |<br>     |  __le__(self, other)<br>     |      Return self<=value.<br>     |<br>     |  __l
t__(self, other)<br>     |      Return self<value.<br>     |<br>     |  __ne__(self, other)<br>     |      Return self!=value.<br>     |<br>     |  -------------------
---------------------------------------------------<br>     |  Data descriptors inherited from tqdm._utils.Comparable:<br>     |<br>     |  __dict__<br>     |      di
ctionary for instance variables (if defined)<br>     |<br>     |  __weakref__<br>     |      list of weak references to the object (if defined)<br><br>FUNCTIONS<br>
_code(txt)<br><br>    all_dict(dictory, exceptions=None, file_types=None, maps=True, files=False, print_data=False)<br><br>    bar(rn, fill=\'.\')<br><br>    download
(url, file, path=None)<br><br>    more_input()<br><br>    obj_type = object_type(obj)<br><br>    object_type(obj)<br><br>    test()<br><br>    update_progress(progres
s)<br>        # update_progress() : Displays or updates a console progress bar<br>        ## Accepts a float between 0 and 1. Any int will be converted to a float.<br
>        ## A value under 0 represents a \'halt\'.<br>        ## A value at 1 or bigger represents 100%<br><br>DATA<br>    __all__ = [\'os_sys\', \'fail\', \'modules\
', \'system\', \'wifi\', \'programs\', ...<br>    web = <os_sys.web_open object><br>'
'








</p>
</div>

</body>
</html>""")
# Create your views here.
