import sys
import traceback
import logging
import json
from collections import defaultdict

import six

from .._actor import Actor, Cmd, Cmds

from ... import flow as flow  # noqa


# -------------------------------- CMDS

class FlowCmds(Cmds):
    pass


@FlowCmds.cmd
class Resolve_Path(Cmd):
    '''
    Returns the oid of the object pointed by 'path'.
    Path may contain . and .., have several consecutive / etc...
    If a coresponding oid of an existing object is not found, None
    is returned
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        try:
            o = self.actor().get_object(self.oid)
        except flow.MissingChildError:
            return None
        return o.oid()


@FlowCmds.cmd
class Split_Oid(Cmd):
    '''
    Returns a 2D list of [label, oid] with all objects
    from up_to_oid to to oid.

    If up_to_oid is None, the oid root is used.

    If skip_maps is True, the oid of parent Map Object
    will be skiped and the label of their mapped_item will
    show the map name.

    '''

    def _decode(self, oid, skip_maps=True, up_to_oid=None):
        self.oid = oid
        self.skip_maps = skip_maps
        self.up_to_oid = up_to_oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        root = o.root()
        if self.up_to_oid is None:
            up_to = root
        else:
            up_to = self.actor().get_object(self.up_to_oid)

        splited = []
        while o not in (up_to, root):
            # skip only if not the first item:
            if splited and self.skip_maps and isinstance(o, flow.MAP_TYPES):
                    mapped_item_name = splited[-1][0]
                    splited[-1][0] = o.name() + ':' + mapped_item_name
            else:
                splited.append([o.name(), o.oid()])
            o = o._mng.parent

        splited.reverse()
        return splited


@FlowCmds.cmd
class LS(Cmd):
    '''
    Return two lists:
    - one with those info for each relations in the given oid:
        (relation_name, relation_type, is_action, is_map, ui_config)
    - one with the name of each mapped item in the given oid.

    The ui_config is a dict with keys like:
        editor
        editor_options
        group
        hidden
        enabled

    '''

    def _decode(self, under, show_hidden=True, show_protected=False):
        self.under_oid = under
        self.show_hidden = show_hidden
        self.show_protected = show_protected

    def _get_relation_infos(self, relation):
        if not self.show_protected and relation.name.startswith('_'):
            return None
        if not self.show_hidden and relation.is_hidden():
            return None

        is_action = False
        is_map = False

        if relation.related_type is not None:
            is_action = issubclass(relation.related_type, flow.Action)
            is_map = issubclass(relation.related_type, flow.MAP_TYPES)

        if is_action and not relation.related_type.SHOW_IN_PARENT_DETAILS:
            return None

        return (
            relation.name,
            relation.relation_type_name(),
            is_action,
            is_map,
            relation.get_ui(),
        )

    def _get_mapped_names(self, o):
        if not isinstance(o, flow.MAP_TYPES):
            return []
        return o.mapped_names()

    def _execute(self):
        actor = self.actor()
        o = actor.get_object(self.under_oid)

        related_info = [
            self._get_relation_infos(relation)
            for relation in o._mng.relations()
        ]
        related_info = [i for i in related_info if i is not None]
        mapped_names = self._get_mapped_names(o)
        return related_info, mapped_names


@FlowCmds.cmd
class Is_Map(Cmd):
    '''
    Returns True if the given oid is a Map
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return isinstance(o, flow.MAP_TYPES)

@FlowCmds.cmd
class Refs(Cmd):
    '''
    Returns True if the given oid is a Map
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o._mng.refs()


@FlowCmds.cmd
class Get_Mapped_Oids(Cmd):
    '''
    Returns a list of oids mapped in the given map_oid
    '''

    def _decode(self, map_oid, page_num=0, page_size=None):
        self.map_oid = map_oid
        self.page_num = page_num
        self.page_size = page_size

    def _execute(self):
        map = self.actor().get_object(self.map_oid)
        return [o.oid() for o in map.mapped_items(self.page_num, self.page_size)]


@FlowCmds.cmd
class Get_Mapped_Columns(Cmd):
    '''
    Returns the columns to show inline for the given map.
    '''

    def _decode(self, map_oid):
        self.map_oid = map_oid

    def _execute(self):
        try:
            map = self.actor().get_object(self.map_oid)
        except (flow.MissingChildError, flow.MissingRelationError):
            raise
        else:
            return map.columns()


@FlowCmds.cmd
class Get_Mapped_Rows(Cmd):
    '''
    Returns all the rows shown inline for the given map.
    '''

    def _decode(self, map_oid):
        self.map_oid = map_oid

    def _execute(self):
        try:
            map = self.actor().get_object(self.map_oid)
        except (flow.MissingChildError, flow.MissingRelationError):
            raise
        else:
            return map.rows()


@FlowCmds.cmd
class Get_Mapped_Row(Cmd):
    '''
    Returns the row shown inline for the oid in the given map.
    '''

    def _decode(self, map_oid, mapped_oid):
        self.map_oid = map_oid
        self.mapped_oid = mapped_oid

    def _execute(self):
        map = self.actor().get_object(self.map_oid)
        mapped = self.actor().get_object(self.mapped_oid)
        oid, row = map.row(mapped)
        # Should we check oid is the right one ? :/
        return row


@FlowCmds.cmd
class Exists(Cmd):
    '''
    Returns True if the given oid exists.
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        try:
            self.actor().get_object(self.oid)
        except (flow.MissingChildError, flow.MissingRelationError):
            return False
        else:
            return True


