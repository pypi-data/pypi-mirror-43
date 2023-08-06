"""Module for containers widgets."""

from tkinter import ttk
from tkinter import Canvas as Tk_Canvas
from tkinter import Menu as Tk_Menu


from opentea.gui_forms.constants import (
    WIDTH_UNIT,
    BG_COLOR,
    GetException,
    SetException,
    SwitchForm,
    create_scrollable_canvas)
from opentea.gui_forms.wincanvas import redirect_canvas_items

from opentea.gui_forms.leaf_widgets import (OTInteger,
                                            OTNumber,
                                            OTEmpty,
                                            OTList,
                                            OTChoice,
                                            OTBoolean,
                                            OTFileBrowser,
                                            OTString,
                                            OTDocu,
                                            OTDescription)


def redirect_widgets(schema, root_frame, name):
    """Redirect to widgets.

    The schema attributes trigger which widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element

    Outputs :
    --------
    none
    """
    out = OTEmpty(schema, root_frame, name)
    if "properties" in schema:
        out = OTContainerWidget(schema, root_frame, name)
    elif "oneOf"in schema:
        out = OTXorWidget(schema, root_frame, name)
    elif "enum" in schema:
        out = OTChoice(schema, root_frame, name)
    elif "type" in schema:
        if schema["type"] == "array":
            if "properties" in schema["items"]:
                out = OTMultipleWidget(schema, root_frame, name)
            else:
                out = OTList(schema, root_frame, name)
        elif schema['type'] == 'integer':
            out = OTInteger(schema, root_frame, name)
        elif schema['type'] == 'number':
            out = OTNumber(schema, root_frame, name)
        elif schema['type'] == 'boolean':
            out = OTBoolean(schema, root_frame, name)
        elif schema["type"] == "string":
            out = redirect_string(schema, root_frame, name)
    return out

def redirect_string(schema, root_frame, name):
    """Redirect to string widgets.

    The schema attributes trigger which string widget will be in use.

    Inputs :
    --------
    schema :  a schema object
    root_frame :  a Tk object were the widget will be grafted
    name : name of the element

    Outputs :
    --------
    none
    """
    out = OTString(schema, root_frame, name)
    if "ot_type" in schema:
        if schema["ot_type"] == "desc":
            out = OTDescription(schema, root_frame, name)
        elif schema["ot_type"] == "docu":
            out = OTDocu(schema, root_frame, name)
        elif schema["ot_type"] == "file":
            out = OTFileBrowser(schema, root_frame, name)
        elif schema["ot_type"] == "canvas_item":
            #out = redirect_canvas_items(schema, root_frame, name)
            out = OTEmpty(schema, root_frame, name)
        elif schema["ot_type"] == "view3d":
            ### To be implemented
            out = OTEmpty(schema, root_frame, name)
        elif schema["ot_type"] == "selection":
            ### To be implemented
            out = OTEmpty(schema, root_frame, name)
    return out

class OTNodeWidget():
    """Factory for OpenTea Widgets Containers."""

    def __init__(self, schema):
        """Startup class."""
        self.tree = dict()
        self.properties = schema["properties"]

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = {}
        for child in self.properties:
            try:
                found = self.tree[child].get()
                if found is not None:
                    out[child] = found
            except GetException:
                pass
        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens"""
        for child in self.properties:
            if child in dict_:
                try:
                    self.tree[child].set(dict_[child])
                except SetException:
                    pass

    def get_status(self):
        status = 1
        for child in self.properties:
            status = min(
                status,
                self.tree[child].get_status())
        return status


class OTContainerWidget(OTNodeWidget):
    """OT container widget."""

    def __init__(self, schema, root_frame, name, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        n_width : float
             relative size of the widget

        """
        super().__init__(schema)
        title = "#" + name
        if "title" in schema:
            title = schema["title"]
        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=name,
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)
        """Forcing the widget size"""
        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)
        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)
        self._forceps = ttk.Frame(self._holder,
                                  width=WIDTH_UNIT,
                                  height=1)
        self._forceps.pack(side="top")
        # CHILDREN
        for name_child in self.properties:
            schm_child = self.properties[name_child]
            self.tree[name_child] = redirect_widgets(schm_child,
                                                     self._holder,
                                                     name_child)


