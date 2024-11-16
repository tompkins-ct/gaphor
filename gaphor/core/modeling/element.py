#!/usr/bin/env python
"""Base class for model elements."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from gaphor.core.modeling.base import Base
from gaphor.core.modeling.properties import (
    attribute,
    relation_many,
    relation_one,
)

if TYPE_CHECKING:
    from gaphor.core.modeling.diagram import Diagram
    from gaphor.core.modeling.presentation import Presentation
    from gaphor.UML import Comment, Relationship

log = logging.getLogger(__name__)


class Element(Base):
    name: attribute[str] = attribute("name", str)
    note: attribute[str] = attribute("note", str)
    comment: relation_many[Comment]
    ownedDiagram: relation_many[Diagram]
    ownedElement: relation_many[Element]
    owner: relation_one[Element]
    presentation: relation_many[Presentation]
    relationship: relation_many[Relationship]
    sourceRelationship: relation_many[Relationship]
    targetRelationship: relation_many[Relationship]

    # From UML:
    appliedStereotype: relation_many[Element]

    @property
    def qualifiedName(self) -> list[str]:
        """Returns the qualified name of the element as a list."""
        from gaphor.diagram.group import self_and_owners

        qname = [e.name or "??" for e in self_and_owners(self)]
        qname.reverse()
        return qname
