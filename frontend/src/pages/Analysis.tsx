import React from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Download } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { FinancialSummary } from '../components/dashboard/FinancialSummary';
import { DebtCard } from '../components/dashboard/DebtCard';
import { SavingsCard } from '../components/dashboard/SavingsCard';
import { BudgetCard } from '../components/dashboard/BudgetCard';
import { RiskCard } from '../components/dashboard/RiskCard';
import type { AnalysisResponse } from '../lib/api';

export const Analysis: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const location = useLocation();
    const data: AnalysisResponse = location.state?.data;

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis not found</h2>
                    <p className="text-gray-600">Please upload a bank statement to get started.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm sticky top-0 z-10">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Button variant="ghost" onClick={() => window.history.back()}>
                                <ArrowLeft className="w-4 h-4 mr-2" />
                                Back
                            </Button>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">Financial Analysis</h1>
                                <p className="text-sm text-gray-600">ID: {id}</p>
                            </div>
                        </div>
                        <Button variant="outline">
                            <Download className="w-4 h-4 mr-2" />
                            Export PDF
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5 }}
                    className="space-y-8"
                >
                    {/* Summary */}
                    <FinancialSummary
                        totalIncome={data.summary.total_income}
                        totalExpenses={data.summary.total_expenses}
                        netIncome={data.summary.net_income}
                        savingsRate={data.summary.savings_rate}
                        debtToIncomeRatio={data.summary.debt_to_income_ratio}
                    />

                    {/* Analysis Cards Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Debt Card */}
                        {data.analysis.debt && (
                            <DebtCard
                                totalDebt={data.analysis.debt.total_debt || 0}
                                payoffStrategy={data.analysis.debt.payoff_strategy || 'N/A'}
                                monthsToPayoff={data.analysis.debt.months_to_payoff || 0}
                                recommendations={data.analysis.debt.recommendations || []}
                                recommendedMonthlyPayment={data.analysis.debt.recommended_monthly_payment}
                            />
                        )}

                        {/* Savings Card */}
                        {data.analysis.savings && (
                            <SavingsCard
                                monthlySavingsGoal={data.analysis.savings.monthly_savings_goal || 0}
                                emergencyFundGap={data.analysis.savings.emergency_fund_gap || 0}
                                monthsToEmergencyFund={data.analysis.savings.months_to_emergency_fund || 0}
                                recommendations={data.analysis.savings.recommendations || []}
                                monthlySavingsCapacity={data.analysis.savings.monthly_savings_capacity}
                            />
                        )}

                        {/* Budget Card */}
                        {data.analysis.budget && (
                            <BudgetCard
                                monthlySavingsPotential={data.analysis.budget.monthly_savings_potential || 0}
                                overspendingCategories={data.analysis.budget.overspending_categories || []}
                                quickWins={data.analysis.budget.quick_wins || []}
                                recommendedBudget={data.analysis.budget.recommended_budget}
                            />
                        )}

                        {/* Risk Card */}
                        {data.analysis.risk && (
                            <RiskCard
                                overallScore={data.analysis.risk.overall_score || 50}
                                riskLevel={data.analysis.risk.risk_level || 'Medium'}
                                debtRiskScore={data.analysis.risk.debt_risk_score}
                                savingsRiskScore={data.analysis.risk.savings_risk_score}
                                topPriorities={data.analysis.risk.top_priorities || []}
                            />
                        )}
                    </div>

                    {/* Errors/Warnings */}
                    {data.errors && data.errors.length > 0 && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                            <h3 className="text-red-800 font-semibold mb-2">Errors</h3>
                            <ul className="list-disc list-inside text-red-700 text-sm">
                                {data.errors.map((error, i) => (
                                    <li key={i}>{error}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </motion.div>
            </main>
        </div>
    );
};
