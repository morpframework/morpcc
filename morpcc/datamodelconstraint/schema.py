#
import typing
from dataclasses import dataclass, field

import morpfw

#
from deform.widget import TextAreaWidget
from morpcc.deform.referencewidget import ReferenceWidget
from morpcc.deform.vocabularywidget import VocabularyWidget


@dataclass
class DataModelConstraintSchema(morpfw.Schema):

    title: typing.Optional[str] = None
    validator: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "deform.widget": VocabularyWidget("morpcc.datamodelvalidators"),
        },
    )
    parameters: typing.Optional[str] = field(
        default=None, metadata={"deform.widget": TextAreaWidget()}
    )
    datamodel_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "deform.widget": ReferenceWidget("morpcc.datamodel"),
        },
    )
