import pytest
from src.cheeks import Cheeks3D
import dataclasses as dc

cls = Cheeks3D
inst = cls()

@pytest.mark.parametrize("attr", dc.fields(cls))
class TestAttrsCheeks3D:
    def test_has_bounds(self, attr):
        assert hasattr(cls, s:=f"{attr.name}_bounds"),\
            f"{cls.__name__} has no {s} attribute."

    def test_valid_bounds_len(self, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert (l:=len(attr_bounds_val)) == 2,\
            f"{attr.name} has {l} bounds (should be 2)."

    def test_valid_bounds_order(self, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert attr_bounds_val[0] <= attr_bounds_val[1],\
            f"{attr.name} bounds are not in the right order (should be (min, max))."

    def test_has_default(self, attr):
        assert attr.default is not dc.MISSING,\
            f"{attr.name} has no default value."

    def test_valid_default(self, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert attr_bounds_val[0] <= attr.default <= attr_bounds_val[1],\
            f"{attr.name} default value must be between the bound given by {attr.name}_bounds."
