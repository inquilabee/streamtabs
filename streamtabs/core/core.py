import streamlit as st


class STAppException(Exception):
    pass


class STTab:
    """
    Base class for Streamlit pages/apps.
    """

    registry: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "Meta") and hasattr(cls.Meta, "name"):  # type: ignore
            if (
                cls.Meta.name not in STTab.registry  # type: ignore
                and cls not in STTab.registry.values()
            ):
                STTab.registry[cls.Meta.name] = cls  # type: ignore
            else:
                raise STAppException(
                    f"Duplicate app name or class name for {cls.Meta.name}"  # type: ignore
                )
        else:
            raise STAppException("App must define Meta class with `name` attribute.")

    def __init__(self, debug: bool = False):
        self._state = st.session_state
        self.debug = debug

    @property
    def st(self):
        return st

    @property
    def state(self):
        return self._state

    def set_state(self, key, value):
        self._state[key] = value

    def delete_states(self, keys: list[str], ignore_missing: bool = False):
        for key in keys:
            try:
                del self.state[key]
            except KeyError as e:
                if not ignore_missing:
                    raise STAppException(f"State key '{key}' does not exist.") from e

    def check_inputs(self):
        if missing := self.missing_inputs():
            raise STAppException(f"Missing inputs: {', '.join(missing)}")

    def check_outputs(self, output_dict):

        if not isinstance(output_dict, dict):
            raise STAppException(
                f"render() must return a dict, got {type(output_dict)}"
            )

        if missing := self.missing_outputs(output_dict):
            raise STAppException(f"Missing required outputs: {', '.join(missing)}")

    def missing_inputs(self):
        return [
            k for k in getattr(self.Meta, "required_inputs", []) if k not in self.state  # type: ignore
        ]

    def missing_outputs(self, output_dict):
        return [
            k for k in getattr(self.Meta, "required_outputs", []) if k not in output_dict  # type: ignore
        ]

    @staticmethod
    def bordered_text(text, color="#ccc"):
        if not text:
            return

        st.markdown(
            f"""
            <div style='
                border: 2px solid {color};
                padding: 10px;
                border-radius: 6px;
                margin-top: 12px;
                margin-bottom: 12px;
            '>
                {"<br>".join(" ".join(line.split()) for line in text.splitlines())}
            </div>
            """,
            unsafe_allow_html=True,
        )

    def display(self):
        self.bordered_text(self.render.__doc__.strip(), color="black")  # type: ignore

        if missing := self.missing_inputs():
            st.warning(
                f"App `{self.Meta.name}({self.__class__.__name__})` can not be instantiated"  # type: ignore
            )
            if self.debug:
                st.warning(f"Missing input(s): {', '.join(missing)}")
            return

        try:

            rendered_output = self.render(
                **{
                    **self.state,
                    "state": self.state,
                }
            )  # type: ignore

            if rendered_output and isinstance(rendered_output, dict):

                rendered_output = self.handle_output_context(rendered_output)

                self.check_outputs(rendered_output)

                for key, val in rendered_output.items():
                    self.set_state(key, val)

        except Exception as e:
            st.error(f"App '{self.Meta.title}' failed: {e}")  # type: ignore

            if self.debug:
                raise e

    def handle_output_context(self, rendered_output) -> dict:

        def _handle_output_delete_context(output_context):
            delete_context = output_context.pop("delete", {})

            delete_enabled = delete_context.pop("enabled", True)
            states_to_delete = delete_context.pop("states", [])
            ignore_missing_delete = delete_context.pop("ignore_missing", False)
            delete_message = delete_context.pop("message", None)

            if not isinstance(states_to_delete, list):
                raise STAppException(
                    f"Expected 'delete_states' to be a list, got {type(states_to_delete)}"
                )

            if delete_enabled and states_to_delete:
                self.delete_states(
                    states_to_delete, ignore_missing=ignore_missing_delete
                )

                if delete_message:
                    st.info(delete_message)

        output_context = rendered_output.pop("context", {})

        _handle_output_delete_context(output_context)

        return rendered_output

    def render(self, *args, **kwargs):
        """Please implement render method!"""
        raise NotImplementedError("You must implement the render() method.")

    @classmethod
    def run_tabs(cls, debug: bool):
        if not cls.registry:
            st.warning("⚠️ No apps registered.")
            return

        apps_sorted = sorted(
            cls.registry.values(), key=lambda app: getattr(app.Meta, "order", 0)
        )

        tab_titles = [f"{app.Meta.icon} {app.Meta.title}" for app in apps_sorted]

        if not tab_titles:
            st.warning("⚠️ No valid tabs to display.")
            return

        tabs = st.tabs(tab_titles)

        for tab, app_cls in zip(tabs, apps_sorted):
            with tab:
                app: "STTab" = app_cls(debug=debug)
                app.display()
