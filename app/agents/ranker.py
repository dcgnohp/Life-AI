class RankerAgent:
    def select(self, molecules, top_k):
        return sorted(
            molecules,
            key=lambda x: x["score"],
            reverse=True
        )[:top_k]