class OTTabWidget(OTNodeWidget):
    """OT Tab widget container.

    Called for the 1st layer of nodes in the global schema
    """

    def __init__(self, schema, root, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root :  the parent
        name: string naming the widget
        """
        super().__init__(schema)
        self.root = root
        self.icon = None
        title = "#" + name
        if "title" in schema:
            title = schema["title"]

        self._tab = ttk.Frame(self.root.toptabs.nb, name=name)
        self.root.toptabs.nb.add(self._tab, text=title)

        self.tabid = self.root.toptabs.nb.index("end")-1

        # SCROLL FORM
      
        self.scan = create_scrollable_canvas(self._tab)
        self._out_frame = ttk.Frame(self.scan)
        self.scan.create_window((0, 0),
                                       window=self._out_frame,
                                       anchor='nw')

        # FOOTER
        _footer_f = ttk.Frame(self._tab)
        _footer_f.pack(side="top", fill="both", padx=2, pady=3)

        # button_var = StringVar(value="dummy info")
        _button_lb = ttk.Label(_footer_f, text="button_var")

        self.process = None
        if "process" in schema:
            self.process = schema["process"]
        _button_bt = ttk.Button(_footer_f,
                                text="Process",
                                command=self.process_button)

        _button_bt.pack(side="right", padx=2, pady=2)
        _button_lb.pack(side="right", padx=2, pady=2)

        # CHILDREN
        for name_ in schema["properties"]:
            self.tree[name_] = redirect_widgets(schema["properties"][name_],
                                                self._out_frame,
                                                name_)

        self._out_frame.bind("<Configure>",
                             self._update_canvas_bbox_from_inside)

        self.root.toptabs.nb.bind_all('<<mem_check>>', self.on_memory_check, add="+")
        self.root.toptabs.nb.bind_all('<<mem_change>>', self.on_memory_change, add="+")
        self.update_tab_icon('unknown')

    def update_tab_icon(self, icon_name):
        """Update the Tab icon upon status"""
        if self.icon != icon_name:
            self.root.toptabs.nb.tab(self.tabid,
                                   image=self.root.icons[icon_name],
                                   compound='left')
            self.icon = icon_name

    def on_memory_change(self, event):
        """Check if the sender is child of this tab.process

        set to unknown if so"""

        found_parent_tab = False
        parent = event.widget
        while not found_parent_tab:
            parent = parent.master
            if parent is None:
                break

            parent_name = parent.winfo_name()
            if parent_name == 'tk':
                break
            if parent_name == self._tab.winfo_name():
                if isinstance(parent, type(self._tab)):
                    found_parent_tab = True
            
        if found_parent_tab:
            pass
            self.update_tab_icon('unknown')

    def on_memory_check(self, event):
        """Update content upon status of children."""
        state = self.get_status()
        state_icon = 'unknown'
        if state == 1:
            state_icon = 'valid'
        elif state == -1:
            state_icon = 'invalid'

        self.update_tab_icon(state_icon)

    def process_button(self):
        """Action to take without additionnal process"""
        if self.process is None:
            print("No additionnal process pending on this tab...")
        else:
            self.root.execute(self.process)
        self.root.toptabs.nb.event_generate('<<mem_check>>')

    def _update_canvas_bbox_from_inside(self, event=None):
        """Smart grid upon widget size.

        Regrid the object according to the width of the window
        """
        self.scan.configure(scrollregion=self.scan.bbox("all"))
        ncols = max(int(self.root.toptabs.nb.winfo_width()/WIDTH_UNIT + 0.5), 1)
        height = 0
        for children in self._out_frame.winfo_children():
            height += children.winfo_height()
        limit_depth = height / ncols
        max_depth = 0
        x_pos = 10 + 0*WIDTH_UNIT
        y_pos = 10
        for children in self._out_frame.winfo_children():
            children.place(x=x_pos,
                           y=y_pos,
                           anchor="nw")
            y_pos += children.winfo_height() + 2

            if y_pos > limit_depth and ncols > 1:
                max_depth = y_pos
                x_pos += WIDTH_UNIT + 20
                y_pos = 10
            else:
                max_depth = height
        self._out_frame.configure(height=max_depth+40,
                                  width=ncols*(WIDTH_UNIT+20)+20)


class OTMultipleWidget():
    """OT multiple widget."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        """
        self.tree = list()
        self.status = 1
        self.item_schema = schema["items"]
        title = "#" + name
        if "title" in schema:
            title = schema["title"]
        holder = ttk.LabelFrame(
            root_frame,
            text=title,
            name=name,
            relief="sunken",
            width=2*WIDTH_UNIT)

        holder.pack(side="top", fill="x", padx=2, pady=2, expand=False)
        forceps = ttk.Frame(holder, width=2*WIDTH_UNIT, height=1)
        self.tvw = ttk.Treeview(
            holder,
            selectmode="browse",
            height=15)
        scroll_vert = ttk.Scrollbar(
            holder,
            orient="vertical",
            command=self.tvw.yview)
        self.tvw.configure(yscrollcommand=scroll_vert.set)
        self.switchform = SwitchForm(
            holder,
            width=WIDTH_UNIT,
            name='tab_holder')
        forceps.grid(column=0, row=1, columnspan=3)
        scroll_vert.grid(column=1, row=1, sticky="news")
        self.tvw.grid(column=0, row=1, sticky="news")
        self.switchform.grid(column=2, row=1, rowspan=2, sticky="news")
        self.switchform.grid_propagate(0)
        item_props = self.item_schema["properties"]
        self.tvw["columns"] = tuple(item_props.keys())
        col_width = int(WIDTH_UNIT/(len(self.tvw["columns"])+1))
        self.tvw.column("#0", width=col_width)
        self.title_to_key = dict()
        for key in item_props:
            title = key
            if "title" in item_props[key]:
                title = item_props[key]["title"]
            self.tvw.column(key, width=col_width)
            self.tvw.heading(key, text=title)
            self.title_to_key[title] = key

        def tv_simple_click(event):
            """Handle a simple click on treeview."""
            # col = self.tvw.identify_column(event.x)
            row = self.tvw.identify_row(event.y)
            self.switchform.sf_raise(row)

        self.tvw.bind("<Button-1>", tv_simple_click)
        self.refresh_view()
        self.tvw.bind_all('<<mem_change>>', self.refresh_view, add='+')

    def refresh_view(self, event=None):
        """
            Referesh items values on tree view
        """
        headings = [self.tvw.heading(i)['text']
                    for i, _ in enumerate(self.title_to_key, 0)]

        for item in self.tree:
            uid = item.tree['name'].get()
            values = [None]*len(self.title_to_key)
            for title in self.title_to_key:
                key = self.title_to_key[title]
                value = item.tree[key].get()
                if isinstance(value, dict):
                    value = next(iter(value))
                values[headings.index(title)] = str(value)
            self.tvw.item(uid, values=values)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = list()
        for child in self.tree:
            try:
                found = child.get()
                if found is not None:
                    out.append(found)
            except GetException:
                pass
        if not out:
            out = None
        return out

    def set(self, list_):
        """Get the data of children widgets.

        Input :
        -------
        a list with the value of the childrens"""

        ingoing_childs = [item["name"] for item in list_]
        childs_to_add = ingoing_childs.copy()
        childs_to_del = []

        for item_id, item in enumerate(self.tree):
            item_name = item.get()['name']
            if item_name not in ingoing_childs:
                childs_to_del.append(item_name)
            else:
                data_in = list_[ingoing_childs.index(item_name)]
                self.tree[item_id].set(data_in)
                childs_to_add.remove(item_name)

        #print("Ingoing:", ingoing_childs)
        #print("childs_to_add:", childs_to_add)
        #print("childs_to_del", childs_to_del)

        for child_name in childs_to_del:
            self.del_item_by_name(child_name)

        for item_name in childs_to_add:
            data_in = list_[ingoing_childs.index(item_name)]
            multiple_item = OTMultipleItem(self, item_name)
            multiple_item.set(data_in)
            self.tree.insert(-1, multiple_item)

        self.tree = [self.tree[self.index_of_item(name)]
                     for name in ingoing_childs]


    def del_item_by_name(self, name):
        self.tvw.delete(name)
        del self.tree[self.index_of_item(name)]

    def index_of_item(self, name):
        index = None
        for item_id, item in enumerate(self.tree):
            item_name = item.get()['name']
            if item_name == name:
                index = item_id
        return index


    def get_status(self):
        status = 1
        for child in self.tree:
            status = min(
                status,
                child.get_status())
        return status


class OTMultipleItem(OTContainerWidget):
    """OT  multiple widget."""

    def __init__(self, multiple, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        multiple :  a Tk object were the widget will be grafted
        """
        self.tab = multiple.switchform.add(name, title=name)
        super().__init__(multiple.item_schema, self.tab, name)
        multiple.tvw.insert("", "end", iid=name, text=name)


class OTXorWidget():
    """OT  Or-exclusive / oneOf widget."""

    def __init__(self, schema, root_frame, name, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        name: string naming the widget
        n_width : float
             relative size of the widget
        """
        self.tree = dict()
        self.current_child = None
        self._schema = schema
        title = "#" + name
        if "title" in schema:
            title = schema["title"]

        self.current_child = self._schema["oneOf"][0]["required"][0]
        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=name,
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)

        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)
        self._menu_bt = ttk.Menubutton(self._holder,
                                       text="None")

        self._xor_holder = ttk.Frame(self._holder)

        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)
        self._forceps.pack(side="top")
        self._menu_bt.pack(side="top")
        self._xor_holder.pack(side="top", fill="x",
                              padx=2, pady=2, expand=False)

        self._menu_bt.menu = Tk_Menu(self._menu_bt, tearoff=False)
        self._menu_bt["menu"] = self._menu_bt.menu

        for oneof_item in self._schema["oneOf"]:
            nam = oneof_item["required"][0]
            ch_s = oneof_item["properties"][nam]
            title = nam
            if "title" in ch_s:
                title = ch_s["title"]
            self._menu_bt.menu.add_command(
                label=title,
                command=lambda nam=nam: self.xor_callback(nam))

        self.update_xor_content(self.current_child)

    def xor_callback(self, name_child):
        self.update_xor_content(name_child, data_in=None)
        self._menu_bt.event_generate('<<mem_change>>')

    def update_xor_content(self, name_child, data_in=None):
        """Reconfigure XOR button.

        Inputs :
        --------
        name_child : sting, naming the child object
        data_in : dictionary used to pre-fill the data
        """
        self.current_child = name_child
        child_schema = None
        for possible_childs in self._schema["oneOf"]:
            if possible_childs["required"][0] == name_child:
                child_schema = possible_childs["properties"][name_child]

        for child_widget in self._xor_holder.winfo_children():
            child_widget.destroy()

        self.tree = dict()
        self.tree[name_child] = OTContainerWidget(child_schema,
                                                  self._xor_holder,
                                                  name_child)
        if data_in is None:
            self.tree[name_child].set(dict())
        else:
            self.tree[name_child].set(data_in)

        title = name_child
        if "title" in child_schema:
            title = child_schema["title"]
        self._menu_bt.configure(text=title)


    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of current children
        """
        out = dict()
        #print(">>>", self.current_child)
        try:
            found = self.tree[self.current_child].get()
            if found is not None:
                out[self.current_child] = found
            else:
                out[self.current_child] = None
        except GetException:
            pass

        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens
        """
        given_keys = dict_.keys()
        if len(given_keys) > 1:
            raise SetException("Multiple matching option, skipping...")

        for one_of in self._schema["oneOf"]:
            child = next(iter(one_of['properties']))
            if child in dict_:
                try:
                    self.update_xor_content(child, dict_[child])
                except SetException:
                    pass

    def get_status(self):
        return self.tree[self.current_child].get_status()