@FlowCmds.cmd
class Get_Value(Cmd):
    '''
    Returns the value of 'oid'
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.get()


@FlowCmds.cmd
class Get_Value_Choices(Cmd):
    '''
    Returns the choices of the ChoiceValue 'oid'
    '''

    def _decode(self, choice_oid):
        self.oid = choice_oid

    def _execute(self):
        choice_value = self.actor().get_object(self.oid)
        return choice_value.choices()


@FlowCmds.cmd
class Set_Value(Cmd):
    '''
    Change the value of 'oid' to 'value'
    '''

    def _decode(self, oid, value):
        self.oid = oid
        self.value = value

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.set(self.value)


@FlowCmds.cmd
class Get_Summary(Cmd):
    '''
    Returns the summary of 'oid'
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.summary()


@FlowCmds.cmd
class Get_Thumbnail_Info(Cmd):
    '''
    Returns a dict depicting the thumbnail to use for the given oid.
    A thumbnail may be:
        A sequence of image:
            is_sequence == True
            label   -> optional string label to display
            first   -> int first frame of the sequence
            last    -> int last frame of the sequence
            path    -> string path of the sequence with a formater for the frame:
                        /path/to/seq/seq_name.%04i.png
            default_height -> the optional default height of the image to show

        A single image:
            is_image == True
            label   -> optional string label to display
            path    -> string path of the image
            default_height -> the optional default height of the image to show

        A resource ref:
            is_resource == True
            folder  -> string name of the resource folder
            name    -> sting name of the resource file

    If the object does not have thumbnail representation, it defaults to the object's ICON.
    '''

    def _decode(self, oid):
        self.oid = oid

    def get_default(self, o):
        icon = o.__class__.ICON
        info = self.get_resource(icon)
        info['label'] = o.oid()
        return info

    def get_resource(self, icon):
        info = dict(is_resource=True)
        
        if not isinstance(icon, six.string_types):
            info['folder'], info['name'] = icon
        else:
            info['folder'] = 'icons.flow'
            info['name'] = icon
        
        return info

    def _execute(self):
        o = self.actor().get_object(self.oid)
        try:
            thumbnail = o.get_thumbnail_object()
        except AttributeError:
            return self.get_default(o)

        info = {}
    
        is_resource = thumbnail.is_resource()
        if is_resource:
            return self.get_resource(thumbnail.get_resource())
        else:        
            is_sequence = thumbnail.is_sequence()
            info['is_sequence'] = is_sequence
            info['is_image'] = not is_sequence

            info['label'] = thumbnail.get_label()
            info['path'] = thumbnail.get_path()
            info['default_height'] = thumbnail.get_default_height()

            info['first'], info['last'], info['fps'] = thumbnail.get_first_last_fps()

        return info

@FlowCmds.cmd
class Get_Parent_Oid(Cmd):

    def _decode(self, oid, skip_maps=True):
        self.oid = oid
        self.skip_maps = skip_maps

    def _execute(self):
        o = self.actor().get_object(self.oid)
        parent = o._mng.parent
        while self.skip_maps and isinstance(parent, flow.MAP_TYPES):
            parent = parent._mng.parent

        if parent:
            oid = parent.oid()
            if oid:
                return oid
                
        return self.actor().home_root().Home.oid()

