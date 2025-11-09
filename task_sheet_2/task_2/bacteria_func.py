import math

class Bacteria:
    def __init__(self, specie, antibiotic,
                 effective_production_area,
                 effective_degradation_area,
                 growth_rate,
                 initial_population):
        self.specie = specie
        self.antibiotic = antibiotic
        self.kp = effective_production_area   # K_P
        self.kd = effective_degradation_area  # K_D
        self.growth_rate = growth_rate        # g_i
        self.X = initial_population           # X_i(t)

    def p_kill(self, XP, XD):
        """
        Compute:
        Pkill_i = e^{-K_D * XD} * (1 - e^{-K_P * XP})
        """
        return math.exp(-self.kd * XD) * (1 - math.exp(-self.kp * XP))

    def effective_growth(self, XP, XD):
        """
        Compute unnormalised growth term:
        G_i = X_i(t) * g_i * (1 - Pkill_i)
        Returns (G_i, Pkill_i) without updating X_i.
        """
        pkill_i = self.p_kill(XP, XD)
        G_i = self.X * self.growth_rate * (1 - pkill_i)
        return G_i, pkill_i

def simulate(X1, X2, X3, timesteps):
    """
    Run simulation for given timesteps.
    Returns history of populations and kill probabilities.
    """
    history = {
        'X1': [X1.X],
        'X2': [X2.X],
        'X3': [X3.X],
        'P_kill1': [],
        'P_kill2': [],
        'P_kill3': []
    }
    
    for t in range(timesteps):
        # Store current populations before update
        X1_curr = X1.X
        X2_curr = X2.X
        X3_curr = X3.X
        
        # Rock–paper–scissors relations:
        # X2 produces antibiotics harmful to X1, X3 degrades them
        # X3 produces antibiotics harmful to X2, X1 degrades them
        # X1 produces antibiotics harmful to X3, X2 degrades them
        
        G1, pkill1 = X1.effective_growth(XP=X2_curr, XD=X3_curr)
        G2, pkill2 = X2.effective_growth(XP=X3_curr, XD=X1_curr)
        G3, pkill3 = X3.effective_growth(XP=X1_curr, XD=X2_curr)

        total_G = G1 + G2 + G3
        if total_G <= 0:
            # All dead; keep zeros and break
            X1.X, X2.X, X3.X = 0.0, 0.0, 0.0
        else:
            # Normalised update (keeps total population ~ 1)
            X1.X = G1 / total_G
            X2.X = G2 / total_G
            X3.X = G3 / total_G
        
        history['X1'].append(X1.X)
        history['X2'].append(X2.X)
        history['X3'].append(X3.X)
        history['P_kill1'].append(pkill1)
        history['P_kill2'].append(pkill2)
        history['P_kill3'].append(pkill3)
    
    return history