#!/usr/bin/env python
# coding=utf-8
#
# File: EmBCI/embci/viz/screen.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Thu 07 Feb 2019 21:29:21 CST

'''Graphic User Interface utilities based on screen devices.'''

# built-in
import os
import time
import select
import logging
import warnings
import traceback
import threading
import functools

# requirements.txt: data-processing: numpy
# requirements.txt: drivers: pyserial
# requirements.txt: necessary: pillow, decorator
import numpy as np
import serial
from PIL import Image
from decorator import decorator

from ..configs import BASEDIR
from ..io import SerialCommander
from ..utils.ili9341_api import ILI9341_API, rgb565to888, rgb888to565
from ..utils import (time_stamp, find_gui_layouts, ensure_unicode, get_config,
                     serialize, deserialize, get_func_args, config_logger,
                     AttributeDict, AttributeList, Singleton)
from ..constants import (command_dict_uart_screen_winbond_v1,
                         colormapper_uart_screen_winbond_v1,
                         colormapper_spi_screen_ili9341,
                         colormapper_default)

# ===============================================================================
# Constants

logger = config_logger()
__dir__ = os.path.dirname(os.path.abspath(__file__))
__all__ = []

DEFAULT_WIDGET = AttributeDict({
    'point': AttributeList(), 'text': AttributeList(), 'img': AttributeList(),
    'button': AttributeList(), 'line': AttributeList(),
    'circle': AttributeList(), 'circlef': AttributeList(),
    'round': AttributeList(), 'roundf': AttributeList(),
    'rect': AttributeList(), 'rectf': AttributeList(),
    'round_rect': AttributeList(), 'round_rectf': AttributeList()
})

DEFAULT_COLOR = AttributeDict({
    'point': 'blue', 'text': 'black', 'bg': 'white',
    'press': ['red', 'cyan'], 'line': 'red',
    'circle': 'red', 'circlef': 'red',
    'round': 'yellow', 'roundf': 'cyan',
    'rect': 'pink', 'rectf': 'orange',
    'round_rect': 'purple', 'round_rectf': 'purple'
})


# ===============================================================================
# Mini GUI Framework

class Colormap(object):
    '''
    Mapping color (str | int | list | tuple) to specific format that
    screen accept. Default RGB888 tuple.

    Examples
    --------
    >>> mapper = ColorMapping()
    >>> mapper(0xff0000)
    (255, 0, 0)
    >>> mapper([0, 255, 0])
    (0, 255, 0)
    >>> mapper('blue')
    (0, 0, 255)
    >>> mapper['grey']  # equals to mapper('grey')
    (128, 128, 128)
    >>> mapper(None) ==> None
    '''
    _str_dict = colormapper_default

    def __init__(self, str_dict=None, cstr=None, cint=None, carray=None):
        self._str_dict = str_dict or self._str_dict
        self._converters = {}
        self._converters[str] = cstr or self.convert_str
        self._converters[int] = cint or self.convert_int
        self._converters[list] = carray or self.convert_array
        self._converters[tuple] = carray or self.convert_array

    def convert_int(self, v):
        '''RGB24 uint24 to RGB888 tuple'''
        return v >> 16, (v >> 8) & 0xff, v & 0xff

    def convert_str(self, v):
        '''Color name to RGB888 using color mapping dict'''
        try:
            return self._str_dict[v]
        except KeyError:
            raise ValueError('color `{}` is not supported'.format(v))

    def convert_array(self, v):
        '''RGB565 two-bytes array to RGB888 tuple'''
        if len(v) == 2:
            return rgb565to888(*v)
        elif len(v) == 3:
            return tuple(v)
        else:
            raise ValueError('invalid array color `{}`'.format(v))

    def __getitem__(self, *a):
        try:
            return self.__call__(*a)
        except ValueError as e:
            raise KeyError(str(e))

    def __call__(self, *a):
        v = a[0] if len(a) == 1 else a
        if v is None:
            return
        if isinstance(v, int) and (v > 0xFFFFFF or v < 0):
            raise ValueError('invalid 24bit color `{}`'.format(hex(v)))
        if type(v) in self._converters:
            return self._converters[type(v)](v)
        raise TypeError('color type `{}` is not supported'.format(type(v)))


default_colormap = Colormap()


