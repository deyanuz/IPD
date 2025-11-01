from typing import List
import random


class AdvancedStrategyAnalyzer:
    """Advanced strategy analyzer with machine learning principles"""
    def __init__(self):
        self.available_strategies = ["minimax", "fuzzy", "tit_for_tat", "adaptive", "pattern_matcher", "bayesian"]
        self.current_strategy = "minimax"
        self.opponent_pattern = []
        self.strategy_performance = {s: {"wins": 0, "uses": 0} for s in self.available_strategies}
        self.analysis_accuracy = 0.85
        self.pattern_memory = 15
        self.confidence_threshold = 0.7
        
    def analyze_opponent(self, opp_history: List[str], my_score: int, opp_score: int) -> str:
        if len(opp_history) < 3:
            return "minimax"
            
        analysis_confidence = self.calculate_analysis_confidence(opp_history)
        
        if random.random() > self.analysis_accuracy * analysis_confidence:
            return self.get_weighted_random_strategy()
            
        coop_rate = opp_history.count('C') / len(opp_history)
        recent_coop = opp_history[-3:].count('C') / min(3, len(opp_history))
        pattern_consistency = self.calculate_pattern_consistency(opp_history)
        score_differential = my_score - opp_score
        
        strategy_scores = {}
        
        if coop_rate > 0.8 and pattern_consistency > 0.7:
            strategy_scores["pattern_matcher"] = 0.9
            strategy_scores["adaptive"] = 0.6
        elif coop_rate < 0.2 and pattern_consistency > 0.6:
            strategy_scores["minimax"] = 0.9
            strategy_scores["bayesian"] = 0.7
        elif pattern_consistency < 0.4:
            strategy_scores["adaptive"] = 0.8
            strategy_scores["fuzzy"] = 0.7
        elif abs(coop_rate - 0.5) < 0.2 and score_differential < -5:
            strategy_scores["minimax"] = 0.8
            strategy_scores["pattern_matcher"] = 0.6
        else:
            strategy_scores["adaptive"] = 0.7
            strategy_scores["bayesian"] = 0.6
            
        for strategy in strategy_scores:
            success_rate = self.strategy_performance[strategy]["wins"] / max(1, self.strategy_performance[strategy]["uses"])
            strategy_scores[strategy] *= (0.5 + success_rate)
            
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        return best_strategy
        
    def calculate_analysis_confidence(self, opp_history: List[str]) -> float:
        if len(opp_history) < 5:
            return 0.5
        consistency = self.calculate_pattern_consistency(opp_history)
        data_quality = min(1.0, len(opp_history) / 20)
        return (consistency + data_quality) / 2
        
    def calculate_pattern_consistency(self, opp_history: List[str]) -> float:
        if len(opp_history) < 3:
            return 0.5
        transitions = []
        for i in range(1, len(opp_history)):
            transitions.append(opp_history[i-1] + opp_history[i])
        unique_transitions = len(set(transitions))
        max_possible = min(4, len(transitions))
        return 1.0 - (unique_transitions / max_possible)
        
    def get_weighted_random_strategy(self) -> str:
        strategies = []
        weights = []
        for strategy in self.available_strategies:
            success_rate = self.strategy_performance[strategy]["wins"] / max(1, self.strategy_performance[strategy]["uses"])
            weight = 0.1 + success_rate
            strategies.append(strategy)
            weights.append(weight)
        return random.choices(strategies, weights=weights)[0]
        
    def record_strategy_performance(self, strategy: str, won_round: bool):
        self.strategy_performance[strategy]["uses"] += 1
        if won_round:
            self.strategy_performance[strategy]["wins"] += 1