@FlowCmds.cmd
class Get_Navigable_Oids(Cmd):
    '''
    Drop all the Flow projects so they can (should :p) be
    garbage collected.
    Next attemp to access a project will reload its sources
    before instanciatin it.
    '''

    def _decode(self, from_oid, full_oid):
        self._from_oid = from_oid
        self._full_oid = full_oid

    def _execute(self):
        # FIXME: this code from old kabarer should be cleaned.
        from_oid = self._from_oid
        full_oid = self._full_oid

        object = self.actor().get_object(from_oid)
        if object is None:
            return [from_oid]

        def allow_relation(r):
            return (
                # not r.name == object.name()
                not r.name.startswith('_')
                and r.related_type
                and not r.is_hidden()
                and not issubclass(r.related_type, flow.Action)
                and not issubclass(r.related_type, flow.values.Value)
            )

        # FIXME: this should be handled by the relations!
        def get_related_oid(p, n):
            return p + '/' + n

        # full oids with siblings:

        names = from_oid.split('/')
        full_names = full_oid.split('/')
        subs = '/'.join(full_names[len(names):])
        if subs:
            subs = '/' + subs

        parent = object._mng.parent

        parent_oid = parent.oid()
        if isinstance(parent, flow.MAP_TYPES):
            ret = [
                (
                    ''.join((n, subs)),
                    get_related_oid(parent_oid, n) + subs
                )
                for n in parent.mapped_names()
            ]
        else:
            relations = parent._relations
            ret = [
                (
                    ''.join((r.name, subs)),
                    get_related_oid(parent_oid, r.name) + subs
                )
                for r in relations
                if allow_relation(r)
            ]

        # children oids:
        ret.append(None)  # <--- interpreted by ui as a separator

        object_name = object.name()
        oid = object.oid()
        if isinstance(object, flow.MAP_TYPES):
            ret.extend(
                [(object_name + '/' + n, get_related_oid(oid, n))
                 for n in object.mapped_names()]
            )
        else:
            relations = object._relations
            ret.extend(
                (object_name + '/' + r.name, get_related_oid(oid, r.name))
                for r in relations
                if allow_relation(r)
            )

        return ret

@FlowCmds.cmd
class Get_Object_Actions(Cmd):
    '''
    Returns infos about the actions in the given oid.
    '''

    def _decode(self, oid):
        self.oid = oid

    @classmethod
    def get_actions(cls, o, rel_path, without_dialog_only):
        #print('GET ACTION FOR', o.oid())
        show_protected = False
        show_hidden = True

        action_infos = []
        for relation in o._mng.relations():
            if not show_protected and relation.name.startswith('_'):
                continue
            if not show_hidden and relation.is_hidden():
                continue
            relation_related_type = relation.related_type
            if relation.related_type is None:
                continue

            if issubclass(relation_related_type, flow.Action):
                if not rel_path and not relation_related_type.SHOW_IN_PARENT_INLINE:
                    continue

                if without_dialog_only:
                    action = getattr(o, relation.name)
                    if action.needs_dialog():
                        continue

                ui_config = relation.get_ui()
                group = ui_config.get('group')
                action_infos.append((
                    relation.index,
                    group,
                    rel_path + (relation.name,),
                    {
                        'action_icon': relation_related_type.ICON,
                        'ui': ui_config,
                        # FIXME: should be handled by the relation!
                        'oid': o.oid() + '/' + relation.name,
                        'path': rel_path,
                    }
                ))

            elif issubclass(relation_related_type, flow.values.Value):
                action_infos.extend(
                    cls.get_actions(
                        getattr(o, relation.name), rel_path + (relation.name,),
                        without_dialog_only=without_dialog_only
                    )
                )

        return action_infos

    def _execute(self):
        o = self.actor().get_object(self.oid)
        action_infos = self.get_actions(o, (), without_dialog_only=False)
        return action_infos


@FlowCmds.cmd
class Get_Objects_Actions(Cmd):
    '''
    Returns infos about the action commun to all oid in the given oid list.
    '''

    def _decode(self, oids):
        self.oids = oids

    def _execute(self):
        actor = self.actor()
        by_name = defaultdict(list)
        ordered_names = []
        for oid in self.oids:
            o = actor.get_object(oid)
            action_infos = Get_Object_Actions.get_actions(
                o, (), without_dialog_only=True
            )
            for i, g, n, d in action_infos:
                by_name[n].append((i, g, n, d))
                if n not in ordered_names:
                    ordered_names.append(n)

        nb_oids = len(self.oids)
        ret = []
        for name in ordered_names:
            action_infos_list = by_name[name]
            if len(action_infos_list) != nb_oids:
                continue
            action = action_infos_list[0]
            rel_path = '/'.join(action[2])
            action[-1]['oid'] = [oid + '/' + rel_path for oid in self.oids]
            ret.append(action)

        return ret


@FlowCmds.cmd
class Is_Action(Cmd):
    '''
    Returns true if the given oid is an action.
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        try:
            o = self.actor().get_object(self.oid)
        except (flow.MissingChildError, flow.MissingRelationError):
            raise
        else:
            return isinstance(o, flow.Action)


@FlowCmds.cmd
class Action_Needs_Dialog(Cmd):
    '''
    Returns True if the action 'oid' need to show a
    dialog in order to run (ie, it has several buttons).
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.needs_dialog()


