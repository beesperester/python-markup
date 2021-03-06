from __future__ import annotations

import uuid

from typing import Any, Callable, Union

T_element = Union[str, "Element", Callable[..., str]]
T_attribute = Any

SELF_CLOSING_TAGS: list[str] = [
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
]


class DestructureError(Exception):
    ...


class Meta:

    children: list[T_element]
    attributes: dict[str, T_attribute]

    def __init__(
        self,
        *children: T_element,
        **attributes: T_attribute,
    ) -> None:
        self.children = list(children)
        self.attributes = attributes

    def __str__(self) -> str:
        return self.mount()

    def mount(self) -> str:
        return self.render(self.children.copy(), self.attributes.copy())

    def render(
        self, children: list[T_element], attributes: dict[str, T_attribute]
    ) -> str:
        if children:
            children_string = ""

            for child in children:
                if isinstance(child, Element):
                    children_string += child.mount()
                elif callable(child):
                    children_string += child()
                else:
                    children_string += str(child)

            return children_string

        return ""


class Element(Meta):

    tag: str
    indent: bool

    def __init__(
        self,
        tag: str,
        *children: T_element,
        **attributes: T_attribute,
    ) -> None:
        self.tag = tag

        super().__init__(*children, **attributes)

    def render(
        self, children: list[T_element], attributes: dict[str, T_attribute]
    ) -> str:
        def format_attribute(key: str, value: Any) -> str:
            key = key.replace("class_name", "class")

            if isinstance(value, bool):
                if value:
                    return str(key)

                return ""

            return f'{key}="{value}"'

        on_mount: str

        on_mount, *_ = extract_attributes([("onmount", "")], attributes)

        on_mount_string = ""

        if on_mount:
            on_mount = on_mount.replace(
                "this", "document.currentScript.previousElementSibling"
            )

            on_mount_string = f"""<script type="text/javascript">{on_mount}</script>"""

        attributes_string = " ".join(
            [
                format_attribute(key, value)
                for key, value in attributes.items()
                if hasattr(value, "__str__")
                and isinstance(value, (str, int, float, bool))
            ]
        )

        if attributes_string:
            attributes_string = " " + attributes_string

        children_string = super().render(children, attributes)

        if children_string or self.tag not in SELF_CLOSING_TAGS:
            return f"<{self.tag} {attributes_string}>{children_string}</{self.tag}>{on_mount_string}"

        return f"<{self.tag} {attributes_string}/>{on_mount_string}"


# utility functions


def extract_attributes(
    attribute_definitions: list[tuple[str, Any]], attributes: dict[str, T_attribute]
) -> list[Any]:
    values: list[T_attribute] = []

    for attribute_name, attribute_default_value in attribute_definitions:
        value = None

        if attribute_name in attributes.keys():
            value = attributes[attribute_name]

            if attribute_default_value and not isinstance(
                value, attribute_default_value.__class__
            ):
                raise DestructureError(
                    f"Value for '{attribute_name}' must be of type '{attribute_default_value.__class__.__name__}' is '{value.__class__.__name__}'"
                )

            del attributes[attribute_name]
        else:
            value = attribute_default_value

        values.append(value)

    return values


def extend_attributes(attributes, **extra_attributes: Any) -> dict[str, Any]:
    extended_attributes = {**attributes}

    for key, value in extra_attributes.items():
        if key in extended_attributes.keys():
            extended_attributes_value = extended_attributes[key]

            if isinstance(extended_attributes_value, str) and isinstance(value, str):
                extended_attributes[key] = " ".join(
                    list(set(extended_attributes_value.split(" ") + value.split(" ")))
                )
        else:
            extended_attributes[key] = value

    return extended_attributes
