# financial_simulator/core/simulation_pipeline.py

from financial_simulator.core.projection import run_projection

from financial_simulator.analysis.scoring import FinancialScorer
from financial_simulator.analysis.diagnostics import FinancialDiagnostics
from financial_simulator.analysis.recommendations import FinancialRecommendations
from financial_simulator.analysis.readiness import MigrationReadinessIndex
from financial_simulator.analysis.success_predictor import ImmigrationSuccessPredictor

from financial_simulator.risk.immigration_risk import ImmigrationRiskAnalyzer
from financial_simulator.risk.monte_carlo import MonteCarloSimulator

from financial_simulator.strategy.migration_strategy import MigrationStrategyPlanner


class SimulationPipeline:

    def __init__(self, inputs):
        self.inputs = inputs

    def run(self):

        # =========================
        # 1️⃣ CORE SIMULATION
        # =========================
        projection, tax_summary = run_projection(self.inputs)

        # =========================
        # 2️⃣ SCORE
        # =========================
        scorer = FinancialScorer(self.inputs)
        score = scorer.calculate(projection)

        diagnosis = FinancialDiagnostics.build_diagnosis(score)

        # =========================
        # 3️⃣ RISK
        # =========================
        risk_engine = ImmigrationRiskAnalyzer()
        risk = risk_engine.calculate_risk(projection, score)

        # =========================
        # 4️⃣ MONTE CARLO
        # =========================
        monte_carlo = MonteCarloSimulator(self.inputs, runs=300).run()

        # =========================
        # 5️⃣ SUCCESS PREDICTION
        # =========================
        success_engine = ImmigrationSuccessPredictor()
        success = success_engine.predict(
            projection,
            score,
            monte_carlo,
            risk
        )

        # =========================
        # 6️⃣ READINESS
        # =========================
        readiness_engine = MigrationReadinessIndex()
        readiness = readiness_engine.calculate(
            projection,
            score,
            risk,
            monte_carlo
        )

        # =========================
        # 7️⃣ RECOMMENDATIONS
        # =========================
        recommendations = FinancialRecommendations().generate(
            self.inputs,
            projection,
            score
        )

        # =========================
        # 8️⃣ STRATEGY
        # =========================
        strategy = MigrationStrategyPlanner().suggest(
            self.inputs,
            projection,
            score
        )

        return {
            "projection": projection,
            "score": score,
            "diagnosis": diagnosis,
            "risk": risk,
            "success": success,
            "readiness": readiness,
            "recommendations": recommendations,
            "strategy": strategy,
            "monte_carlo": monte_carlo
        }