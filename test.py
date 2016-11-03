from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom)

class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)

    # traverse incoming IS_FROM relation, inflate to Person objects
    inhabitant = RelationshipFrom('Person', 'IS_FROM')


class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')


jim = Person(name='Jim', age=3).save()
jim.age = 4
jim.save() # validation happens here
jim.delete()
jim.refresh() # reload properties from neo


germany = Country(code='DE').save()
jim.country.connect(germany)

if jim.country.is_connected(germany):
    print("Jim's from Germany")

for p in germany.inhabitant.all():
    print(p.name) # Jim

len(germany.inhabitant) # 1

# Find people called 'Jim' in germany
germany.inhabitant.search(name='Jim')

jim.country.disconnect(germany)
