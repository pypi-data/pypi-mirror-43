"""
Search operations.

For the key bindings implementation with attached filters, check
`prompt_toolkit.key_binding.bindings.search`. (Use these for new key bindings
instead of calling these function directly.)
"""
from __future__ import unicode_literals
from .application.current import get_app
from .filters import is_searching, to_filter
from .key_binding.vi_state import InputMode
import six

__all__ = [
    'SearchDirection',
    'start_search',
    'stop_search',
]


class SearchDirection(object):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'

    _ALL = [FORWARD, BACKWARD]


class SearchState(object):
    """
    A search 'query', associated with a search field (like a SearchToolbar).

    Every searchable `BufferControl` points to a `search_buffer_control`
    (another `BufferControls`) which represents the search field. The
    `SearchState` attached to that search field is used for storing the current
    search query.

    It is possible to have one searchfield for multiple `BufferControls`. In
    that case, they'll share the same `SearchState`.
    If there are multiple `BufferControls` that display the same `Buffer`, then
    they can have a different `SearchState` each (if they have a different
    search control).
    """
    __slots__ = ('text', 'direction', 'ignore_case')

    def __init__(self, text='', direction=SearchDirection.FORWARD, ignore_case=False):
        assert isinstance(text, six.text_type)
        assert direction in (SearchDirection.FORWARD, SearchDirection.BACKWARD)

        ignore_case = to_filter(ignore_case)

        self.text = text
        self.direction = direction
        self.ignore_case = ignore_case

    def __repr__(self):
        return '%s(%r, direction=%r, ignore_case=%r)' % (
            self.__class__.__name__, self.text, self.direction, self.ignore_case)

    def __invert__(self):
        """
        Create a new SearchState where backwards becomes forwards and the other
        way around.
        """
        if self.direction == SearchDirection.BACKWARD:
            direction = SearchDirection.FORWARD
        else:
            direction = SearchDirection.BACKWARD

        return SearchState(text=self.text, direction=direction, ignore_case=self.ignore_case)


def start_search(buffer_control=None, direction=SearchDirection.FORWARD):
    """
    Start search through the given `buffer_control` using the
    `search_buffer_control`.

    :param buffer_control: Start search for this `BufferControl`. If not given,
        search through the current control.
    """
    from ..layout.controls import BufferControl
    assert buffer_control is None or isinstance(buffer_control, BufferControl)
    assert direction in SearchDirection._ALL

    layout = get_app().layout

    # When no control is given, use the current control if that's a BufferControl.
    if buffer_control is None:
        if not isinstance(layout.current_control, BufferControl):
            return
        buffer_control = layout.current_control

    # Only if this control is searchable.
    search_buffer_control = buffer_control.search_buffer_control

    if search_buffer_control:
        buffer_control.search_state.direction = direction

        # Make sure to focus the search BufferControl
        layout.focus(search_buffer_control)

        # Remember search link.
        layout.search_links[search_buffer_control] = buffer_control

        # If we're in Vi mode, make sure to go into insert mode.
        get_app().vi_state.input_mode = InputMode.INSERT


def stop_search(buffer_control=None):
    """
    Stop search through the given `buffer_control`.
    """
    from ..layout.controls import BufferControl
    assert buffer_control is None or isinstance(buffer_control, BufferControl)

    layout = get_app().layout

    if buffer_control is None:
        buffer_control = layout.search_target_buffer_control
        search_buffer_control = buffer_control.search_buffer_control
    else:
        assert buffer_control in layout.search_links.values()
        search_buffer_control = _get_reverse_search_links(layout)[buffer_control]

    # Focus the original buffer again.
    layout.focus(buffer_control)

    # Remove the search link.
    del layout.search_links[search_buffer_control]

    # Reset content of search control.
    search_buffer_control.buffer.reset()

    # If we're in Vi mode, go back to navigation mode.
    get_app().vi_state.input_mode = InputMode.NAVIGATION


def do_incremental_search(direction, count=1):
    """
    Apply search, but keep search buffer focused.
    """
    assert is_searching()
    assert direction in SearchDirection._ALL

    layout = get_app().layout

    search_control = layout.current_control
    prev_control = layout.search_target_buffer_control
    search_state = prev_control.search_state

    # Update search_state.
    direction_changed = search_state.direction != direction

    search_state.text = search_control.buffer.text
    search_state.direction = direction

    # Apply search to current buffer.
    if not direction_changed:
        prev_control.buffer.apply_search(
            search_state, include_current_position=False, count=count)


def accept_search():
    """
    Accept current search query. Focus original `BufferControl` again.
    """
    layout = get_app().layout

    search_control = layout.current_control
    target_buffer_control = layout.search_target_buffer_control
    search_state = target_buffer_control.search_state

    # Update search state.
    if search_control.buffer.text:
        search_state.text = search_control.buffer.text

    # Apply search.
    target_buffer_control.buffer.apply_search(search_state, include_current_position=True)

    # Add query to history of search line.
    search_control.buffer.append_to_history()

    # Stop search and focus previous control again.
    stop_search(target_buffer_control)


def _get_reverse_search_links(layout):
    """
    Return mapping from BufferControl to SearchBufferControl.
    """
    return dict((buffer_control, search_buffer_control)
            for search_buffer_control, buffer_control in layout.search_links.items())
