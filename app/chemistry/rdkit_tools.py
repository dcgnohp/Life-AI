from typing import Optional, Dict, Any
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, QED


def compute_descriptors(smiles: str) -> Optional[Dict[str, Any]]:
    """
    Validate SMILES, sanitize molecule, and compute core descriptors.
    Returns None if molecule is invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    try:
        Chem.SanitizeMol(mol)
    except Exception:
        return None

    try:
        qed = QED.qed(mol)
    except Exception:
        qed = 0.0

    return {
        "smiles": smiles,
        "mw": Descriptors.MolWt(mol),
        "logp": Crippen.MolLogP(mol),
        "hbd": rdMolDescriptors.CalcNumHBD(mol),
        "hba": rdMolDescriptors.CalcNumHBA(mol),
        "tpsa": rdMolDescriptors.CalcTPSA(mol),
        "rot_bonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "qed": qed,
    }
