import streamlit as st


class STSidebarException(Exception):
    pass


class STSidebar:
    """
    Base class for sidebar widgets in Streamlit.
    """

    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "Meta") and hasattr(cls.Meta, "name"):
            STSidebar.registry[cls.Meta.name] = cls
        else:
            raise STSidebarException(
                "Sidebar app must define a Meta class with `name`."
            )

    def __init__(self):
        self._state = st.session_state

    @classmethod
    def run_sidebars(cls):
        for app_cls in cls.registry.values():
            app = app_cls()
            with st.sidebar:
                app.display()

    def display(self):
        try:
            output = self.render()

            if output and isinstance(output, dict):
                for key, val in output.items():
                    self._state[key] = val
        except Exception as e:
            st.sidebar.error(f"Sidebar '{self.Meta.name}' failed: {e}")
            raise e

    def render(self):
        raise NotImplementedError("Sidebar component must implement `render()`.")