class DrawElementMixin(object):
    '''
    GUI instance has a variable `widget` representing current frame. Elements
    added into the widget will not display on screen until method `render` is
    called.

    Encoding is used to decode string and render text elements. Because some
    screen device accept bytes data and only implement local encodings such
    as GBK232 inside screen microchip. Default use UTF-8.

    GUI subclass of DrawElementMixin should implement method `send`.

    Draw Elements
    -------------
    draw_point      -- Draw a point.
    draw_line       -- Draw straight line.
    draw_rect       -- Draw rectangle or filled rectangle.
    draw_circle     -- Draw circle with start angle and end angle.
    draw_text       -- Draw string with specific font and size.
    draw_round      -- Draw rounded corner: quarter `arc` or `sector`.
    draw_round_rect -- Draw rectangle with rounded corner.
    draw_img        -- Draw an 3D array or PIL image.
    draw_button     -- Draw button: `button` = `text` + `rect`
    display_img     -- Display image on whole screen for a while.
    '''
    encoding = 'utf8'
    width, height = 320, 240

    def __init__(self):
        '''only used for testing'''
        # cannot directly draw on DEFAULT_WIDGET, it's used as a template
        self.widget = DEFAULT_WIDGET.deepcopy()
        self.color = DEFAULT_COLOR.deepcopy()

    def _pre_draw_check(name):
        '''
        1. user provide param *a and **k
        2. modify *a and add `element` & `id` to **k
        3. real function finally recieve *a, **k and defaults
        # TODO: text auto-linefeed
        '''
        @decorator
        def wrapper(func, self, *a, **k):
            # ensure element border inside screen
            a = self._check_position(name, a)
            # map all types of color to RGB888
            args, _ = get_func_args(func)
            for n, arg in enumerate(args):
                if arg.startswith('color') and len(a) > n:
                    a[n] = default_colormap(a[n])
            # add element into self.widget
            k['element'] = name + ('f' if k.get('fill', False) else '')
            k['id'] = max(self.widget[k['element']].id or [0]) + 1
            func(self, *a, **k)
            if k.pop('render', True):
                self.render(**k)
        return wrapper

    def _check_position(self, name, args):
        '''
        Modify arguments to a proper value to keep elements inside screen.

        Parameters
        ----------
        name : str
            Element name.
        args : array-like
            User provided arguments which contains position configs.
        '''
        if name in ['point', 'text', 'img', 'button']:
            args[0] = max(min(args[0], self.width - 1), 0)
            args[1] = max(min(args[1], self.height - 1), 0)
        elif name in ['circle', 'round']:
            args[0] = max(min(args[0], self.width - 2), 1)
            args[1] = max(min(args[1], self.height - 2), 1)
            right, down = self.width - 1 - args[0], self.height - 1 - args[1]
            args[2] = max(min(args[0], args[1], right, down, args[2]), 0)
        elif name in ['rect', 'rectf', 'round_rect', 'round_rectf']:
            args[0], args[2] = min(args[0], args[2]), max(args[0], args[2])
            args[1], args[3] = min(args[1], args[3]), max(args[1], args[3])
            args[0] = max(min(args[0], self.width - 1), 0)
            args[1] = max(min(args[1], self.height - 1), 0)
            args[2] = max(min(args[2], self.width - 1), args[0])
            args[3] = max(min(args[3], self.height - 1), args[1])
        elif name in ['line']:
            args[0] = max(min(args[0], self.width - 1), 0)
            args[1] = max(min(args[1], self.height - 1), 0)
            args[2] = max(min(args[2], self.width - 1), 0)
            args[3] = max(min(args[3], self.height - 1), 0)
        else:
            raise ValueError('element `{}` is not supported'.format(name))
        return args

    def __repr__(self):
        info, maxlen = '', 12
        for key in self.widget:
            id_str = ', '.join(map(str, self.widget[key].id))
            info += ' {:11s} | {}\n'.format(key, id_str if id_str else None)
            maxlen = max(maxlen, len(id_str))
        return ('<%s at %s\n' % (self.name, hex(id(self))) +
                ' Widget summary:\n elements    | id\n' +
                ' %s+%s\n%s>' % ('-' * 11, '-' * maxlen, info))

    def default_callback(self, x, y, bt):
        '''default button callback'''
        logger.info('[Touch Screen] touch button {} - `{}` at ({}, {}) at {}'
                    .format(bt['id'], bt['s'], x, y, time_stamp()))

    @_pre_draw_check('img')
    def draw_img(self, x, y, img, color_bg=None, **k):
        '''
        Draw image on current frame.

        Parameters
        ----------
        x, y : int
            Left upper coordinate of image in pixel.
        img : array-like or PIL.image
            2/3D array and PIL image object are supported.
        color_bg : str or int, optional
            Background color of image.
        '''
        img = np.atleast_2d(img).astype(np.uint8)
        assert img.ndim <= 3, 'Invalid image shape {}!'.format(img.shape)
        if img.ndim == 2:
            img = np.repeat(img[:, :, np.newaxis], 3, axis=2)
        self.widget.img.append(AttributeDict({
            'x1': x, 'y1': y, 'x2': x + img.shape[1], 'y2': y + img.shape[0],
            'id': k['id'], 'x': x, 'y': y, 'img': img, 'bg': color_bg}))

    @_pre_draw_check('button')
    def draw_button(self, x, y, s, color_text=None, size=16, font=None,
                    callback=None, color_rect='black', **k):
        '''
        Draw a button on current frame,

        Parameters
        ----------
        x, y : int
            Left upper coordinate of button text in pixel.
        s : str
            Button text string to display.
        color_text : str or int, optional
            Color of button text.
        callback : function, optional
            Callback function will be called with arguments (x, y, button)
            after button is clicked.
        color_rect : str or int, optional
            Color of outside rectangle of button.

        See Also
        --------
        draw_text
        default_callback
        '''
        s = ensure_unicode(s)
        w, h = self.getsize(s, size, font)
        if not callable(callback):
            callback = self.default_callback
        self.widget.button.append(AttributeDict({
            'x1': max(x - 1, 0), 'y1': max(y - 1, 0),
            'x2': min(x + w + 1, self.width - 1),
            'y2': min(y + h + 1, self.height - 1),
            'id': k['id'], 'x': x, 'y': y,
            's': s, 'size': size, 'font': font,
            'ct': color_text or self.color['text'],
            'cr': color_rect,
            'callback': callback}))

    @_pre_draw_check('point')
    def draw_point(self, x, y, color=None, **k):
        self.widget['point'].append(AttributeDict({
            'x1': x, 'y1': y, 'x2': x, 'y2': y, 'x': x, 'y': y,
            'id': k['id'], 'c': color or self.color['point']}))

    @_pre_draw_check('line')
    def draw_line(self, x1, y1, x2, y2, color=None, **k):
        self.widget['line'].append(AttributeDict({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'id': k['id'], 'c': color or self.color['line']}))

    @_pre_draw_check('rect')
    def draw_rect(self, x1, y1, x2, y2, color=None, fill=False, **k):
        '''
        Draw rectangle on current frame.

        Parameters
        ----------
        x1, y1 : int
            Left upper coordinate of rectangle in pixel.
        x2, y2 : int
            Right lower coordinate of rectangle in pixel.
        color : str or int, optional
            Color of rectangle border.
        fill : bool, optional
            Fill rectangle with border color, default False.
        '''
        self.widget[k['element']].append(AttributeDict({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'id': k['id'], 'c': color or self.color[k['element']]}))

    @_pre_draw_check('round')
    def draw_round(self, x, y, r, m, color=None, fill=False, **k):
        '''
        Draw a rounded corner (quarter arc | sector) on current frame.

        Parameters
        ----------
        x, y : int
            Center coordinate of rounded corner.
        r : int
            Radius of rounded corner.
        m : int
            corner number

            ====== ====================================
            corner              position
            ====== ====================================
            0        0 -  90 degree: right upper corner
            1       90 - 180 degree:  left upper corner
            2      180 - 270 degree:  left lower corner
            3      270 - 360 degree: right lower corner
        color : str or int, optional
            Color of rounded corner.
        fill : bool, optional
            Fill rounded corner(arc) into a sector, default False.
        '''
        if m == 0:
            x1, y1, x2, y2 = x, y - r, x + r, y
        elif m == 1:
            x1, y1, x2, y2 = x - r, y - r, x, y
        elif m == 2:
            x1, y1, x2, y2 = x - r, y, x, y + r
        elif m == 3:
            x1, y1, x2, y2 = x, y, x + r, y + r
        self.widget[k['element']].append(AttributeDict({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'x': x, 'y': y, 'r': r, 'm': m,
            'id': k['id'], 'c': color or self.color[k['element']]}))

    @_pre_draw_check('round_rect')
    def draw_round_rect(self, x1, y1, x2, y2, r, color=None, fill=False, **k):
        '''
        Draw rectangle with rounded corners.

        See Also
        --------
        draw_rect
        draw_round
        '''
        self.widget[k['element']].append(AttributeDict({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'r': r,
            'id': k['id'], 'c': color or self.color[k['element']]}))

    @_pre_draw_check('circle')
    def draw_circle(self, x, y, r, color=None, s=0, e=360, fill=False, **k):
        '''
        Draw an arc/circle on current frame.

        Parameters
        ----------
        x, y : int
            Center coordinate of circle.
        r : int
            Radius of circle.
        color : str or int, optional
            Color of circle.
        s : int, optional
            Start angle of arc/circle in degree, default 0.
        e : int, optional
            End angle of arc/circle in degree, default 360.
        fill : bool, optional
            Fill arc/circle with border color, default False.
        '''
        self.widget[k['element']].append(AttributeDict({
            'x1': x - r, 'y1': y - r, 'x2': x + r, 'y2': y + r,
            'x': x, 'y': y, 'r': r, 's': s, 'e': e,
            'id': k['id'], 'c': color or self.color[k['element']]}))

    @_pre_draw_check('text')
    def draw_text(self, x, y, s, color=None, size=16, font=None, **k):
        '''
        Draw text on current frame.

        Parameters
        ----------
        x, y : int
            Left upper coordinate of text element.
        s : str
            Text string to display.
        color : str or int, optioanl
            Color of text.
        size : int, optional
            Size of text in pixel, default 16.
        font : str, optional
            Font name of text, or an absolute path to font file.
        '''
        s = ensure_unicode(s)
        w, h = self.getsize(s, size, font)
        self.widget['text'].append(AttributeDict({
            'x1': x, 'y1': y,
            'x2': min(x + w, self.width - 1),
            'y2': min(y + h, self.height - 1),
            'id': k['id'], 'x': x, 'y': y,
            's': s, 'size': size, 'font': font,
            'c': color or self.color['text']}))

    def display_img(self, filename_or_img, *a, **k):
        if isinstance(filename_or_img, str):
            img = Image.open(filename_or_img)
        elif isinstance(filename_or_img, np.ndarray):
            img = Image.fromarray(filename_or_img)
        elif Image.isImageType(filename_or_img):
            img = filename_or_img
        else:
            return
        self.freeze_frame()

        # adjust img size
        w, h = img.size
        if (float(w) / h) >= (float(self.width) / self.height):
            img = img.resize((self.width, int(float(self.width) / w * h)))
        else:
            img = img.resize((int(float(self.height) / h * w), self.height))

        # place image on center of the frame
        w, h = np.array([self.width, self.height]) - img.size
        self.draw_img(w / 2, h / 2, img)

        # add footer guide text
        s1 = u'\u4efb\u610f\u70b9\u51fb\u5f00\u59cb'
        w, h = self.getsize(s1, size=18)
        w, h = (self.width - w) / 2, self.height - 2 * h - 3
        self.draw_text(w, h, s1, 'red', 18)
        s2 = 'click to continue'
        w, h = self.getsize(s2, size=18)
        w, h = (self.width - w) / 2, self.height - 1 * h - 5
        self.draw_text(w, h, s2, 'red', 18)

        # click the screen to break
        if self._touch_started:
            self._touch_pause.clear()  # pause _touchscreen_handler thread
            time.sleep(1.1)
            self._get_touch_point(timeout=10)  # auto-break after 10 seconds
            self._touch_pause.set()  # resume _touchscreen_handler thread
        else:
            time.sleep(5)
        self.recover_frame()

    def getsize(self, s, *a):
        '''Get width and height pixel of string.'''
        return len(s) * 8, 16

    def render(self, element=None, id=None, clear=True, *a, **k):
        '''Render elements stored in self.widget to screen.'''
        # render all
        if None in [element, id]:
            self.clear()  # clear all screen
            for element in self.widget:
                for e in self.widget[element]:
                    self.render(element, e.id, clear=False)
        # render one element
        e = self.widget[element, id]
        if e is None:
            return
        if clear:
            self.clear(**e)  # clear specific element
        try:
            getattr(self, 'render_%s_hook' % element)(e)
        except TypeError:
            self.send(element, **e)

    def render_button_hook(self, e):
        e.c = e.ct
        self.send('text', **e)
        e.c = e.cr
        self.send('rect', **e)
        del e.c

    def clear(self, x1=None, y1=None, x2=None, y2=None, bg=None, **k):
        '''
        Clear screen area with specific color.

        Parameters
        ----------
        x1, y1, x2, y2 : int
            Area left-upper and right-lower corner coordinates.
        bg : color, optional
            Background color that set area to after clear.

        Examples
        --------
        >>> gui = GUIClass()
        >>> gui.draw_line(0, 0, 100, 100, color='blue')
        >>> gui.clear(20, 20, 40, 40, 'black')  # clear area with black color
        >>> gui.clear(**gui.widget['line', 1])  # clear element line.1
        >>> gui.clear(bg='green')  # clear whole screen green
        '''
        if None in [x1, y1, x2, y2]:
            self.send('clear', c=(bg or self.color['bg']))
        else:
            self.send('rectf', c=(bg or self.color['bg']),
                      x1=min(x1, x2), y1=min(y1, y2),
                      x2=max(x1, x2), y2=max(y1, y2))

    def send(self, *a, **k):
        warnings.warn(RuntimeWarning('Not implemented yet.'))
        logger.debug('=' * 80)
        logger.debug(a, k)
        logger.debug('=' * 80)


