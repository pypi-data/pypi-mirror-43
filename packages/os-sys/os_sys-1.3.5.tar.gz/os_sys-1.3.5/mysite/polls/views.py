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
<a href="#progress bars">progress bars</a><br>
<a href="#discription">discription</a><br>
<a href="#help">help(os_sys)</a>
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


<html><p>

<br>
<br>
<br>No Python documentation found for 'Bar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'ChargingBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Countdown'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Counter'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'FillingCirclesBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'FillingSquaresBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'IncrementalBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Infinite'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'LineSpinner'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'MoonSpinner'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Pie'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'PieSpinner'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'PixelBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'PixelSpinner'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Progress'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'ShadyBar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Spinner'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Stack'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'Thread'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'WriteMixin'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'WritelnMixin'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '__all__'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '__builtins__'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '__cached__'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on str object:
<br>
<br>__doc__ = class str(object)
<br> |  str(object='') -> str
<br> |  str(bytes_or_buffer[, encoding[, errors]]) -> str
<br> |
<br> |  Create a new string object from the given object. If encoding or
<br> |  errors is specified, then the object must expose a data buffer
<br> |  that will be decoded using the given encoding and error handler.
<br> |  Otherwise, returns the result of object.__str__() (if defined)
<br> |  or repr(object).
<br> |  encoding defaults to sys.getdefaultencoding().
<br> |  errors defaults to 'strict'.
<br> |
<br> |  Methods defined here:
<br> |
<br> |  __add__(self, value, /)
<br> |      Return self+value.
<br> |
<br> |  __contains__(self, key, /)
<br> |      Return key in self.
<br> |
<br> |  __eq__(self, value, /)
<br> |      Return self==value.
<br> |
<br> |  __format__(self, format_spec, /)
<br> |      Return a formatted version of the string as described by format_spec.
<br> |
<br> |  __ge__(self, value, /)
<br> |      Return self>=value.
<br> |
<br> |  __getattribute__(self, name, /)
<br> |      Return getattr(self, name).
<br> |
<br> |  __getitem__(self, key, /)
<br> |      Return self[key].
<br> |
<br> |  __getnewargs__(...)
<br> |
<br> |  __gt__(self, value, /)
<br> |      Return self>value.
<br> |
<br> |  __hash__(self, /)
<br> |      Return hash(self).
<br> |
<br> |  __iter__(self, /)
<br> |      Implement iter(self).
<br> |
<br> |  __le__(self, value, /)
<br> |      Return self<=value.
<br> |
<br> |  __len__(self, /)
<br> |      Return len(self).
<br> |
<br> |  __lt__(self, value, /)
<br> |      Return self<value.
<br> |
<br> |  __mod__(self, value, /)
<br> |      Return self%value.
<br> |
<br> |  __mul__(self, value, /)
<br> |      Return self*value.
<br> |
<br> |  __ne__(self, value, /)
<br> |      Return self!=value.
<br> |
<br> |  __repr__(self, /)
<br> |      Return repr(self).
<br> |
<br> |  __rmod__(self, value, /)
<br> |      Return value%self.
<br> |
<br> |  __rmul__(self, value, /)
<br> |      Return value*self.
<br> |
<br> |  __sizeof__(self, /)
<br> |      Return the size of the string in memory, in bytes.
<br> |
<br> |  __str__(self, /)
<br> |      Return str(self).
<br> |
<br> |  capitalize(self, /)
<br> |      Return a capitalized version of the string.
<br> |
<br> |      More specifically, make the first character have upper case and the rest lower
<br> |      case.
<br> |
<br> |  casefold(self, /)
<br> |      Return a version of the string suitable for caseless comparisons.
<br> |
<br> |  center(self, width, fillchar=' ', /)
<br> |      Return a centered string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  count(...)
<br> |      S.count(sub[, start[, end]]) -> int
<br> |
<br> |      Return the number of non-overlapping occurrences of substring sub in
<br> |      string S[start:end].  Optional arguments start and end are
<br> |      interpreted as in slice notation.
<br> |
<br> |  encode(self, /, encoding='utf-8', errors='strict')
<br> |      Encode the string using the codec registered for encoding.
<br> |
<br> |      encoding
<br> |        The encoding in which to encode the string.
<br> |      errors
<br> |        The error handling scheme to use for encoding errors.
<br> |        The default is 'strict' meaning that encoding errors raise a
<br> |        UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
<br> |        'xmlcharrefreplace' as well as any other name registered with
<br> |        codecs.register_error that can handle UnicodeEncodeErrors.
<br> |
<br> |  endswith(...)
<br> |      S.endswith(suffix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S ends with the specified suffix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      suffix can also be a tuple of strings to try.
<br> |
<br> |  expandtabs(self, /, tabsize=8)
<br> |      Return a copy where all tab characters are expanded using spaces.
<br> |
<br> |      If tabsize is not given, a tab size of 8 characters is assumed.
<br> |
<br> |  find(...)
<br> |      S.find(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  format(...)
<br> |      S.format(*args, **kwargs) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from args and kwargs.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  format_map(...)
<br> |      S.format_map(mapping) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from mapping.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  index(...)
<br> |      S.index(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  isalnum(self, /)
<br> |      Return True if the string is an alpha-numeric string, False otherwise.
<br> |
<br> |      A string is alpha-numeric if all characters in the string are alpha-numeric and
<br> |      there is at least one character in the string.
<br> |
<br> |  isalpha(self, /)
<br> |      Return True if the string is an alphabetic string, False otherwise.
<br> |
<br> |      A string is alphabetic if all characters in the string are alphabetic and there
<br> |      is at least one character in the string.
<br> |
<br> |  isascii(self, /)
<br> |      Return True if all characters in the string are ASCII, False otherwise.
<br> |
<br> |      ASCII characters have code points in the range U+0000-U+007F.
<br> |      Empty string is ASCII too.
<br> |
<br> |  isdecimal(self, /)
<br> |      Return True if the string is a decimal string, False otherwise.
<br> |
<br> |      A string is a decimal string if all characters in the string are decimal and
<br> |      there is at least one character in the string.
<br> |
<br> |  isdigit(self, /)
<br> |      Return True if the string is a digit string, False otherwise.
<br> |
<br> |      A string is a digit string if all characters in the string are digits and there
<br> |      is at least one character in the string.
<br> |
<br> |  isidentifier(self, /)
<br> |      Return True if the string is a valid Python identifier, False otherwise.
<br> |
<br> |      Use keyword.iskeyword() to test for reserved identifiers such as "def" and
<br> |      "class".
<br> |
<br> |  islower(self, /)
<br> |      Return True if the string is a lowercase string, False otherwise.
<br> |
<br> |      A string is lowercase if all cased characters in the string are lowercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  isnumeric(self, /)
<br> |      Return True if the string is a numeric string, False otherwise.
<br> |
<br> |      A string is numeric if all characters in the string are numeric and there is at
<br> |      least one character in the string.
<br> |
<br> |  isprintable(self, /)
<br> |      Return True if the string is printable, False otherwise.
<br> |
<br> |      A string is printable if all of its characters are considered printable in
<br> |      repr() or if it is empty.
<br> |
<br> |  isspace(self, /)
<br> |      Return True if the string is a whitespace string, False otherwise.
<br> |
<br> |      A string is whitespace if all characters in the string are whitespace and there
<br> |      is at least one character in the string.
<br> |
<br> |  istitle(self, /)
<br> |      Return True if the string is a title-cased string, False otherwise.
<br> |
<br> |      In a title-cased string, upper- and title-case characters may only
<br> |      follow uncased characters and lowercase characters only cased ones.
<br> |
<br> |  isupper(self, /)
<br> |      Return True if the string is an uppercase string, False otherwise.
<br> |
<br> |      A string is uppercase if all cased characters in the string are uppercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  join(self, iterable, /)
<br> |      Concatenate any number of strings.
<br> |
<br> |      The string whose method is called is inserted in between each given string.
<br> |      The result is returned as a new string.
<br> |
<br> |      Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
<br> |
<br> |  ljust(self, width, fillchar=' ', /)
<br> |      Return a left-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  lower(self, /)
<br> |      Return a copy of the string converted to lowercase.
<br> |
<br> |  lstrip(self, chars=None, /)
<br> |      Return a copy of the string with leading whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  partition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string.  If the separator is found,
<br> |      returns a 3-tuple containing the part before the separator, the separator
<br> |      itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing the original string
<br> |      and two empty strings.
<br> |
<br> |  replace(self, old, new, count=-1, /)
<br> |      Return a copy with all occurrences of substring old replaced by new.
<br> |
<br> |        count
<br> |          Maximum number of occurrences to replace.
<br> |          -1 (the default value) means replace all occurrences.
<br> |
<br> |      If the optional argument count is given, only the first count occurrences are
<br> |      replaced.
<br> |
<br> |  rfind(...)
<br> |      S.rfind(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  rindex(...)
<br> |      S.rindex(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  rjust(self, width, fillchar=' ', /)
<br> |      Return a right-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  rpartition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string, starting at the end. If
<br> |      the separator is found, returns a 3-tuple containing the part before the
<br> |      separator, the separator itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing two empty strings
<br> |      and the original string.
<br> |
<br> |  rsplit(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |        sep
<br> |          The delimiter according which to split the string.
<br> |          None (the default value) means split according to any whitespace,
<br> |          and discard empty strings from the result.
<br> |        maxsplit
<br> |          Maximum number of splits to do.
<br> |          -1 (the default value) means no limit.
<br> |
<br> |      Splits are done starting at the end of the string and working to the front.
<br> |
<br> |  rstrip(self, chars=None, /)
<br> |      Return a copy of the string with trailing whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  split(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |      sep
<br> |        The delimiter according which to split the string.
<br> |        None (the default value) means split according to any whitespace,
<br> |        and discard empty strings from the result.
<br> |      maxsplit
<br> |        Maximum number of splits to do.
<br> |        -1 (the default value) means no limit.
<br> |
<br> |  splitlines(self, /, keepends=False)
<br> |      Return a list of the lines in the string, breaking at line boundaries.
<br> |
<br> |      Line breaks are not included in the resulting list unless keepends is given and
<br> |      true.
<br> |
<br> |  startswith(...)
<br> |      S.startswith(prefix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S starts with the specified prefix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      prefix can also be a tuple of strings to try.
<br> |
<br> |  strip(self, chars=None, /)
<br> |      Return a copy of the string with leading and trailing whitespace remove.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  swapcase(self, /)
<br> |      Convert uppercase characters to lowercase and lowercase characters to uppercase.
<br> |
<br> |  title(self, /)
<br> |      Return a version of the string where each word is titlecased.
<br> |
<br> |      More specifically, words start with uppercased characters and all remaining
<br> |      cased characters have lower case.
<br> |
<br> |  translate(self, table, /)
<br> |      Replace each character in the string using the given translation table.
<br> |
<br> |        table
<br> |          Translation table, which must be a mapping of Unicode ordinals to
<br> |          Unicode ordinals, strings, or None.
<br> |
<br> |      The table must implement lookup/indexing via __getitem__, for instance a
<br> |      dictionary or list.  If this operation raises LookupError, the character is
<br> |      left untouched.  Characters mapped to None are deleted.
<br> |
<br> |  upper(self, /)
<br> |      Return a copy of the string converted to uppercase.
<br> |
<br> |  zfill(self, width, /)
<br> |      Pad a numeric string with zeros on the left, to fill a field of the given width.
<br> |
<br> |      The string is never truncated.
<br> |
<br> |  <hr>
<br> |  Static methods defined here:
<br> |
<br> |  __new__(*args, **kwargs) from builtins.type
<br> |      Create and return a new object.  See help(type) for accurate signature.
<br> |
<br> |  maketrans(x, y=None, z=None, /)
<br> |      Return a translation table usable for str.translate().
<br> |
<br> |      If there is only one argument, it must be a dictionary mapping Unicode
<br> |      ordinals (integers) or characters to Unicode ordinals, strings or None.
<br> |      Character keys will be then converted to ordinals.
<br> |      If there are two arguments, they must be strings of equal length, and
<br> |      in the resulting dictionary, each character in x will be mapped to the
<br> |      character at the same position in y. If there is a third argument, it
<br> |      must be a string, whose characters will be mapped to None in the result.
<br>
<br>No Python documentation found for '__file__'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on class BuiltinImporter in module importlib._bootstrap:
<br>
<br>__loader__ = class BuiltinImporter(builtins.object)
<br> |  Meta path import for built-in modules.
<br> |
<br> |  All methods are either class or static methods to avoid the need to
<br> |  instantiate the class.
<br> |
<br> |  Class methods defined here:
<br> |
<br> |  create_module(spec) from builtins.type
<br> |      Create a built-in module
<br> |
<br> |  exec_module(module) from builtins.type
<br> |      Exec a built-in module
<br> |
<br> |  find_module(fullname, path=None) from builtins.type
<br> |      Find the built-in module.
<br> |
<br> |      If 'path' is ever specified then the search is considered a failure.
<br> |
<br> |      This method is deprecated.  Use find_spec() instead.
<br> |
<br> |  find_spec(fullname, path=None, target=None) from builtins.type
<br> |
<br> |  get_code(fullname) from builtins.type
<br> |      Return None as built-in modules do not have code objects.
<br> |
<br> |  get_source(fullname) from builtins.type
<br> |      Return None as built-in modules do not have source code.
<br> |
<br> |  is_package(fullname) from builtins.type
<br> |      Return False as built-in modules are never packages.
<br> |
<br> |  load_module = _load_module_shim(fullname) from builtins.type
<br> |      Load the specified module into sys.modules and return it.
<br> |
<br> |      This method is deprecated.  Use loader.exec_module instead.
<br> |
<br> |  <hr>
<br> |  Static methods defined here:
<br> |
<br> |  module_repr(module)
<br> |      Return repr for the module.
<br> |
<br> |      The method is deprecated.  The import machinery does the job itself.
<br> |
<br> |  <hr>
<br> |  Data descriptors defined here:
<br> |
<br> |  __dict__
<br> |      dictionary for instance variables (if defined)
<br> |
<br> |  __weakref__
<br> |      list of weak references to the object (if defined)
<br>
<br>Help on str object:
<br>
<br>__name__ = class str(object)
<br> |  str(object='') -> str
<br> |  str(bytes_or_buffer[, encoding[, errors]]) -> str
<br> |
<br> |  Create a new string object from the given object. If encoding or
<br> |  errors is specified, then the object must expose a data buffer
<br> |  that will be decoded using the given encoding and error handler.
<br> |  Otherwise, returns the result of object.__str__() (if defined)
<br> |  or repr(object).
<br> |  encoding defaults to sys.getdefaultencoding().
<br> |  errors defaults to 'strict'.
<br> |
<br> |  Methods defined here:
<br> |
<br> |  __add__(self, value, /)
<br> |      Return self+value.
<br> |
<br> |  __contains__(self, key, /)
<br> |      Return key in self.
<br> |
<br> |  __eq__(self, value, /)
<br> |      Return self==value.
<br> |
<br> |  __format__(self, format_spec, /)
<br> |      Return a formatted version of the string as described by format_spec.
<br> |
<br> |  __ge__(self, value, /)
<br> |      Return self>=value.
<br> |
<br> |  __getattribute__(self, name, /)
<br> |      Return getattr(self, name).
<br> |
<br> |  __getitem__(self, key, /)
<br> |      Return self[key].
<br> |
<br> |  __getnewargs__(...)
<br> |
<br> |  __gt__(self, value, /)
<br> |      Return self>value.
<br> |
<br> |  __hash__(self, /)
<br> |      Return hash(self).
<br> |
<br> |  __iter__(self, /)
<br> |      Implement iter(self).
<br> |
<br> |  __le__(self, value, /)
<br> |      Return self<=value.
<br> |
<br> |  __len__(self, /)
<br> |      Return len(self).
<br> |
<br> |  __lt__(self, value, /)
<br> |      Return self<value.
<br> |
<br> |  __mod__(self, value, /)
<br> |      Return self%value.
<br> |
<br> |  __mul__(self, value, /)
<br> |      Return self*value.
<br> |
<br> |  __ne__(self, value, /)
<br> |      Return self!=value.
<br> |
<br> |  __repr__(self, /)
<br> |      Return repr(self).
<br> |
<br> |  __rmod__(self, value, /)
<br> |      Return value%self.
<br> |
<br> |  __rmul__(self, value, /)
<br> |      Return value*self.
<br> |
<br> |  __sizeof__(self, /)
<br> |      Return the size of the string in memory, in bytes.
<br> |
<br> |  __str__(self, /)
<br> |      Return str(self).
<br> |
<br> |  capitalize(self, /)
<br> |      Return a capitalized version of the string.
<br> |
<br> |      More specifically, make the first character have upper case and the rest lower
<br> |      case.
<br> |
<br> |  casefold(self, /)
<br> |      Return a version of the string suitable for caseless comparisons.
<br> |
<br> |  center(self, width, fillchar=' ', /)
<br> |      Return a centered string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  count(...)
<br> |      S.count(sub[, start[, end]]) -> int
<br> |
<br> |      Return the number of non-overlapping occurrences of substring sub in
<br> |      string S[start:end].  Optional arguments start and end are
<br> |      interpreted as in slice notation.
<br> |
<br> |  encode(self, /, encoding='utf-8', errors='strict')
<br> |      Encode the string using the codec registered for encoding.
<br> |
<br> |      encoding
<br> |        The encoding in which to encode the string.
<br> |      errors
<br> |        The error handling scheme to use for encoding errors.
<br> |        The default is 'strict' meaning that encoding errors raise a
<br> |        UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
<br> |        'xmlcharrefreplace' as well as any other name registered with
<br> |        codecs.register_error that can handle UnicodeEncodeErrors.
<br> |
<br> |  endswith(...)
<br> |      S.endswith(suffix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S ends with the specified suffix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      suffix can also be a tuple of strings to try.
<br> |
<br> |  expandtabs(self, /, tabsize=8)
<br> |      Return a copy where all tab characters are expanded using spaces.
<br> |
<br> |      If tabsize is not given, a tab size of 8 characters is assumed.
<br> |
<br> |  find(...)
<br> |      S.find(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  format(...)
<br> |      S.format(*args, **kwargs) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from args and kwargs.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  format_map(...)
<br> |      S.format_map(mapping) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from mapping.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  index(...)
<br> |      S.index(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  isalnum(self, /)
<br> |      Return True if the string is an alpha-numeric string, False otherwise.
<br> |
<br> |      A string is alpha-numeric if all characters in the string are alpha-numeric and
<br> |      there is at least one character in the string.
<br> |
<br> |  isalpha(self, /)
<br> |      Return True if the string is an alphabetic string, False otherwise.
<br> |
<br> |      A string is alphabetic if all characters in the string are alphabetic and there
<br> |      is at least one character in the string.
<br> |
<br> |  isascii(self, /)
<br> |      Return True if all characters in the string are ASCII, False otherwise.
<br> |
<br> |      ASCII characters have code points in the range U+0000-U+007F.
<br> |      Empty string is ASCII too.
<br> |
<br> |  isdecimal(self, /)
<br> |      Return True if the string is a decimal string, False otherwise.
<br> |
<br> |      A string is a decimal string if all characters in the string are decimal and
<br> |      there is at least one character in the string.
<br> |
<br> |  isdigit(self, /)
<br> |      Return True if the string is a digit string, False otherwise.
<br> |
<br> |      A string is a digit string if all characters in the string are digits and there
<br> |      is at least one character in the string.
<br> |
<br> |  isidentifier(self, /)
<br> |      Return True if the string is a valid Python identifier, False otherwise.
<br> |
<br> |      Use keyword.iskeyword() to test for reserved identifiers such as "def" and
<br> |      "class".
<br> |
<br> |  islower(self, /)
<br> |      Return True if the string is a lowercase string, False otherwise.
<br> |
<br> |      A string is lowercase if all cased characters in the string are lowercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  isnumeric(self, /)
<br> |      Return True if the string is a numeric string, False otherwise.
<br> |
<br> |      A string is numeric if all characters in the string are numeric and there is at
<br> |      least one character in the string.
<br> |
<br> |  isprintable(self, /)
<br> |      Return True if the string is printable, False otherwise.
<br> |
<br> |      A string is printable if all of its characters are considered printable in
<br> |      repr() or if it is empty.
<br> |
<br> |  isspace(self, /)
<br> |      Return True if the string is a whitespace string, False otherwise.
<br> |
<br> |      A string is whitespace if all characters in the string are whitespace and there
<br> |      is at least one character in the string.
<br> |
<br> |  istitle(self, /)
<br> |      Return True if the string is a title-cased string, False otherwise.
<br> |
<br> |      In a title-cased string, upper- and title-case characters may only
<br> |      follow uncased characters and lowercase characters only cased ones.
<br> |
<br> |  isupper(self, /)
<br> |      Return True if the string is an uppercase string, False otherwise.
<br> |
<br> |      A string is uppercase if all cased characters in the string are uppercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  join(self, iterable, /)
<br> |      Concatenate any number of strings.
<br> |
<br> |      The string whose method is called is inserted in between each given string.
<br> |      The result is returned as a new string.
<br> |
<br> |      Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
<br> |
<br> |  ljust(self, width, fillchar=' ', /)
<br> |      Return a left-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  lower(self, /)
<br> |      Return a copy of the string converted to lowercase.
<br> |
<br> |  lstrip(self, chars=None, /)
<br> |      Return a copy of the string with leading whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  partition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string.  If the separator is found,
<br> |      returns a 3-tuple containing the part before the separator, the separator
<br> |      itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing the original string
<br> |      and two empty strings.
<br> |
<br> |  replace(self, old, new, count=-1, /)
<br> |      Return a copy with all occurrences of substring old replaced by new.
<br> |
<br> |        count
<br> |          Maximum number of occurrences to replace.
<br> |          -1 (the default value) means replace all occurrences.
<br> |
<br> |      If the optional argument count is given, only the first count occurrences are
<br> |      replaced.
<br> |
<br> |  rfind(...)
<br> |      S.rfind(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  rindex(...)
<br> |      S.rindex(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  rjust(self, width, fillchar=' ', /)
<br> |      Return a right-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  rpartition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string, starting at the end. If
<br> |      the separator is found, returns a 3-tuple containing the part before the
<br> |      separator, the separator itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing two empty strings
<br> |      and the original string.
<br> |
<br> |  rsplit(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |        sep
<br> |          The delimiter according which to split the string.
<br> |          None (the default value) means split according to any whitespace,
<br> |          and discard empty strings from the result.
<br> |        maxsplit
<br> |          Maximum number of splits to do.
<br> |          -1 (the default value) means no limit.
<br> |
<br> |      Splits are done starting at the end of the string and working to the front.
<br> |
<br> |  rstrip(self, chars=None, /)
<br> |      Return a copy of the string with trailing whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  split(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |      sep
<br> |        The delimiter according which to split the string.
<br> |        None (the default value) means split according to any whitespace,
<br> |        and discard empty strings from the result.
<br> |      maxsplit
<br> |        Maximum number of splits to do.
<br> |        -1 (the default value) means no limit.
<br> |
<br> |  splitlines(self, /, keepends=False)
<br> |      Return a list of the lines in the string, breaking at line boundaries.
<br> |
<br> |      Line breaks are not included in the resulting list unless keepends is given and
<br> |      true.
<br> |
<br> |  startswith(...)
<br> |      S.startswith(prefix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S starts with the specified prefix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      prefix can also be a tuple of strings to try.
<br> |
<br> |  strip(self, chars=None, /)
<br> |      Return a copy of the string with leading and trailing whitespace remove.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  swapcase(self, /)
<br> |      Convert uppercase characters to lowercase and lowercase characters to uppercase.
<br> |
<br> |  title(self, /)
<br> |      Return a version of the string where each word is titlecased.
<br> |
<br> |      More specifically, words start with uppercased characters and all remaining
<br> |      cased characters have lower case.
<br> |
<br> |  translate(self, table, /)
<br> |      Replace each character in the string using the given translation table.
<br> |
<br> |        table
<br> |          Translation table, which must be a mapping of Unicode ordinals to
<br> |          Unicode ordinals, strings, or None.
<br> |
<br> |      The table must implement lookup/indexing via __getitem__, for instance a
<br> |      dictionary or list.  If this operation raises LookupError, the character is
<br> |      left untouched.  Characters mapped to None are deleted.
<br> |
<br> |  upper(self, /)
<br> |      Return a copy of the string converted to uppercase.
<br> |
<br> |  zfill(self, width, /)
<br> |      Pad a numeric string with zeros on the left, to fill a field of the given width.
<br> |
<br> |      The string is never truncated.
<br> |
<br> |  <hr>
<br> |  Static methods defined here:
<br> |
<br> |  __new__(*args, **kwargs) from builtins.type
<br> |      Create and return a new object.  See help(type) for accurate signature.
<br> |
<br> |  maketrans(x, y=None, z=None, /)
<br> |      Return a translation table usable for str.translate().
<br> |
<br> |      If there is only one argument, it must be a dictionary mapping Unicode
<br> |      ordinals (integers) or characters to Unicode ordinals, strings or None.
<br> |      Character keys will be then converted to ordinals.
<br> |      If there are two arguments, they must be strings of equal length, and
<br> |      in the resulting dictionary, each character in x will be mapped to the
<br> |      character at the same position in y. If there is a third argument, it
<br> |      must be a string, whose characters will be mapped to None in the result.
<br>
<br>Help on str object:
<br>
<br>__package__ = class str(object)
<br> |  str(object='') -> str
<br> |  str(bytes_or_buffer[, encoding[, errors]]) -> str
<br> |
<br> |  Create a new string object from the given object. If encoding or
<br> |  errors is specified, then the object must expose a data buffer
<br> |  that will be decoded using the given encoding and error handler.
<br> |  Otherwise, returns the result of object.__str__() (if defined)
<br> |  or repr(object).
<br> |  encoding defaults to sys.getdefaultencoding().
<br> |  errors defaults to 'strict'.
<br> |
<br> |  Methods defined here:
<br> |
<br> |  __add__(self, value, /)
<br> |      Return self+value.
<br> |
<br> |  __contains__(self, key, /)
<br> |      Return key in self.
<br> |
<br> |  __eq__(self, value, /)
<br> |      Return self==value.
<br> |
<br> |  __format__(self, format_spec, /)
<br> |      Return a formatted version of the string as described by format_spec.
<br> |
<br> |  __ge__(self, value, /)
<br> |      Return self>=value.
<br> |
<br> |  __getattribute__(self, name, /)
<br> |      Return getattr(self, name).
<br> |
<br> |  __getitem__(self, key, /)
<br> |      Return self[key].
<br> |
<br> |  __getnewargs__(...)
<br> |
<br> |  __gt__(self, value, /)
<br> |      Return self>value.
<br> |
<br> |  __hash__(self, /)
<br> |      Return hash(self).
<br> |
<br> |  __iter__(self, /)
<br> |      Implement iter(self).
<br> |
<br> |  __le__(self, value, /)
<br> |      Return self<=value.
<br> |
<br> |  __len__(self, /)
<br> |      Return len(self).
<br> |
<br> |  __lt__(self, value, /)
<br> |      Return self<value.
<br> |
<br> |  __mod__(self, value, /)
<br> |      Return self%value.
<br> |
<br> |  __mul__(self, value, /)
<br> |      Return self*value.
<br> |
<br> |  __ne__(self, value, /)
<br> |      Return self!=value.
<br> |
<br> |  __repr__(self, /)
<br> |      Return repr(self).
<br> |
<br> |  __rmod__(self, value, /)
<br> |      Return value%self.
<br> |
<br> |  __rmul__(self, value, /)
<br> |      Return value*self.
<br> |
<br> |  __sizeof__(self, /)
<br> |      Return the size of the string in memory, in bytes.
<br> |
<br> |  __str__(self, /)
<br> |      Return str(self).
<br> |
<br> |  capitalize(self, /)
<br> |      Return a capitalized version of the string.
<br> |
<br> |      More specifically, make the first character have upper case and the rest lower
<br> |      case.
<br> |
<br> |  casefold(self, /)
<br> |      Return a version of the string suitable for caseless comparisons.
<br> |
<br> |  center(self, width, fillchar=' ', /)
<br> |      Return a centered string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  count(...)
<br> |      S.count(sub[, start[, end]]) -> int
<br> |
<br> |      Return the number of non-overlapping occurrences of substring sub in
<br> |      string S[start:end].  Optional arguments start and end are
<br> |      interpreted as in slice notation.
<br> |
<br> |  encode(self, /, encoding='utf-8', errors='strict')
<br> |      Encode the string using the codec registered for encoding.
<br> |
<br> |      encoding
<br> |        The encoding in which to encode the string.
<br> |      errors
<br> |        The error handling scheme to use for encoding errors.
<br> |        The default is 'strict' meaning that encoding errors raise a
<br> |        UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
<br> |        'xmlcharrefreplace' as well as any other name registered with
<br> |        codecs.register_error that can handle UnicodeEncodeErrors.
<br> |
<br> |  endswith(...)
<br> |      S.endswith(suffix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S ends with the specified suffix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      suffix can also be a tuple of strings to try.
<br> |
<br> |  expandtabs(self, /, tabsize=8)
<br> |      Return a copy where all tab characters are expanded using spaces.
<br> |
<br> |      If tabsize is not given, a tab size of 8 characters is assumed.
<br> |
<br> |  find(...)
<br> |      S.find(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  format(...)
<br> |      S.format(*args, **kwargs) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from args and kwargs.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  format_map(...)
<br> |      S.format_map(mapping) -> str
<br> |
<br> |      Return a formatted version of S, using substitutions from mapping.
<br> |      The substitutions are identified by braces ('{' and '}').
<br> |
<br> |  index(...)
<br> |      S.index(sub[, start[, end]]) -> int
<br> |
<br> |      Return the lowest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  isalnum(self, /)
<br> |      Return True if the string is an alpha-numeric string, False otherwise.
<br> |
<br> |      A string is alpha-numeric if all characters in the string are alpha-numeric and
<br> |      there is at least one character in the string.
<br> |
<br> |  isalpha(self, /)
<br> |      Return True if the string is an alphabetic string, False otherwise.
<br> |
<br> |      A string is alphabetic if all characters in the string are alphabetic and there
<br> |      is at least one character in the string.
<br> |
<br> |  isascii(self, /)
<br> |      Return True if all characters in the string are ASCII, False otherwise.
<br> |
<br> |      ASCII characters have code points in the range U+0000-U+007F.
<br> |      Empty string is ASCII too.
<br> |
<br> |  isdecimal(self, /)
<br> |      Return True if the string is a decimal string, False otherwise.
<br> |
<br> |      A string is a decimal string if all characters in the string are decimal and
<br> |      there is at least one character in the string.
<br> |
<br> |  isdigit(self, /)
<br> |      Return True if the string is a digit string, False otherwise.
<br> |
<br> |      A string is a digit string if all characters in the string are digits and there
<br> |      is at least one character in the string.
<br> |
<br> |  isidentifier(self, /)
<br> |      Return True if the string is a valid Python identifier, False otherwise.
<br> |
<br> |      Use keyword.iskeyword() to test for reserved identifiers such as "def" and
<br> |      "class".
<br> |
<br> |  islower(self, /)
<br> |      Return True if the string is a lowercase string, False otherwise.
<br> |
<br> |      A string is lowercase if all cased characters in the string are lowercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  isnumeric(self, /)
<br> |      Return True if the string is a numeric string, False otherwise.
<br> |
<br> |      A string is numeric if all characters in the string are numeric and there is at
<br> |      least one character in the string.
<br> |
<br> |  isprintable(self, /)
<br> |      Return True if the string is printable, False otherwise.
<br> |
<br> |      A string is printable if all of its characters are considered printable in
<br> |      repr() or if it is empty.
<br> |
<br> |  isspace(self, /)
<br> |      Return True if the string is a whitespace string, False otherwise.
<br> |
<br> |      A string is whitespace if all characters in the string are whitespace and there
<br> |      is at least one character in the string.
<br> |
<br> |  istitle(self, /)
<br> |      Return True if the string is a title-cased string, False otherwise.
<br> |
<br> |      In a title-cased string, upper- and title-case characters may only
<br> |      follow uncased characters and lowercase characters only cased ones.
<br> |
<br> |  isupper(self, /)
<br> |      Return True if the string is an uppercase string, False otherwise.
<br> |
<br> |      A string is uppercase if all cased characters in the string are uppercase and
<br> |      there is at least one cased character in the string.
<br> |
<br> |  join(self, iterable, /)
<br> |      Concatenate any number of strings.
<br> |
<br> |      The string whose method is called is inserted in between each given string.
<br> |      The result is returned as a new string.
<br> |
<br> |      Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'
<br> |
<br> |  ljust(self, width, fillchar=' ', /)
<br> |      Return a left-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  lower(self, /)
<br> |      Return a copy of the string converted to lowercase.
<br> |
<br> |  lstrip(self, chars=None, /)
<br> |      Return a copy of the string with leading whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  partition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string.  If the separator is found,
<br> |      returns a 3-tuple containing the part before the separator, the separator
<br> |      itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing the original string
<br> |      and two empty strings.
<br> |
<br> |  replace(self, old, new, count=-1, /)
<br> |      Return a copy with all occurrences of substring old replaced by new.
<br> |
<br> |        count
<br> |          Maximum number of occurrences to replace.
<br> |          -1 (the default value) means replace all occurrences.
<br> |
<br> |      If the optional argument count is given, only the first count occurrences are
<br> |      replaced.
<br> |
<br> |  rfind(...)
<br> |      S.rfind(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Return -1 on failure.
<br> |
<br> |  rindex(...)
<br> |      S.rindex(sub[, start[, end]]) -> int
<br> |
<br> |      Return the highest index in S where substring sub is found,
<br> |      such that sub is contained within S[start:end].  Optional
<br> |      arguments start and end are interpreted as in slice notation.
<br> |
<br> |      Raises ValueError when the substring is not found.
<br> |
<br> |  rjust(self, width, fillchar=' ', /)
<br> |      Return a right-justified string of length width.
<br> |
<br> |      Padding is done using the specified fill character (default is a space).
<br> |
<br> |  rpartition(self, sep, /)
<br> |      Partition the string into three parts using the given separator.
<br> |
<br> |      This will search for the separator in the string, starting at the end. If
<br> |      the separator is found, returns a 3-tuple containing the part before the
<br> |      separator, the separator itself, and the part after it.
<br> |
<br> |      If the separator is not found, returns a 3-tuple containing two empty strings
<br> |      and the original string.
<br> |
<br> |  rsplit(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |        sep
<br> |          The delimiter according which to split the string.
<br> |          None (the default value) means split according to any whitespace,
<br> |          and discard empty strings from the result.
<br> |        maxsplit
<br> |          Maximum number of splits to do.
<br> |          -1 (the default value) means no limit.
<br> |
<br> |      Splits are done starting at the end of the string and working to the front.
<br> |
<br> |  rstrip(self, chars=None, /)
<br> |      Return a copy of the string with trailing whitespace removed.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  split(self, /, sep=None, maxsplit=-1)
<br> |      Return a list of the words in the string, using sep as the delimiter string.
<br> |
<br> |      sep
<br> |        The delimiter according which to split the string.
<br> |        None (the default value) means split according to any whitespace,
<br> |        and discard empty strings from the result.
<br> |      maxsplit
<br> |        Maximum number of splits to do.
<br> |        -1 (the default value) means no limit.
<br> |
<br> |  splitlines(self, /, keepends=False)
<br> |      Return a list of the lines in the string, breaking at line boundaries.
<br> |
<br> |      Line breaks are not included in the resulting list unless keepends is given and
<br> |      true.
<br> |
<br> |  startswith(...)
<br> |      S.startswith(prefix[, start[, end]]) -> bool
<br> |
<br> |      Return True if S starts with the specified prefix, False otherwise.
<br> |      With optional start, test S beginning at that position.
<br> |      With optional end, stop comparing S at that position.
<br> |      prefix can also be a tuple of strings to try.
<br> |
<br> |  strip(self, chars=None, /)
<br> |      Return a copy of the string with leading and trailing whitespace remove.
<br> |
<br> |      If chars is given and not None, remove characters in chars instead.
<br> |
<br> |  swapcase(self, /)
<br> |      Convert uppercase characters to lowercase and lowercase characters to uppercase.
<br> |
<br> |  title(self, /)
<br> |      Return a version of the string where each word is titlecased.
<br> |
<br> |      More specifically, words start with uppercased characters and all remaining
<br> |      cased characters have lower case.
<br> |
<br> |  translate(self, table, /)
<br> |      Replace each character in the string using the given translation table.
<br> |
<br> |        table
<br> |          Translation table, which must be a mapping of Unicode ordinals to
<br> |          Unicode ordinals, strings, or None.
<br> |
<br> |      The table must implement lookup/indexing via __getitem__, for instance a
<br> |      dictionary or list.  If this operation raises LookupError, the character is
<br> |      left untouched.  Characters mapped to None are deleted.
<br> |
<br> |  upper(self, /)
<br> |      Return a copy of the string converted to uppercase.
<br> |
<br> |  zfill(self, width, /)
<br> |      Pad a numeric string with zeros on the left, to fill a field of the given width.
<br> |
<br> |      The string is never truncated.
<br> |
<br> |  <hr>
<br> |  Static methods defined here:
<br> |
<br> |  __new__(*args, **kwargs) from builtins.type
<br> |      Create and return a new object.  See help(type) for accurate signature.
<br> |
<br> |  maketrans(x, y=None, z=None, /)
<br> |      Return a translation table usable for str.translate().
<br> |
<br> |      If there is only one argument, it must be a dictionary mapping Unicode
<br> |      ordinals (integers) or characters to Unicode ordinals, strings or None.
<br> |      Character keys will be then converted to ordinals.
<br> |      If there are two arguments, they must be strings of equal length, and
<br> |      in the resulting dictionary, each character in x will be mapped to the
<br> |      character at the same position in y. If there is a third argument, it
<br> |      must be a string, whose characters will be mapped to None in the result.
<br>
<br>No Python documentation found for '__path__'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on ModuleSpec in module importlib._bootstrap object:
<br>
<br>__spec__ = class ModuleSpec(builtins.object)
<br> |  __spec__(name, loader, *, origin=None, loader_state=None, is_package=None)
<br> |
<br> |  The specification for a module, used for loading.
<br> |
<br> |  A module's spec is the source for information about the module.  For
<br> |  data associated with the module, including source, use the spec's
<br> |  loader.
<br> |
<br> |  `name` is the absolute name of the module.  `loader` is the loader
<br> |  to use when loading the module.  `parent` is the name of the
<br> |  package the module is in.  The parent is derived from the name.
<br> |
<br> |  `is_package` determines if the module is considered a package or
<br> |  not.  On modules this is reflected by the `__path__` attribute.
<br> |
<br> |  `origin` is the specific location used by the loader from which to
<br> |  load the module, if that information is available.  When filename is
<br> |  set, origin will match.
<br> |
<br> |  `has_location` indicates that a spec's "origin" reflects a location.
<br> |  When this is True, `__file__` attribute of the module is set.
<br> |
<br> |  `cached` is the location of the cached bytecode file, if any.  It
<br> |  corresponds to the `__cached__` attribute.
<br> |
<br> |  `submodule_search_locations` is the sequence of path entries to
<br> |  search when importing submodules.  If set, is_package should be
<br> |  True--and False otherwise.
<br> |
<br> |  Packages are simply modules that (may) have submodules.  If a spec
<br> |  has a non-None value in `submodule_search_locations`, the import
<br> |  system will consider modules loaded from the spec as packages.
<br> |
<br> |  Only finders (see importlib.abc.MetaPathFinder and
<br> |  importlib.abc.PathEntryFinder) should modify ModuleSpec instances.
<br> |
<br> |  Methods defined here:
<br> |
<br> |  __eq__(self, other)
<br> |      Return self==value.
<br> |
<br> |  __init__(self, name, loader, *, origin=None, loader_state=None, is_package=None)
<br> |      Initialize self.  See help(type(self)) for accurate signature.
<br> |
<br> |  __repr__(self)
<br> |      Return repr(self).
<br> |
<br> |  <hr>
<br> |  Data descriptors defined here:
<br> |
<br> |  __dict__
<br> |      dictionary for instance variables (if defined)
<br> |
<br> |  __weakref__
<br> |      list of weak references to the object (if defined)
<br> |
<br> |  cached
<br> |
<br> |  has_location
<br> |
<br> |  parent
<br> |      The name of the module's parent.
<br> |
<br> |  <hr>
<br> |  Data and other attributes defined here:
<br> |
<br> |  __hash__ = None
<br>
<br>No Python documentation found for '_code'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '_download'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '_g'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '_ins'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '_m'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for '_t_q_d_m_'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'all_dict'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'bar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'c_list'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'cmd_parser'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on package docs:
<br>
<br>NAME
<br>    docs
<br>
<br>PACKAGE CONTENTS
<br>
<br>
<br>FILE
<br>    (built-in)
<br>
<br>
<br>Help on package download:
<br>
<br>NAME
<br>    download - A tiny module to make downloading with python super easy.
<br>
<br>PACKAGE CONTENTS
<br>    download
<br>    tests (package)
<br>
<br>VERSION
<br>    0.3.3
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\site-packages\download\__init__.py
<br>
<br>
<br>No Python documentation found for 'get_newest_version'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'gpl'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'gui_bar'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'kill'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'make_text'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'more_input'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'msg'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'my_module'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'obj_type'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'object_type'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on module os:
<br>
<br>NAME
<br>    os - OS routines for NT or Posix depending on what system we're on.
<br>
<br>DESCRIPTION
<br>    This exports:
<br>      - all functions from posix or nt, e.g. unlink, stat, etc.
<br>      - os.path is either posixpath or ntpath
<br>      - os.name is either 'posix' or 'nt'
<br>      - os.curdir is a string representing the current directory (always '.')
<br>      - os.pardir is a string representing the parent directory (always '..')
<br>      - os.sep is the (or a most common) pathname separator ('/' or '\\')
<br>      - os.extsep is the extension separator (always '.')
<br>      - os.altsep is the alternate pathname separator (None or '/')
<br>      - os.pathsep is the component separator used in $PATH etc
<br>      - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
<br>      - os.defpath is the default search path for executables
<br>      - os.devnull is the file path of the null device ('/dev/null', etc.)
<br>
<br>    Programs that import and use 'os' stand a better chance of being
<br>    portable between different platforms.  Of course, they must then
<br>    only use functions that are defined by all platforms (e.g., unlink
<br>    and opendir), and leave all pathname manipulation to os.path
<br>    (e.g., split and join).
<br>
<br>CLASSES
<br>    builtins.Exception(builtins.BaseException)
<br>        builtins.OSError
<br>    builtins.object
<br>        nt.DirEntry
<br>    builtins.tuple(builtins.object)
<br>        nt.times_result
<br>        nt.uname_result
<br>        stat_result
<br>        statvfs_result
<br>        terminal_size
<br>
<br>    class DirEntry(builtins.object)
<br>     |  Methods defined here:
<br>     |
<br>     |  __fspath__(self, /)
<br>     |      Returns the path for the entry.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  inode(self, /)
<br>     |      Return inode of the entry; cached per entry.
<br>     |
<br>     |  is_dir(self, /, *, follow_symlinks=True)
<br>     |      Return True if the entry is a directory; cached per entry.
<br>     |
<br>     |  is_file(self, /, *, follow_symlinks=True)
<br>     |      Return True if the entry is a file; cached per entry.
<br>     |
<br>     |  is_symlink(self, /)
<br>     |      Return True if the entry is a symbolic link; cached per entry.
<br>     |
<br>     |  stat(self, /, *, follow_symlinks=True)
<br>     |      Return stat_result object for the entry; cached per entry.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  name
<br>     |      the entry's base filename, relative to scandir() "path" argument
<br>     |
<br>     |  path
<br>     |      the entry's full path name; equivalent to os.path.join(scandir_path, entry.name)
<br>
<br>    error = class OSError(Exception)
<br>     |  Base class for I/O related errors.
<br>     |
<br>     |  Method resolution order:
<br>     |      OSError
<br>     |      Exception
<br>     |      BaseException
<br>     |      object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  characters_written
<br>     |
<br>     |  errno
<br>     |      POSIX exception code
<br>     |
<br>     |  filename
<br>     |      exception filename
<br>     |
<br>     |  filename2
<br>     |      second exception filename
<br>     |
<br>     |  strerror
<br>     |      exception strerror
<br>     |
<br>     |  winerror
<br>     |      Win32 exception code
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class stat_result(builtins.tuple)
<br>     |  stat_result(iterable=(), /)
<br>     |
<br>     |  stat_result: Result from stat, fstat, or lstat.
<br>     |
<br>     |  This object may be accessed either as a tuple of
<br>     |    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
<br>     |  or via the attributes st_mode, st_ino, st_dev, st_nlink, st_uid, and so on.
<br>     |
<br>     |  Posix/windows: If your platform supports st_blksize, st_blocks, st_rdev,
<br>     |  or st_flags, they are available as attributes only.
<br>     |
<br>     |  See os.stat for more information.
<br>     |
<br>     |  Method resolution order:
<br>     |      stat_result
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  st_atime
<br>     |      time of last access
<br>     |
<br>     |  st_atime_ns
<br>     |      time of last access in nanoseconds
<br>     |
<br>     |  st_ctime
<br>     |      time of last change
<br>     |
<br>     |  st_ctime_ns
<br>     |      time of last change in nanoseconds
<br>     |
<br>     |  st_dev
<br>     |      device
<br>     |
<br>     |  st_file_attributes
<br>     |      Windows file attribute bits
<br>     |
<br>     |  st_gid
<br>     |      group ID of owner
<br>     |
<br>     |  st_ino
<br>     |      inode
<br>     |
<br>     |  st_mode
<br>     |      protection bits
<br>     |
<br>     |  st_mtime
<br>     |      time of last modification
<br>     |
<br>     |  st_mtime_ns
<br>     |      time of last modification in nanoseconds
<br>     |
<br>     |  st_nlink
<br>     |      number of hard links
<br>     |
<br>     |  st_size
<br>     |      total size, in bytes
<br>     |
<br>     |  st_uid
<br>     |      user ID of owner
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 17
<br>     |
<br>     |  n_sequence_fields = 10
<br>     |
<br>     |  n_unnamed_fields = 3
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>    class statvfs_result(builtins.tuple)
<br>     |  statvfs_result(iterable=(), /)
<br>     |
<br>     |  statvfs_result: Result from statvfs or fstatvfs.
<br>     |
<br>     |  This object may be accessed either as a tuple of
<br>     |    (bsize, frsize, blocks, bfree, bavail, files, ffree, favail, flag, namemax),
<br>     |  or via the attributes f_bsize, f_frsize, f_blocks, f_bfree, and so on.
<br>     |
<br>     |  See os.statvfs for more information.
<br>     |
<br>     |  Method resolution order:
<br>     |      statvfs_result
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  f_bavail
<br>     |
<br>     |  f_bfree
<br>     |
<br>     |  f_blocks
<br>     |
<br>     |  f_bsize
<br>     |
<br>     |  f_favail
<br>     |
<br>     |  f_ffree
<br>     |
<br>     |  f_files
<br>     |
<br>     |  f_flag
<br>     |
<br>     |  f_frsize
<br>     |
<br>     |  f_fsid
<br>     |
<br>     |  f_namemax
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 11
<br>     |
<br>     |  n_sequence_fields = 10
<br>     |
<br>     |  n_unnamed_fields = 0
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>    class terminal_size(builtins.tuple)
<br>     |  terminal_size(iterable=(), /)
<br>     |
<br>     |  A tuple of (columns, lines) for holding terminal window size
<br>     |
<br>     |  Method resolution order:
<br>     |      terminal_size
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  columns
<br>     |      width of the terminal window in characters
<br>     |
<br>     |  lines
<br>     |      height of the terminal window in characters
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 2
<br>     |
<br>     |  n_sequence_fields = 2
<br>     |
<br>     |  n_unnamed_fields = 0
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>    class times_result(builtins.tuple)
<br>     |  times_result(iterable=(), /)
<br>     |
<br>     |  times_result: Result from os.times().
<br>     |
<br>     |  This object may be accessed either as a tuple of
<br>     |    (user, system, children_user, children_system, elapsed),
<br>     |  or via the attributes user, system, children_user, children_system,
<br>     |  and elapsed.
<br>     |
<br>     |  See os.times for more information.
<br>     |
<br>     |  Method resolution order:
<br>     |      times_result
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  children_system
<br>     |      system time of children
<br>     |
<br>     |  children_user
<br>     |      user time of children
<br>     |
<br>     |  elapsed
<br>     |      elapsed time since an arbitrary point in the past
<br>     |
<br>     |  system
<br>     |      system time
<br>     |
<br>     |  user
<br>     |      user time
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 5
<br>     |
<br>     |  n_sequence_fields = 5
<br>     |
<br>     |  n_unnamed_fields = 0
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>    class uname_result(builtins.tuple)
<br>     |  uname_result(iterable=(), /)
<br>     |
<br>     |  uname_result: Result from os.uname().
<br>     |
<br>     |  This object may be accessed either as a tuple of
<br>     |    (sysname, nodename, release, version, machine),
<br>     |  or via the attributes sysname, nodename, release, version, and machine.
<br>     |
<br>     |  See os.uname for more information.
<br>     |
<br>     |  Method resolution order:
<br>     |      uname_result
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  machine
<br>     |      hardware identifier
<br>     |
<br>     |  nodename
<br>     |      name of machine on network (implementation-defined)
<br>     |
<br>     |  release
<br>     |      operating system release
<br>     |
<br>     |  sysname
<br>     |      operating system name
<br>     |
<br>     |  version
<br>     |      operating system version
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 5
<br>     |
<br>     |  n_sequence_fields = 5
<br>     |
<br>     |  n_unnamed_fields = 0
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>FUNCTIONS
<br>    _exit(status)
<br>        Exit to the system with specified status, without normal exit processing.
<br>
<br>    abort()
<br>        Abort the interpreter immediately.
<br>
<br>        This function 'dumps core' or otherwise fails in the hardest way possible
<br>        on the hosting operating system.  This function never returns.
<br>
<br>    access(path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True)
<br>        Use the real uid/gid to test for access to a path.
<br>
<br>          path
<br>            Path to be tested; can be string or bytes
<br>          mode
<br>            Operating-system mode bitfield.  Can be F_OK to test existence,
<br>            or the inclusive-OR of R_OK, W_OK, and X_OK.
<br>          dir_fd
<br>            If not None, it should be a file descriptor open to a directory,
<br>            and path should be relative; path will then be relative to that
<br>            directory.
<br>          effective_ids
<br>            If True, access will use the effective uid/gid instead of
<br>            the real uid/gid.
<br>          follow_symlinks
<br>            If False, and the last element of the path is a symbolic link,
<br>            access will examine the symbolic link itself instead of the file
<br>            the link points to.
<br>
<br>        dir_fd, effective_ids, and follow_symlinks may not be implemented
<br>          on your platform.  If they are unavailable, using them will raise a
<br>          NotImplementedError.
<br>
<br>        Note that most operations will use the effective uid/gid, therefore this
<br>          routine can be used in a suid/sgid environment to test if the invoking user
<br>          has the specified access to the path.
<br>
<br>    chdir(path)
<br>        Change the current working directory to the specified path.
<br>
<br>        path may always be specified as a string.
<br>        On some platforms, path may also be specified as an open file descriptor.
<br>          If this functionality is unavailable, using it raises an exception.
<br>
<br>    chmod(path, mode, *, dir_fd=None, follow_symlinks=True)
<br>        Change the access permissions of a file.
<br>
<br>          path
<br>            Path to be modified.  May always be specified as a str or bytes.
<br>            On some platforms, path may also be specified as an open file descriptor.
<br>            If this functionality is unavailable, using it raises an exception.
<br>          mode
<br>            Operating-system mode bitfield.
<br>          dir_fd
<br>            If not None, it should be a file descriptor open to a directory,
<br>            and path should be relative; path will then be relative to that
<br>            directory.
<br>          follow_symlinks
<br>            If False, and the last element of the path is a symbolic link,
<br>            chmod will modify the symbolic link itself instead of the file
<br>            the link points to.
<br>
<br>        It is an error to use dir_fd or follow_symlinks when specifying path as
<br>          an open file descriptor.
<br>        dir_fd and follow_symlinks may not be implemented on your platform.
<br>          If they are unavailable, using them will raise a NotImplementedError.
<br>
<br>    close(fd)
<br>        Close a file descriptor.
<br>
<br>    closerange(fd_low, fd_high, /)
<br>        Closes all file descriptors in [fd_low, fd_high), ignoring errors.
<br>
<br>    cpu_count()
<br>        Return the number of CPUs in the system; return None if indeterminable.
<br>
<br>        This number is not equivalent to the number of CPUs the current process can
<br>        use.  The number of usable CPUs can be obtained with
<br>        ``len(os.sched_getaffinity(0))``
<br>
<br>    device_encoding(fd)
<br>        Return a string describing the encoding of a terminal's file descriptor.
<br>
<br>        The file descriptor must be attached to a terminal.
<br>        If the device is not a terminal, return None.
<br>
<br>    dup(fd, /)
<br>        Return a duplicate of a file descriptor.
<br>
<br>    dup2(fd, fd2, inheritable=True)
<br>        Duplicate file descriptor.
<br>
<br>    execl(file, *args)
<br>        execl(file, *args)
<br>
<br>        Execute the executable file with argument list args, replacing the
<br>        current process.
<br>
<br>    execle(file, *args)
<br>        execle(file, *args, env)
<br>
<br>        Execute the executable file with argument list args and
<br>        environment env, replacing the current process.
<br>
<br>    execlp(file, *args)
<br>        execlp(file, *args)
<br>
<br>        Execute the executable file (which is searched for along $PATH)
<br>        with argument list args, replacing the current process.
<br>
<br>    execlpe(file, *args)
<br>        execlpe(file, *args, env)
<br>
<br>        Execute the executable file (which is searched for along $PATH)
<br>        with argument list args and environment env, replacing the current
<br>        process.
<br>
<br>    execv(path, argv, /)
<br>        Execute an executable path with arguments, replacing current process.
<br>
<br>        path
<br>          Path of executable file.
<br>        argv
<br>          Tuple or list of strings.
<br>
<br>    execve(path, argv, env)
<br>        Execute an executable path with arguments, replacing current process.
<br>
<br>        path
<br>          Path of executable file.
<br>        argv
<br>          Tuple or list of strings.
<br>        env
<br>          Dictionary of strings mapping to strings.
<br>
<br>    execvp(file, args)
<br>        execvp(file, args)
<br>
<br>        Execute the executable file (which is searched for along $PATH)
<br>        with argument list args, replacing the current process.
<br>        args may be a list or tuple of strings.
<br>
<br>    execvpe(file, args, env)
<br>        execvpe(file, args, env)
<br>
<br>        Execute the executable file (which is searched for along $PATH)
<br>        with argument list args and environment env , replacing the
<br>        current process.
<br>        args may be a list or tuple of strings.
<br>
<br>    fdopen(fd, *args, **kwargs)
<br>        # Supply os.fdopen()
<br>
<br>    fsdecode(filename)
<br>        Decode filename (an os.PathLike, bytes, or str) from the filesystem
<br>        encoding with 'surrogateescape' error handler, return str unchanged. On
<br>        Windows, use 'strict' error handler if the file system encoding is
<br>        'mbcs' (which is the default encoding).
<br>
<br>    fsencode(filename)
<br>        Encode filename (an os.PathLike, bytes, or str) to the filesystem
<br>        encoding with 'surrogateescape' error handler, return bytes unchanged.
<br>        On Windows, use 'strict' error handler if the file system encoding is
<br>        'mbcs' (which is the default encoding).
<br>
<br>    fspath(path)
<br>        Return the file system path representation of the object.
<br>
<br>        If the object is str or bytes, then allow it to pass through as-is. If the
<br>        object defines __fspath__(), then return the result of that method. All other
<br>        types raise a TypeError.
<br>
<br>    fstat(fd)
<br>        Perform a stat system call on the given file descriptor.
<br>
<br>        Like stat(), but for an open file descriptor.
<br>        Equivalent to os.stat(fd).
<br>
<br>    fsync(fd)
<br>        Force write of fd to disk.
<br>
<br>    ftruncate(fd, length, /)
<br>        Truncate a file, specified by file descriptor, to a specific length.
<br>
<br>    get_exec_path(env=None)
<br>        Returns the sequence of directories that will be searched for the
<br>        named executable (similar to a shell) when launching a process.
<br>
<br>        *env* must be an environment variable dict or None.  If *env* is None,
<br>        os.environ will be used.
<br>
<br>    get_handle_inheritable(handle, /)
<br>        Get the close-on-exe flag of the specified file descriptor.
<br>
<br>    get_inheritable(fd, /)
<br>        Get the close-on-exe flag of the specified file descriptor.
<br>
<br>    get_terminal_size(...)
<br>        Return the size of the terminal window as (columns, lines).
<br>
<br>        The optional argument fd (default standard output) specifies
<br>        which file descriptor should be queried.
<br>
<br>        If the file descriptor is not connected to a terminal, an OSError
<br>        is thrown.
<br>
<br>        This function will only be defined if an implementation is
<br>        available for this system.
<br>
<br>        shutil.get_terminal_size is the high-level function which should
<br>        normally be used, os.get_terminal_size is the low-level implementation.
<br>
<br>    getcwd()
<br>        Return a unicode string representing the current working directory.
<br>
<br>    getcwdb()
<br>        Return a bytes string representing the current working directory.
<br>
<br>    getenv(key, default=None)
<br>        Get an environment variable, return None if it doesn't exist.
<br>        The optional second argument can specify an alternate default.
<br>        key, default and the result are str.
<br>
<br>    getlogin()
<br>        Return the actual login name.
<br>
<br>    getpid()
<br>        Return the current process id.
<br>
<br>    getppid()
<br>        Return the parent's process id.
<br>
<br>        If the parent process has already exited, Windows machines will still
<br>        return its id; others systems will return the id of the 'init' process (1).
<br>
<br>    isatty(fd, /)
<br>        Return True if the fd is connected to a terminal.
<br>
<br>        Return True if the file descriptor is an open file descriptor
<br>        connected to the slave end of a terminal.
<br>
<br>    kill(pid, signal, /)
<br>        Kill a process with a signal.
<br>
<br>    link(src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True)
<br>        Create a hard link to a file.
<br>
<br>        If either src_dir_fd or dst_dir_fd is not None, it should be a file
<br>          descriptor open to a directory, and the respective path string (src or dst)
<br>          should be relative; the path will then be relative to that directory.
<br>        If follow_symlinks is False, and the last element of src is a symbolic
<br>          link, link will create a link to the symbolic link itself instead of the
<br>          file the link points to.
<br>        src_dir_fd, dst_dir_fd, and follow_symlinks may not be implemented on your
<br>          platform.  If they are unavailable, using them will raise a
<br>          NotImplementedError.
<br>
<br>    listdir(path=None)
<br>        Return a list containing the names of the files in the directory.
<br>
<br>        path can be specified as either str or bytes.  If path is bytes,
<br>          the filenames returned will also be bytes; in all other circumstances
<br>          the filenames returned will be str.
<br>        If path is None, uses the path='.'.
<br>        On some platforms, path may also be specified as an open file descriptor;\
<br>          the file descriptor must refer to a directory.
<br>          If this functionality is unavailable, using it raises NotImplementedError.
<br>
<br>        The list is in arbitrary order.  It does not include the special
<br>        entries '.' and '..' even if they are present in the directory.
<br>
<br>    lseek(fd, position, how, /)
<br>        Set the position of a file descriptor.  Return the new position.
<br>
<br>        Return the new cursor position in number of bytes
<br>        relative to the beginning of the file.
<br>
<br>    lstat(path, *, dir_fd=None)
<br>        Perform a stat system call on the given path, without following symbolic links.
<br>
<br>        Like stat(), but do not follow symbolic links.
<br>        Equivalent to stat(path, follow_symlinks=False).
<br>
<br>    makedirs(name, mode=511, exist_ok=False)
<br>        makedirs(name [, mode=0o777][, exist_ok=False])
<br>
<br>        Super-mkdir; create a leaf directory and all intermediate ones.  Works like
<br>        mkdir, except that any intermediate path segment (not just the rightmost)
<br>        will be created if it does not exist. If the target directory already
<br>        exists, raise an OSError if exist_ok is False. Otherwise no exception is
<br>        raised.  This is recursive.
<br>
<br>    mkdir(path, mode=511, *, dir_fd=None)
<br>        Create a directory.
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>        The mode argument is ignored on Windows.
<br>
<br>    open(path, flags, mode=511, *, dir_fd=None)
<br>        Open a file for low level IO.  Returns a file descriptor (integer).
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    pipe()
<br>        Create a pipe.
<br>
<br>        Returns a tuple of two file descriptors:
<br>          (read_fd, write_fd)
<br>
<br>    popen(cmd, mode='r', buffering=-1)
<br>        # Supply os.popen()
<br>
<br>    putenv(name, value, /)
<br>        Change or add an environment variable.
<br>
<br>    read(fd, length, /)
<br>        Read from a file descriptor.  Returns a bytes object.
<br>
<br>    readlink(...)
<br>        readlink(path, *, dir_fd=None) -> path
<br>
<br>        Return a string representing the path to which the symbolic link points.
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    remove(path, *, dir_fd=None)
<br>        Remove a file (same as unlink()).
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    removedirs(name)
<br>        removedirs(name)
<br>
<br>        Super-rmdir; remove a leaf directory and all empty intermediate
<br>        ones.  Works like rmdir except that, if the leaf directory is
<br>        successfully removed, directories corresponding to rightmost path
<br>        segments will be pruned away until either the whole path is
<br>        consumed or an error occurs.  Errors during this latter phase are
<br>        ignored -- they generally mean that a directory was not empty.
<br>
<br>    rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)
<br>        Rename a file or directory.
<br>
<br>        If either src_dir_fd or dst_dir_fd is not None, it should be a file
<br>          descriptor open to a directory, and the respective path string (src or dst)
<br>          should be relative; the path will then be relative to that directory.
<br>        src_dir_fd and dst_dir_fd, may not be implemented on your platform.
<br>          If they are unavailable, using them will raise a NotImplementedError.
<br>
<br>    renames(old, new)
<br>        renames(old, new)
<br>
<br>        Super-rename; create directories as necessary and delete any left
<br>        empty.  Works like rename, except creation of any intermediate
<br>        directories needed to make the new pathname good is attempted
<br>        first.  After the rename, directories corresponding to rightmost
<br>        path segments of the old name will be pruned until either the
<br>        whole path is consumed or a nonempty directory is found.
<br>
<br>        Note: this function can fail with the new directory structure made
<br>        if you lack permissions needed to unlink the leaf directory or
<br>        file.
<br>
<br>    replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None)
<br>        Rename a file or directory, overwriting the destination.
<br>
<br>        If either src_dir_fd or dst_dir_fd is not None, it should be a file
<br>          descriptor open to a directory, and the respective path string (src or dst)
<br>          should be relative; the path will then be relative to that directory.
<br>        src_dir_fd and dst_dir_fd, may not be implemented on your platform.
<br>          If they are unavailable, using them will raise a NotImplementedError."
<br>
<br>    rmdir(path, *, dir_fd=None)
<br>        Remove a directory.
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    scandir(path=None)
<br>        Return an iterator of DirEntry objects for given path.
<br>
<br>        path can be specified as either str, bytes or path-like object.  If path
<br>        is bytes, the names of yielded DirEntry objects will also be bytes; in
<br>        all other circumstances they will be str.
<br>
<br>        If path is None, uses the path='.'.
<br>
<br>    set_handle_inheritable(handle, inheritable, /)
<br>        Set the inheritable flag of the specified handle.
<br>
<br>    set_inheritable(fd, inheritable, /)
<br>        Set the inheritable flag of the specified file descriptor.
<br>
<br>    spawnl(mode, file, *args)
<br>        spawnl(mode, file, *args) -> integer
<br>
<br>        Execute file with arguments from args in a subprocess.
<br>        If mode == P_NOWAIT return the pid of the process.
<br>        If mode == P_WAIT return the process's exit code if it exits normally;
<br>        otherwise return -SIG, where SIG is the signal that killed it.
<br>
<br>    spawnle(mode, file, *args)
<br>        spawnle(mode, file, *args, env) -> integer
<br>
<br>        Execute file with arguments from args in a subprocess with the
<br>        supplied environment.
<br>        If mode == P_NOWAIT return the pid of the process.
<br>        If mode == P_WAIT return the process's exit code if it exits normally;
<br>        otherwise return -SIG, where SIG is the signal that killed it.
<br>
<br>    spawnv(mode, path, argv, /)
<br>        Execute the program specified by path in a new process.
<br>
<br>        mode
<br>          Mode of process creation.
<br>        path
<br>          Path of executable file.
<br>        argv
<br>          Tuple or list of strings.
<br>
<br>    spawnve(mode, path, argv, env, /)
<br>        Execute the program specified by path in a new process.
<br>
<br>        mode
<br>          Mode of process creation.
<br>        path
<br>          Path of executable file.
<br>        argv
<br>          Tuple or list of strings.
<br>        env
<br>          Dictionary of strings mapping to strings.
<br>
<br>    startfile(filepath, operation=None)
<br>        startfile(filepath [, operation])
<br>
<br>        Start a file with its associated application.
<br>
<br>        When "operation" is not specified or "open", this acts like
<br>        double-clicking the file in Explorer, or giving the file name as an
<br>        argument to the DOS "start" command: the file is opened with whatever
<br>        application (if any) its extension is associated.
<br>        When another "operation" is given, it specifies what should be done with
<br>        the file.  A typical operation is "print".
<br>
<br>        startfile returns as soon as the associated application is launched.
<br>        There is no option to wait for the application to close, and no way
<br>        to retrieve the application's exit status.
<br>
<br>        The filepath is relative to the current directory.  If you want to use
<br>        an absolute path, make sure the first character is not a slash ("/");
<br>        the underlying Win32 ShellExecute function doesn't work if it is.
<br>
<br>    stat(path, *, dir_fd=None, follow_symlinks=True)
<br>        Perform a stat system call on the given path.
<br>
<br>          path
<br>            Path to be examined; can be string, bytes, path-like object or
<br>            open-file-descriptor int.
<br>          dir_fd
<br>            If not None, it should be a file descriptor open to a directory,
<br>            and path should be a relative string; path will then be relative to
<br>            that directory.
<br>          follow_symlinks
<br>            If False, and the last element of the path is a symbolic link,
<br>            stat will examine the symbolic link itself instead of the file
<br>            the link points to.
<br>
<br>        dir_fd and follow_symlinks may not be implemented
<br>          on your platform.  If they are unavailable, using them will raise a
<br>          NotImplementedError.
<br>
<br>        It's an error to use dir_fd or follow_symlinks when specifying path as
<br>          an open file descriptor.
<br>
<br>    strerror(code, /)
<br>        Translate an error code to a message string.
<br>
<br>    symlink(src, dst, target_is_directory=False, *, dir_fd=None)
<br>        Create a symbolic link pointing to src named dst.
<br>
<br>        target_is_directory is required on Windows if the target is to be
<br>          interpreted as a directory.  (On Windows, symlink requires
<br>          Windows 6.0 or greater, and raises a NotImplementedError otherwise.)
<br>          target_is_directory is ignored on non-Windows platforms.
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    system(command)
<br>        Execute the command in a subshell.
<br>
<br>    times()
<br>        Return a collection containing process timing information.
<br>
<br>        The object returned behaves like a named tuple with these fields:
<br>          (utime, stime, cutime, cstime, elapsed_time)
<br>        All fields are floating point numbers.
<br>
<br>    truncate(path, length)
<br>        Truncate a file, specified by path, to a specific length.
<br>
<br>        On some platforms, path may also be specified as an open file descriptor.
<br>          If this functionality is unavailable, using it raises an exception.
<br>
<br>    umask(mask, /)
<br>        Set the current numeric umask and return the previous umask.
<br>
<br>    unlink(path, *, dir_fd=None)
<br>        Remove a file (same as remove()).
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        dir_fd may not be implemented on your platform.
<br>          If it is unavailable, using it will raise a NotImplementedError.
<br>
<br>    urandom(size, /)
<br>        Return a bytes object containing random bytes suitable for cryptographic use.
<br>
<br>    utime(path, times=None, *, ns=None, dir_fd=None, follow_symlinks=True)
<br>        Set the access and modified time of path.
<br>
<br>        path may always be specified as a string.
<br>        On some platforms, path may also be specified as an open file descriptor.
<br>          If this functionality is unavailable, using it raises an exception.
<br>
<br>        If times is not None, it must be a tuple (atime, mtime);
<br>            atime and mtime should be expressed as float seconds since the epoch.
<br>        If ns is specified, it must be a tuple (atime_ns, mtime_ns);
<br>            atime_ns and mtime_ns should be expressed as integer nanoseconds
<br>            since the epoch.
<br>        If times is None and ns is unspecified, utime uses the current time.
<br>        Specifying tuples for both times and ns is an error.
<br>
<br>        If dir_fd is not None, it should be a file descriptor open to a directory,
<br>          and path should be relative; path will then be relative to that directory.
<br>        If follow_symlinks is False, and the last element of the path is a symbolic
<br>          link, utime will modify the symbolic link itself instead of the file the
<br>          link points to.
<br>        It is an error to use dir_fd or follow_symlinks when specifying path
<br>          as an open file descriptor.
<br>        dir_fd and follow_symlinks may not be available on your platform.
<br>          If they are unavailable, using them will raise a NotImplementedError.
<br>
<br>    waitpid(pid, options, /)
<br>        Wait for completion of a given process.
<br>
<br>        Returns a tuple of information regarding the process:
<br>            (pid, status << 8)
<br>
<br>        The options argument is ignored on Windows.
<br>
<br>    walk(top, topdown=True, onerror=None, followlinks=False)
<br>        Directory tree generator.
<br>
<br>        For each directory in the directory tree rooted at top (including top
<br>        itself, but excluding '.' and '..'), yields a 3-tuple
<br>
<br>            dirpath, dirnames, filenames
<br>
<br>        dirpath is a string, the path to the directory.  dirnames is a list of
<br>        the names of the subdirectories in dirpath (excluding '.' and '..').
<br>        filenames is a list of the names of the non-directory files in dirpath.
<br>        Note that the names in the lists are just names, with no path components.
<br>        To get a full path (which begins with top) to a file or directory in
<br>        dirpath, do os.path.join(dirpath, name).
<br>
<br>        If optional arg 'topdown' is true or not specified, the triple for a
<br>        directory is generated before the triples for any of its subdirectories
<br>        (directories are generated top down).  If topdown is false, the triple
<br>        for a directory is generated after the triples for all of its
<br>        subdirectories (directories are generated bottom up).
<br>
<br>        When topdown is true, the caller can modify the dirnames list in-place
<br>        (e.g., via del or slice assignment), and walk will only recurse into the
<br>        subdirectories whose names remain in dirnames; this can be used to prune the
<br>        search, or to impose a specific order of visiting.  Modifying dirnames when
<br>        topdown is false is ineffective, since the directories in dirnames have
<br>        already been generated by the time dirnames itself is generated. No matter
<br>        the value of topdown, the list of subdirectories is retrieved before the
<br>        tuples for the directory and its subdirectories are generated.
<br>
<br>        By default errors from the os.scandir() call are ignored.  If
<br>        optional arg 'onerror' is specified, it should be a function; it
<br>        will be called with one argument, an OSError instance.  It can
<br>        report the error to continue with the walk, or raise the exception
<br>        to abort the walk.  Note that the filename is available as the
<br>        filename attribute of the exception object.
<br>
<br>        By default, os.walk does not follow symbolic links to subdirectories on
<br>        systems that support them.  In order to get this functionality, set the
<br>        optional argument 'followlinks' to true.
<br>
<br>        Caution:  if you pass a relative pathname for top, don't change the
<br>        current working directory between resumptions of walk.  walk never
<br>        changes the current directory, and assumes that the client doesn't
<br>        either.
<br>
<br>        Example:
<br>
<br>        import os
<br>        from os.path import join, getsize
<br>        for root, dirs, files in os.walk('python/Lib/email'):
<br>            print(root, "consumes", end="")
<br>            print(sum([getsize(join(root, name)) for name in files]), end="")
<br>            print("bytes in", len(files), "non-directory files")
<br>            if 'CVS' in dirs:
<br>                dirs.remove('CVS')  # don't visit CVS directories
<br>
<br>    write(fd, data, /)
<br>        Write a bytes object to a file descriptor.
<br>
<br>DATA
<br>    F_OK = 0
<br>    O_APPEND = 8
<br>    O_BINARY = 32768
<br>    O_CREAT = 256
<br>    O_EXCL = 1024
<br>    O_NOINHERIT = 128
<br>    O_RANDOM = 16
<br>    O_RDONLY = 0
<br>    O_RDWR = 2
<br>    O_SEQUENTIAL = 32
<br>    O_SHORT_LIVED = 4096
<br>    O_TEMPORARY = 64
<br>    O_TEXT = 16384
<br>    O_TRUNC = 512
<br>    O_WRONLY = 1
<br>    P_DETACH = 4
<br>    P_NOWAIT = 1
<br>    P_NOWAITO = 3
<br>    P_OVERLAY = 2
<br>    P_WAIT = 0
<br>    R_OK = 4
<br>    SEEK_CUR = 1
<br>    SEEK_END = 2
<br>    SEEK_SET = 0
<br>    TMP_MAX = 2147483647
<br>    W_OK = 2
<br>    X_OK = 1
<br>    __all__ = ['altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep', ...
<br>    altsep = '/'
<br>    curdir = '.'
<br>    defpath = r'.;C:\bin'
<br>    devnull = 'nul'
<br>    environ = environ({'ALLUSERSPROFILE': 'C:\\ProgramData', '... 'C:\\Use...
<br>    extsep = '.'
<br>    linesep = '\r\n'
<br>    name = 'nt'
<br>    pardir = '..'
<br>    pathsep = ';'
<br>    sep = r'\'
<br>    supports_bytes_environ = False
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\os.py
<br>
<br>
<br>No Python documentation found for 'os_sys_lib'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'osm'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'path'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'print_all_dirs'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'progres_types'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'progress_bar_loading'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'progress_types'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on package requests:
<br>
<br>NAME
<br>    requests
<br>
<br>DESCRIPTION
<br>    Requests HTTP Library
<br>    ~~~~~~~~~~~~~~~~~~~~~
<br>
<br>    Requests is an HTTP library, written in Python, for human beings. Basic GET
<br>    usage:
<br>
<br>       >>> import requests
<br>       >>> r = requests.get('https://www.python.org')
<br>       >>> r.status_code
<br>       200
<br>       >>> 'Python is a programming language' in r.content
<br>       True
<br>
<br>    ... or POST:
<br>
<br>       >>> payload = dict(key1='value1', key2='value2')
<br>       >>> r = requests.post('https://httpbin.org/post', data=payload)
<br>       >>> print(r.text)
<br>       {
<br>         ...
<br>         "form": {
<br>           "key2": "value2",
<br>           "key1": "value1"
<br>         },
<br>         ...
<br>       }
<br>
<br>    The other HTTP methods are supported - see `requests.api`. Full documentation
<br>    is at <http://python-requests.org>.
<br>
<br>    :copyright: (c) 2017 by Kenneth Reitz.
<br>    :license: Apache 2.0, see LICENSE for more details.
<br>
<br>PACKAGE CONTENTS
<br>    __version__
<br>    _internal_utils
<br>    adapters
<br>    api
<br>    auth
<br>    certs
<br>    compat
<br>    cookies
<br>    exceptions
<br>    help
<br>    hooks
<br>    models
<br>    packages
<br>    sessions
<br>    status_codes
<br>    structures
<br>    utils
<br>
<br>FUNCTIONS
<br>    check_compatibility(urllib3_version, chardet_version)
<br>
<br>DATA
<br>    __author_email__ = 'me@kennethreitz.org'
<br>    __build__ = 139520
<br>    __cake__ = '\u2728 \U0001f370 \u2728'
<br>    __copyright__ = 'Copyright 2018 Kenneth Reitz'
<br>    __description__ = 'Python HTTP for Humans.'
<br>    __license__ = 'Apache 2.0'
<br>    __title__ = 'requests'
<br>    __url__ = 'http://python-requests.org'
<br>    codes = <lookup 'status_codes'>
<br>
<br>VERSION
<br>    2.21.0
<br>
<br>AUTHOR
<br>    Kenneth Reitz
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\roaming\python\python37\site-packages\requests\__init__.py
<br>
<br>
<br>No Python documentation found for 'run_apart'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'run_background'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'run_cmds'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'run_cmds_'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'show_progres'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'stop'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>Help on module subprocess:
<br>
<br>NAME
<br>    subprocess - Subprocesses with accessible I/O streams
<br>
<br>DESCRIPTION
<br>    This module allows you to spawn processes, connect to their
<br>    input/output/error pipes, and obtain their return codes.
<br>
<br>    For a complete description of this module see the Python documentation.
<br>
<br>    Main API
<br>    ========
<br>    run(...): Runs a command, waits for it to complete, then returns a
<br>              CompletedProcess instance.
<br>    Popen(...): A class for flexibly executing a command in a new process
<br>
<br>    Constants
<br>    ---------
<br>    DEVNULL: Special value that indicates that os.devnull should be used
<br>    PIPE:    Special value that indicates a pipe should be created
<br>    STDOUT:  Special value that indicates that stderr should go to stdout
<br>
<br>
<br>    Older API
<br>    =========
<br>    call(...): Runs a command, waits for it to complete, then returns
<br>        the return code.
<br>    check_call(...): Same as call() but raises CalledProcessError()
<br>        if return code is not 0
<br>    check_output(...): Same as check_call() but returns the contents of
<br>        stdout instead of a return code
<br>    getoutput(...): Runs a command in the shell, waits for it to complete,
<br>        then returns the output
<br>    getstatusoutput(...): Runs a command in the shell, waits for it to complete,
<br>        then returns a (exitcode, output) tuple
<br>
<br>CLASSES
<br>    builtins.Exception(builtins.BaseException)
<br>        SubprocessError
<br>            CalledProcessError
<br>            TimeoutExpired
<br>    builtins.object
<br>        CompletedProcess
<br>        Popen
<br>        STARTUPINFO
<br>
<br>    class CalledProcessError(SubprocessError)
<br>     |  CalledProcessError(returncode, cmd, output=None, stderr=None)
<br>     |
<br>     |  Raised when run() is called with check=True and the process
<br>     |  returns a non-zero exit status.
<br>     |
<br>     |  Attributes:
<br>     |    cmd, returncode, stdout, stderr, output
<br>     |
<br>     |  Method resolution order:
<br>     |      CalledProcessError
<br>     |      SubprocessError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, returncode, cmd, output=None, stderr=None)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __str__(self)
<br>     |      Return str(self).
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  stdout
<br>     |      Alias for output attribute, to match stderr
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from SubprocessError:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.Exception:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class CompletedProcess(builtins.object)
<br>     |  CompletedProcess(args, returncode, stdout=None, stderr=None)
<br>     |
<br>     |  A process that has finished running.
<br>     |
<br>     |  This is returned by run().
<br>     |
<br>     |  Attributes:
<br>     |    args: The list or str args passed to run().
<br>     |    returncode: The exit code of the process, negative for signals.
<br>     |    stdout: The standard output (None if not captured).
<br>     |    stderr: The standard error (None if not captured).
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, args, returncode, stdout=None, stderr=None)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  check_returncode(self)
<br>     |      Raise CalledProcessError if the exit code is non-zero.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class Popen(builtins.object)
<br>     |  Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None, text=None)
<br>     |
<br>     |  Execute a child program in a new process.
<br>     |
<br>     |  For a complete description of the arguments see the Python documentation.
<br>     |
<br>     |  Arguments:
<br>     |    args: A string, or a sequence of program arguments.
<br>     |
<br>     |    bufsize: supplied as the buffering argument to the open() function when
<br>     |        creating the stdin/stdout/stderr pipe file objects
<br>     |
<br>     |    executable: A replacement program to execute.
<br>     |
<br>     |    stdin, stdout and stderr: These specify the executed programs' standard
<br>     |        input, standard output and standard error file handles, respectively.
<br>     |
<br>     |    preexec_fn: (POSIX only) An object to be called in the child process
<br>     |        just before the child is executed.
<br>     |
<br>     |    close_fds: Controls closing or inheriting of file descriptors.
<br>     |
<br>     |    shell: If true, the command will be executed through the shell.
<br>     |
<br>     |    cwd: Sets the current directory before the child is executed.
<br>     |
<br>     |    env: Defines the environment variables for the new process.
<br>     |
<br>     |    text: If true, decode stdin, stdout and stderr using the given encoding
<br>     |        (if set) or the system default otherwise.
<br>     |
<br>     |    universal_newlines: Alias of text, provided for backwards compatibility.
<br>     |
<br>     |    startupinfo and creationflags (Windows only)
<br>     |
<br>     |    restore_signals (POSIX only)
<br>     |
<br>     |    start_new_session (POSIX only)
<br>     |
<br>     |    pass_fds (POSIX only)
<br>     |
<br>     |    encoding and errors: Text mode encoding and error handling to use for
<br>     |        file objects stdin, stdout and stderr.
<br>     |
<br>     |  Attributes:
<br>     |      stdin, stdout, stderr, pid, returncode
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __del__(self, _maxsize=9223372036854775807, _warn=<built-in function warn>)
<br>     |
<br>     |  __enter__(self)
<br>     |
<br>     |  __exit__(self, exc_type, value, traceback)
<br>     |
<br>     |  __init__(self, args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None, text=None)
<br>     |      Create new Popen instance.
<br>     |
<br>     |  communicate(self, input=None, timeout=None)
<br>     |      Interact with process: Send data to stdin and close it.
<br>     |      Read data from stdout and stderr, until end-of-file is
<br>     |      reached.  Wait for process to terminate.
<br>     |
<br>     |      The optional "input" argument should be data to be sent to the
<br>     |      child process, or None, if no data should be sent to the child.
<br>     |      communicate() returns a tuple (stdout, stderr).
<br>     |
<br>     |      By default, all communication is in bytes, and therefore any
<br>     |      "input" should be bytes, and the (stdout, stderr) will be bytes.
<br>     |      If in text mode (indicated by self.text_mode), any "input" should
<br>     |      be a string, and (stdout, stderr) will be strings decoded
<br>     |      according to locale encoding, or by "encoding" if set. Text mode
<br>     |      is triggered by setting any of text, encoding, errors or
<br>     |      universal_newlines.
<br>     |
<br>     |  kill = terminate(self)
<br>     |
<br>     |  poll(self)
<br>     |      Check if child process has terminated. Set and return returncode
<br>     |      attribute.
<br>     |
<br>     |  send_signal(self, sig)
<br>     |      Send a signal to the process.
<br>     |
<br>     |  terminate(self)
<br>     |      Terminates the process.
<br>     |
<br>     |  wait(self, timeout=None)
<br>     |      Wait for child process to terminate; returns self.returncode.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  universal_newlines
<br>
<br>    class STARTUPINFO(builtins.object)
<br>     |  STARTUPINFO(*, dwFlags=0, hStdInput=None, hStdOutput=None, hStdError=None, wShowWindow=0, lpAttributeList=None)
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, *, dwFlags=0, hStdInput=None, hStdOutput=None, hStdError=None, wShowWindow=0, lpAttributeList=None)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class SubprocessError(builtins.Exception)
<br>     |  Common base class for all non-exit exceptions.
<br>     |
<br>     |  Method resolution order:
<br>     |      SubprocessError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.Exception:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.Exception:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TimeoutExpired(SubprocessError)
<br>     |  TimeoutExpired(cmd, timeout, output=None, stderr=None)
<br>     |
<br>     |  This exception is raised when the timeout expires while waiting for a
<br>     |  child process.
<br>     |
<br>     |  Attributes:
<br>     |      cmd, output, stdout, stderr, timeout
<br>     |
<br>     |  Method resolution order:
<br>     |      TimeoutExpired
<br>     |      SubprocessError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, cmd, timeout, output=None, stderr=None)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __str__(self)
<br>     |      Return str(self).
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  stdout
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from SubprocessError:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.Exception:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>FUNCTIONS
<br>    call(*popenargs, timeout=None, **kwargs)
<br>        Run command with arguments.  Wait for command to complete or
<br>        timeout, then return the returncode attribute.
<br>
<br>        The arguments are the same as for the Popen constructor.  Example:
<br>
<br>        retcode = call(["ls", "-l"])
<br>
<br>    check_call(*popenargs, **kwargs)
<br>        Run command with arguments.  Wait for command to complete.  If
<br>        the exit code was zero then return, otherwise raise
<br>        CalledProcessError.  The CalledProcessError object will have the
<br>        return code in the returncode attribute.
<br>
<br>        The arguments are the same as for the call function.  Example:
<br>
<br>        check_call(["ls", "-l"])
<br>
<br>    check_output(*popenargs, timeout=None, **kwargs)
<br>        Run command with arguments and return its output.
<br>
<br>        If the exit code was non-zero it raises a CalledProcessError.  The
<br>        CalledProcessError object will have the return code in the returncode
<br>        attribute and output in the output attribute.
<br>
<br>        The arguments are the same as for the Popen constructor.  Example:
<br>
<br>        >>> check_output(["ls", "-l", "/dev/null"])
<br>        b'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'
<br>
<br>        The stdout argument is not allowed as it is used internally.
<br>        To capture standard error in the result, use stderr=STDOUT.
<br>
<br>        >>> check_output(["/bin/sh", "-c",
<br>        ...               "ls -l non_existent_file ; exit 0"],
<br>        ...              stderr=STDOUT)
<br>        b'ls: non_existent_file: No such file or directory\n'
<br>
<br>        There is an additional optional argument, "input", allowing you to
<br>        pass a string to the subprocess's stdin.  If you use this argument
<br>        you may not also use the Popen constructor's "stdin" argument, as
<br>        it too will be used internally.  Example:
<br>
<br>        >>> check_output(["sed", "-e", "s/foo/bar/"],
<br>        ...              input=b"when in the course of fooman events\n")
<br>        b'when in the course of barman events\n'
<br>
<br>        By default, all communication is in bytes, and therefore any "input"
<br>        should be bytes, and the return value wil be bytes.  If in text mode,
<br>        any "input" should be a string, and the return value will be a string
<br>        decoded according to locale encoding, or by "encoding" if set. Text mode
<br>        is triggered by setting any of text, encoding, errors or universal_newlines.
<br>
<br>    getoutput(cmd)
<br>        Return output (stdout or stderr) of executing cmd in a shell.
<br>
<br>        Like getstatusoutput(), except the exit status is ignored and the return
<br>        value is a string containing the command's output.  Example:
<br>
<br>        >>> import subprocess
<br>        >>> subprocess.getoutput('ls /bin/ls')
<br>        '/bin/ls'
<br>
<br>    getstatusoutput(cmd)
<br>        Return (exitcode, output) of executing cmd in a shell.
<br>
<br>        Execute the string 'cmd' in a shell with 'check_output' and
<br>        return a 2-tuple (status, output). The locale encoding is used
<br>        to decode the output and process newlines.
<br>
<br>        A trailing newline is stripped from the output.
<br>        The exit status for the command can be interpreted
<br>        according to the rules for the function 'wait'. Example:
<br>
<br>        >>> import subprocess
<br>        >>> subprocess.getstatusoutput('ls /bin/ls')
<br>        (0, '/bin/ls')
<br>        >>> subprocess.getstatusoutput('cat /bin/junk')
<br>        (1, 'cat: /bin/junk: No such file or directory')
<br>        >>> subprocess.getstatusoutput('/bin/junk')
<br>        (127, 'sh: /bin/junk: not found')
<br>        >>> subprocess.getstatusoutput('/bin/kill $$')
<br>        (-15, '')
<br>
<br>    run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs)
<br>        Run command with arguments and return a CompletedProcess instance.
<br>
<br>        The returned instance will have attributes args, returncode, stdout and
<br>        stderr. By default, stdout and stderr are not captured, and those attributes
<br>        will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them.
<br>
<br>        If check is True and the exit code was non-zero, it raises a
<br>        CalledProcessError. The CalledProcessError object will have the return code
<br>        in the returncode attribute, and output & stderr attributes if those streams
<br>        were captured.
<br>
<br>        If timeout is given, and the process takes too long, a TimeoutExpired
<br>        exception will be raised.
<br>
<br>        There is an optional argument "input", allowing you to
<br>        pass bytes or a string to the subprocess's stdin.  If you use this argument
<br>        you may not also use the Popen constructor's "stdin" argument, as
<br>        it will be used internally.
<br>
<br>        By default, all communication is in bytes, and therefore any "input" should
<br>        be bytes, and the stdout and stderr will be bytes. If in text mode, any
<br>        "input" should be a string, and stdout and stderr will be strings decoded
<br>        according to locale encoding, or by "encoding" if set. Text mode is
<br>        triggered by setting any of text, encoding, errors or universal_newlines.
<br>
<br>        The other arguments are the same as for the Popen constructor.
<br>
<br>DATA
<br>    ABOVE_NORMAL_PRIORITY_CLASS = 32768
<br>    BELOW_NORMAL_PRIORITY_CLASS = 16384
<br>    CREATE_BREAKAWAY_FROM_JOB = 16777216
<br>    CREATE_DEFAULT_ERROR_MODE = 67108864
<br>    CREATE_NEW_CONSOLE = 16
<br>    CREATE_NEW_PROCESS_GROUP = 512
<br>    CREATE_NO_WINDOW = 134217728
<br>    DETACHED_PROCESS = 8
<br>    DEVNULL = -3
<br>    HIGH_PRIORITY_CLASS = 128
<br>    IDLE_PRIORITY_CLASS = 64
<br>    NORMAL_PRIORITY_CLASS = 32
<br>    PIPE = -1
<br>    REALTIME_PRIORITY_CLASS = 256
<br>    STARTF_USESHOWWINDOW = 1
<br>    STARTF_USESTDHANDLES = 256
<br>    STDOUT = -2
<br>    STD_ERROR_HANDLE = 4294967284
<br>    STD_INPUT_HANDLE = 4294967286
<br>    STD_OUTPUT_HANDLE = 4294967285
<br>    SW_HIDE = 0
<br>    __all__ = ['Popen', 'PIPE', 'STDOUT', 'call', 'check_call', 'getstatus...
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\subprocess.py
<br>
<br>
<br>Help on built-in module sys:
<br>
<br>NAME
<br>    sys
<br>
<br>MODULE REFERENCE
<br>    https://docs.python.org/3.7/library/sys
<br>
<br>    The following documentation is automatically generated from the Python
<br>    source files.  It may be incomplete, incorrect or include features that
<br>    are considered implementation detail and may vary between Python
<br>    implementations.  When in doubt, consult the module reference at the
<br>    location listed above.
<br>
<br>DESCRIPTION
<br>    This module provides access to some objects used or maintained by the
<br>    interpreter and to functions that interact strongly with the interpreter.
<br>
<br>    Dynamic objects:
<br>
<br>    argv -- command line arguments; argv[0] is the script pathname if known
<br>    path -- module search path; path[0] is the script directory, else ''
<br>    modules -- dictionary of loaded modules
<br>
<br>    displayhook -- called to show results in an interactive session
<br>    excepthook -- called to handle any uncaught exception other than SystemExit
<br>      To customize printing in an interactive session or to install a custom
<br>      top-level exception handler, assign other functions to replace these.
<br>
<br>    stdin -- standard input file object; used by input()
<br>    stdout -- standard output file object; used by print()
<br>    stderr -- standard error object; used for error messages
<br>      By assigning other file objects (or objects that behave like files)
<br>      to these, it is possible to redirect all of the interpreter's I/O.
<br>
<br>    last_type -- type of last uncaught exception
<br>    last_value -- value of last uncaught exception
<br>    last_traceback -- traceback of last uncaught exception
<br>      These three are only available in an interactive session after a
<br>      traceback has been printed.
<br>
<br>    Static objects:
<br>
<br>    builtin_module_names -- tuple of module names built into this interpreter
<br>    copyright -- copyright notice pertaining to this interpreter
<br>    exec_prefix -- prefix used to find the machine-specific Python library
<br>    executable -- absolute path of the executable binary of the Python interpreter
<br>    float_info -- a struct sequence with information about the float implementation.
<br>    float_repr_style -- string indicating the style of repr() output for floats
<br>    hash_info -- a struct sequence with information about the hash algorithm.
<br>    hexversion -- version information encoded as a single integer
<br>    implementation -- Python implementation information.
<br>    int_info -- a struct sequence with information about the int implementation.
<br>    maxsize -- the largest supported length of containers.
<br>    maxunicode -- the value of the largest Unicode code point
<br>    platform -- platform identifier
<br>    prefix -- prefix used to find the Python library
<br>    thread_info -- a struct sequence with information about the thread implementation.
<br>    version -- the version of this interpreter as a string
<br>    version_info -- version information as a named tuple
<br>    dllhandle -- [Windows only] integer handle of the Python DLL
<br>    winver -- [Windows only] version number of the Python DLL
<br>    _enablelegacywindowsfsencoding -- [Windows only]
<br>    __stdin__ -- the original stdin; don't touch!
<br>    __stdout__ -- the original stdout; don't touch!
<br>    __stderr__ -- the original stderr; don't touch!
<br>    __displayhook__ -- the original displayhook; don't touch!
<br>    __excepthook__ -- the original excepthook; don't touch!
<br>
<br>    Functions:
<br>
<br>    displayhook() -- print an object to the screen, and save it in builtins._
<br>    excepthook() -- print an exception and its traceback to sys.stderr
<br>    exc_info() -- return thread-safe information about the current exception
<br>    exit() -- exit the interpreter by raising SystemExit
<br>    getdlopenflags() -- returns flags to be used for dlopen() calls
<br>    getprofile() -- get the global profiling function
<br>    getrefcount() -- return the reference count for an object (plus one :-)
<br>    getrecursionlimit() -- return the max recursion depth for the interpreter
<br>    getsizeof() -- return the size of an object in bytes
<br>    gettrace() -- get the global debug tracing function
<br>    setcheckinterval() -- control how often the interpreter checks for events
<br>    setdlopenflags() -- set the flags to be used for dlopen() calls
<br>    setprofile() -- set the global profiling function
<br>    setrecursionlimit() -- set the max recursion depth for the interpreter
<br>    settrace() -- set the global debug tracing function
<br>
<br>FUNCTIONS
<br>    __breakpointhook__ = breakpointhook(...)
<br>        breakpointhook(*args, **kws)
<br>
<br>        This hook function is called by built-in breakpoint().
<br>
<br>    __displayhook__ = displayhook(...)
<br>        displayhook(object) -> None
<br>
<br>        Print an object to sys.stdout and also save it in builtins._
<br>
<br>    __excepthook__ = excepthook(...)
<br>        excepthook(exctype, value, traceback) -> None
<br>
<br>        Handle an exception by displaying it with a traceback on sys.stderr.
<br>
<br>    breakpointhook(...)
<br>        breakpointhook(*args, **kws)
<br>
<br>        This hook function is called by built-in breakpoint().
<br>
<br>    call_tracing(...)
<br>        call_tracing(func, args) -> object
<br>
<br>        Call func(*args), while tracing is enabled.  The tracing state is
<br>        saved, and restored afterwards.  This is intended to be called from
<br>        a debugger from a checkpoint, to recursively debug some other code.
<br>
<br>    callstats(...)
<br>        callstats() -> tuple of integers
<br>
<br>        Return a tuple of function call statistics, if CALL_PROFILE was defined
<br>        when Python was built.  Otherwise, return None.
<br>
<br>        When enabled, this function returns detailed, implementation-specific
<br>        details about the number of function calls executed. The return value is
<br>        a 11-tuple where the entries in the tuple are counts of:
<br>        0. all function calls
<br>        1. calls to PyFunction_Type objects
<br>        2. PyFunction calls that do not create an argument tuple
<br>        3. PyFunction calls that do not create an argument tuple
<br>           and bypass PyEval_EvalCodeEx()
<br>        4. PyMethod calls
<br>        5. PyMethod calls on bound methods
<br>        6. PyType calls
<br>        7. PyCFunction calls
<br>        8. generator calls
<br>        9. All other calls
<br>        10. Number of stack pops performed by call_function()
<br>
<br>    exc_info(...)
<br>        exc_info() -> (type, value, traceback)
<br>
<br>        Return information about the most recent exception caught by an except
<br>        clause in the current stack frame or in an older stack frame.
<br>
<br>    excepthook(...)
<br>        excepthook(exctype, value, traceback) -> None
<br>
<br>        Handle an exception by displaying it with a traceback on sys.stderr.
<br>
<br>    exit(...)
<br>        exit([status])
<br>
<br>        Exit the interpreter by raising SystemExit(status).
<br>        If the status is omitted or None, it defaults to zero (i.e., success).
<br>        If the status is an integer, it will be used as the system exit status.
<br>        If it is another kind of object, it will be printed and the system
<br>        exit status will be one (i.e., failure).
<br>
<br>    get_asyncgen_hooks(...)
<br>        get_asyncgen_hooks()
<br>
<br>        Return a namedtuple of installed asynchronous generators hooks (firstiter, finalizer).
<br>
<br>    get_coroutine_origin_tracking_depth()
<br>        Check status of origin tracking for coroutine objects in this thread.
<br>
<br>    get_coroutine_wrapper(...)
<br>        get_coroutine_wrapper()
<br>
<br>        Return the wrapper for coroutine objects set by sys.set_coroutine_wrapper.
<br>
<br>    getallocatedblocks(...)
<br>        getallocatedblocks() -> integer
<br>
<br>        Return the number of memory blocks currently allocated, regardless of their
<br>        size.
<br>
<br>    getcheckinterval(...)
<br>        getcheckinterval() -> current check interval; see setcheckinterval().
<br>
<br>    getdefaultencoding(...)
<br>        getdefaultencoding() -> string
<br>
<br>        Return the current default string encoding used by the Unicode
<br>        implementation.
<br>
<br>    getfilesystemencodeerrors(...)
<br>        getfilesystemencodeerrors() -> string
<br>
<br>        Return the error mode used to convert Unicode filenames in
<br>        operating system filenames.
<br>
<br>    getfilesystemencoding(...)
<br>        getfilesystemencoding() -> string
<br>
<br>        Return the encoding used to convert Unicode filenames in
<br>        operating system filenames.
<br>
<br>    getprofile(...)
<br>        getprofile()
<br>
<br>        Return the profiling function set with sys.setprofile.
<br>        See the profiler chapter in the library manual.
<br>
<br>    getrecursionlimit(...)
<br>        getrecursionlimit()
<br>
<br>        Return the current value of the recursion limit, the maximum depth
<br>        of the Python interpreter stack.  This limit prevents infinite
<br>        recursion from causing an overflow of the C stack and crashing Python.
<br>
<br>    getrefcount(...)
<br>        getrefcount(object) -> integer
<br>
<br>        Return the reference count of object.  The count returned is generally
<br>        one higher than you might expect, because it includes the (temporary)
<br>        reference as an argument to getrefcount().
<br>
<br>    getsizeof(...)
<br>        getsizeof(object, default) -> int
<br>
<br>        Return the size of object in bytes.
<br>
<br>    getswitchinterval(...)
<br>        getswitchinterval() -> current thread switch interval; see setswitchinterval().
<br>
<br>    gettrace(...)
<br>        gettrace()
<br>
<br>        Return the global debug tracing function set with sys.settrace.
<br>        See the debugger chapter in the library manual.
<br>
<br>    getwindowsversion(...)
<br>        getwindowsversion()
<br>
<br>        Return information about the running version of Windows as a named tuple.
<br>        The members are named: major, minor, build, platform, service_pack,
<br>        service_pack_major, service_pack_minor, suite_mask, and product_type. For
<br>        backward compatibility, only the first 5 items are available by indexing.
<br>        All elements are numbers, except service_pack and platform_type which are
<br>        strings, and platform_version which is a 3-tuple. Platform is always 2.
<br>        Product_type may be 1 for a workstation, 2 for a domain controller, 3 for a
<br>        server. Platform_version is a 3-tuple containing a version number that is
<br>        intended for identifying the OS rather than feature detection.
<br>
<br>    intern(...)
<br>        intern(string) -> string
<br>
<br>        ``Intern'' the given string.  This enters the string in the (global)
<br>        table of interned strings whose purpose is to speed up dictionary lookups.
<br>        Return the string itself or the previously interned string object with the
<br>        same value.
<br>
<br>    is_finalizing(...)
<br>        is_finalizing()
<br>        Return True if Python is exiting.
<br>
<br>    set_asyncgen_hooks(...)
<br>        set_asyncgen_hooks(*, firstiter=None, finalizer=None)
<br>
<br>        Set a finalizer for async generators objects.
<br>
<br>    set_coroutine_origin_tracking_depth(depth)
<br>        Enable or disable origin tracking for coroutine objects in this thread.
<br>
<br>        Coroutine objects will track 'depth' frames of traceback information about
<br>        where they came from, available in their cr_origin attribute. Set depth of 0
<br>        to disable.
<br>
<br>    set_coroutine_wrapper(...)
<br>        set_coroutine_wrapper(wrapper)
<br>
<br>        Set a wrapper for coroutine objects.
<br>
<br>    setcheckinterval(...)
<br>        setcheckinterval(n)
<br>
<br>        Tell the Python interpreter to check for asynchronous events every
<br>        n instructions.  This also affects how often thread switches occur.
<br>
<br>    setprofile(...)
<br>        setprofile(function)
<br>
<br>        Set the profiling function.  It will be called on each function call
<br>        and return.  See the profiler chapter in the library manual.
<br>
<br>    setrecursionlimit(...)
<br>        setrecursionlimit(n)
<br>
<br>        Set the maximum depth of the Python interpreter stack to n.  This
<br>        limit prevents infinite recursion from causing an overflow of the C
<br>        stack and crashing Python.  The highest possible limit is platform-
<br>        dependent.
<br>
<br>    setswitchinterval(...)
<br>        setswitchinterval(n)
<br>
<br>        Set the ideal thread switching delay inside the Python interpreter
<br>        The actual frequency of switching threads can be lower if the
<br>        interpreter executes long sequences of uninterruptible code
<br>        (this is implementation-specific and workload-dependent).
<br>
<br>        The parameter must represent the desired switching delay in seconds
<br>        A typical value is 0.005 (5 milliseconds).
<br>
<br>    settrace(...)
<br>        settrace(function)
<br>
<br>        Set the global debug tracing function.  It will be called on each
<br>        function call.  See the debugger chapter in the library manual.
<br>
<br>DATA
<br>    __stderr__ = None
<br>    __stdin__ = None
<br>    __stdout__ = None
<br>    api_version = 1013
<br>    argv = ['C:/mattie/own lib/own lib/os_sys/frameworks/python_frameworks...
<br>    base_exec_prefix = r'C:\Users\matthijs\AppData\Local\Programs\Python\P...
<br>    base_prefix = r'C:\Users\matthijs\AppData\Local\Programs\Python\Python...
<br>    builtin_module_names = ('_abc', '_ast', '_bisect', '_blake2', '_codecs...
<br>    byteorder = 'little'
<br>    copyright = 'Copyright (c) 2001-2018 Python Software Foundati...ematis...
<br>    dllhandle = 140731667709952
<br>    dont_write_bytecode = False
<br>    exec_prefix = r'C:\Users\matthijs\AppData\Local\Programs\Python\Python...
<br>    executable = r'C:\Users\matthijs\AppData\Local\Programs\Python\Python3...
<br>    flags = sys.flags(debug=0, inspect=0, interactive=0, opt...ation=1, is...
<br>    float_info = sys.float_info(max=1.7976931348623157e+308, max_...epsilo...
<br>    float_repr_style = 'short'
<br>    hash_info = sys.hash_info(width=64, modulus=2305843009213693...iphash2...
<br>    hexversion = 50790640
<br>    implementation = namespace(cache_tag='cpython-37', hexversion=507...in...
<br>    int_info = sys.int_info(bits_per_digit=30, sizeof_digit=4)
<br>    last_value = AttributeError("module 'os_sys' has no attribute 'i'")
<br>    maxsize = 9223372036854775807
<br>    maxunicode = 1114111
<br>    meta_path = [<class '_frozen_importlib.BuiltinImporter'>, <class '_fro...
<br>    modules = {'__builtins__': {'ArithmeticError': <class 'ArithmeticError...
<br>    path = ['C:/mattie/own lib/own lib/os_sys/frameworks', r'C:\Users\matt...
<br>    path_hooks = [<class 'zipimport.zipimporter'>, <function FileFinder.pa...
<br>    path_importer_cache = {'C:/mattie/own lib/own lib/os_sys/frameworks': ...
<br>    platform = 'win32'
<br>    prefix = r'C:\Users\matthijs\AppData\Local\Programs\Python\Python37'
<br>    stderr = <idlelib.run.PseudoOutputFile object>
<br>    stdin = <idlelib.run.PseudoInputFile object>
<br>    stdout = <idlelib.run.PseudoOutputFile object>
<br>    thread_info = sys.thread_info(name='nt', lock=None, version=None)
<br>    version = '3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.191...
<br>    version_info = sys.version_info(major=3, minor=7, micro=0, releaseleve...
<br>    warnoptions = []
<br>    winver = '3.7'
<br>
<br>FILE
<br>    (built-in)
<br>
<br>
<br>Help on package test:
<br>
<br>NAME
<br>    test - # Dummy file to make this directory a package.
<br>
<br>PACKAGE CONTENTS
<br>    __main__
<br>    _test_multiprocessing
<br>    ann_module
<br>    ann_module2
<br>    ann_module3
<br>    audiotests
<br>    autotest
<br>    bad_coding
<br>    bad_coding2
<br>    bad_getattr
<br>    bad_getattr2
<br>    bad_getattr3
<br>    badsyntax_3131
<br>    badsyntax_future10
<br>    badsyntax_future3
<br>    badsyntax_future4
<br>    badsyntax_future5
<br>    badsyntax_future6
<br>    badsyntax_future7
<br>    badsyntax_future8
<br>    badsyntax_future9
<br>    badsyntax_pep3120
<br>    bisect
<br>    bytecode_helper
<br>    coding20731
<br>    curses_tests
<br>    dataclass_module_1
<br>    dataclass_module_1_str
<br>    dataclass_module_2
<br>    dataclass_module_2_str
<br>    datetimetester
<br>    dis_module
<br>    doctest_aliases
<br>    double_const
<br>    encoded_modules (package)
<br>    final_a
<br>    final_b
<br>    fork_wait
<br>    future_test1
<br>    future_test2
<br>    gdb_sample
<br>    good_getattr
<br>    imp_dummy
<br>    inspect_fodder
<br>    inspect_fodder2
<br>    leakers (package)
<br>    libregrtest (package)
<br>    list_tests
<br>    lock_tests
<br>    make_ssl_certs
<br>    mapping_tests
<br>    memory_watchdog
<br>    mock_socket
<br>    mod_generics_cache
<br>    mp_fork_bomb
<br>    mp_preload
<br>    multibytecodec_support
<br>    outstanding_bugs
<br>    pickletester
<br>    profilee
<br>    pyclbr_input
<br>    pydoc_mod
<br>    pydocfodder
<br>    pythoninfo
<br>    re_tests
<br>    regrtest
<br>    relimport
<br>    reperf
<br>    sample_doctest
<br>    sample_doctest_no_docstrings
<br>    sample_doctest_no_doctests
<br>    seq_tests
<br>    signalinterproctester
<br>    sortperf
<br>    ssl_servers
<br>    ssltests
<br>    string_tests
<br>    support (package)
<br>    test___all__
<br>    test___future__
<br>    test__locale
<br>    test__opcode
<br>    test__osx_support
<br>    test_abc
<br>    test_abstract_numbers
<br>    test_aifc
<br>    test_argparse
<br>    test_array
<br>    test_asdl_parser
<br>    test_ast
<br>    test_asyncgen
<br>    test_asynchat
<br>    test_asyncio (package)
<br>    test_asyncore
<br>    test_atexit
<br>    test_audioop
<br>    test_augassign
<br>    test_base64
<br>    test_baseexception
<br>    test_bdb
<br>    test_bigaddrspace
<br>    test_bigmem
<br>    test_binascii
<br>    test_binhex
<br>    test_binop
<br>    test_bisect
<br>    test_bool
<br>    test_buffer
<br>    test_bufio
<br>    test_builtin
<br>    test_bytes
<br>    test_bz2
<br>    test_c_locale_coercion
<br>    test_calendar
<br>    test_call
<br>    test_capi
<br>    test_cgi
<br>    test_cgitb
<br>    test_charmapcodec
<br>    test_class
<br>    test_cmath
<br>    test_cmd
<br>    test_cmd_line
<br>    test_cmd_line_script
<br>    test_code
<br>    test_code_module
<br>    test_codeccallbacks
<br>    test_codecencodings_cn
<br>    test_codecencodings_hk
<br>    test_codecencodings_iso2022
<br>    test_codecencodings_jp
<br>    test_codecencodings_kr
<br>    test_codecencodings_tw
<br>    test_codecmaps_cn
<br>    test_codecmaps_hk
<br>    test_codecmaps_jp
<br>    test_codecmaps_kr
<br>    test_codecmaps_tw
<br>    test_codecs
<br>    test_codeop
<br>    test_collections
<br>    test_colorsys
<br>    test_compare
<br>    test_compile
<br>    test_compileall
<br>    test_complex
<br>    test_concurrent_futures
<br>    test_configparser
<br>    test_contains
<br>    test_context
<br>    test_contextlib
<br>    test_contextlib_async
<br>    test_copy
<br>    test_copyreg
<br>    test_coroutines
<br>    test_cprofile
<br>    test_crashers
<br>    test_crypt
<br>    test_csv
<br>    test_ctypes
<br>    test_curses
<br>    test_dataclasses
<br>    test_datetime
<br>    test_dbm
<br>    test_dbm_dumb
<br>    test_dbm_gnu
<br>    test_dbm_ndbm
<br>    test_decimal
<br>    test_decorators
<br>    test_defaultdict
<br>    test_deque
<br>    test_descr
<br>    test_descrtut
<br>    test_devpoll
<br>    test_dict
<br>    test_dict_version
<br>    test_dictcomps
<br>    test_dictviews
<br>    test_difflib
<br>    test_dis
<br>    test_distutils
<br>    test_doctest
<br>    test_doctest2
<br>    test_docxmlrpc
<br>    test_dtrace
<br>    test_dummy_thread
<br>    test_dummy_threading
<br>    test_dynamic
<br>    test_dynamicclassattribute
<br>    test_eintr
<br>    test_email (package)
<br>    test_embed
<br>    test_ensurepip
<br>    test_enum
<br>    test_enumerate
<br>    test_eof
<br>    test_epoll
<br>    test_errno
<br>    test_exception_hierarchy
<br>    test_exception_variations
<br>    test_exceptions
<br>    test_extcall
<br>    test_faulthandler
<br>    test_fcntl
<br>    test_file
<br>    test_file_eintr
<br>    test_filecmp
<br>    test_fileinput
<br>    test_fileio
<br>    test_finalization
<br>    test_float
<br>    test_flufl
<br>    test_fnmatch
<br>    test_fork1
<br>    test_format
<br>    test_fractions
<br>    test_frame
<br>    test_frozen
<br>    test_fstring
<br>    test_ftplib
<br>    test_funcattrs
<br>    test_functools
<br>    test_future
<br>    test_future3
<br>    test_future4
<br>    test_future5
<br>    test_gc
<br>    test_gdb
<br>    test_generator_stop
<br>    test_generators
<br>    test_genericclass
<br>    test_genericpath
<br>    test_genexps
<br>    test_getargs2
<br>    test_getopt
<br>    test_getpass
<br>    test_gettext
<br>    test_glob
<br>    test_global
<br>    test_grammar
<br>    test_grp
<br>    test_gzip
<br>    test_hash
<br>    test_hashlib
<br>    test_heapq
<br>    test_hmac
<br>    test_html
<br>    test_htmlparser
<br>    test_http_cookiejar
<br>    test_http_cookies
<br>    test_httplib
<br>    test_httpservers
<br>    test_idle
<br>    test_imaplib
<br>    test_imghdr
<br>    test_imp
<br>    test_import (package)
<br>    test_importlib (package)
<br>    test_index
<br>    test_inspect
<br>    test_int
<br>    test_int_literal
<br>    test_io
<br>    test_ioctl
<br>    test_ipaddress
<br>    test_isinstance
<br>    test_iter
<br>    test_iterlen
<br>    test_itertools
<br>    test_json (package)
<br>    test_keyword
<br>    test_keywordonlyarg
<br>    test_kqueue
<br>    test_largefile
<br>    test_lib2to3
<br>    test_linecache
<br>    test_list
<br>    test_listcomps
<br>    test_locale
<br>    test_logging
<br>    test_long
<br>    test_longexp
<br>    test_lzma
<br>    test_macpath
<br>    test_mailbox
<br>    test_mailcap
<br>    test_marshal
<br>    test_math
<br>    test_memoryio
<br>    test_memoryview
<br>    test_metaclass
<br>    test_mimetypes
<br>    test_minidom
<br>    test_mmap
<br>    test_module
<br>    test_modulefinder
<br>    test_msilib
<br>    test_multibytecodec
<br>    test_multiprocessing_fork
<br>    test_multiprocessing_forkserver
<br>    test_multiprocessing_main_handling
<br>    test_multiprocessing_spawn
<br>    test_netrc
<br>    test_nis
<br>    test_nntplib
<br>    test_normalization
<br>    test_ntpath
<br>    test_numeric_tower
<br>    test_opcodes
<br>    test_openpty
<br>    test_operator
<br>    test_optparse
<br>    test_ordered_dict
<br>    test_os
<br>    test_ossaudiodev
<br>    test_osx_env
<br>    test_parser
<br>    test_pathlib
<br>    test_pdb
<br>    test_peepholer
<br>    test_pickle
<br>    test_pickletools
<br>    test_pipes
<br>    test_pkg
<br>    test_pkgimport
<br>    test_pkgutil
<br>    test_platform
<br>    test_plistlib
<br>    test_poll
<br>    test_popen
<br>    test_poplib
<br>    test_posix
<br>    test_posixpath
<br>    test_pow
<br>    test_pprint
<br>    test_print
<br>    test_profile
<br>    test_property
<br>    test_pstats
<br>    test_pty
<br>    test_pulldom
<br>    test_pwd
<br>    test_py_compile
<br>    test_pyclbr
<br>    test_pydoc
<br>    test_pyexpat
<br>    test_queue
<br>    test_quopri
<br>    test_raise
<br>    test_random
<br>    test_range
<br>    test_re
<br>    test_readline
<br>    test_regrtest
<br>    test_repl
<br>    test_reprlib
<br>    test_resource
<br>    test_richcmp
<br>    test_rlcompleter
<br>    test_robotparser
<br>    test_runpy
<br>    test_sax
<br>    test_sched
<br>    test_scope
<br>    test_script_helper
<br>    test_secrets
<br>    test_select
<br>    test_selectors
<br>    test_set
<br>    test_setcomps
<br>    test_shelve
<br>    test_shlex
<br>    test_shutil
<br>    test_signal
<br>    test_site
<br>    test_slice
<br>    test_smtpd
<br>    test_smtplib
<br>    test_smtpnet
<br>    test_sndhdr
<br>    test_socket
<br>    test_socketserver
<br>    test_sort
<br>    test_source_encoding
<br>    test_spwd
<br>    test_sqlite
<br>    test_ssl
<br>    test_startfile
<br>    test_stat
<br>    test_statistics
<br>    test_strftime
<br>    test_string
<br>    test_string_literals
<br>    test_stringprep
<br>    test_strptime
<br>    test_strtod
<br>    test_struct
<br>    test_structmembers
<br>    test_structseq
<br>    test_subclassinit
<br>    test_subprocess
<br>    test_sunau
<br>    test_sundry
<br>    test_super
<br>    test_support
<br>    test_symbol
<br>    test_symtable
<br>    test_syntax
<br>    test_sys
<br>    test_sys_setprofile
<br>    test_sys_settrace
<br>    test_sysconfig
<br>    test_syslog
<br>    test_tarfile
<br>    test_tcl
<br>    test_telnetlib
<br>    test_tempfile
<br>    test_textwrap
<br>    test_thread
<br>    test_threaded_import
<br>    test_threadedtempfile
<br>    test_threading
<br>    test_threading_local
<br>    test_threadsignals
<br>    test_time
<br>    test_timeit
<br>    test_timeout
<br>    test_tix
<br>    test_tk
<br>    test_tokenize
<br>    test_tools (package)
<br>    test_trace
<br>    test_traceback
<br>    test_tracemalloc
<br>    test_ttk_guionly
<br>    test_ttk_textonly
<br>    test_tuple
<br>    test_turtle
<br>    test_typechecks
<br>    test_types
<br>    test_typing
<br>    test_ucn
<br>    test_unary
<br>    test_unicode
<br>    test_unicode_file
<br>    test_unicode_file_functions
<br>    test_unicode_identifiers
<br>    test_unicodedata
<br>    test_unittest
<br>    test_univnewlines
<br>    test_unpack
<br>    test_unpack_ex
<br>    test_urllib
<br>    test_urllib2
<br>    test_urllib2_localnet
<br>    test_urllib2net
<br>    test_urllib_response
<br>    test_urllibnet
<br>    test_urlparse
<br>    test_userdict
<br>    test_userlist
<br>    test_userstring
<br>    test_utf8_mode
<br>    test_utf8source
<br>    test_uu
<br>    test_uuid
<br>    test_venv
<br>    test_wait3
<br>    test_wait4
<br>    test_warnings (package)
<br>    test_wave
<br>    test_weakref
<br>    test_weakset
<br>    test_webbrowser
<br>    test_winconsoleio
<br>    test_winreg
<br>    test_winsound
<br>    test_with
<br>    test_wsgiref
<br>    test_xdrlib
<br>    test_xml_dom_minicompat
<br>    test_xml_etree
<br>    test_xml_etree_c
<br>    test_xmlrpc
<br>    test_xmlrpc_net
<br>    test_xxtestfuzz
<br>    test_yield_from
<br>    test_zipapp
<br>    test_zipfile
<br>    test_zipfile64
<br>    test_zipimport
<br>    test_zipimport_support
<br>    test_zlib
<br>    testcodec
<br>    tf_inherit_check
<br>    threaded_import_hangers
<br>    time_hashlib
<br>    tracedmodules (package)
<br>    win_console_handler
<br>    xmltests
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\test\__init__.py
<br>
<br>
<br>Help on module threading:
<br>
<br>NAME
<br>    threading - Thread module emulating a subset of Java's threading model.
<br>
<br>CLASSES
<br>    builtins.Exception(builtins.BaseException)
<br>        builtins.RuntimeError
<br>            BrokenBarrierError
<br>    builtins.object
<br>        _thread._local
<br>        Barrier
<br>        Condition
<br>        Event
<br>        Semaphore
<br>            BoundedSemaphore
<br>        Thread
<br>            Timer
<br>
<br>    class Barrier(builtins.object)
<br>     |  Barrier(parties, action=None, timeout=None)
<br>     |
<br>     |  Implements a Barrier.
<br>     |
<br>     |  Useful for synchronizing a fixed number of threads at known synchronization
<br>     |  points.  Threads block on 'wait()' and are simultaneously once they have all
<br>     |  made that call.
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, parties, action=None, timeout=None)
<br>     |      Create a barrier, initialised to 'parties' threads.
<br>     |
<br>     |      'action' is a callable which, when supplied, will be called by one of
<br>     |      the threads after they have all entered the barrier and just prior to
<br>     |      releasing them all. If a 'timeout' is provided, it is uses as the
<br>     |      default for all subsequent 'wait()' calls.
<br>     |
<br>     |  abort(self)
<br>     |      Place the barrier into a 'broken' state.
<br>     |
<br>     |      Useful in case of error.  Any currently waiting threads and threads
<br>     |      attempting to 'wait()' will have BrokenBarrierError raised.
<br>     |
<br>     |  reset(self)
<br>     |      Reset the barrier to the initial state.
<br>     |
<br>     |      Any threads currently waiting will get the BrokenBarrier exception
<br>     |      raised.
<br>     |
<br>     |  wait(self, timeout=None)
<br>     |      Wait for the barrier.
<br>     |
<br>     |      When the specified number of threads have started waiting, they are all
<br>     |      simultaneously awoken. If an 'action' was provided for the barrier, one
<br>     |      of the threads will have executed that callback prior to returning.
<br>     |      Returns an individual index number from 0 to 'parties-1'.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  broken
<br>     |      Return True if the barrier is in a broken state.
<br>     |
<br>     |  n_waiting
<br>     |      Return the number of threads currently waiting at the barrier.
<br>     |
<br>     |  parties
<br>     |      Return the number of threads required to trip the barrier.
<br>
<br>    class BoundedSemaphore(Semaphore)
<br>     |  BoundedSemaphore(value=1)
<br>     |
<br>     |  Implements a bounded semaphore.
<br>     |
<br>     |  A bounded semaphore checks to make sure its current value doesn't exceed its
<br>     |  initial value. If it does, ValueError is raised. In most situations
<br>     |  semaphores are used to guard resources with limited capacity.
<br>     |
<br>     |  If the semaphore is released too many times it's a sign of a bug. If not
<br>     |  given, value defaults to 1.
<br>     |
<br>     |  Like regular semaphores, bounded semaphores manage a counter representing
<br>     |  the number of release() calls minus the number of acquire() calls, plus an
<br>     |  initial value. The acquire() method blocks if necessary until it can return
<br>     |  without making the counter negative. If not given, value defaults to 1.
<br>     |
<br>     |  Method resolution order:
<br>     |      BoundedSemaphore
<br>     |      Semaphore
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, value=1)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  release(self)
<br>     |      Release a semaphore, incrementing the internal counter by one.
<br>     |
<br>     |      When the counter is zero on entry and another thread is waiting for it
<br>     |      to become larger than zero again, wake up that thread.
<br>     |
<br>     |      If the number of releases exceeds the number of acquires,
<br>     |      raise a ValueError.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from Semaphore:
<br>     |
<br>     |  __enter__ = acquire(self, blocking=True, timeout=None)
<br>     |      Acquire a semaphore, decrementing the internal counter by one.
<br>     |
<br>     |      When invoked without arguments: if the internal counter is larger than
<br>     |      zero on entry, decrement it by one and return immediately. If it is zero
<br>     |      on entry, block, waiting until some other thread has called release() to
<br>     |      make it larger than zero. This is done with proper interlocking so that
<br>     |      if multiple acquire() calls are blocked, release() will wake exactly one
<br>     |      of them up. The implementation may pick one at random, so the order in
<br>     |      which blocked threads are awakened should not be relied on. There is no
<br>     |      return value in this case.
<br>     |
<br>     |      When invoked with blocking set to true, do the same thing as when called
<br>     |      without arguments, and return true.
<br>     |
<br>     |      When invoked with blocking set to false, do not block. If a call without
<br>     |      an argument would block, return false immediately; otherwise, do the
<br>     |      same thing as when called without arguments, and return true.
<br>     |
<br>     |      When invoked with a timeout other than None, it will block for at
<br>     |      most timeout seconds.  If acquire does not complete successfully in
<br>     |      that interval, return false.  Return true otherwise.
<br>     |
<br>     |  __exit__(self, t, v, tb)
<br>     |
<br>     |  acquire(self, blocking=True, timeout=None)
<br>     |      Acquire a semaphore, decrementing the internal counter by one.
<br>     |
<br>     |      When invoked without arguments: if the internal counter is larger than
<br>     |      zero on entry, decrement it by one and return immediately. If it is zero
<br>     |      on entry, block, waiting until some other thread has called release() to
<br>     |      make it larger than zero. This is done with proper interlocking so that
<br>     |      if multiple acquire() calls are blocked, release() will wake exactly one
<br>     |      of them up. The implementation may pick one at random, so the order in
<br>     |      which blocked threads are awakened should not be relied on. There is no
<br>     |      return value in this case.
<br>     |
<br>     |      When invoked with blocking set to true, do the same thing as when called
<br>     |      without arguments, and return true.
<br>     |
<br>     |      When invoked with blocking set to false, do not block. If a call without
<br>     |      an argument would block, return false immediately; otherwise, do the
<br>     |      same thing as when called without arguments, and return true.
<br>     |
<br>     |      When invoked with a timeout other than None, it will block for at
<br>     |      most timeout seconds.  If acquire does not complete successfully in
<br>     |      that interval, return false.  Return true otherwise.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from Semaphore:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class BrokenBarrierError(builtins.RuntimeError)
<br>     |  Unspecified run-time error.
<br>     |
<br>     |  Method resolution order:
<br>     |      BrokenBarrierError
<br>     |      builtins.RuntimeError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.RuntimeError:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.RuntimeError:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class Condition(builtins.object)
<br>     |  Condition(lock=None)
<br>     |
<br>     |  Class that implements a condition variable.
<br>     |
<br>     |  A condition variable allows one or more threads to wait until they are
<br>     |  notified by another thread.
<br>     |
<br>     |  If the lock argument is given and not None, it must be a Lock or RLock
<br>     |  object, and it is used as the underlying lock. Otherwise, a new RLock object
<br>     |  is created and used as the underlying lock.
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __enter__(self)
<br>     |
<br>     |  __exit__(self, *args)
<br>     |
<br>     |  __init__(self, lock=None)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  notify(self, n=1)
<br>     |      Wake up one or more threads waiting on this condition, if any.
<br>     |
<br>     |      If the calling thread has not acquired the lock when this method is
<br>     |      called, a RuntimeError is raised.
<br>     |
<br>     |      This method wakes up at most n of the threads waiting for the condition
<br>     |      variable; it is a no-op if no threads are waiting.
<br>     |
<br>     |  notifyAll = notify_all(self)
<br>     |
<br>     |  notify_all(self)
<br>     |      Wake up all threads waiting on this condition.
<br>     |
<br>     |      If the calling thread has not acquired the lock when this method
<br>     |      is called, a RuntimeError is raised.
<br>     |
<br>     |  wait(self, timeout=None)
<br>     |      Wait until notified or until a timeout occurs.
<br>     |
<br>     |      If the calling thread has not acquired the lock when this method is
<br>     |      called, a RuntimeError is raised.
<br>     |
<br>     |      This method releases the underlying lock, and then blocks until it is
<br>     |      awakened by a notify() or notify_all() call for the same condition
<br>     |      variable in another thread, or until the optional timeout occurs. Once
<br>     |      awakened or timed out, it re-acquires the lock and returns.
<br>     |
<br>     |      When the timeout argument is present and not None, it should be a
<br>     |      floating point number specifying a timeout for the operation in seconds
<br>     |      (or fractions thereof).
<br>     |
<br>     |      When the underlying lock is an RLock, it is not released using its
<br>     |      release() method, since this may not actually unlock the lock when it
<br>     |      was acquired multiple times recursively. Instead, an internal interface
<br>     |      of the RLock class is used, which really unlocks it even when it has
<br>     |      been recursively acquired several times. Another internal interface is
<br>     |      then used to restore the recursion level when the lock is reacquired.
<br>     |
<br>     |  wait_for(self, predicate, timeout=None)
<br>     |      Wait until a condition evaluates to True.
<br>     |
<br>     |      predicate should be a callable which result will be interpreted as a
<br>     |      boolean value.  A timeout may be provided giving the maximum time to
<br>     |      wait.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class Event(builtins.object)
<br>     |  Class implementing event objects.
<br>     |
<br>     |  Events manage a flag that can be set to true with the set() method and reset
<br>     |  to false with the clear() method. The wait() method blocks until the flag is
<br>     |  true.  The flag is initially false.
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  clear(self)
<br>     |      Reset the internal flag to false.
<br>     |
<br>     |      Subsequently, threads calling wait() will block until set() is called to
<br>     |      set the internal flag to true again.
<br>     |
<br>     |  isSet = is_set(self)
<br>     |
<br>     |  is_set(self)
<br>     |      Return true if and only if the internal flag is true.
<br>     |
<br>     |  set(self)
<br>     |      Set the internal flag to true.
<br>     |
<br>     |      All threads waiting for it to become true are awakened. Threads
<br>     |      that call wait() once the flag is true will not block at all.
<br>     |
<br>     |  wait(self, timeout=None)
<br>     |      Block until the internal flag is true.
<br>     |
<br>     |      If the internal flag is true on entry, return immediately. Otherwise,
<br>     |      block until another thread calls set() to set the flag to true, or until
<br>     |      the optional timeout occurs.
<br>     |
<br>     |      When the timeout argument is present and not None, it should be a
<br>     |      floating point number specifying a timeout for the operation in seconds
<br>     |      (or fractions thereof).
<br>     |
<br>     |      This method returns the internal flag on exit, so it will always return
<br>     |      True except if a timeout is given and the operation times out.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class Semaphore(builtins.object)
<br>     |  Semaphore(value=1)
<br>     |
<br>     |  This class implements semaphore objects.
<br>     |
<br>     |  Semaphores manage a counter representing the number of release() calls minus
<br>     |  the number of acquire() calls, plus an initial value. The acquire() method
<br>     |  blocks if necessary until it can return without making the counter
<br>     |  negative. If not given, value defaults to 1.
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __enter__ = acquire(self, blocking=True, timeout=None)
<br>     |
<br>     |  __exit__(self, t, v, tb)
<br>     |
<br>     |  __init__(self, value=1)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  acquire(self, blocking=True, timeout=None)
<br>     |      Acquire a semaphore, decrementing the internal counter by one.
<br>     |
<br>     |      When invoked without arguments: if the internal counter is larger than
<br>     |      zero on entry, decrement it by one and return immediately. If it is zero
<br>     |      on entry, block, waiting until some other thread has called release() to
<br>     |      make it larger than zero. This is done with proper interlocking so that
<br>     |      if multiple acquire() calls are blocked, release() will wake exactly one
<br>     |      of them up. The implementation may pick one at random, so the order in
<br>     |      which blocked threads are awakened should not be relied on. There is no
<br>     |      return value in this case.
<br>     |
<br>     |      When invoked with blocking set to true, do the same thing as when called
<br>     |      without arguments, and return true.
<br>     |
<br>     |      When invoked with blocking set to false, do not block. If a call without
<br>     |      an argument would block, return false immediately; otherwise, do the
<br>     |      same thing as when called without arguments, and return true.
<br>     |
<br>     |      When invoked with a timeout other than None, it will block for at
<br>     |      most timeout seconds.  If acquire does not complete successfully in
<br>     |      that interval, return false.  Return true otherwise.
<br>     |
<br>     |  release(self)
<br>     |      Release a semaphore, incrementing the internal counter by one.
<br>     |
<br>     |      When the counter is zero on entry and another thread is waiting for it
<br>     |      to become larger than zero again, wake up that thread.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class Thread(builtins.object)
<br>     |  Thread(group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None)
<br>     |
<br>     |  A class that represents a thread of control.
<br>     |
<br>     |  This class can be safely subclassed in a limited fashion. There are two ways
<br>     |  to specify the activity: by passing a callable object to the constructor, or
<br>     |  by overriding the run() method in a subclass.
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None)
<br>     |      This constructor should always be called with keyword arguments. Arguments are:
<br>     |
<br>     |      *group* should be None; reserved for future extension when a ThreadGroup
<br>     |      class is implemented.
<br>     |
<br>     |      *target* is the callable object to be invoked by the run()
<br>     |      method. Defaults to None, meaning nothing is called.
<br>     |
<br>     |      *name* is the thread name. By default, a unique name is constructed of
<br>     |      the form "Thread-N" where N is a small decimal number.
<br>     |
<br>     |      *args* is the argument tuple for the target invocation. Defaults to ().
<br>     |
<br>     |      *kwargs* is a dictionary of keyword arguments for the target
<br>     |      invocation. Defaults to {}.
<br>     |
<br>     |      If a subclass overrides the constructor, it must make sure to invoke
<br>     |      the base class constructor (Thread.__init__()) before doing anything
<br>     |      else to the thread.
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  getName(self)
<br>     |
<br>     |  isAlive = is_alive(self)
<br>     |
<br>     |  isDaemon(self)
<br>     |
<br>     |  is_alive(self)
<br>     |      Return whether the thread is alive.
<br>     |
<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()
<br>     |      returns a list of all alive threads.
<br>     |
<br>     |  join(self, timeout=None)
<br>     |      Wait until the thread terminates.
<br>     |
<br>     |      This blocks the calling thread until the thread whose join() method is
<br>     |      called terminates -- either normally or through an unhandled exception
<br>     |      or until the optional timeout occurs.
<br>     |
<br>     |      When the timeout argument is present and not None, it should be a
<br>     |      floating point number specifying a timeout for the operation in seconds
<br>     |      (or fractions thereof). As join() always returns None, you must call
<br>     |      isAlive() after join() to decide whether a timeout happened -- if the
<br>     |      thread is still alive, the join() call timed out.
<br>     |
<br>     |      When the timeout argument is not present or None, the operation will
<br>     |      block until the thread terminates.
<br>     |
<br>     |      A thread can be join()ed many times.
<br>     |
<br>     |      join() raises a RuntimeError if an attempt is made to join the current
<br>     |      thread as that would cause a deadlock. It is also an error to join() a
<br>     |      thread before it has been started and attempts to do so raises the same
<br>     |      exception.
<br>     |
<br>     |  run(self)
<br>     |      Method representing the thread's activity.
<br>     |
<br>     |      You may override this method in a subclass. The standard run() method
<br>     |      invokes the callable object passed to the object's constructor as the
<br>     |      target argument, if any, with sequential and keyword arguments taken
<br>     |      from the args and kwargs arguments, respectively.
<br>     |
<br>     |  setDaemon(self, daemonic)
<br>     |
<br>     |  setName(self, name)
<br>     |
<br>     |  start(self)
<br>     |      Start the thread's activity.
<br>     |
<br>     |      It must be called at most once per thread object. It arranges for the
<br>     |      object's run() method to be invoked in a separate thread of control.
<br>     |
<br>     |      This method will raise a RuntimeError if called more than once on the
<br>     |      same thread object.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  daemon
<br>     |      A boolean value indicating whether this thread is a daemon thread.
<br>     |
<br>     |      This must be set before start() is called, otherwise RuntimeError is
<br>     |      raised. Its initial value is inherited from the creating thread; the
<br>     |      main thread is not a daemon thread and therefore all threads created in
<br>     |      the main thread default to daemon = False.
<br>     |
<br>     |      The entire Python program exits when no alive non-daemon threads are
<br>     |      left.
<br>     |
<br>     |  ident
<br>     |      Thread identifier of this thread or None if it has not been started.
<br>     |
<br>     |      This is a nonzero integer. See the get_ident() function. Thread
<br>     |      identifiers may be recycled when a thread exits and another thread is
<br>     |      created. The identifier is available even after the thread has exited.
<br>     |
<br>     |  name
<br>     |      A string used for identification purposes only.
<br>     |
<br>     |      It has no semantics. Multiple threads may be given the same name. The
<br>     |      initial name is set by the constructor.
<br>
<br>    ThreadError = class RuntimeError(Exception)
<br>     |  Unspecified run-time error.
<br>     |
<br>     |  Method resolution order:
<br>     |      RuntimeError
<br>     |      Exception
<br>     |      BaseException
<br>     |      object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class Timer(Thread)
<br>     |  Timer(interval, function, args=None, kwargs=None)
<br>     |
<br>     |  Call a function after a specified number of seconds:
<br>     |
<br>     |  t = Timer(30.0, f, args=None, kwargs=None)
<br>     |  t.start()
<br>     |  t.cancel()     # stop the timer's action if it's still waiting
<br>     |
<br>     |  Method resolution order:
<br>     |      Timer
<br>     |      Thread
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, interval, function, args=None, kwargs=None)
<br>     |      This constructor should always be called with keyword arguments. Arguments are:
<br>     |
<br>     |      *group* should be None; reserved for future extension when a ThreadGroup
<br>     |      class is implemented.
<br>     |
<br>     |      *target* is the callable object to be invoked by the run()
<br>     |      method. Defaults to None, meaning nothing is called.
<br>     |
<br>     |      *name* is the thread name. By default, a unique name is constructed of
<br>     |      the form "Thread-N" where N is a small decimal number.
<br>     |
<br>     |      *args* is the argument tuple for the target invocation. Defaults to ().
<br>     |
<br>     |      *kwargs* is a dictionary of keyword arguments for the target
<br>     |      invocation. Defaults to {}.
<br>     |
<br>     |      If a subclass overrides the constructor, it must make sure to invoke
<br>     |      the base class constructor (Thread.__init__()) before doing anything
<br>     |      else to the thread.
<br>     |
<br>     |  cancel(self)
<br>     |      Stop the timer if it hasn't finished yet.
<br>     |
<br>     |  run(self)
<br>     |      Method representing the thread's activity.
<br>     |
<br>     |      You may override this method in a subclass. The standard run() method
<br>     |      invokes the callable object passed to the object's constructor as the
<br>     |      target argument, if any, with sequential and keyword arguments taken
<br>     |      from the args and kwargs arguments, respectively.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from Thread:
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  getName(self)
<br>     |
<br>     |  isAlive = is_alive(self)
<br>     |      Return whether the thread is alive.
<br>     |
<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()
<br>     |      returns a list of all alive threads.
<br>     |
<br>     |  isDaemon(self)
<br>     |
<br>     |  is_alive(self)
<br>     |      Return whether the thread is alive.
<br>     |
<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()
<br>     |      returns a list of all alive threads.
<br>     |
<br>     |  join(self, timeout=None)
<br>     |      Wait until the thread terminates.
<br>     |
<br>     |      This blocks the calling thread until the thread whose join() method is
<br>     |      called terminates -- either normally or through an unhandled exception
<br>     |      or until the optional timeout occurs.
<br>     |
<br>     |      When the timeout argument is present and not None, it should be a
<br>     |      floating point number specifying a timeout for the operation in seconds
<br>     |      (or fractions thereof). As join() always returns None, you must call
<br>     |      isAlive() after join() to decide whether a timeout happened -- if the
<br>     |      thread is still alive, the join() call timed out.
<br>     |
<br>     |      When the timeout argument is not present or None, the operation will
<br>     |      block until the thread terminates.
<br>     |
<br>     |      A thread can be join()ed many times.
<br>     |
<br>     |      join() raises a RuntimeError if an attempt is made to join the current
<br>     |      thread as that would cause a deadlock. It is also an error to join() a
<br>     |      thread before it has been started and attempts to do so raises the same
<br>     |      exception.
<br>     |
<br>     |  setDaemon(self, daemonic)
<br>     |
<br>     |  setName(self, name)
<br>     |
<br>     |  start(self)
<br>     |      Start the thread's activity.
<br>     |
<br>     |      It must be called at most once per thread object. It arranges for the
<br>     |      object's run() method to be invoked in a separate thread of control.
<br>     |
<br>     |      This method will raise a RuntimeError if called more than once on the
<br>     |      same thread object.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from Thread:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  daemon
<br>     |      A boolean value indicating whether this thread is a daemon thread.
<br>     |
<br>     |      This must be set before start() is called, otherwise RuntimeError is
<br>     |      raised. Its initial value is inherited from the creating thread; the
<br>     |      main thread is not a daemon thread and therefore all threads created in
<br>     |      the main thread default to daemon = False.
<br>     |
<br>     |      The entire Python program exits when no alive non-daemon threads are
<br>     |      left.
<br>     |
<br>     |  ident
<br>     |      Thread identifier of this thread or None if it has not been started.
<br>     |
<br>     |      This is a nonzero integer. See the get_ident() function. Thread
<br>     |      identifiers may be recycled when a thread exits and another thread is
<br>     |      created. The identifier is available even after the thread has exited.
<br>     |
<br>     |  name
<br>     |      A string used for identification purposes only.
<br>     |
<br>     |      It has no semantics. Multiple threads may be given the same name. The
<br>     |      initial name is set by the constructor.
<br>
<br>    local = class _local(builtins.object)
<br>     |  Thread-local data
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>
<br>FUNCTIONS
<br>    Lock = allocate_lock(...)
<br>        allocate_lock() -> lock object
<br>        (allocate() is an obsolete synonym)
<br>
<br>        Create a new lock object. See help(type(threading.Lock())) for
<br>        information about locks.
<br>
<br>    RLock(*args, **kwargs)
<br>        Factory function that returns a new reentrant lock.
<br>
<br>        A reentrant lock must be released by the thread that acquired it. Once a
<br>        thread has acquired a reentrant lock, the same thread may acquire it again
<br>        without blocking; the thread must release it once for each time it has
<br>        acquired it.
<br>
<br>    active_count()
<br>        Return the number of Thread objects currently alive.
<br>
<br>        The returned count is equal to the length of the list returned by
<br>        enumerate().
<br>
<br>    current_thread()
<br>        Return the current Thread object, corresponding to the caller's thread of control.
<br>
<br>        If the caller's thread of control was not created through the threading
<br>        module, a dummy thread object with limited functionality is returned.
<br>
<br>    enumerate()
<br>        Return a list of all Thread objects currently alive.
<br>
<br>        The list includes daemonic threads, dummy thread objects created by
<br>        current_thread(), and the main thread. It excludes terminated threads and
<br>        threads that have not yet been started.
<br>
<br>    get_ident(...)
<br>        get_ident() -> integer
<br>
<br>        Return a non-zero integer that uniquely identifies the current thread
<br>        amongst other threads that exist simultaneously.
<br>        This may be used to identify per-thread resources.
<br>        Even though on some platforms threads identities may appear to be
<br>        allocated consecutive numbers starting at 1, this behavior should not
<br>        be relied upon, and the number should be seen purely as a magic cookie.
<br>        A thread's identity may be reused for another thread after it exits.
<br>
<br>    main_thread()
<br>        Return the main thread object.
<br>
<br>        In normal conditions, the main thread is the thread from which the
<br>        Python interpreter was started.
<br>
<br>    setprofile(func)
<br>        Set a profile function for all threads started from the threading module.
<br>
<br>        The func will be passed to sys.setprofile() for each thread, before its
<br>        run() method is called.
<br>
<br>    settrace(func)
<br>        Set a trace function for all threads started from the threading module.
<br>
<br>        The func will be passed to sys.settrace() for each thread, before its run()
<br>        method is called.
<br>
<br>    stack_size(...)
<br>        stack_size([size]) -> size
<br>
<br>        Return the thread stack size used when creating new threads.  The
<br>        optional size argument specifies the stack size (in bytes) to be used
<br>        for subsequently created threads, and must be 0 (use platform or
<br>        configured default) or a positive integer value of at least 32,768 (32k).
<br>        If changing the thread stack size is unsupported, a ThreadError
<br>        exception is raised.  If the specified size is invalid, a ValueError
<br>        exception is raised, and the stack size is unmodified.  32k bytes
<br>         currently the minimum supported stack size value to guarantee
<br>        sufficient stack space for the interpreter itself.
<br>
<br>        Note that some platforms may have particular restrictions on values for
<br>        the stack size, such as requiring a minimum stack size larger than 32 KiB or
<br>        requiring allocation in multiples of the system memory page size
<br>        - platform documentation should be referred to for more information
<br>        (4 KiB pages are common; using multiples of 4096 for the stack size is
<br>        the suggested approach in the absence of more specific information).
<br>
<br>DATA
<br>    TIMEOUT_MAX = 4294967.0
<br>    __all__ = ['get_ident', 'active_count', 'Condition', 'current_thread',...
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\threading.py
<br>
<br>
<br>Help on built-in module time:
<br>
<br>NAME
<br>    time - This module provides various functions to manipulate time values.
<br>
<br>DESCRIPTION
<br>    There are two standard representations of time.  One is the number
<br>    of seconds since the Epoch, in UTC (a.k.a. GMT).  It may be an integer
<br>    or a floating point number (to represent fractions of seconds).
<br>    The Epoch is system-defined; on Unix, it is generally January 1st, 1970.
<br>    The actual value can be retrieved by calling gmtime(0).
<br>
<br>    The other representation is a tuple of 9 integers giving local time.
<br>    The tuple items are:
<br>      year (including century, e.g. 1998)
<br>      month (1-12)
<br>      day (1-31)
<br>      hours (0-23)
<br>      minutes (0-59)
<br>      seconds (0-59)
<br>      weekday (0-6, Monday is 0)
<br>      Julian day (day in the year, 1-366)
<br>      DST (Daylight Savings Time) flag (-1, 0 or 1)
<br>    If the DST flag is 0, the time is given in the regular time zone;
<br>    if it is 1, the time is given in the DST time zone;
<br>    if it is -1, mktime() should guess based on the date and time.
<br>
<br>CLASSES
<br>    builtins.tuple(builtins.object)
<br>        struct_time
<br>
<br>    class struct_time(builtins.tuple)
<br>     |  struct_time(iterable=(), /)
<br>     |
<br>     |  The time value as returned by gmtime(), localtime(), and strptime(), and
<br>     |  accepted by asctime(), mktime() and strftime().  May be considered as a
<br>     |  sequence of 9 integers.
<br>     |
<br>     |  Note that several fields' values are not the same as those defined by
<br>     |  the C language standard for struct tm.  For example, the value of the
<br>     |  field tm_year is the actual year, not year - 1900.  See individual
<br>     |  fields' descriptions for details.
<br>     |
<br>     |  Method resolution order:
<br>     |      struct_time
<br>     |      builtins.tuple
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  tm_gmtoff
<br>     |      offset from UTC in seconds
<br>     |
<br>     |  tm_hour
<br>     |      hours, range [0, 23]
<br>     |
<br>     |  tm_isdst
<br>     |      1 if summer time is in effect, 0 if not, and -1 if unknown
<br>     |
<br>     |  tm_mday
<br>     |      day of month, range [1, 31]
<br>     |
<br>     |  tm_min
<br>     |      minutes, range [0, 59]
<br>     |
<br>     |  tm_mon
<br>     |      month of year, range [1, 12]
<br>     |
<br>     |  tm_sec
<br>     |      seconds, range [0, 61])
<br>     |
<br>     |  tm_wday
<br>     |      day of week, range [0, 6], Monday is 0
<br>     |
<br>     |  tm_yday
<br>     |      day of year, range [1, 366]
<br>     |
<br>     |  tm_year
<br>     |      year, for example, 1993
<br>     |
<br>     |  tm_zone
<br>     |      abbreviation of timezone name
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  n_fields = 11
<br>     |
<br>     |  n_sequence_fields = 9
<br>     |
<br>     |  n_unnamed_fields = 0
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.tuple:
<br>     |
<br>     |  __add__(self, value, /)
<br>     |      Return self+value.
<br>     |
<br>     |  __contains__(self, key, /)
<br>     |      Return key in self.
<br>     |
<br>     |  __eq__(self, value, /)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, value, /)
<br>     |      Return self>=value.
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __getitem__(self, key, /)
<br>     |      Return self[key].
<br>     |
<br>     |  __getnewargs__(self, /)
<br>     |
<br>     |  __gt__(self, value, /)
<br>     |      Return self>value.
<br>     |
<br>     |  __hash__(self, /)
<br>     |      Return hash(self).
<br>     |
<br>     |  __iter__(self, /)
<br>     |      Implement iter(self).
<br>     |
<br>     |  __le__(self, value, /)
<br>     |      Return self<=value.
<br>     |
<br>     |  __len__(self, /)
<br>     |      Return len(self).
<br>     |
<br>     |  __lt__(self, value, /)
<br>     |      Return self<value.
<br>     |
<br>     |  __mul__(self, value, /)
<br>     |      Return self*value.
<br>     |
<br>     |  __ne__(self, value, /)
<br>     |      Return self!=value.
<br>     |
<br>     |  __rmul__(self, value, /)
<br>     |      Return value*self.
<br>     |
<br>     |  count(self, value, /)
<br>     |      Return number of occurrences of value.
<br>     |
<br>     |  index(self, value, start=0, stop=9223372036854775807, /)
<br>     |      Return first index of value.
<br>     |
<br>     |      Raises ValueError if the value is not present.
<br>
<br>FUNCTIONS
<br>    asctime(...)
<br>        asctime([tuple]) -> string
<br>
<br>        Convert a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.
<br>        When the time tuple is not present, current time as returned by localtime()
<br>        is used.
<br>
<br>    clock(...)
<br>        clock() -> floating point number
<br>
<br>        Return the CPU time or real time since the start of the process or since
<br>        the first call to clock().  This has as much precision as the system
<br>        records.
<br>
<br>    ctime(...)
<br>        ctime(seconds) -> string
<br>
<br>        Convert a time in seconds since the Epoch to a string in local time.
<br>        This is equivalent to asctime(localtime(seconds)). When the time tuple is
<br>        not present, current time as returned by localtime() is used.
<br>
<br>    get_clock_info(...)
<br>        get_clock_info(name: str) -> dict
<br>
<br>        Get information of the specified clock.
<br>
<br>    gmtime(...)
<br>        gmtime([seconds]) -> (tm_year, tm_mon, tm_mday, tm_hour, tm_min,
<br>                               tm_sec, tm_wday, tm_yday, tm_isdst)
<br>
<br>        Convert seconds since the Epoch to a time tuple expressing UTC (a.k.a.
<br>        GMT).  When 'seconds' is not passed in, convert the current time instead.
<br>
<br>        If the platform supports the tm_gmtoff and tm_zone, they are available as
<br>        attributes only.
<br>
<br>    localtime(...)
<br>        localtime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,
<br>                                  tm_sec,tm_wday,tm_yday,tm_isdst)
<br>
<br>        Convert seconds since the Epoch to a time tuple expressing local time.
<br>        When 'seconds' is not passed in, convert the current time instead.
<br>
<br>    mktime(...)
<br>        mktime(tuple) -> floating point number
<br>
<br>        Convert a time tuple in local time to seconds since the Epoch.
<br>        Note that mktime(gmtime(0)) will not generally return zero for most
<br>        time zones; instead the returned value will either be equal to that
<br>        of the timezone or altzone attributes on the time module.
<br>
<br>    monotonic(...)
<br>        monotonic() -> float
<br>
<br>        Monotonic clock, cannot go backward.
<br>
<br>    monotonic_ns(...)
<br>        monotonic_ns() -> int
<br>
<br>        Monotonic clock, cannot go backward, as nanoseconds.
<br>
<br>    perf_counter(...)
<br>        perf_counter() -> float
<br>
<br>        Performance counter for benchmarking.
<br>
<br>    perf_counter_ns(...)
<br>        perf_counter_ns() -> int
<br>
<br>        Performance counter for benchmarking as nanoseconds.
<br>
<br>    process_time(...)
<br>        process_time() -> float
<br>
<br>        Process time for profiling: sum of the kernel and user-space CPU time.
<br>
<br>    process_time_ns(...)
<br>        process_time() -> int
<br>
<br>        Process time for profiling as nanoseconds:
<br>        sum of the kernel and user-space CPU time.
<br>
<br>    sleep(...)
<br>        sleep(seconds)
<br>
<br>        Delay execution for a given number of seconds.  The argument may be
<br>        a floating point number for subsecond precision.
<br>
<br>    strftime(...)
<br>        strftime(format[, tuple]) -> string
<br>
<br>        Convert a time tuple to a string according to a format specification.
<br>        See the library reference manual for formatting codes. When the time tuple
<br>        is not present, current time as returned by localtime() is used.
<br>
<br>        Commonly used format codes:
<br>
<br>        %Y  Year with century as a decimal number.
<br>        %m  Month as a decimal number [01,12].
<br>        %d  Day of the month as a decimal number [01,31].
<br>        %H  Hour (24-hour clock) as a decimal number [00,23].
<br>        %M  Minute as a decimal number [00,59].
<br>        %S  Second as a decimal number [00,61].
<br>        %z  Time zone offset from UTC.
<br>        %a  Locale's abbreviated weekday name.
<br>        %A  Locale's full weekday name.
<br>        %b  Locale's abbreviated month name.
<br>        %B  Locale's full month name.
<br>        %c  Locale's appropriate date and time representation.
<br>        %I  Hour (12-hour clock) as a decimal number [01,12].
<br>        %p  Locale's equivalent of either AM or PM.
<br>
<br>        Other codes may be available on your platform.  See documentation for
<br>        the C library strftime function.
<br>
<br>    strptime(...)
<br>        strptime(string, format) -> struct_time
<br>
<br>        Parse a string to a time tuple according to a format specification.
<br>        See the library reference manual for formatting codes (same as
<br>        strftime()).
<br>
<br>        Commonly used format codes:
<br>
<br>        %Y  Year with century as a decimal number.
<br>        %m  Month as a decimal number [01,12].
<br>        %d  Day of the month as a decimal number [01,31].
<br>        %H  Hour (24-hour clock) as a decimal number [00,23].
<br>        %M  Minute as a decimal number [00,59].
<br>        %S  Second as a decimal number [00,61].
<br>        %z  Time zone offset from UTC.
<br>        %a  Locale's abbreviated weekday name.
<br>        %A  Locale's full weekday name.
<br>        %b  Locale's abbreviated month name.
<br>        %B  Locale's full month name.
<br>        %c  Locale's appropriate date and time representation.
<br>        %I  Hour (12-hour clock) as a decimal number [01,12].
<br>        %p  Locale's equivalent of either AM or PM.
<br>
<br>        Other codes may be available on your platform.  See documentation for
<br>        the C library strftime function.
<br>
<br>    thread_time(...)
<br>        thread_time() -> float
<br>
<br>        Thread time for profiling: sum of the kernel and user-space CPU time.
<br>
<br>    thread_time_ns(...)
<br>        thread_time() -> int
<br>
<br>        Thread time for profiling as nanoseconds:
<br>        sum of the kernel and user-space CPU time.
<br>
<br>    time(...)
<br>        time() -> floating point number
<br>
<br>        Return the current time in seconds since the Epoch.
<br>        Fractions of a second may be present if the system clock provides them.
<br>
<br>    time_ns(...)
<br>        time_ns() -> int
<br>
<br>        Return the current time in nanoseconds since the Epoch.
<br>
<br>DATA
<br>    altzone = -7200
<br>    daylight = 1
<br>    timezone = -3600
<br>    tzname = ('West-Europa (standaardtijd)', 'West-Europa (zomertijd)')
<br>
<br>FILE
<br>    (built-in)
<br>
<br>
<br>Help on package tqdm:
<br>
<br>NAME
<br>    tqdm
<br>
<br>PACKAGE CONTENTS
<br>    __main__
<br>    _main
<br>    _monitor
<br>    _tqdm
<br>    _tqdm_gui
<br>    _tqdm_notebook
<br>    _tqdm_pandas
<br>    _utils
<br>    _version
<br>    auto (package)
<br>    autonotebook (package)
<br>
<br>CLASSES
<br>    builtins.KeyError(builtins.LookupError)
<br>        tqdm._tqdm.TqdmKeyError
<br>    builtins.RuntimeWarning(builtins.Warning)
<br>        tqdm._monitor.TqdmSynchronisationWarning
<br>    builtins.TypeError(builtins.Exception)
<br>        tqdm._tqdm.TqdmTypeError
<br>    builtins.Warning(builtins.Exception)
<br>        tqdm._tqdm.TqdmWarning
<br>            tqdm._tqdm.TqdmDeprecationWarning(tqdm._tqdm.TqdmWarning, builtins.DeprecationWarning)
<br>            tqdm._tqdm.TqdmExperimentalWarning(tqdm._tqdm.TqdmWarning, builtins.FutureWarning)
<br>            tqdm._tqdm.TqdmMonitorWarning(tqdm._tqdm.TqdmWarning, builtins.RuntimeWarning)
<br>    threading.Thread(builtins.object)
<br>        tqdm._monitor.TMonitor
<br>    tqdm._utils.Comparable(builtins.object)
<br>        tqdm._tqdm.tqdm
<br>            tqdm._tqdm_gui.tqdm_gui
<br>
<br>    class TMonitor(threading.Thread)
<br>     |  TMonitor(tqdm_cls, sleep_interval)
<br>     |
<br>     |  Monitoring thread for tqdm bars.
<br>     |  Monitors if tqdm bars are taking too much time to display
<br>     |  and readjusts miniters automatically if necessary.
<br>     |
<br>     |  Parameters
<br>     |  ----------
<br>     |  tqdm_cls  : class
<br>     |      tqdm class to use (can be core tqdm or a submodule).
<br>     |  sleep_interval  : fload
<br>     |      Time to sleep between monitoring checks.
<br>     |
<br>     |  Method resolution order:
<br>     |      TMonitor
<br>     |      threading.Thread
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, tqdm_cls, sleep_interval)
<br>     |      This constructor should always be called with keyword arguments. Arguments are:
<br>     |
<br>     |      *group* should be None; reserved for future extension when a ThreadGroup
<br>     |      class is implemented.
<br>     |
<br>     |      *target* is the callable object to be invoked by the run()
<br>     |      method. Defaults to None, meaning nothing is called.
<br>     |
<br>     |      *name* is the thread name. By default, a unique name is constructed of
<br>     |      the form "Thread-N" where N is a small decimal number.
<br>     |
<br>     |      *args* is the argument tuple for the target invocation. Defaults to ().
<br>     |
<br>     |      *kwargs* is a dictionary of keyword arguments for the target
<br>     |      invocation. Defaults to {}.
<br>     |
<br>     |      If a subclass overrides the constructor, it must make sure to invoke
<br>     |      the base class constructor (Thread.__init__()) before doing anything
<br>     |      else to the thread.
<br>     |
<br>     |  exit(self)
<br>     |
<br>     |  get_instances(self)
<br>     |
<br>     |  report(self)
<br>     |
<br>     |  run(self)
<br>     |      Method representing the thread's activity.
<br>     |
<br>     |      You may override this method in a subclass. The standard run() method
<br>     |      invokes the callable object passed to the object's constructor as the
<br>     |      target argument, if any, with sequential and keyword arguments taken
<br>     |      from the args and kwargs arguments, respectively.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from threading.Thread:
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  getName(self)
<br>     |
<br>     |  isAlive = is_alive(self)
<br>     |      Return whether the thread is alive.
<br>     |
<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()
<br>     |      returns a list of all alive threads.
<br>     |
<br>     |  isDaemon(self)
<br>     |
<br>     |  is_alive(self)
<br>     |      Return whether the thread is alive.
<br>     |
<br>     |      This method returns True just before the run() method starts until just
<br>     |      after the run() method terminates. The module function enumerate()
<br>     |      returns a list of all alive threads.
<br>     |
<br>     |  join(self, timeout=None)
<br>     |      Wait until the thread terminates.
<br>     |
<br>     |      This blocks the calling thread until the thread whose join() method is
<br>     |      called terminates -- either normally or through an unhandled exception
<br>     |      or until the optional timeout occurs.
<br>     |
<br>     |      When the timeout argument is present and not None, it should be a
<br>     |      floating point number specifying a timeout for the operation in seconds
<br>     |      (or fractions thereof). As join() always returns None, you must call
<br>     |      isAlive() after join() to decide whether a timeout happened -- if the
<br>     |      thread is still alive, the join() call timed out.
<br>     |
<br>     |      When the timeout argument is not present or None, the operation will
<br>     |      block until the thread terminates.
<br>     |
<br>     |      A thread can be join()ed many times.
<br>     |
<br>     |      join() raises a RuntimeError if an attempt is made to join the current
<br>     |      thread as that would cause a deadlock. It is also an error to join() a
<br>     |      thread before it has been started and attempts to do so raises the same
<br>     |      exception.
<br>     |
<br>     |  setDaemon(self, daemonic)
<br>     |
<br>     |  setName(self, name)
<br>     |
<br>     |  start(self)
<br>     |      Start the thread's activity.
<br>     |
<br>     |      It must be called at most once per thread object. It arranges for the
<br>     |      object's run() method to be invoked in a separate thread of control.
<br>     |
<br>     |      This method will raise a RuntimeError if called more than once on the
<br>     |      same thread object.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from threading.Thread:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  daemon
<br>     |      A boolean value indicating whether this thread is a daemon thread.
<br>     |
<br>     |      This must be set before start() is called, otherwise RuntimeError is
<br>     |      raised. Its initial value is inherited from the creating thread; the
<br>     |      main thread is not a daemon thread and therefore all threads created in
<br>     |      the main thread default to daemon = False.
<br>     |
<br>     |      The entire Python program exits when no alive non-daemon threads are
<br>     |      left.
<br>     |
<br>     |  ident
<br>     |      Thread identifier of this thread or None if it has not been started.
<br>     |
<br>     |      This is a nonzero integer. See the get_ident() function. Thread
<br>     |      identifiers may be recycled when a thread exits and another thread is
<br>     |      created. The identifier is available even after the thread has exited.
<br>     |
<br>     |  name
<br>     |      A string used for identification purposes only.
<br>     |
<br>     |      It has no semantics. Multiple threads may be given the same name. The
<br>     |      initial name is set by the constructor.
<br>
<br>    class TqdmDeprecationWarning(TqdmWarning, builtins.DeprecationWarning)
<br>     |  TqdmDeprecationWarning(msg, fp_write=None, *a, **k)
<br>     |
<br>     |  base class for all tqdm warnings.
<br>     |
<br>     |  Used for non-external-code-breaking errors, such as garbled printing.
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmDeprecationWarning
<br>     |      TqdmWarning
<br>     |      builtins.DeprecationWarning
<br>     |      builtins.Warning
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods inherited from TqdmWarning:
<br>     |
<br>     |  __init__(self, msg, fp_write=None, *a, **k)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from TqdmWarning:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.DeprecationWarning:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmExperimentalWarning(TqdmWarning, builtins.FutureWarning)
<br>     |  TqdmExperimentalWarning(msg, fp_write=None, *a, **k)
<br>     |
<br>     |  beta feature, unstable API and behaviour
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmExperimentalWarning
<br>     |      TqdmWarning
<br>     |      builtins.FutureWarning
<br>     |      builtins.Warning
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods inherited from TqdmWarning:
<br>     |
<br>     |  __init__(self, msg, fp_write=None, *a, **k)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from TqdmWarning:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.FutureWarning:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmKeyError(builtins.KeyError)
<br>     |  Mapping key not found.
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmKeyError
<br>     |      builtins.KeyError
<br>     |      builtins.LookupError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.KeyError:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.LookupError:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmMonitorWarning(TqdmWarning, builtins.RuntimeWarning)
<br>     |  TqdmMonitorWarning(msg, fp_write=None, *a, **k)
<br>     |
<br>     |  tqdm monitor errors which do not affect external functionality
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmMonitorWarning
<br>     |      TqdmWarning
<br>     |      builtins.RuntimeWarning
<br>     |      builtins.Warning
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods inherited from TqdmWarning:
<br>     |
<br>     |  __init__(self, msg, fp_write=None, *a, **k)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from TqdmWarning:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.RuntimeWarning:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmSynchronisationWarning(builtins.RuntimeWarning)
<br>     |  tqdm multi-thread/-process errors which may cause incorrect nesting
<br>     |  but otherwise no adverse effects
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmSynchronisationWarning
<br>     |      builtins.RuntimeWarning
<br>     |      builtins.Warning
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.RuntimeWarning:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.RuntimeWarning:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmTypeError(builtins.TypeError)
<br>     |  Inappropriate argument type.
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmTypeError
<br>     |      builtins.TypeError
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.TypeError:
<br>     |
<br>     |  __init__(self, /, *args, **kwargs)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.TypeError:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class TqdmWarning(builtins.Warning)
<br>     |  TqdmWarning(msg, fp_write=None, *a, **k)
<br>     |
<br>     |  base class for all tqdm warnings.
<br>     |
<br>     |  Used for non-external-code-breaking errors, such as garbled printing.
<br>     |
<br>     |  Method resolution order:
<br>     |      TqdmWarning
<br>     |      builtins.Warning
<br>     |      builtins.Exception
<br>     |      builtins.BaseException
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, msg, fp_write=None, *a, **k)
<br>     |      Initialize self.  See help(type(self)) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from builtins.Warning:
<br>     |
<br>     |  __new__(*args, **kwargs) from builtins.type
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from builtins.BaseException:
<br>     |
<br>     |  __delattr__(self, name, /)
<br>     |      Implement delattr(self, name).
<br>     |
<br>     |  __getattribute__(self, name, /)
<br>     |      Return getattr(self, name).
<br>     |
<br>     |  __reduce__(...)
<br>     |      Helper for pickle.
<br>     |
<br>     |  __repr__(self, /)
<br>     |      Return repr(self).
<br>     |
<br>     |  __setattr__(self, name, value, /)
<br>     |      Implement setattr(self, name, value).
<br>     |
<br>     |  __setstate__(...)
<br>     |
<br>     |  __str__(self, /)
<br>     |      Return str(self).
<br>     |
<br>     |  with_traceback(...)
<br>     |      Exception.with_traceback(tb) --
<br>     |      set self.__traceback__ to tb and return self.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from builtins.BaseException:
<br>     |
<br>     |  __cause__
<br>     |      exception cause
<br>     |
<br>     |  __context__
<br>     |      exception context
<br>     |
<br>     |  __dict__
<br>     |
<br>     |  __suppress_context__
<br>     |
<br>     |  __traceback__
<br>     |
<br>     |  args
<br>
<br>    class tqdm(tqdm._utils.Comparable)
<br>     |  tqdm(*args, **kwargs)
<br>     |
<br>     |  Decorate an iterable object, returning an iterator which acts exactly
<br>     |  like the original iterable, but prints a dynamically updating
<br>     |  progressbar every time a value is requested.
<br>     |
<br>     |  Method resolution order:
<br>     |      tqdm
<br>     |      tqdm._utils.Comparable
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __del__(self)
<br>     |
<br>     |  __enter__(self)
<br>     |
<br>     |  __exit__(self, *exc)
<br>     |
<br>     |  __hash__(self)
<br>     |      Return hash(self).
<br>     |
<br>     |  __init__(self, iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1, maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False, dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None, unit_divisor=1000, gui=False, **kwargs)
<br>     |      Parameters
<br>     |      ----------
<br>     |      iterable  : iterable, optional
<br>     |          Iterable to decorate with a progressbar.
<br>     |          Leave blank to manually manage the updates.
<br>     |      desc  : str, optional
<br>     |          Prefix for the progressbar.
<br>     |      total  : int, optional
<br>     |          The number of expected iterations. If unspecified,
<br>     |          len(iterable) is used if possible. If float("inf") or as a last
<br>     |          resort, only basic progress statistics are displayed
<br>     |          (no ETA, no progressbar).
<br>     |          If `gui` is True and this parameter needs subsequent updating,
<br>     |          specify an initial arbitrary large positive integer,
<br>     |          e.g. int(9e9).
<br>     |      leave  : bool, optional
<br>     |          If [default: True], keeps all traces of the progressbar
<br>     |          upon termination of iteration.
<br>     |      file  : `io.TextIOWrapper` or `io.StringIO`, optional
<br>     |          Specifies where to output the progress messages
<br>     |          (default: sys.stderr). Uses `file.write(str)` and `file.flush()`
<br>     |          methods.
<br>     |      ncols  : int, optional
<br>     |          The width of the entire output message. If specified,
<br>     |          dynamically resizes the progressbar to stay within this bound.
<br>     |          If unspecified, attempts to use environment width. The
<br>     |          fallback is a meter width of 10 and no limit for the counter and
<br>     |          statistics. If 0, will not print any meter (only stats).
<br>     |      mininterval  : float, optional
<br>     |          Minimum progress display update interval [default: 0.1] seconds.
<br>     |      maxinterval  : float, optional
<br>     |          Maximum progress display update interval [default: 10] seconds.
<br>     |          Automatically adjusts `miniters` to correspond to `mininterval`
<br>     |          after long display update lag. Only works if `dynamic_miniters`
<br>     |          or monitor thread is enabled.
<br>     |      miniters  : int, optional
<br>     |          Minimum progress display update interval, in iterations.
<br>     |          If 0 and `dynamic_miniters`, will automatically adjust to equal
<br>     |          `mininterval` (more CPU efficient, good for tight loops).
<br>     |          If > 0, will skip display of specified number of iterations.
<br>     |          Tweak this and `mininterval` to get very efficient loops.
<br>     |          If your progress is erratic with both fast and slow iterations
<br>     |          (network, skipping items, etc) you should set miniters=1.
<br>     |      ascii  : bool, optional
<br>     |          If unspecified or False, use unicode (smooth blocks) to fill
<br>     |          the meter. The fallback is to use ASCII characters `1-9 #`.
<br>     |      disable  : bool, optional
<br>     |          Whether to disable the entire progressbar wrapper
<br>     |          [default: False]. If set to None, disable on non-TTY.
<br>     |      unit  : str, optional
<br>     |          String that will be used to define the unit of each iteration
<br>     |          [default: it].
<br>     |      unit_scale  : bool or int or float, optional
<br>     |          If 1 or True, the number of iterations will be reduced/scaled
<br>     |          automatically and a metric prefix following the
<br>     |          International System of Units standard will be added
<br>     |          (kilo, mega, etc.) [default: False]. If any other non-zero
<br>     |          number, will scale `total` and `n`.
<br>     |      dynamic_ncols  : bool, optional
<br>     |          If set, constantly alters `ncols` to the environment (allowing
<br>     |          for window resizes) [default: False].
<br>     |      smoothing  : float, optional
<br>     |          Exponential moving average smoothing factor for speed estimates
<br>     |          (ignored in GUI mode). Ranges from 0 (average speed) to 1
<br>     |          (current/instantaneous speed) [default: 0.3].
<br>     |      bar_format  : str, optional
<br>     |          Specify a custom bar string formatting. May impact performance.
<br>     |          [default: '{l_bar}{bar}{r_bar}'], where
<br>     |          l_bar='{desc}: {percentage:3.0f}%|' and
<br>     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
<br>     |            '{rate_fmt}{postfix}]'
<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
<br>     |          Note that a trailing ": " is automatically removed after {desc}
<br>     |          if the latter is empty.
<br>     |      initial  : int, optional
<br>     |          The initial counter value. Useful when restarting a progress
<br>     |          bar [default: 0].
<br>     |      position  : int, optional
<br>     |          Specify the line offset to print this bar (starting from 0)
<br>     |          Automatic if unspecified.
<br>     |          Useful to manage multiple bars at once (eg, from threads).
<br>     |      postfix  : dict or *, optional
<br>     |          Specify additional stats to display at the end of the bar.
<br>     |          Calls `set_postfix(**postfix)` if possible (dict).
<br>     |      unit_divisor  : float, optional
<br>     |          [default: 1000], ignored unless `unit_scale` is True.
<br>     |      gui  : bool, optional
<br>     |          WARNING: internal parameter - do not use.
<br>     |          Use tqdm_gui(...) instead. If set, will attempt to use
<br>     |          matplotlib animations for a graphical output [default: False].
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : decorated iterator.
<br>     |
<br>     |  __iter__(self)
<br>     |      Backward-compatibility to use: for x in tqdm(iterable)
<br>     |
<br>     |  __len__(self)
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  clear(self, nolock=False)
<br>     |      Clear current bar display
<br>     |
<br>     |  close(self)
<br>     |      Cleanup and (if leave=False) close the progressbar.
<br>     |
<br>     |  display(self, msg=None, pos=None)
<br>     |      Use `self.sp` and to display `msg` in the specified `pos`.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      msg  : what to display (default: repr(self))
<br>     |      pos  : position to display in. (default: abs(self.pos))
<br>     |
<br>     |  moveto(self, n)
<br>     |
<br>     |  refresh(self, nolock=False)
<br>     |      Force refresh the display of this bar
<br>     |
<br>     |  set_description(self, desc=None, refresh=True)
<br>     |      Set/modify description of the progress bar.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      desc  : str, optional
<br>     |      refresh  : bool, optional
<br>     |          Forces refresh [default: True].
<br>     |
<br>     |  set_description_str(self, desc=None, refresh=True)
<br>     |      Set/modify description without ': ' appended.
<br>     |
<br>     |  set_postfix(self, ordered_dict=None, refresh=True, **kwargs)
<br>     |      Set/modify postfix (additional stats)
<br>     |      with automatic formatting based on datatype.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      ordered_dict  : dict or OrderedDict, optional
<br>     |      refresh  : bool, optional
<br>     |          Forces refresh [default: True].
<br>     |      kwargs  : dict, optional
<br>     |
<br>     |  set_postfix_str(self, s='', refresh=True)
<br>     |      Postfix without dictionary expansion, similar to prefix handling.
<br>     |
<br>     |  unpause(self)
<br>     |      Restart tqdm timer from last print time.
<br>     |
<br>     |  update(self, n=1)
<br>     |      Manually update the progress bar, useful for streams
<br>     |      such as reading files.
<br>     |      E.g.:
<br>     |      >>> t = tqdm(total=filesize) # Initialise
<br>     |      >>> for current_buffer in stream:
<br>     |      ...    ...
<br>     |      ...    t.update(len(current_buffer))
<br>     |      >>> t.close()
<br>     |      The last line is highly recommended, but possibly not necessary if
<br>     |      `t.update()` will be called in such a way that `filesize` will be
<br>     |      exactly reached and printed.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int, optional
<br>     |          Increment to add to the internal counter of iterations
<br>     |          [default: 1].
<br>     |
<br>     |  <hr>
<br>     |  Class methods defined here:
<br>     |
<br>     |  external_write_mode(file=None, nolock=False) from builtins.type
<br>     |      Disable tqdm within context and refresh tqdm when exits.
<br>     |      Useful when writing to standard output stream
<br>     |
<br>     |  get_lock() from builtins.type
<br>     |      Get the global lock. Construct it if it does not exist.
<br>     |
<br>     |  pandas(*targs, **tkwargs) from builtins.type
<br>     |      Registers the given `tqdm` class with
<br>     |          pandas.core.
<br>     |          ( frame.DataFrame
<br>     |          | series.Series
<br>     |          | groupby.DataFrameGroupBy
<br>     |          | groupby.SeriesGroupBy
<br>     |          ).progress_apply
<br>     |
<br>     |      A new instance will be create every time `progress_apply` is called,
<br>     |      and each instance will automatically close() upon completion.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      targs, tkwargs  : arguments for the tqdm instance
<br>     |
<br>     |      Examples
<br>     |      --------
<br>     |      >>> import pandas as pd
<br>     |      >>> import numpy as np
<br>     |      >>> from tqdm import tqdm, tqdm_gui
<br>     |      >>>
<br>     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
<br>     |      >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
<br>     |      >>> # Now you can use `progress_apply` instead of `apply`
<br>     |      >>> df.groupby(0).progress_apply(lambda x: x**2)
<br>     |
<br>     |      References
<br>     |      ----------
<br>     |      https://stackoverflow.com/questions/18603270/
<br>     |      progress-indicator-during-pandas-operations-python
<br>     |
<br>     |  set_lock(lock) from builtins.type
<br>     |      Set the global lock.
<br>     |
<br>     |  write(s, file=None, end='\n', nolock=False) from builtins.type
<br>     |      Print a message via tqdm (without overlap with bars)
<br>     |
<br>     |  <hr>
<br>     |  Static methods defined here:
<br>     |
<br>     |  __new__(cls, *args, **kwargs)
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  ema(x, mu=None, alpha=0.3)
<br>     |      Exponential moving average: smoothing to give progressively lower
<br>     |      weights to older values.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      x  : float
<br>     |          New value to include in EMA.
<br>     |      mu  : float, optional
<br>     |          Previous EMA value.
<br>     |      alpha  : float, optional
<br>     |          Smoothing factor in range [0, 1], [default: 0.3].
<br>     |          Increase to give more weight to recent values.
<br>     |          Ranges from 0 (yields mu) to 1 (yields x).
<br>     |
<br>     |  format_interval(t)
<br>     |      Formats a number of seconds as a clock time, [H:]MM:SS
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      t  : int
<br>     |          Number of seconds.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          [H:]MM:SS
<br>     |
<br>     |  format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000, **extra_kwargs)
<br>     |      Return a string-based progress bar given some parameters
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int
<br>     |          Number of finished iterations.
<br>     |      total  : int
<br>     |          The expected total number of iterations. If meaningless (), only
<br>     |          basic progress statistics are displayed (no ETA).
<br>     |      elapsed  : float
<br>     |          Number of seconds passed since start.
<br>     |      ncols  : int, optional
<br>     |          The width of the entire output message. If specified,
<br>     |          dynamically resizes the progress meter to stay within this bound
<br>     |          [default: None]. The fallback meter width is 10 for the progress
<br>     |          bar + no limit for the iterations counter and statistics. If 0,
<br>     |          will not print any meter (only stats).
<br>     |      prefix  : str, optional
<br>     |          Prefix message (included in total width) [default: ''].
<br>     |          Use as {desc} in bar_format string.
<br>     |      ascii  : bool, optional
<br>     |          If not set, use unicode (smooth blocks) to fill the meter
<br>     |          [default: False]. The fallback is to use ASCII characters
<br>     |          (1-9 #).
<br>     |      unit  : str, optional
<br>     |          The iteration unit [default: 'it'].
<br>     |      unit_scale  : bool or int or float, optional
<br>     |          If 1 or True, the number of iterations will be printed with an
<br>     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
<br>     |          [default: False]. If any other non-zero number, will scale
<br>     |          `total` and `n`.
<br>     |      rate  : float, optional
<br>     |          Manual override for iteration rate.
<br>     |          If [default: None], uses n/elapsed.
<br>     |      bar_format  : str, optional
<br>     |          Specify a custom bar string formatting. May impact performance.
<br>     |          [default: '{l_bar}{bar}{r_bar}'], where
<br>     |          l_bar='{desc}: {percentage:3.0f}%|' and
<br>     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
<br>     |            '{rate_fmt}{postfix}]'
<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
<br>     |          Note that a trailing ": " is automatically removed after {desc}
<br>     |          if the latter is empty.
<br>     |      postfix  : *, optional
<br>     |          Similar to `prefix`, but placed at the end
<br>     |          (e.g. for additional stats).
<br>     |          Note: postfix is usually a string (not a dict) for this method,
<br>     |          and will if possible be set to postfix = ', ' + postfix.
<br>     |          However other types are supported (#382).
<br>     |      unit_divisor  : float, optional
<br>     |          [default: 1000], ignored unless `unit_scale` is True.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : Formatted meter and stats, ready to display.
<br>     |
<br>     |  format_num(n)
<br>     |      Intelligent scientific notation (.3g).
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int or float or Numeric
<br>     |          A Number.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          Formatted number.
<br>     |
<br>     |  format_sizeof(num, suffix='', divisor=1000)
<br>     |      Formats a number (greater than unity) with SI Order of Magnitude
<br>     |      prefixes.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      num  : float
<br>     |          Number ( >= 1) to format.
<br>     |      suffix  : str, optional
<br>     |          Post-postfix [default: ''].
<br>     |      divisor  : float, optionl
<br>     |          Divisor between prefixes [default: 1000].
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          Number with Order of Magnitude SI unit postfix.
<br>     |
<br>     |  status_printer(file)
<br>     |      Manage the printing and in-place updating of a line of characters.
<br>     |      Note that if the string is longer than a line, then in-place
<br>     |      updating may not work (it will print a new line at each refresh).
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors defined here:
<br>     |
<br>     |  format_dict
<br>     |      Public API for read-only member access
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes defined here:
<br>     |
<br>     |  monitor = None
<br>     |
<br>     |  monitor_interval = 10
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from tqdm._utils.Comparable:
<br>     |
<br>     |  __eq__(self, other)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, other)
<br>     |      Return self>=value.
<br>     |
<br>     |  __gt__(self, other)
<br>     |      Return self>value.
<br>     |
<br>     |  __le__(self, other)
<br>     |      Return self<=value.
<br>     |
<br>     |  __lt__(self, other)
<br>     |      Return self<value.
<br>     |
<br>     |  __ne__(self, other)
<br>     |      Return self!=value.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from tqdm._utils.Comparable:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>    class tqdm_gui(tqdm._tqdm.tqdm)
<br>     |  tqdm_gui(*args, **kwargs)
<br>     |
<br>     |  Experimental GUI version of tqdm!
<br>     |
<br>     |  Method resolution order:
<br>     |      tqdm_gui
<br>     |      tqdm._tqdm.tqdm
<br>     |      tqdm._utils.Comparable
<br>     |      builtins.object
<br>     |
<br>     |  Methods defined here:
<br>     |
<br>     |  __init__(self, *args, **kwargs)
<br>     |      Parameters
<br>     |      ----------
<br>     |      iterable  : iterable, optional
<br>     |          Iterable to decorate with a progressbar.
<br>     |          Leave blank to manually manage the updates.
<br>     |      desc  : str, optional
<br>     |          Prefix for the progressbar.
<br>     |      total  : int, optional
<br>     |          The number of expected iterations. If unspecified,
<br>     |          len(iterable) is used if possible. If float("inf") or as a last
<br>     |          resort, only basic progress statistics are displayed
<br>     |          (no ETA, no progressbar).
<br>     |          If `gui` is True and this parameter needs subsequent updating,
<br>     |          specify an initial arbitrary large positive integer,
<br>     |          e.g. int(9e9).
<br>     |      leave  : bool, optional
<br>     |          If [default: True], keeps all traces of the progressbar
<br>     |          upon termination of iteration.
<br>     |      file  : `io.TextIOWrapper` or `io.StringIO`, optional
<br>     |          Specifies where to output the progress messages
<br>     |          (default: sys.stderr). Uses `file.write(str)` and `file.flush()`
<br>     |          methods.
<br>     |      ncols  : int, optional
<br>     |          The width of the entire output message. If specified,
<br>     |          dynamically resizes the progressbar to stay within this bound.
<br>     |          If unspecified, attempts to use environment width. The
<br>     |          fallback is a meter width of 10 and no limit for the counter and
<br>     |          statistics. If 0, will not print any meter (only stats).
<br>     |      mininterval  : float, optional
<br>     |          Minimum progress display update interval [default: 0.1] seconds.
<br>     |      maxinterval  : float, optional
<br>     |          Maximum progress display update interval [default: 10] seconds.
<br>     |          Automatically adjusts `miniters` to correspond to `mininterval`
<br>     |          after long display update lag. Only works if `dynamic_miniters`
<br>     |          or monitor thread is enabled.
<br>     |      miniters  : int, optional
<br>     |          Minimum progress display update interval, in iterations.
<br>     |          If 0 and `dynamic_miniters`, will automatically adjust to equal
<br>     |          `mininterval` (more CPU efficient, good for tight loops).
<br>     |          If > 0, will skip display of specified number of iterations.
<br>     |          Tweak this and `mininterval` to get very efficient loops.
<br>     |          If your progress is erratic with both fast and slow iterations
<br>     |          (network, skipping items, etc) you should set miniters=1.
<br>     |      ascii  : bool, optional
<br>     |          If unspecified or False, use unicode (smooth blocks) to fill
<br>     |          the meter. The fallback is to use ASCII characters `1-9 #`.
<br>     |      disable  : bool, optional
<br>     |          Whether to disable the entire progressbar wrapper
<br>     |          [default: False]. If set to None, disable on non-TTY.
<br>     |      unit  : str, optional
<br>     |          String that will be used to define the unit of each iteration
<br>     |          [default: it].
<br>     |      unit_scale  : bool or int or float, optional
<br>     |          If 1 or True, the number of iterations will be reduced/scaled
<br>     |          automatically and a metric prefix following the
<br>     |          International System of Units standard will be added
<br>     |          (kilo, mega, etc.) [default: False]. If any other non-zero
<br>     |          number, will scale `total` and `n`.
<br>     |      dynamic_ncols  : bool, optional
<br>     |          If set, constantly alters `ncols` to the environment (allowing
<br>     |          for window resizes) [default: False].
<br>     |      smoothing  : float, optional
<br>     |          Exponential moving average smoothing factor for speed estimates
<br>     |          (ignored in GUI mode). Ranges from 0 (average speed) to 1
<br>     |          (current/instantaneous speed) [default: 0.3].
<br>     |      bar_format  : str, optional
<br>     |          Specify a custom bar string formatting. May impact performance.
<br>     |          [default: '{l_bar}{bar}{r_bar}'], where
<br>     |          l_bar='{desc}: {percentage:3.0f}%|' and
<br>     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
<br>     |            '{rate_fmt}{postfix}]'
<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
<br>     |          Note that a trailing ": " is automatically removed after {desc}
<br>     |          if the latter is empty.
<br>     |      initial  : int, optional
<br>     |          The initial counter value. Useful when restarting a progress
<br>     |          bar [default: 0].
<br>     |      position  : int, optional
<br>     |          Specify the line offset to print this bar (starting from 0)
<br>     |          Automatic if unspecified.
<br>     |          Useful to manage multiple bars at once (eg, from threads).
<br>     |      postfix  : dict or *, optional
<br>     |          Specify additional stats to display at the end of the bar.
<br>     |          Calls `set_postfix(**postfix)` if possible (dict).
<br>     |      unit_divisor  : float, optional
<br>     |          [default: 1000], ignored unless `unit_scale` is True.
<br>     |      gui  : bool, optional
<br>     |          WARNING: internal parameter - do not use.
<br>     |          Use tqdm_gui(...) instead. If set, will attempt to use
<br>     |          matplotlib animations for a graphical output [default: False].
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : decorated iterator.
<br>     |
<br>     |  __iter__(self)
<br>     |      Backward-compatibility to use: for x in tqdm(iterable)
<br>     |
<br>     |  close(self)
<br>     |      Cleanup and (if leave=False) close the progressbar.
<br>     |
<br>     |  update(self, n=1)
<br>     |      Manually update the progress bar, useful for streams
<br>     |      such as reading files.
<br>     |      E.g.:
<br>     |      >>> t = tqdm(total=filesize) # Initialise
<br>     |      >>> for current_buffer in stream:
<br>     |      ...    ...
<br>     |      ...    t.update(len(current_buffer))
<br>     |      >>> t.close()
<br>     |      The last line is highly recommended, but possibly not necessary if
<br>     |      `t.update()` will be called in such a way that `filesize` will be
<br>     |      exactly reached and printed.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int, optional
<br>     |          Increment to add to the internal counter of iterations
<br>     |          [default: 1].
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from tqdm._tqdm.tqdm:
<br>     |
<br>     |  __del__(self)
<br>     |
<br>     |  __enter__(self)
<br>     |
<br>     |  __exit__(self, *exc)
<br>     |
<br>     |  __hash__(self)
<br>     |      Return hash(self).
<br>     |
<br>     |  __len__(self)
<br>     |
<br>     |  __repr__(self)
<br>     |      Return repr(self).
<br>     |
<br>     |  clear(self, nolock=False)
<br>     |      Clear current bar display
<br>     |
<br>     |  display(self, msg=None, pos=None)
<br>     |      Use `self.sp` and to display `msg` in the specified `pos`.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      msg  : what to display (default: repr(self))
<br>     |      pos  : position to display in. (default: abs(self.pos))
<br>     |
<br>     |  moveto(self, n)
<br>     |
<br>     |  refresh(self, nolock=False)
<br>     |      Force refresh the display of this bar
<br>     |
<br>     |  set_description(self, desc=None, refresh=True)
<br>     |      Set/modify description of the progress bar.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      desc  : str, optional
<br>     |      refresh  : bool, optional
<br>     |          Forces refresh [default: True].
<br>     |
<br>     |  set_description_str(self, desc=None, refresh=True)
<br>     |      Set/modify description without ': ' appended.
<br>     |
<br>     |  set_postfix(self, ordered_dict=None, refresh=True, **kwargs)
<br>     |      Set/modify postfix (additional stats)
<br>     |      with automatic formatting based on datatype.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      ordered_dict  : dict or OrderedDict, optional
<br>     |      refresh  : bool, optional
<br>     |          Forces refresh [default: True].
<br>     |      kwargs  : dict, optional
<br>     |
<br>     |  set_postfix_str(self, s='', refresh=True)
<br>     |      Postfix without dictionary expansion, similar to prefix handling.
<br>     |
<br>     |  unpause(self)
<br>     |      Restart tqdm timer from last print time.
<br>     |
<br>     |  <hr>
<br>     |  Class methods inherited from tqdm._tqdm.tqdm:
<br>     |
<br>     |  external_write_mode(file=None, nolock=False) from builtins.type
<br>     |      Disable tqdm within context and refresh tqdm when exits.
<br>     |      Useful when writing to standard output stream
<br>     |
<br>     |  get_lock() from builtins.type
<br>     |      Get the global lock. Construct it if it does not exist.
<br>     |
<br>     |  pandas(*targs, **tkwargs) from builtins.type
<br>     |      Registers the given `tqdm` class with
<br>     |          pandas.core.
<br>     |          ( frame.DataFrame
<br>     |          | series.Series
<br>     |          | groupby.DataFrameGroupBy
<br>     |          | groupby.SeriesGroupBy
<br>     |          ).progress_apply
<br>     |
<br>     |      A new instance will be create every time `progress_apply` is called,
<br>     |      and each instance will automatically close() upon completion.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      targs, tkwargs  : arguments for the tqdm instance
<br>     |
<br>     |      Examples
<br>     |      --------
<br>     |      >>> import pandas as pd
<br>     |      >>> import numpy as np
<br>     |      >>> from tqdm import tqdm, tqdm_gui
<br>     |      >>>
<br>     |      >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
<br>     |      >>> tqdm.pandas(ncols=50)  # can use tqdm_gui, optional kwargs, etc
<br>     |      >>> # Now you can use `progress_apply` instead of `apply`
<br>     |      >>> df.groupby(0).progress_apply(lambda x: x**2)
<br>     |
<br>     |      References
<br>     |      ----------
<br>     |      https://stackoverflow.com/questions/18603270/
<br>     |      progress-indicator-during-pandas-operations-python
<br>     |
<br>     |  set_lock(lock) from builtins.type
<br>     |      Set the global lock.
<br>     |
<br>     |  write(s, file=None, end='\n', nolock=False) from builtins.type
<br>     |      Print a message via tqdm (without overlap with bars)
<br>     |
<br>     |  <hr>
<br>     |  Static methods inherited from tqdm._tqdm.tqdm:
<br>     |
<br>     |  __new__(cls, *args, **kwargs)
<br>     |      Create and return a new object.  See help(type) for accurate signature.
<br>     |
<br>     |  ema(x, mu=None, alpha=0.3)
<br>     |      Exponential moving average: smoothing to give progressively lower
<br>     |      weights to older values.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      x  : float
<br>     |          New value to include in EMA.
<br>     |      mu  : float, optional
<br>     |          Previous EMA value.
<br>     |      alpha  : float, optional
<br>     |          Smoothing factor in range [0, 1], [default: 0.3].
<br>     |          Increase to give more weight to recent values.
<br>     |          Ranges from 0 (yields mu) to 1 (yields x).
<br>     |
<br>     |  format_interval(t)
<br>     |      Formats a number of seconds as a clock time, [H:]MM:SS
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      t  : int
<br>     |          Number of seconds.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          [H:]MM:SS
<br>     |
<br>     |  format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None, bar_format=None, postfix=None, unit_divisor=1000, **extra_kwargs)
<br>     |      Return a string-based progress bar given some parameters
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int
<br>     |          Number of finished iterations.
<br>     |      total  : int
<br>     |          The expected total number of iterations. If meaningless (), only
<br>     |          basic progress statistics are displayed (no ETA).
<br>     |      elapsed  : float
<br>     |          Number of seconds passed since start.
<br>     |      ncols  : int, optional
<br>     |          The width of the entire output message. If specified,
<br>     |          dynamically resizes the progress meter to stay within this bound
<br>     |          [default: None]. The fallback meter width is 10 for the progress
<br>     |          bar + no limit for the iterations counter and statistics. If 0,
<br>     |          will not print any meter (only stats).
<br>     |      prefix  : str, optional
<br>     |          Prefix message (included in total width) [default: ''].
<br>     |          Use as {desc} in bar_format string.
<br>     |      ascii  : bool, optional
<br>     |          If not set, use unicode (smooth blocks) to fill the meter
<br>     |          [default: False]. The fallback is to use ASCII characters
<br>     |          (1-9 #).
<br>     |      unit  : str, optional
<br>     |          The iteration unit [default: 'it'].
<br>     |      unit_scale  : bool or int or float, optional
<br>     |          If 1 or True, the number of iterations will be printed with an
<br>     |          appropriate SI metric prefix (k = 10^3, M = 10^6, etc.)
<br>     |          [default: False]. If any other non-zero number, will scale
<br>     |          `total` and `n`.
<br>     |      rate  : float, optional
<br>     |          Manual override for iteration rate.
<br>     |          If [default: None], uses n/elapsed.
<br>     |      bar_format  : str, optional
<br>     |          Specify a custom bar string formatting. May impact performance.
<br>     |          [default: '{l_bar}{bar}{r_bar}'], where
<br>     |          l_bar='{desc}: {percentage:3.0f}%|' and
<br>     |          r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
<br>     |            '{rate_fmt}{postfix}]'
<br>     |          Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
<br>     |            percentage, rate, rate_fmt, rate_noinv, rate_noinv_fmt,
<br>     |            rate_inv, rate_inv_fmt, elapsed, remaining, desc, postfix.
<br>     |          Note that a trailing ": " is automatically removed after {desc}
<br>     |          if the latter is empty.
<br>     |      postfix  : *, optional
<br>     |          Similar to `prefix`, but placed at the end
<br>     |          (e.g. for additional stats).
<br>     |          Note: postfix is usually a string (not a dict) for this method,
<br>     |          and will if possible be set to postfix = ', ' + postfix.
<br>     |          However other types are supported (#382).
<br>     |      unit_divisor  : float, optional
<br>     |          [default: 1000], ignored unless `unit_scale` is True.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : Formatted meter and stats, ready to display.
<br>     |
<br>     |  format_num(n)
<br>     |      Intelligent scientific notation (.3g).
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      n  : int or float or Numeric
<br>     |          A Number.
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          Formatted number.
<br>     |
<br>     |  format_sizeof(num, suffix='', divisor=1000)
<br>     |      Formats a number (greater than unity) with SI Order of Magnitude
<br>     |      prefixes.
<br>     |
<br>     |      Parameters
<br>     |      ----------
<br>     |      num  : float
<br>     |          Number ( >= 1) to format.
<br>     |      suffix  : str, optional
<br>     |          Post-postfix [default: ''].
<br>     |      divisor  : float, optionl
<br>     |          Divisor between prefixes [default: 1000].
<br>     |
<br>     |      Returns
<br>     |      -------
<br>     |      out  : str
<br>     |          Number with Order of Magnitude SI unit postfix.
<br>     |
<br>     |  status_printer(file)
<br>     |      Manage the printing and in-place updating of a line of characters.
<br>     |      Note that if the string is longer than a line, then in-place
<br>     |      updating may not work (it will print a new line at each refresh).
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from tqdm._tqdm.tqdm:
<br>     |
<br>     |  format_dict
<br>     |      Public API for read-only member access
<br>     |
<br>     |  <hr>
<br>     |  Data and other attributes inherited from tqdm._tqdm.tqdm:
<br>     |
<br>     |  monitor = None
<br>     |
<br>     |  monitor_interval = 10
<br>     |
<br>     |  <hr>
<br>     |  Methods inherited from tqdm._utils.Comparable:
<br>     |
<br>     |  __eq__(self, other)
<br>     |      Return self==value.
<br>     |
<br>     |  __ge__(self, other)
<br>     |      Return self>=value.
<br>     |
<br>     |  __gt__(self, other)
<br>     |      Return self>value.
<br>     |
<br>     |  __le__(self, other)
<br>     |      Return self<=value.
<br>     |
<br>     |  __lt__(self, other)
<br>     |      Return self<value.
<br>     |
<br>     |  __ne__(self, other)
<br>     |      Return self!=value.
<br>     |
<br>     |  <hr>
<br>     |  Data descriptors inherited from tqdm._utils.Comparable:
<br>     |
<br>     |  __dict__
<br>     |      dictionary for instance variables (if defined)
<br>     |
<br>     |  __weakref__
<br>     |      list of weak references to the object (if defined)
<br>
<br>FUNCTIONS
<br>    main(fp=<idlelib.run.PseudoOutputFile object at 0x0000027A2ADC4EB8>, argv=None)
<br>        Parameters (internal use only)
<br>        ---------
<br>        fp  : file-like object for tqdm
<br>        argv  : list (default: sys.argv[1:])
<br>
<br>    tgrange(*args, **kwargs)
<br>        A shortcut for tqdm_gui(xrange(*args), **kwargs).
<br>        On Python3+ range is used instead of xrange.
<br>
<br>    tnrange(*args, **kwargs)
<br>        A shortcut for tqdm_notebook(xrange(*args), **kwargs).
<br>        On Python3+ range is used instead of xrange.
<br>
<br>    tqdm_notebook(*args, **kwargs)
<br>        See tqdm._tqdm_notebook.tqdm_notebook for full documentation
<br>
<br>    tqdm_pandas(tclass, *targs, **tkwargs)
<br>        Registers the given `tqdm` instance with
<br>        `pandas.core.groupby.DataFrameGroupBy.progress_apply`.
<br>        It will even close() the `tqdm` instance upon completion.
<br>
<br>        Parameters
<br>        ----------
<br>        tclass  : tqdm class you want to use (eg, tqdm, tqdm_notebook, etc)
<br>        targs and tkwargs  : arguments for the tqdm instance
<br>
<br>        Examples
<br>        --------
<br>        >>> import pandas as pd
<br>        >>> import numpy as np
<br>        >>> from tqdm import tqdm, tqdm_pandas
<br>        >>>
<br>        >>> df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))
<br>        >>> tqdm_pandas(tqdm, leave=True)  # can use tqdm_gui, optional kwargs, etc
<br>        >>> # Now you can use `progress_apply` instead of `apply`
<br>        >>> df.groupby(0).progress_apply(lambda x: x**2)
<br>
<br>        References
<br>        ----------
<br>        https://stackoverflow.com/questions/18603270/
<br>        progress-indicator-during-pandas-operations-python
<br>
<br>    trange(*args, **kwargs)
<br>        A shortcut for tqdm(xrange(*args), **kwargs).
<br>        On Python3+ range is used instead of xrange.
<br>
<br>DATA
<br>    __all__ = ['tqdm', 'tqdm_gui', 'trange', 'tgrange', 'tqdm_pandas', 'tq...
<br>
<br>VERSION
<br>    4.30.0
<br>
<br>FILE
<br>    c:\users\matthijs\appdata\local\programs\python\python37\lib\site-packages\tqdm\__init__.py
<br>
<br>
<br>No Python documentation found for 'tqdm_gui'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'tqdm_loop'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'unicode_literals'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'update_progress'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'web'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
<br>
<br>No Python documentation found for 'web_open'.
<br>Use help() to get the interactive help utility.
<br>Use help(str) for help on the str class.
 </p></html>





</p>
</div>

</body>
</html>""")
# Create your views here.


