import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget, TextAreaWidget
from morpcc.deform.referencewidget import ReferenceWidget


@dataclass
class IndexSchema(morpfw.Schema):

    name: typing.Optional[str] = field(default=None, metadata={"required": True})
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    type: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "deform.widget": SelectWidget(
                values=[
                    ("fulltextindex", "Full Text Index"),
                    ("keywordindex", "Keyword Index"),
                ]
            ),
        },
    )
    description: typing.Optional[str] = field(
        default=None, metadata={"deform.widget": TextAreaWidget()}
    )