class TouchScreenMixin(object):
    '''
    Touch Screen
    ------------
    touch_sense             -- Touch sensibility (max frequency).
    touch_button_animation  -- Whether display animation after button clicked.
    touch_screen_animation  -- Whether display animation after screen touched.
    touchscreen_start       -- Start handler thread to run button callbacks.
    touchscreen_close       -- Close touchscreen connection and stop handler.
    touchscreen_calibration -- Run calibrate guide to correct touch point.
    '''
    _touch_lock = threading.Lock()
    _touch_epoll = select.epoll()
    _touch_prevx, _touch_prevy = 0, 0
    _cali_matrix = np.array([[1, 1], [0, 0]])
    touch_sense = 1
    touch_button_animation = True
    touch_screen_animation = True

    def __init__(self):
        '''only used for testing'''
        self.widget = DEFAULT_WIDGET.deepcopy()
        self.color = DEFAULT_COLOR.deepcopy()
        self._touch_started = False

    def touchscreen_start(self, port, baud=115200, block=False):
        '''
        Resistive touchscreen touch point can be accessed by Analog-to-Digital
        Converter(ADC). In EmBCI hardware we use ESP32 to read it and transfer
        touch info to embedded Linux by UART connection.

        Parameters
        ----------
        port : str
            Port name to establish serial connection.
        baud : int, optional
            Default baudrate is 115200.
        '''
        if self._touch_started:
            return
        self._touch_serial = serial.Serial(port, baud)
        self._touch_serial.flushInput()

        self._touch_epoll.register(self._touch_serial, select.EPOLLIN)
        self._touch_close = threading.Event()
        self._touch_close.clear()
        self._touch_pause = threading.Event()
        self._touch_pause.set()

        self._callback_threads = []
        self._touch_thread = threading.Thread(target=self._handle_touch)
        self._touch_thread.setDaemon(True)
        self._touch_thread.start()

        self._last_touch = time.time()
        self._touch_started = True

        # block current thread(usually main thread) by looply sleep, until
        # `self.close` is called or `self._flag_close` is set.
        if block:
            while not self._touch_close.isSet():
                time.sleep(1)

    def touchscreen_close(self):
        if not self._touch_started:
            return
        self._touch_close.set()
        self._touch_pause.clear()
        time.sleep(1.1)
        self._touch_epoll.unregister(self._touch_serial)
        self._touch_serial.write('\xaa\xaa\xaa\xaa')  # send close signal
        time.sleep(0.5)
        self._touch_serial.close()
        self._callback_threads = []
        self._touch_started = False

    def touchscreen_calibration(self, *a, **k):
        if not self._touch_started:
            logging.error('[Screen GUI] touch screen not initialized yet!')
            return
        self._touch_pause.clear()  # pause _touchscreen_handler thread
        self.freeze_frame()
        self.touch_sense = 1
        self._cali_matrix = np.array([[1, 1], [0, 0]])
        time.sleep(1.1)
        # display prompt string
        s = 'touch calibration'
        w, h = np.array([self.width, self.height]) - self.getsize(s, size=20)
        self.draw_text(w / 2, h / 2, s, color='green', size=20)
        # points where to be touched
        pts = np.array([[20, 20],
                        [self.width - 20, 20],
                        [20, self.height - 20],
                        [self.width - 20, self.height - 20]])
        # points where user touched
        ptt = np.zeros((4, 2))
        try:
            for i in range(4):
                logger.info('[Calibration] this is %d/4 points' % (i + 1))
                self.draw_circle(pts[i][0], pts[i][1], 4, 'blue')
                ptt[i] = self._get_touch_point()
                logger.info('[Calibration] touch at {}, {}'.format(*ptt[i]))
                self.draw_circle(pts[i][0], pts[i][1], 2, 'green', fill=True)
            self._cali_matrix = np.array([
                np.polyfit(ptt[:, 0], pts[:, 0], 1),
                np.polyfit(ptt[:, 1], pts[:, 1], 1)]).T
            logger.info('[Screen GUI] calibration done!\nTarget point:\n{}\n'
                        'Touched point:\n{}\ncalibration result matrix:\n{}\n'
                        .format(ptt, pts, self._cali_matrix))
        except Exception:
            logger.error(traceback.format_exc())
        finally:
            self.recover_frame()
            self._touch_pause.set()  # resume _touchscreen_handler thread

    def _get_touch_point(self, timeout=-1):
        '''
        Parse touch screen data into point coordinates in pixel.

        Parameters
        ----------
        timeout : int or float
            Timeout in seconds. -1 makes it never time out.

        Returns
        -------
        x, y : tuple of { None, -1, int }
            Return (None, None) if device is unreachable because of serial
            connection error or stopped touch thread,
            Return (-1, -1) if timeout or touch too frequently.
            Return (x, y) coordinates in pixel after calibration normally.
        '''
        if self._touch_close.isSet():
            return None, None
        # avoid being called from multiple threads
        with self._touch_lock:
            rlist = self._touch_epoll.poll(timeout=timeout)
            if not rlist:
                return -1, -1
            raw = self._touch_serial.read_until().strip()
            self._touch_serial.flushInput()
            # avoid touch screen too frequently(sensible)
            if (time.time() - self._last_touch) < (1.0 / self.touch_sense):
                return -1, -1
            self._last_touch = time.time()
            # raw string should be like "y, x, presure"
            try:
                y, x, _ = map(int, raw.split(','))
            except ValueError:
                logger.error('[Touch Screen] Invalid input %s' % raw)
                return None, None
            # get real touch point by applying calibration matrix
            pt = self._cali_matrix[0] * [y, x] + self._cali_matrix[1]
            return tuple(abs(pt))

    def _get_clicked_buttons(self, x, y):
        '''return button elements whose rect contain touch point (x, y)'''
        pick = np.array([
            np.array(self.widget.button.x1) < x,
            np.array(self.widget.button.x2) > x,
            np.array(self.widget.button.y1) < y,
            np.array(self.widget.button.y2) > y
        ]).T
        return [self.widget.button[id] for id in
                np.array(self.widget.button.id)[list(map(all, pick))]]

    def _touch_button_animate(self, bt):
        '''display animation on clicked button(blink~)'''
        if bt.ct != self.color['press'][0]:
            c = self.color['press'][0]
        else:
            c = self.color['press'][1]
        bt.c = c
        self.send('text', **bt)
        if bt.cr is not None:
            self.send('rect', **bt)
        time.sleep(0.3)
        bt.c = bt.ct
        self.send('text', **bt)
        if bt.cr is not None:
            bt.c = bt.cr
            self.send('rect', **bt)
        del bt.c

    def _touch_screen_animate(self, x, y):
        '''act like a mouse pointer'''
        self.send('point', self._touch_prevx,
                  self._touch_prevy, self.color['bg'])
        self.send('point', x, y, self.color['point'])
        self._touch_prevx, self._touch_prevy = x, y

    def _touchscreen_handler(self):
        while not self._touch_close.isSet():
            self._touch_pause.wait()
            x, y = self._get_touch_point(timeout=1)
            if None in [x, y]:
                raise RuntimeError('touch screen device read error')
            if x == y == -1:
                continue
            for bt in self._get_clicked_buttons(x, y):
                self._callback_threads.append(
                    threading.Thread(target=bt.callback, args=(x, y, bt)))
                self._callback_threads[-1].start()
                if self.touch_button_animation:
                    self._touch_button_animate(bt)
            if self.touch_screen_animation:
                self._touch_screen_animate(x, y)
        logger.info('[Touch Screen] touch handler thread exit.')

    def send(self, *a, **k):
        warnings.warn(RuntimeWarning('Not implemented yet.'))
        logger.debug('=' * 80)
        logger.debug(a, k)
        logger.debug('=' * 80)


