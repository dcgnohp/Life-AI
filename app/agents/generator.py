import random
from typing import List


class GeneratorAgent:
    def generate(self, seeds: List[str], n_candidates: int) -> List[str]:
        generated = set()

        attempts = 0
        max_attempts = n_candidates * 10 

        while len(generated) < n_candidates and attempts < max_attempts:
            seed = random.choice(seeds)
            mutated = self.mutate(seed)

            if mutated != seed:
                generated.add(mutated)

            attempts += 1

        return list(generated)

    def mutate(self, smiles: str) -> str:
        mutation_type = random.choice([
            "swap_halogen",
            "add_methyl",
            "remove_methyl"
        ])

        if mutation_type == "swap_halogen":
            return self.swap_halogen(smiles)

        if mutation_type == "add_methyl":
            return self.add_methyl(smiles)

        if mutation_type == "remove_methyl":
            return self.remove_methyl(smiles)

        return smiles

    def swap_halogen(self, smiles: str) -> str:
        if "F" in smiles:
            return smiles.replace("F", "Cl", 1)
        if "Cl" in smiles:
            return smiles.replace("Cl", "F", 1)
        return smiles

    def add_methyl(self, smiles: str) -> str:
        return smiles + "C"

    def remove_methyl(self, smiles: str) -> str:
        if smiles.endswith("C"):
            return smiles[:-1]
        return smiles