@FlowCmds.cmd
class Get_Action_Buttons(Cmd):
    '''
    Returns the list of buttons for the action 'oid'.
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.get_buttons()


@FlowCmds.cmd
class Run_Action(Cmd):
    '''
    Runs the action 'oid' with button 'button'.
    '''

    def _decode(self, oid, button):
        self.oid = oid
        self.button = button

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.run(self.button)


@FlowCmds.cmd
class To_Mime_Data(Cmd):
    '''
    Returns dict {type: bytes} for all the given oids.
    '''

    def _decode(self, oids):
        self.oids = oids

    def _execute(self):
        ret = {}
        oids = '\r\n'.join(self.oids).encode('UTF-8')

        ret['text/plain'] = oids
        ret['application/json'] = json.dumps(self.oids).encode('UTF-8')

        ret['kabaret/flow_oids'] = oids
        ret['kabaret/flow_oid'] = self.oids[0].encode('UTF-8')

        return ret


@FlowCmds.cmd
class Can_Handle_Mime_Formats(Cmd):
    '''
    Returns True if at least one of the given mime formats are
    handled by the Flow.
    (i.e: is one of the ones decoded by From_Mime_Data())
    '''

    def _decode(self, mime_formats):
        self.mime_formats = mime_formats

    def _execute(self):
        #print(self.mime_formats, 'kabaret/flow_oids' in self.mime_formats)
        return (
            'kabaret/flow_oids' in self.mime_formats
            or
            'kabaret/flow_oid' in self.mime_formats
            or
            'text/uri-list' in self.mime_formats
        )


@FlowCmds.cmd
class From_Mime_Data(Cmd):
    '''
    Returns a list of oid and a list of urls found in the
    given {forma: bytes} dict.
    If the mime data does not contain oids, None is returned.
    '''

    def _decode(self, mime_data):
        self.mime_data = mime_data

    def _execute(self):
        try:
            data = self.mime_data['kabaret/flow_oids']
        except KeyError:
            try:
                data = self.mime_data['kabaret/flow_oid']
            except KeyError:
                oids = []
            else:
                oids = [data.decode('UTF-8')]
        else:
            oids = data.decode('UTF-8').split()

        try:
            data = self.mime_data['text/uri-list']
        except KeyError:
            urls = []
        else:
            urls = data.decode('UTF-8').split()

        return oids, urls


@FlowCmds.cmd
class Get_Connection_Targets(Cmd):
    '''
    Returns a list of (oid, label, icon) for each relation of the given oid
    accepting to connect the given source_oids and/or urls.

    The returned oids are either ConnectAction of Ref.
    Each one is suitable for a Connect cmd with the given oid.
    '''

    # FIXME: the returned list should contain the ui_config from the relation !

    def _decode(self, oid, source_oids, source_urls):
        self.oid = oid
        self.source_oids = source_oids
        self.source_urls = source_urls

    def _execute(self):
        actor = self.actor()
        target = actor.get_object(self.oid)
        source_objects = [actor.get_object(oid) for oid in self.source_oids]

        ret = []

        if len(source_objects) == 1:
            if isinstance(target, flow.values.Ref):
                #print("TARGET IS REF !")
                so = source_objects[0]
                if target.can_set(so):
                    ret.append((
                        self.oid,
                        'Set %r as %s' % (so.oid(), target.name()),
                        'Ref'
                    ))

        for relation in target._mng.relations():
            if relation.related_type and issubclass(relation.related_type, flow.ConnectAction):
                #print(relation.name + "  connect action !")
                caction = getattr(target, relation.name)
                label = caction.accept_label(
                    objects=source_objects, urls=self.source_urls
                )
                #print(relation.name + "  label:", label)
                if label is not None:
                    ret.append((
                        caction.oid(), label, caction.ICON
                    ))

        return ret


@FlowCmds.cmd
class Connect(Cmd):
    '''
    Connects the 'target_oid' to 'source_oids' and/or source_urls.

    If the target is a Ref, source_oids must contain only one oid
    and source_urls must be emptry. The Ref will be set with the
    provided oid.

    In the target is not a Ref, it is considered a ConnectAction
    and its run() method is called with the given source_oids and
    source_urls.

    '''
    def _decode(self, target_oid, source_oids, source_urls):
        self.target_oid = target_oid
        self.source_oids = source_oids
        self.source_urls = source_urls

    def _execute(self):
        actor = self.actor()
        target = actor.get_object(self.target_oid)

        if isinstance(target, flow.values.Ref):
            if len(self.source_oids) != 1:
                raise ValueError(
                    'Cannot connect more/less than one object to a Ref (got %r)' % (
                        self.source_oids
                    )
                )
            source = actor.get_object(self.source_oids[0])
            target.set(source)

        else:
            sources = [
                actor.get_object(oid)
                for oid in self.source_oids
            ]
            target.run(sources, self.source_urls)


@FlowCmds.cmd
class Get_Source_Display(Cmd):
    '''
    Returns a prettiest label than an oid.
    '''

    def _decode(self, oid):
        self.oid = oid

    def _execute(self):
        o = self.actor().get_object(self.oid)
        return o.get_source_display(self.oid)


@FlowCmds.cmd
class Get_Connection(Cmd):
    '''
    Returns the oid of the connection source, a nice display string, and an icon name.
    '''

    def _decode(self, connection_oid):
        self.connection_oid = connection_oid

    def _execute(self):
        ref = self.actor().get_object(self.connection_oid)
        source = ref.get()
        if source is None:
            return None, None, None
        source_oid = source.oid()
        return source_oid, source.get_source_display(source_oid), source.ICON


@FlowCmds.cmd
class Call(Cmd):
    '''
    Calls a method or lists methods of an Object.
    (Use '?' as method_name to receive the list or method names)
    '''

    def _decode(self, oid, method_name, args, kwargs):
        self.oid = oid
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    def _execute(self):
        object = self.actor().get_object(self.oid)

        if self.method_name == '?':
            # return a list of callable methods
            ret = []
            import inspect
            for n in dir(object):
                if n.startswith('__'):
                    continue
                o = getattr(object, n)
                if inspect.ismethod(o):
                    ret.append((n, inspect.getargspec(o)))
            return ret
        else:
            method = getattr(object, self.method_name)

            # json tend to use unicode for dict keys, but unicodes can't be
            # used as keyword names so:
            kw = dict([(str(k), v) for k, v in self.kwargs.items()])
            result = method(*self.args, **kw)

        return result


@FlowCmds.cmd
class Flush_Projects(Cmd):
    '''
    Drop all the Flow projects so they can (should :p) be
    garbage collected.
    Next attemp to access a project will reload its sources
    before instanciatin it.
    '''

    def _decode(self):
        pass

    def _execute(self):
        self.actor().flush_projects()


@FlowCmds.cmd
class Exec_Script(Cmd):

    def _decode(self, oid, script, globals_dict):
        self._oid = oid
        self._script = script
        self._globals_dict = globals_dict

    def _execute(self):
        my_object = self.actor().get_object(self._oid)
        if my_object is None:
            raise ValueError('Could not find object %r'%(self._oid,))

        globals_dict = self._globals_dict.copy()
        globals_dict['self'] = my_object

        is_statement = False
        try:
            code = compile(self._script, '<string>', 'eval')
        except SyntaxError:
            is_statement = True
            code = compile(self._script, '<string>', 'exec')

        try:
            if not is_statement:
                self.actor().log('-> EVAL:')
                result = eval(code, globals_dict)

            else:
                self.actor().log('-> EXEC:')
                exec(code, globals_dict)

        except Exception as e:
            """Provide context (line number and text) for an error that is caught.
            Ordinarily, syntax and Indent errors are caught during initial
            compilation in exec(), and the traceback traces back to this file.
            So these need to be treated separately.
            Other errors trace back to the file/script being run.
            """
            type_, value_, traceback_ = sys.exc_info()
            if type_ == SyntaxError:
                errorMessage = "%s\n%s" % (value_.text.rstrip(), " " * (value_.offset - 1) + "^")
                # rstrip to remove trailing \n, output needs to be fixed width font for the ^ to align correctly
                errorText = "Syntax Error on line %s" % value_.lineno
            elif type_ == IndentationError:
                # (no offset is provided for an IndentationError
                errorMessage = value_.text.rstrip()
                errorText = "Unexpected Indent on line %s" % value_.lineno
            else:
                errorText = traceback.format_exception_only(type_, value_)[0]
                format_string = "In file: {0}\nIn function: {2} at line: {1}. Line with error:\n{3}"
                tbList = traceback.extract_tb(traceback_)
                tb = tbList[-1]
                errorMessage = format_string.format(*tb)
            m = "\n**********************\n%s\n%s\n**********************" % (errorText, errorMessage)
            self.actor().log(m)

        else:
            if not is_statement:
                self.actor().log('>>> %r'%(result,))

        finally:
            try:
                globals_dict.pop('self')
            except KeyError:
                pass
            return globals_dict

# -------------------------------- FLOW OBJECTS


class RedisValueStore(flow.AbstractValueStore):

    def __init__(self, redis_db, cluster_name, project_name):
        super(RedisValueStore, self).__init__()
        self._db = redis_db
        self._cluster_name = cluster_name
        self._project_name = project_name
        self._namespace = ':'.join((
            self._cluster_name, 'Flow', self._project_name
        ))

    # def save_to(self, filename):
    #     with open(filename, 'w') as fh:
    #         fh.write('DATA = '+pprint.pformat(self.store))
    #     print('MemoryValueStore saved to', filename)

    # def load(self, filename):
    #     namespace = {}
    #     execfile(filename, namespace, namespace)
    #     data = namespace['DATA']
    #     self.store = data
    #     print('MemoryValueStore Loaded', filename)

    # def pprint(self):
    #     return pprint.pprint(self.store)

    def _key(self, key):
        return '%s:%s' % (self._namespace, key)

    def _d(self, value):
        return json.dumps(value)

    def _l(self, string):
        try:
            return json.loads(string)
        except ValueError as err:
            raise KeyError(str(err))

    def get(self, key):
        return self._l(self._db[self._key(key)])

    def set(self, key, value):
        self._db[self._key(key)] = self._d(value)

    def delete(self, key):
        try:
            del self._db[self._key(key)]
        except KeyError:
            return

    # deprecated, one must use hash
    # def update(self, key, **new_values):
    #     try:
    #         self._db[self._key(key)]
    #     except KeyError:
    #         self.set(new_values)
    #     else:
    #         self._db.hmset(self._key(key), new_values)

    def incr(self, key, by):
        self._db.incr(self._key(key), by)

    def decr(self, key, by):
        self.incr(key, -by)

    #--- Ordererd Sting Set

    def oss_get(self, key):
        return self.oss_get_range(key, 0, -1)

    def oss_get_range(self, key, first, last):
        return self._db.zrange(self._key(key), first, last)

    def oss_has(self, key, member):
        return self._db.zscore(self._key(key), member) is not None

    def oss_add(self, key, member, score):
        self.oss_set_score(key, member, score)

    def oss_remove(self, key, member):
        return self._db.zrem(self._key(key), member)

    def oss_len(self, key):
        return self._db.zcard(self._key(key))

    def oss_get_score(self, key, member):
        return self._db.zscore(self._key(key))

    def oss_set_score(self, key, member, score):
        self._db.zadd(self._key(key), **{member: score})

    #--- HASH

    def hash_get_key(self, key, hash_key):
        # hget
        return self._l(self._db.hget(self._key(key), hash_key))

    def hash_has_key(self, key, hash_key):
        # hexists
        return self._db.hexists(self._key(key), hash_key)
        # try:
        #     return hash_key in self.store[key]
        # except:
        #     return False

    def del_hash_key(self, key, hash_key):
        # hdel
        self._db.hdel(self._key(key), hash_key)

    def get_hash(self, key):
        # not the same as get_hash_as_dict bc it keep order
        keys = self.get_hash_keys(key)
        return [
            (k, self.hash_get_key(key, k))
            for k in keys
        ]

    def get_hash_as_dict(self, key):
        # hgetall
        d = self._db.hgetall(self._key(key))
        d = dict([
            (k, self._l(v))
            for k, v in six.iteritems(d)

        ])
        return d

    def get_hash_keys(self, key):
        # hkeys
        return self._db.hkeys(self._key(key))
        # try:
        #     return self.store[key].keys()
        # except:
        #     return []

    def get_hash_len(self, key):
        # hlen
        return self._db.hlen(self._key(key))
        # try:
        #     return len(self.store[key])
        # except KeyError:
        #     return 0

    def update_hash(self, key, mapping):
        # hmset
        mapping = [
            (k, self._d(v))
            for k, v in six.iteritems(mapping)
        ]
        self._db.hmset(self._key(key), mapping)

    def set_hash(self, key, mapping):
        k = self._key(key)
        self._db.delete(k)
        if mapping:
            # mapping can be a 2d list or a dict:
            if isinstance(mapping, dict):
                mapping = mapping.items()
            mapping = [
                (mk, self._d(v))
                for mk, v in mapping            ]
            # looks like redis dont want to set {} as mapping...
            self._db.hmset(k, mapping)

    def set_hash_key(self, key, hash_key, value):
        # hset
        return self._db.hset(
            self._key(key), hash_key, self._d(value)
        )


class ProjectRoot(flow.Root):
    '''
    The ProjectRoot hold a single project and is stored in the Actor.
    It is used by the actor to find object with a given oid, and
    inside the project's flow to access the project from it children.
    '''

    def _set_session(self, session):
        self._session = session

    def session(self):
        return self._session

    def _set_project(self, project):
        self._project = project
        # # We need this in order to have ref's source_oid working when specified as absolute:
        # setattr(self, project.name(), project)

    def get_mapped(self, name):
        '''
        This is needed to have Ref's working with source_oid specified as absolute
        '''
        if name == self._project.name():
            return self._project

    def project(self):
        return self._project

    def get_object(self, oid):
        if oid.startswith('/'):
            oid = oid[1:]

        project_name = self._project.name()
        if oid == project_name:
            return self._project
        this_project_name, path = oid.split('/', 1)
        if this_project_name != project_name:
            raise ValueError(
                'The oid %r in not under project %r' % (
                    oid, self._project.oid()
                )
            )

        return self._project._mng.get_object(path)


# ------- HOME FLOW

class CreateProjectAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    _projects = flow.Parent()
    project_name = flow.Param('MyProject')
    project_type = flow.Param('dev_studio.flow.demo_project.DemoProject')

    def get_buttons(self):
        return ['Test Type', 'Create Project']

    def run(self, button):
        flow_actor = self.root().flow_actor

        if button == 'Test Type':
            try:
                TYPE = import_object(self.project_type.get())
            except Exception as err:
                self.message.set(
                    '<font color=red>Error:</font><br>%s' % (err,)
                )
            else:
                self.message.set('Project Type looks good:\n%s'%(TYPE,))
            return self.get_result(close=False)

        else:
            flow_actor.create_project(
                self.project_name.get(),
                self.project_type.get()
            )
            self._projects.touch()
            return self.get_result()

class ProjectStatusChoiceValue(flow.values.ChoiceValue):

    CHOICES = ('NYS', 'WIP', 'DONE', 'Archived')

class SetProjectStatusAction(flow.Action):

    ICON = 'input'

    _home = flow.Parent()

    project_name = flow.Param('')
    status = flow.Param('WIP', ProjectStatusChoiceValue)

    def get_buttons(self):
        return ['Test Project Name', 'Set Status']

    def run(self, button):
        actor = self.root().flow_actor
        project_name = self.project_name.get().strip()

        if button == 'Test Project Name':
            ok = actor.has_project(project_name)
            if ok:
                self.message.set('Project %r found' % (project_name,))
            else:
                self.message.set(
                    '<font color=red>Project %r not found !</font>' % (
                        project_name,
                    )
                )
            return self.get_result(close=False)

        actor.set_project_status(project_name, self.status.get())
        self._home.touch()


class ToggleArchivedProjectsAction(flow.Action):

    _home = flow.Parent()

    def needs_dialog(self):
        return False

    def get_buttons(self):
        return []

    def run(self, button):
        self._home.do_toggle_archived_projects()


class ToggleProjectsTypeAction(flow.Action):

    _home = flow.Parent()

    def needs_dialog(self):
        return False

    def get_buttons(self):
        return []

    def run(self, button):
        self._home.do_toggle_projects_type()


class ProjectsMap(flow.Map):

    ICON = 'asset_family'

    toggle_archived_projects = flow.Child(ToggleArchivedProjectsAction)
    toggle_project_type = flow.Child(ToggleProjectsTypeAction)

    create_project = flow.Child(CreateProjectAction).ui(group='Admin')
    set_project_status = flow.Child(SetProjectStatusAction).ui(group='Admin')

    def __init__(self, *args, **kwargs):
        super(ProjectsMap, self).__init__(*args, **kwargs)
        self._show_archived = False
        self._show_project_type = False

    def do_toggle_archived_projects(self):
        self._show_archived = not self._show_archived
        self.touch()

    def do_toggle_projects_type(self):
        self._show_project_type = not self._show_project_type
        self.touch()

    def columns(self):
        cols = ['Name', 'Status']
        if self._show_project_type:
            cols.append('Type')
        return cols

    def rows(self):
        rows = []
        projects_info = self.root().flow_actor.get_projects_info()
        for name, infos in projects_info:
            type_name = infos['type']
            status = infos['status']
            if not self._show_archived and status == 'Archived':
                continue
            style = dict(
                icon=('icons.gui', 'team'),
                Status_icon=('icons.status', status),
            )
            rows.append((
                '/' + name,
                dict(
                    Name=name,
                    Status=status,
                    Type=type_name,
                    _style=style,
                )
            ))
        return rows


class Home(flow.SessionObject):

    projects = flow.Child(ProjectsMap).ui(auto_fit=False, columns_width=(50, 20))

class HomeRoot(flow.Root):

    def set_flow_actor(self, flow_actor):
        self.flow_actor = flow_actor

    Home = flow.Child(Home)


# -------------------------------- ACTOR

class ProjectRegistryValueStore(RedisValueStore):

    def __init__(self, redis_db, cluster_name):
        super(RedisValueStore, self).__init__()
        self._db = redis_db
        self._cluster_name = cluster_name
        self._namespace = ':'.join((
            self._cluster_name, 'FlowConfig'
        ))


def import_object(
    object_qualified_name, reload_modules=True, clear_linecache=True
):
    # print('#------#')
    # print('#------# IMPORT OJECT', object_qualified_name)
    # print('#------#')
    if reload_modules:
        module_name = object_qualified_name.split('.', 1)[0]
        if 'KABARET' in module_name.upper():
            logging.getLogger('kabaret.flow').info('\n'.join((
                '[WARNING] CANNOT IMPORT PROJECT TYPE FROM KABARET'
                ' WITH reload_modules OPTION!'
            )))
        else:
            # print('#-----# reload modules', reload_modules, '->', module_name)
            for k in sorted(sys.modules.keys()):
                if k.startswith(module_name):
                    # print('[-]', k)
                    del sys.modules[k]
                else:
                    # print('[ ]', k)
                    pass

    if clear_linecache:
        # this is needed because of a bug in inspect which does not do
        # linecache.checkcache() in getsource()
        # fixed in py3k (I think)
        # It could be skipped for release... I guess. but needed for now
        # to have the flow run the reloaded code in client actions.
        import linecache
        linecache.clearcache()

    return _tornado_import_object(object_qualified_name)


def _tornado_import_object(name):
    '''code from tornado.util.import_object'''
    # py2 avoid unicodes:
    name = str(name)

    if name.count('.') == 0:
        return __import__(name, None, None)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])


class Flow(Actor):

    def __init__(self, session):
        super(Flow, self).__init__(session)
        self._home_root = None  # This is the root for the "Home" flow.

        self.touch_unsubscribe = None

        self._project_list_value_store = None
        self.project_roots = {}

    def _create_cmds(self):
        return FlowCmds(self)

    def on_session_connected(self):
        self.log('Configurint Project Registry')
        cluster = self.session().get_actor('Cluster')
        db = cluster.get_db()
        cluster_name = cluster.get_cluster_name()
        self._project_list_value_store = ProjectRegistryValueStore(
            db, cluster_name
        )

        self.log('Subcribing to flow_touched messages.')
        self.touch_unsubscribe = self.session().channels_subscribe(
            flow_touched=self._on_touch_message
        )

    def die(self):
        if self.touch_unsubscribe is not None:
            self.touch_unsubscribe()

    def _on_touch_message(self, message):
        oid = message['data']
        self.session().dispatch_event('flow_touched', oid=oid)

    def _on_object_touched(self, object):
        self.session().publish(flow_touched=object.oid())

    def home_root(self):
        if self._home_root is not None:
            return self._home_root

        value_store = self.create_home_value_store()
        self._home_root = HomeRoot(value_store)
        self._home_root.add_object_touched_handler(self._on_object_touched)
        self._home_root.set_flow_actor(self)

        return self._home_root

    def get_projects_info(self):
        project_types = self._project_list_value_store.get_hash_as_dict(
            'ProjectsType'
        )
        project_statuses = self._project_list_value_store.get_hash_as_dict(
            'ProjectsStatus'
        )
        ret = []
        for project_name in sorted(project_types):
            ret.append((
                project_name,
                dict(
                    type=project_types[project_name],
                    status=project_statuses[project_name]
                )
            ))
        return ret

    def has_project(self, project_name):
        return self._project_list_value_store.hash_has_key(
            'ProjectsType', project_name
        )

    def create_project(self, project_name, qualified_type_name):
        if self.has_project(project_name):
            raise ValueError('A Project %r already exists'%(project_name,))

        self._project_list_value_store.set_hash_key(
            'ProjectsType', project_name, qualified_type_name
        )
        self._project_list_value_store.set_hash_key(
            'ProjectsStatus', project_name, 'NYS'
        )

    def get_project_qualified_type_name(self, project_name):
        return self._project_list_value_store.hash_get_key(
            'ProjectsType', project_name
        )

    def get_project_status(self, project_name):
        return self._project_list_value_store.hash_get_key(
            'ProjectsStatus', project_name
        )

    def set_project_status(self, project_name, status):
        return self._project_list_value_store.set_hash_key(
            'ProjectsStatus', project_name, status
        )

    def create_home_value_store(self):
        return self.create_project_value_store('_Home_')

    def create_project_value_store(self, project_name):
        cluster = self.session().get_actor('Cluster')
        db = cluster.get_db()
        cluster_name = cluster.get_cluster_name()
        return RedisValueStore(db, cluster_name, project_name)

    def flush_projects(self):
        self.project_roots.clear()

    def get_project_root(self, project_name):
        try:
            return self.project_roots[project_name]
        except Exception:
            pass
        project_type_name = self.get_project_qualified_type_name(project_name)
        try:
            ProjectType = import_object(project_type_name)
        except Exception as err:
            message = 'Could not create project %r: ' \
                'unable to load the project class %r: %s' % (
                    project_name,
                    project_type_name,
                    err
                )
            self._session.log_error(traceback.format_exc())
            self._session.log_error(
                message
            )
            raise Exception(
                message
            )

        value_store = self.create_project_value_store(project_name)
        root = ProjectRoot(value_store)
        project = ProjectType(root, project_name)
        root._set_project(project)
        root._set_session(self.session())
        root.add_object_touched_handler(self._on_object_touched)
        self.project_roots[project_name] = root

        return root

    def get_object(self, oid):
        home_oid = self.home_root().Home.oid()
        if oid in (None, home_oid):
            return self.home_root().Home

        if oid.startswith(home_oid + "/"):
            try:
                return self.home_root()._mng.get_object(oid)
            except (flow.MissingChildError, flow.MissingRelationError):
                raise

        project_name = oid.split('/', 2)[1]
        root = self.get_project_root(project_name)
        return root.get_object(oid)