class GUIControlMixin(object):
    '''
    GUI Control
    -----------
    move_element   -- Move element to specific position (x, y) in pixel.
    remove_element -- Delete element by `name` and `id`.
    save_frame     -- Save current widgets into a layout file.
    load_frame     -- Load widgets from specific layout file.
    freeze_frame   -- Stack current frame widgets to background.
    recover_frame  -- Recover lastest frame widgets from background.
    empty_frame    -- Clear current frame by emptying widget dict.
    '''

    def __init__(self):
        '''only used for testing'''
        self.widget = DEFAULT_WIDGET.deepcopy()
        self._frame_fifo = []

    def _get_element(self, element=None, id=None):
        elements = [key for key in self.widget.keys() if self.widget[key]]
        if len(elements) == 0:
            logger.warn('Empty widget bucket now!')
            return
        if element not in elements:
            logger.warn('Choose element from {}'.format(elements))
            return
        return self.widget[element, id]

    def move_element(self, element=None, id=None, x=0, y=0):
        e = self._get_element(element, id)
        if e is None:
            return
        e.x1, e.x2, e.y1, e.y2 = e.x1 + x, e.x2 + x, e.y1 + y, e.y2 + y
        if 'x' in e:
            e.x, e.y = e.x + x, e.y + y
        self.render()

    def remove_element(self, element=None, id=None):
        e = self._get_element(element, id)
        if e is None:
            return
        self.widget[element].remove(e)
        self.render()

    def save_frame(self, dir_or_file, method='dill', overwrite=True):
        '''
        Save current frame into a layout file.

        Parameters
        ----------
        dir_or_file : str
            Specifiying filename to save or layout file directory.
        format : str
            Serializition method, choose one from `dill`(default) and `json`
        overwrite : bool, optional
            True(default) to overwrite layout file if it already exists.

        Notes
        -----
        More detail about `dill` is available at
        https://github.com/uqfoundation/dill
        '''
        d = os.path.dirname(dir_or_file)
        if not os.path.exists(d):
            os.makedirs(d)

        # dir_or_file: non-exist file | exist file | exist directory
        if os.path.isdir(dir_or_file):
            fn = os.path.join(dir_or_file, 'layout-%s.pcl' % time_stamp())
        elif os.path.exists(dir_or_file) and not overwrite:
            fn = os.path.join(dir_or_file, 'layout-%s.pcl' % time_stamp())
        else:
            fn = dir_or_file

        # auto trailing with extension
        _, ext = os.path.splitext(fn)
        if method not in ext:
            fn += '.{}'.format(method)

        try:
            with open(fn, 'w') as f:
                f.write(serialize(self.widget, method))
            logger.info(self.name + 'save layout `{}` success.'.format(fn))
        except Exception:
            logger.info(self.name + 'save layout `{}` failed.'.format(fn))
            logger.error(traceback.format_ext())

    def load_frame(self, dir_or_file, method='dill', extend=False):
        '''
        Load widgets from specific layout file.

        Parameters
        ----------
        dir_or_file : str
            Layout filename to load or directory under which search for file.
        format : str
            Deserializition method, choose one from `dill`(default) and `json`
        extend : bool
            True to merge loaded widgets into current frame. False to replace
            current widgets with loaded one. Default False.
        '''
        if not os.path.exists(dir_or_file):
            logger.error(self.name + ' invalid dir or layout file name')
            return

        # dir_or_file: exist file | exist directory
        if os.path.isfile(dir_or_file):
            fn = dir_or_file
        else:
            fn = find_gui_layouts(dir_or_file)
            if fn is None:
                logger.error('{} no available layout in {}'.format(
                    self.name, dir_or_file))
                return

        # ensure deserialization method match file extension
        _, ext = os.path.splitext(fn)
        if ext and method not in ext:
            method = ext[1:]

        try:
            with open(fn) as f:
                tmp = deserialize(f.read(), method)
            logger.info(self.name + 'load layout `{}` success.'.format(fn))
        except Exception:
            logger.info(self.name + 'load layout `{}` failed.'.format(fn))
            logger.error(traceback.format_ext())
            return
        if extend:
            for element in self.widget:
                self.widget[element].extend(tmp[element])
        else:
            self.widget = tmp
        self.render()

    def freeze_frame(self):
        '''Stack current frame widgets to background'''
        self._frame_fifo.append(self.widget)
        self.empty_frame()

    def recover_frame(self):
        '''Recover lastest frame widgets from background'''
        if self._frame_fifo:
            self.widget = self._frame_fifo.pop(0)
        self.render()

    def empty_frame(self):
        '''clear current frame by emptying widget dict'''
        self.widget = DEFAULT_WIDGET.deepcopy()
        self.render()

    def render(self, *a, **k):
        DrawElementMixin.render(self, *a, **k)


