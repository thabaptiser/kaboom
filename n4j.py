from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    Relationship, RelationshipFrom)

class Page(StructuredNode):
    link = StringProperty(unique_index=True, required=True)
    page_text = StringProperty(required=True)
    # traverse incoming IS_FROM relation, inflate to Person objects
    contained_word = Relationship('Word', 'CONTAINS')


class Word(StructuredNode):
    text = StringProperty(unique_index=True)
    frequency = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    page = Relationship(Page, 'CONTAINS')
