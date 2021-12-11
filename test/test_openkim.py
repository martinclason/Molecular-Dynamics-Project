from ase.calculators.kim.kim import KIM

def test_loading_openkim_potential():
  try:
    openKIMid = "Sim_ASAP_EMT_Rasmussen_AgAuCu__SM_847706399649_000"
    # calc = KIM(openKIMid)
  except:
    assert False, f"Couldn't load openKIM model with id {openKIMid}"