__all__ += ['Colormap']
__guidoc__ = ''.join([
    DrawElementMixin.__doc__,
    GUIControlMixin.__doc__,
    TouchScreenMixin.__doc__,
])


# ===============================================================================
# UART Screen: Winbond 2.3' 220x176 LCD

def uartscreen_winbond_v1_carray(v):
    '''RGB888/RGB565 to 4bits color'''
    if len(v) == 2:
        v = rgb565to888(*v)
    if len(v) == 3:
        b = 0b1000
        for n, i in enumerate(v):
            if i > 128:
                b += 1 << n
        return b
    else:
        raise ValueError('invalid array color `{}`'.format(v))


class SerialScreenGUI(DrawElementMixin, TouchScreenMixin, GUIControlMixin,
                      SerialCommander):
    __doc__ = 'GUI class of UART controlled screen.\n' + __guidoc__

    # Drawing configs
    encoding = 'gbk'
    height, width = 220, 176

    # Touchscreen configs
    _cali_matrix = np.array([[0.2969, 0.2238], [-53.2104, -22.8996]])
    touch_sense = 4

    # Serial configs
    colormap = Colormap(
        str_dict=colormapper_uart_screen_winbond_v1,
        carray=uartscreen_winbond_v1_carray,
        cint=lambda v: uartscreen_winbond_v1_carray(
            (v >> 16, v >> 8 & 0xff, v & 0xff)))
    API = functools.partial(
        SerialCommander, command_dict_uart_screen_winbond_v1)

    def __init__(self, API=None, name=None, widget=None, color=None, *a, **k):
        '''
        Constructor for SerialScreenGUI.

        Parameters
        ----------
        API : class
            Serial connection and communication API class.
            Default use class `embci.io.SerialCommander`.
        name : str
            Instance name used for logging.
        widget, color : AttributeDict
            Check `DEFAULT_WIDGET` and `DEFAULT_COLOR`
        width, height : int
            Screen width and height in pixel.
        encoding : str
            Default GBK
        touch_sense : number
            Touchscreen sensibility.
        '''
        for key in k:
            if (key in ['height', 'width', 'encoding', 'touch_sense']
                    and k[key] is not None):
                setattr(self, key, k[key])
        self.widget = widget or DEFAULT_WIDGET.deepcopy()
        self.color = color or DEFAULT_COLOR.deepcopy()
        self._started = False
        self._touch_started = False
        self._frame_fifo = []

        self.name = name or '[Serial Screen GUI Commander {}]'.format(
            SerialCommander.__num__)
        self._api = (API or self.API)(self.name, *a, **k)

    def start(self, port='/dev/ttyS1', baudrate=115200):
        if self._started:
            return
        self._api.start(port, baudrate)
        self.send('dir', 1)  # set screen vertical
        self._started = True

    def close(self, *a, **k):
        if not self._started:
            return
        self.send('clear', c='black')
        self.touchscreen_close()
        self._api.close(self)
        self._started = False

    def send(self, key, *a, **k):
        ret = self._api.get_command(key)
        if ret is None:
            raise ValueError('element `{}` is not supported'.format(key))
        # Winbond v1 accept 4bits color number
        if 'c' in k:
            k['c'] = self.colormap(k['c'])
        # UART send bytesarray (Winbond GBK encoding)
        if 's' in k:
            k['s'] = k['s'].encode(self.encoding)
        try:
            ret[0] = ret[0].format(*a, **k)
        except (IndexError, KeyError):
            logger.error('{} unmatched element {} and param: {}, {}, {}'
                         .format(self.name, key, ret[0], a, k))
        with self._api._command_lock:
            self._api._command_serial.write(ret[0])
            time.sleep(ret[1])
        return key

    def getsize(self, s, size=None, font=None):
        '''
        Get width and height of string `s` with `size` and `font`

        Parameters
        ----------
        s : unicode
        size : int, optional
        font : str, optional
            If offered font filename doesn't exists or font type is not
            supported, use default font.

        Returns
        -------
        size : tuple of int
            size (width, height) in pixel
        '''
        # Serial Screen use 8 pixels for English characters and 16 pixels
        # for Chinese characters(GBK encoding)
        en_zh = [ord(char) > 255 for char in s]
        return en_zh.count(False) * 8 + en_zh.count(True) * 16, 16

    def render_img_hook(self, e):
        img = e.img[:, :, 0]
        x1, y1, x2, y2 = e.x1, e.y1, e.x2, e.y2
        cmd, delay = self._api._command_dict['point']
        with self._api._command_lock:
            for x in range(x2 - x1):
                for y in range(y2 - y1):
                    tosend = cmd.format(x=x1 + x, y=y1 + y, c=img[y, x]/16)
                    self._api._command_serial.write(tosend)
                    time.sleep(delay)

    def setsize(self, *a, **k):
        '''for compatibility'''
        pass

    def setfont(self, *a, **k):
        '''for compatibility'''
        pass


