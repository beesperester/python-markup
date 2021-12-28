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
        return self.render(self.children, self.attributes)

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
    hydrogen_id: str
    add_hydrogen_id: bool

    def __init__(
        self,
        tag: str,
        *children: T_element,
        **attributes: T_attribute,
    ) -> None:
        self.tag = tag
        self.hydrogen_id = uuid.uuid4().hex[:6]
        self.add_hydrogen_id = True

        super().__init__(*children, **attributes)

    def mount(self) -> str:
        return self.render(self.children, self.attributes)

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

        hydrogen_id_string = ""

        if self.add_hydrogen_id:
            hydrogen_id_string = f'hydrogenid="{self.hydrogen_id}"'

        children_string = super().render(children, attributes)

        if children_string or self.tag not in SELF_CLOSING_TAGS:
            return f"<{self.tag} {hydrogen_id_string}{attributes_string}>{children_string}</{self.tag}>"

        return f"<{self.tag} {hydrogen_id_string}{attributes_string}/>"


# utility functions


def destructure(
    attribute_names: list[str], attributes: dict[str, T_attribute]
) -> list[Any]:
    values: list[T_attribute] = []

    for attribute_name in attribute_names:
        if attribute_name in attributes.keys():
            values.append(attributes[attribute_name])

            del attributes[attribute_name]
        else:
            values.append(None)

    return values


def merge_attributes(attributes, **extra_attributes: Any) -> dict[str, Any]:
    merged_attributes = {**attributes}

    for key, value in extra_attributes.items():
        if key in merged_attributes.keys():
            merged_attributes_value = merged_attributes[key]

            if isinstance(merged_attributes_value, str) and isinstance(value, str):
                merged_attributes[key] = " ".join(
                    list(set(merged_attributes_value.split(" ") + value.split(" ")))
                )
        else:
            merged_attributes[key] = value

    return merged_attributes