class PowerfulAdaptiveAI:
    """Powerful adaptive AI"""
    def __init__(self):
        self.name = "Adaptive AI"
        self.analyzer = AdvancedStrategyAnalyzer()
        self.my_history = []
        self.opp_history = []
        self.current_strategy = "minimax"
        self.strategy_change_cooldown = 0
        self.learning_rate = 0.85
        self.prediction_accuracy = 0.88
        self.risk_tolerance = 0.4
        self.consecutive_losses = 0
        self.aggression_level = 0.3
        self.pattern_memory = []
        self.bayesian_prior = 0.5
        
    def update_bayesian_prior(self, move: str):
        if move == 'C':
            self.bayesian_prior = min(0.95, self.bayesian_prior * 1.1)
        else:
            self.bayesian_prior = max(0.05, self.bayesian_prior * 0.9)
            
    def bayesian_decision(self) -> str:
        if not self.opp_history:
            return 'C'
        recent_coop = self.opp_history[-3:].count('C') / min(3, len(self.opp_history))
        evidence_strength = min(1.0, len(self.opp_history) / 10)
        likelihood = recent_coop
        posterior = (likelihood * self.bayesian_prior) / (
            likelihood * self.bayesian_prior + (1 - likelihood) * (1 - self.bayesian_prior))
        confidence = abs(posterior - 0.5) * 2
        if confidence > 0.6:
            return 'C' if posterior > 0.5 else 'D'
        else:
            return self.minimax_decision()
            
    def pattern_matcher_decision(self) -> str:
        if len(self.opp_history) < 4:
            return self.minimax_decision()
        recent_pattern = ''.join(self.opp_history[-4:])
        pattern_responses = {
            "CCCC": 'D', "DDDD": 'C', "CDCD": self.opp_history[-1],
            "DCDC": self.opp_history[-1], "CCDC": 'D', "DDCD": 'C',
        }
        if recent_pattern in pattern_responses:
            return pattern_responses[recent_pattern]
        return self.markov_prediction()
        
    def markov_prediction(self) -> str:
        if len(self.opp_history) < 3:
            return self.minimax_decision()
        current_state = ''.join(self.opp_history[-2:])
        transitions = {'C': 0, 'D': 0}
        for i in range(2, len(self.opp_history)):
            if ''.join(self.opp_history[i-2:i]) == current_state:
                next_move = self.opp_history[i]
                transitions[next_move] += 1
        total = sum(transitions.values())
        if total == 0:
            return self.minimax_decision()
        predicted_move = max(transitions, key=transitions.get)
        return 'D' if predicted_move == 'C' else 'C'
        
    def minimax_decision(self) -> str:
        if not self.opp_history:
            return 'C'
        coop_rate = self.opp_history.count('C') / len(self.opp_history)
        recent_trend = self.opp_history[-3:].count('C') / min(3, len(self.opp_history))
        weighted_coop = coop_rate * 0.4 + recent_trend * 0.6
        risk_adjustment = 1.0 - self.risk_tolerance
        ev_coop = weighted_coop * 3 + (1 - weighted_coop) * 0
        ev_defect = weighted_coop * 5 * risk_adjustment + (1 - weighted_coop) * 1
        if len(self.my_history) > 10:
            score_ratio = sum([1 for m in self.my_history if m == 'D']) / len(self.my_history)
            if score_ratio > 0.7:
                ev_defect *= 0.9
        return 'C' if ev_coop > ev_defect else 'D'
        
    def fuzzy_decision(self) -> str:
        if not self.opp_history:
            return 'C'
        coop_rate = self.opp_history.count('C') / len(self.opp_history)
        recent_trend = self.opp_history[-3:].count('C') / min(3, len(self.opp_history))
        consistency = self.analyzer.calculate_pattern_consistency(self.opp_history)
        if coop_rate > 0.8 and recent_trend > 0.6:
            return 'C' if random.random() < 0.9 else 'D'
        elif coop_rate < 0.2 and recent_trend < 0.4:
            return 'D' if random.random() < 0.9 else 'C'
        elif consistency > 0.7:
            return self.pattern_matcher_decision()
        elif abs(coop_rate - 0.5) < 0.3 and consistency < 0.4:
            return self.tit_for_tat_decision()
        else:
            return self.bayesian_decision()
            
    def tit_for_tat_decision(self) -> str:
        if not self.opp_history:
            return 'C'
        if self.opp_history[-1] == 'D':
            overall_coop = self.opp_history.count('C') / len(self.opp_history)
            forgiveness_prob = 0.1 + (overall_coop * 0.3)
            if random.random() < forgiveness_prob:
                return 'C'
        return self.opp_history[-1]
        
    def adaptive_decision(self) -> str:
        if not self.opp_history:
            return 'C'
        success_rate = self.calculate_comprehensive_success()
        if success_rate > 0.7:
            if self.my_history:
                return self.my_history[-1] if random.random() < 0.8 else 'D'
            else:
                return 'C'
        elif success_rate < 0.4:
            self.consecutive_losses += 1
            self.aggression_level = min(0.8, self.aggression_level + 0.1)
            if self.consecutive_losses > 2:
                return 'D'
            else:
                return 'C' if random.random() < 0.3 else 'D'
        else:
            self.consecutive_losses = 0
            return 'C' if random.random() < 0.6 else 'D'
            
    def calculate_comprehensive_success(self) -> float:
        if len(self.my_history) < 2:
            return 0.5
        total_score = 0
        max_possible = 0
        for i in range(len(self.my_history)):
            my_move = self.my_history[i]
            opp_move = self.opp_history[i]
            if (my_move, opp_move) == ('C', 'C'):
                total_score += 3
            elif (my_move, opp_move) == ('C', 'D'):
                total_score += 0
            elif (my_move, opp_move) == ('D', 'C'):
                total_score += 5
            else:
                total_score += 1
            max_possible += 5
        base_rate = total_score / max_possible
        exploit_success = sum(1 for i in range(len(self.my_history)) 
                            if self.my_history[i] == 'D' and self.opp_history[i] == 'C') / max(1, len(self.my_history))
        comprehensive_success = (base_rate * 0.7) + (exploit_success * 0.3)
        return min(1.0, comprehensive_success)
        
    def decide_move(self, round_num: int, my_score: int, opp_score: int) -> str:
        should_analyze = (self.strategy_change_cooldown <= 0 and 
                         len(self.opp_history) >= 3 and 
                         (round_num % 3 == 0 or len(self.opp_history) < 8))
                         
        if should_analyze:
            new_strategy = self.analyzer.analyze_opponent(self.opp_history, my_score, opp_score)
            if new_strategy != self.current_strategy:
                self.current_strategy = new_strategy
                self.strategy_change_cooldown = random.randint(2, 5)
        else:
            self.strategy_change_cooldown = max(0, self.strategy_change_cooldown - 1)
            
        if random.random() < 0.01:
            return random.choice(['C', 'D'])
            
        if self.current_strategy == "minimax":
            move = self.minimax_decision()
        elif self.current_strategy == "fuzzy":
            move = self.fuzzy_decision()
        elif self.current_strategy == "tit_for_tat":
            move = self.tit_for_tat_decision()
        elif self.current_strategy == "adaptive":
            move = self.adaptive_decision()
        elif self.current_strategy == "pattern_matcher":
            move = self.pattern_matcher_decision()
        elif self.current_strategy == "bayesian":
            move = self.bayesian_decision()
        else:
            move = self.minimax_decision()
            
        self.update_bayesian_prior(move)
        return move
        
    def reset(self):
        self.my_history = []
        self.opp_history = []
        self.current_strategy = "minimax"
        self.strategy_change_cooldown = 0
        self.consecutive_losses = 0
        self.aggression_level = 0.3
        self.bayesian_prior = 0.5
        self.analyzer = AdvancedStrategyAnalyzer()

