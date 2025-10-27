import pytest
from src.cheeks import Cheeks3Dcore
import dataclasses as dc


params = [
    (cls, f)
    for cls in Cheeks3Dcore.__subclasses__()
    for f in dc.fields(cls)
]


@pytest.mark.parametrize("cls,attr", params)
class TestAttrsCheeks3D:
    def test_has_bounds(self, cls, attr):
        assert hasattr(cls, s:=f"{attr.name}_bounds"),\
            f"{cls.__name__} has no {s} attribute."

    def test_valid_bounds_len(self, cls, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert (l:=len(attr_bounds_val)) == 2,\
            f"{attr.name} has {l} bounds (should be 2)."

    def test_valid_bounds_order(self, cls, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert attr_bounds_val[0] <= attr_bounds_val[1],\
            f"{attr.name} bounds are not in the right order (should be (min, max))."

    def test_has_default(self, cls, attr):
        assert attr.default is not dc.MISSING,\
            f"{attr.name} has no default value."

    def test_valid_default(self, cls, attr):
        attr_bounds_val = getattr(cls, f"{attr.name}_bounds")
        assert attr_bounds_val[0] <= attr.default <= attr_bounds_val[1],\
            f"{attr.name} default value must be between the bound given by {attr.name}_bounds."


class TestCheeks3Dcore:
    def test_warn_on_inst(self):
        with pytest.warns(UserWarning, match="abstract"):
            Cheeks3Dcore(10, 0, 1, 0, 1)
