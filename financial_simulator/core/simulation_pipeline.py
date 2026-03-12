# financial_simulator/core/simulation_pipeline.py

from financial_simulator.core.engine import ProjectionEngine
from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.insights import FinancialInsights
from financial_simulator.analysis.success_predictor import ImmigrationSuccessPredictor
from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.risk.monte_carlo import MonteCarloSimulator
from financial_simulator.strategy.migration_strategy import MigrationStrategyPlanner


class SimulationPipeline:

    def run(self, inputs):

        # 1️⃣ Projection
        engine = ProjectionEngine(inputs)
        result = engine.simulate(force=True)

        # 2️⃣ Score
        scorer = FinancialScorer(inputs)
        score = scorer.calculate(result)

        # 3️⃣ Risk
        risk_analyzer = ImmigrationRiskAnalyzer()
        risk = risk_analyzer.calculate_risk(result, score)

        # 4️⃣ Monte Carlo
        monte_carlo = MonteCarloSimulator(inputs).run()

        # 5️⃣ Success probability
        predictor = ImmigrationSuccessPredictor()
        success = predictor.predict(result, score, monte_carlo, risk)

        # 6️⃣ Strategy
        planner = MigrationStrategyPlanner()
        strategy = planner.suggest(inputs, result)

        # 7️⃣ Insights
        insights_engine = FinancialInsights()
        insights = insights_engine.generate(result, score)

        return {
            "projection": result,
            "score": score,
            "risk": risk,
            "monte_carlo": monte_carlo,
            "success_probability": success,
            "strategy": strategy,
            "insights": insights
        }