class StrategicOpponentAI:
    """Enhanced opponent AI"""
    def __init__(self, ai_type: str):
        self.ai_type = ai_type
        self.name = f"{ai_type.replace('_', ' ').title()} AI"
        self.my_history = []
        self.opp_history = []
        self.personality = self.initialize_personality(ai_type)
        
    def initialize_personality(self, ai_type):
        personalities = {
            "cooperative": {"coop_bias": 0.8, "forgiveness": 0.9, "aggression": 0.1, "adaptability": 0.3},
            "aggressive": {"coop_bias": 0.2, "forgiveness": 0.1, "aggression": 0.9, "adaptability": 0.6},
            "random": {"coop_bias": 0.5, "forgiveness": 0.5, "aggression": 0.5, "adaptability": 1.0},
            "tit_for_tat": {"coop_bias": 0.5, "forgiveness": 0.3, "aggression": 0.5, "adaptability": 0.7},
            "forgiving": {"coop_bias": 0.7, "forgiveness": 0.8, "aggression": 0.2, "adaptability": 0.5},
            "strategic": {"coop_bias": 0.6, "forgiveness": 0.4, "aggression": 0.6, "adaptability": 0.9},
            "unpredictable": {"coop_bias": 0.5, "forgiveness": 0.5, "aggression": 0.5, "adaptability": 0.8},
            "exploitative": {"coop_bias": 0.4, "forgiveness": 0.2, "aggression": 0.8, "adaptability": 0.7},
            "mirror": {"coop_bias": 0.5, "forgiveness": 0.5, "aggression": 0.5, "adaptability": 0.6}
        }
        return personalities.get(ai_type, personalities["random"])
    
    def get_strength(self) -> float:
        strengths = {
            "cooperative": 0.6, "aggressive": 0.8, "random": 0.4,
            "tit_for_tat": 0.7, "forgiving": 0.5, "strategic": 0.9,
            "unpredictable": 0.75, "exploitative": 0.85, "mirror": 0.7
        }
        return strengths.get(self.ai_type, 0.5)
    
    def decide_move(self, round_num: int, my_score: int, opp_score: int) -> str:
        if self.ai_type == "cooperative":
            return 'C' if random.random() < 0.8 else 'D'
        elif self.ai_type == "aggressive":
            return 'D' if random.random() < 0.8 else 'C'
        elif self.ai_type == "random":
            return 'C' if random.random() < 0.5 else 'D'
        elif self.ai_type == "tit_for_tat":
            if not self.opp_history:
                return 'C'
            return self.opp_history[-1]
        elif self.ai_type == "forgiving":
            if not self.opp_history:
                return 'C'
            if self.opp_history[-1] == 'D' and random.random() < self.personality["forgiveness"]:
                return 'C'
            return self.opp_history[-1]
        elif self.ai_type == "strategic":
            if len(self.opp_history) < 3:
                return 'C'
            if len(self.opp_history) >= 5:
                recent_pattern = self.opp_history[-3:]
                if len(set(recent_pattern)) == 1:
                    return 'D' if recent_pattern[0] == 'C' else 'C'
            coop_rate = self.opp_history.count('C') / len(self.opp_history)
            return 'C' if coop_rate > 0.6 else 'D'
        elif self.ai_type == "unpredictable":
            if len(self.my_history) < 2:
                return 'C'
            if random.random() < 0.3:
                return 'D' if self.my_history[-1] == 'C' else 'C'
            else:
                return self.opp_history[-1] if self.opp_history else 'C'
        elif self.ai_type == "exploitative":
            if len(self.opp_history) < 4:
                return 'C'
            if all(move == 'C' for move in self.opp_history[-2:]):
                return 'D'
            elif all(move == 'D' for move in self.opp_history[-2:]):
                return 'C'
            else:
                return 'D' if random.random() < 0.6 else 'C'
        elif self.ai_type == "mirror":
            if not self.opp_history:
                return 'C'
            if random.random() < 0.1:
                return 'D' if self.opp_history[-1] == 'C' else 'C'
            return self.opp_history[-1]
        else:
            return 'C'
            
    def reset(self):
        self.my_history = []
        self.opp_history = []
