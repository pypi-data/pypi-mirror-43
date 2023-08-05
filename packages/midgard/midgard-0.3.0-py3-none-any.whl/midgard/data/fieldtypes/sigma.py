"""A Dataset sigma field

"""

# Midgard imports
from midgard.data.fieldtypes._fieldtype import FieldType
from midgard.data.sigma import SigmaArray
from midgard.dev import plugins


@plugins.register
class SigmaField(FieldType):

    _subfields = ["sigma"]
    _factory = staticmethod(SigmaArray)

    def _post_init(self, val, **field_args):
        """Initialize float field"""
        if isinstance(val, SigmaArray):
            data = val
        else:
            data = self._factory(val, **field_args)

        # Check that the correct number of observations are given
        if len(data) != self.num_obs:
            raise ValueError(f"{self.name!r} initialized with {len(data)} values, expected {self.num_obs}")

        # We only support 1- and 2-dimensional arrays
        if data.ndim < 1 or data.ndim > 2:
            raise ValueError(
                f"{self.name!r} initialized with {data.ndim}-dimensional data, "
                "only 1- and 2-dimensional values are supported"
            )

        # Handle units
        if self._unit is not None:
            cols = 1 if data.ndim == 1 else data.shape[1]
            if isinstance(self._unit, str):
                self._unit = (self._unit,) * cols
            elif len(self._unit) != cols:
                raise ValueError(f"Number of units ({len(self._units)}) must equal number of columns ({cols})")

        # Store the data as a SigmaArray
        self.data = data

    @classmethod
    def _read(cls, h5_group, _) -> "SigmaField":
        """Read a SigmaField from a HDF5 data source"""
        name = h5_group.attrs["fieldname"]
        val = h5_group[name][...]
        sigma = h5_group["sigma"][...]
        return cls(num_obs=len(val), name=name, val=val, sigma=sigma)

    def _write(self, h5_group, _) -> None:
        """Write a SigmaField to a HDF5 data source"""
        h5_group.attrs["fieldname"] = self.name
        h5_field = h5_group.create_dataset(self.name, self.data.shape, dtype=self.data.dtype)
        h5_field[...] = self.data
        h5_field = h5_group.create_dataset("sigma", self.data.shape, dtype=self.data.sigma.dtype)
        h5_field[...] = self.data.sigma
