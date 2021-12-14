from ase.calculators.kim.kim import KIM
import pytest


@pytest.mark.openkim
def test_loading_universal_openkim_potential():
  try:
    openKIMid = "LJ_ElliottAkerson_2015_Universal__MO_959249795837_003"
    calc = KIM(openKIMid)
  except:
    assert False, f"Couldn't load universal openKIM model with id {openKIMid}"

@pytest.mark.openkim
def test_loading_openkim_potential():
  try:
    openKIMid = "Sim_ASAP_EMT_Rasmussen_AgAuCu__SM_847706399649_000"
    calc = KIM(openKIMid)
  except:
    assert False, f"Couldn't load openKIM model with id {openKIMid}"