__all__ += ['SerialScreenGUI']


# ===============================================================================
# SPI Screen: ILI9341 2.4' 320x240 LCD

try:
    from ..configs import PIN_ILI9341_DC, PIN_ILI9341_RST
except ImportError:
    PIN_ILI9341_DC = get_config('PIN_ILI9341_DC', 2)
    PIN_ILI9341_RST = get_config('PIN_ILI9341_RST')  # , 3)


def spiscreen_ili9341_carray(v):
    '''RGB888 to RGB565 two-bytes array'''
    if len(v) == 2:
        return v
    elif len(v) == 3:
        return rgb888to565(*v)
    else:
        raise ValueError('invalid array color `{}`'.format(v))


class SPIScreenGUI(DrawElementMixin, TouchScreenMixin, GUIControlMixin):
    __doc__ = 'GUI class of SPI controlled screen.\n' + __guidoc__
    __metaclass__ = Singleton
    name = '[SPI Screen GUI Commander]'

    # Drawing configs
    encoding = 'utf8'
    height, width = 320, 240

    # Touchscreen configs
    _cali_matrix = np.array([[0.1911, -0.1490], [-22.0794, 255.0536]])
    touch_sense = 4

    # SPI configs
    colormap = Colormap(
        str_dict=colormapper_spi_screen_ili9341,
        carray=spiscreen_ili9341_carray,
        cint=lambda v: spiscreen_ili9341_carray(
            (v >> 16, v >> 8 & 0xff, v & 0xff)))
    API = functools.partial(
        ILI9341_API, PIN_ILI9341_DC, PIN_ILI9341_RST, width, height)

    def __init__(self, API=None, widget=None, color=None, *a, **k):
        '''
        Constructor for SPIScreenGUI.

        Parameters
        ----------
        API : class
            SPI connection and communication API class.
            Default use class `embci.utils.ili9341_api.ILI9341_API`.
        widget, color : AttributeDict
            Check `DEFAULT_WIDGET` and `DEFAULT_COLOR`
        width, height : int
            Screen width and height in pixel.
        encoding : str
            Default UTF-8.
        touch_sense : number
            Touchscreen sensibility.
        '''
        for key in k:
            if (key in ['height', 'width', 'encoding', 'touch_sense']
                    and k[key] is not None):
                setattr(self, key, k[key])
        self.widget = widget or DEFAULT_WIDGET.deepcopy()
        self.color = color or DEFAULT_COLOR.deepcopy()
        self._started = False
        self._touch_started = False
        self._frame_fifo = []

        self._api = (API or self.API)(*a, **k)
        self.setsize = self._api.setsize
        self.setfont = self._api.setfont
        self.setfont(os.path.join(BASEDIR, 'files/fonts/yahei_mono.ttf'))

    def start(self):
        if self._started:
            return
        self._api.start()
        self._started = True

    def close(self):
        if not self._started:
            return
        self._api.close()
        self.touchscreen_close()
        self._started = False

    def send(self, name, *a, **k):
        '''Send command `name` to SPI Screen'''
        if 'c' in k:
            k['c'] = self.colormap(k['c'])
        if 's' in k:
            k['s'] = k['s'].encode(self.encoding)
        if hasattr(self._api, 'draw_' + name):
            getattr(self._api, 'draw_' + name)(*a, **k)
        elif hasattr(self._api, name):
            getattr(self._api, name)(*a, **k)
        else:
            logger.error('{} Cannot render element `{}`!'.format(
                self.name, name))

    def getsize(self, s, size=None, font=None):
        '''
        Get width and height of string `s` with `size` and `font`

        Parameters
        ----------
        s : str
        size : int
            Optional
        font : str
            Optional. If offered font filename doesn't exists or filetype
            unsupported, use default font.

        Returns
        -------
        size : tuple of int
            size (width, height) in pixel
        '''
        if size is not None:
            self.setsize(size)
        if font is not None and os.path.exist(font):
            self.setfont(font)
        w, h = self._api.font.getsize(s)
        return w / 2, h / 2


__all__ += ['SPIScreenGUI']

# THE END
