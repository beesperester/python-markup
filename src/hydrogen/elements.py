from __future__ import annotations

import uuid

from typing import Any, Callable, Union

T_element = Union[str, "Element", Callable[..., str]]
T_attribute = Any


class Element:

    tag: str
    children: list[T_element]
    attributes: dict[str, T_attribute]
    indent: bool
    hydrogen_id: str

    def __init__(
        self,
        tag: str,
        *children: T_element,
        **attributes: T_attribute,
    ) -> None:
        self.tag = tag
        self.children = list(children)
        self.attributes = attributes
        self.hydrogen_id = uuid.uuid4().hex[:6]

    def __str__(self) -> str:
        return self.mount()

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

        hydrogen_id_string = f'hydrogenid="{self.hydrogen_id}"'

        if children:
            children_string = ""

            for child in children:
                if isinstance(child, Element):
                    children_string += child.mount()
                elif callable(child):
                    children_string += child()
                else:
                    children_string += str(child)

            return f"<{self.tag} {hydrogen_id_string}{attributes_string}>{children_string}</{self.tag}>"

        return f"<{self.tag} {hydrogen_id_string}{attributes_string}/>"


# assorted html elements


class html(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("html", *children, **attributes)


class head(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("head", *children, **attributes)


class title(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("title", *children, **attributes)


class style(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("style", *children, **attributes)


class script(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("script", *children, **attributes)


class body(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("body", *children, **attributes)


class div(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("div", *children, **attributes)


class p(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("p", *children, **attributes)


class span(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("span", *children, **attributes)


class a(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("a", *children, **attributes)


class h1(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h1", *children, **attributes)


class h2(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h2", *children, **attributes)


class h3(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h3", *children, **attributes)


class h4(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h4", *children, **attributes)


class h5(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h5", *children, **attributes)


class h6(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("h6", *children, **attributes)


class ol(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("ol", *children, **attributes)


class dl(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("dl", *children, **attributes)


class dd(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("dd", *children, **attributes)


class ul(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("ul", *children, **attributes)


class li(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("li", *children, **attributes)


class video(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("video", *children, **attributes)


class source(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("source", *children, **attributes)


class form(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("form", *children, **attributes)


class input(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("input", *children, **attributes)


class button(Element):
    def __init__(self, *children: T_element, **attributes: Any) -> None:
        super().__init__("button", *children, **attributes)


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
