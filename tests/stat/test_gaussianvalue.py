from pyerman.stat import GaussianValue
import pytest

class TestGaussian:

  @pytest.mark.xfail(raises=ValueError)
  def test_init_none(self):
    GaussianValue()


  def test_simple(self):
    gauss = GaussianValue([1,2,3])
    assert(gauss.val == 2.0)

