``styled-log``: logging.Formatter subclass that allows for custom formatted and styled logging.
=================================================================================================


By default, powered by [Colorama](https://github.com/tartley/colorama).

Allows for both ansi-styling capabilities for logger attributes, AND ansi-styling for particular values of that attribute. 

https://gitlab.com/ittVannak/styled-log/blob/master/styled-log.gif

## Examples:

##### Quick use:
```
import logging

# don't call basicConfig

logger = logging.getLogger('test_logger')
styled_formatter = StyledFormatter()

writes_to_console = logging.StreamHandler(sys.stderr)
writes_to_console.setFormatter(styled_formatter)

logger.addHandler(writes_to_console)
```

##### Log structure customization:
```
import logging

# don't call basicConfig

logger = logging.getLogger('test_logger')

custom_map = OrderedDict()
custom_map['%(asctime)s'] = ('blue_fore',)
custom_map['%(module)s'] = ('yellow_fore',)
custom_map['%(lineno)s'] = ('red_fore',)
custom_map['%(message)s'] = None
custom_map['%(levelname)s'] = {
                                'DEBUG'   : ('cyan_fore',), 
                                'INFO'    : ('blue_fore',),
                                'ERROR'   : ('red_fore', 'bright_style'),
                                'WARNING' : ('red_fore', 'bright_style'),
                                'CRITICAL': ('red_fore', 'bright_style')
                                }

styled_formatter = StyledFormatter(custom_map)

writes_to_console = logging.StreamHandler(sys.stderr)
writes_to_console.setFormatter(styled_formatter)

logger.addHandler(writes_to_console)
logger.info('hey there!')

2019-03-24 10:35:59,091 ; <ipython-input-2-7091e3083bda> ; 190 ; hey there! ;     INFO
```

##### Maximum customization:
```

import logging

# don't call basicConfig

logger = logging.getLogger('test_logger')

custom_ansi_map = {
'red': '\x1b[31m', 
'blue':'\x1b[34m', 
'green':'\x1b[32m'
}

load_ansi_map(custom_ansi_map)

# now every subsequent styling string we provide must be either 'red','blue', or 'green'

custom_map = OrderedDict()
custom_map['%(asctime)s'] = ('blue',)
custom_map['%(module)s'] = ('red',)
custom_map['%(lineno)s'] = ('red',)
custom_map['%(message)s'] = None
custom_map['%(levelname)s'] = {
'DEBUG'   : ('green', ), 
'INFO'    : ('blue', ),
'ERROR'   : ('red', ),
'WARNING' : ('red', ),
'CRITICAL': ('red', )
}

styled_formatter = StyledFormatter(custom_map)

writes_to_console = logging.StreamHandler(sys.stderr)
writes_to_console.setFormatter(styled_formatter)

logger.addHandler(writes_to_console)
logger.info('hey there!')

2019-03-24 10:35:59,091 ; <ipython-input-2-7091e3083bda> ; 190 ; hey there! ;     INFO
```

## Design

There are many ways this could be implemented, but my primary goals were:
1. Designing for readability -- i.e.  built around an ansi-map.
2. Not reinventing another ansi library.
3. Keeping ansi-code logic separate from logger formatting logic 
4. Keeping to the logging library's design principles

Knowing that, here are some basic concepts in this library:


* **global ansi map**: dictionary of human-readable names to ansi style codes.

* **load_ansi_map**: function that sets global ansi map value. Allows user to supply their own human-readable names to ansi style codes.

* **styledFormatter**: subclass of logging.Formatter, allowing for styled bylines for each logging message. **Styling arguments for this class must align with the human-readable names in the global ansi map.** 

* **style**: function that actually references the global ansi map and applies the ansi code.

* **show_ansi_map**: function that shows the effects of the different ansi codes on a string.

## Important Notes
1. Again,  **styling arguments for styledFormatter must align with the keys in the global ansi map.**  This means 
    1. if you chose to provide a custom ansi map, it the map must contain the keys referenced in the optional styledFormatter arguments
    2. or, you explicitly provide the values for those arguments to align with your ansi map.
2. Even though you can provide ```%()d/f``` attributes as normal, we are string formatting, so they will come back as strings, though I don't expect that to be an issue.

## Questions:
**Why tuples?**
1. You can apply more than one ansi code to a string. For example, it might make sense for "ALERT" to be both red and bright, in which case the call to style (when using the default ansi map) would be:
```style(text="ALERT", ("red_fore", "bright_style"))```

**Why a global dictionary**?
1. To separate concerns of the log byline format from the ansi codes.
2. One less argument in the styledFormatter instantiation.
3. I prefer the usability of an explicit ```load_ansi_map(custom_ansi_map)```
4. Allows user to programmatically change styles without having to reinstantiate their formatter. Consider styling like:
```low_intensity: some_ansi, mid_intensity:another_ansi, high_intensity: a_third_ansi``` and then being able to switch those values on the fly.

## Struggles:
1. How much customization is too much - I still don't know the answer.
2. How much liberty can I take from the typical formatting argument structure?
3. Finding  a way to leverage ```__slots__```.