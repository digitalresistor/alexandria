from pyramid.compat import (
        text_type,
        binary_type
        )

from sqlalchemy.ext.hybrid import (
        hybrid_property,
        Comparator,
        )

class IdnaComparator(Comparator):
    def __eq__(self, other):
        if isinstance(other, text_type):
            other = other.encode('idna').decode('utf-8')
        elif isinstance(other, binary_type):
            other = other
        else:
            raise ValueError("Unable to encode to IDNA format.")

        return self.__clause_element__() == other
