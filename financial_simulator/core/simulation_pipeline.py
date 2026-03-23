# financial_simulator/core/simulation_pipeline.py

from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.insights import FinancialInsights
from financial_simulator.analysis.success_predictor import ImmigrationSuccessPredictor

from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.strategy.migration_strategy import MigrationStrategyPlanner

from financial_simulator.core.projection import run_projection


class SimulationPipeline:

    def run(self, inputs, run_monte_carlo: bool = False):

        context = {}

        # =========================
        # 1️⃣ CORE SIMULATION
        # =========================
        result, tax_summary = run_projection(inputs)

        context["projection"] = result
        context["tax_summary"] = tax_summary

        # =========================
        # 2️⃣ MONTE CARLO (OPTIONAL)
        # =========================
        monte_carlo = None

        if run_monte_carlo:
            from financial_simulator.risk.monte_carlo import MonteCarloSimulator
            monte_carlo = MonteCarloSimulator(inputs).run()

        context["monte_carlo"] = monte_carlo

        # =========================
        # 3️⃣ SCORING
        # =========================
        scorer = FinancialScorer(inputs, tax_summary)
        score = scorer.calculate(result)

        context["score"] = score

        # =========================
        # 4️⃣ RISK ANALYSIS
        # =========================
        risk_analyzer = ImmigrationRiskAnalyzer()
        risk = risk_analyzer.calculate_risk(result, score)

        context["risk"] = risk

        # =========================
        # 5️⃣ SUCCESS PREDICTION
        # =========================
        predictor = ImmigrationSuccessPredictor()
        success = predictor.predict(result, score, monte_carlo, risk)

        context["success_probability"] = success

        # =========================
        # 6️⃣ STRATEGY
        # =========================
        planner = MigrationStrategyPlanner()
        strategy = planner.suggest(inputs, result)

        context["strategy"] = strategy

        # =========================
        # 7️⃣ INSIGHTS
        # =========================
        insights_engine = FinancialInsights()
        insights = insights_engine.generate(result, score)

        context["insights"] = insights

        # =========================
        # FINAL OUTPUT
        # =========================
        return context