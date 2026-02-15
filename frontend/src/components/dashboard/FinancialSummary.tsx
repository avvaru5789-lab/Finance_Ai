import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, TrendingUp, TrendingDown } from 'lucide-react';
import { Card } from '../ui/Card';
import { formatCurrency, formatPercent } from '../../lib/utils';

interface FinancialSummaryProps {
    totalIncome: number;
    totalExpenses: number;
    netIncome: number;
    savingsRate: number;
    debtToIncomeRatio?: number;
}

export const FinancialSummary: React.FC<FinancialSummaryProps> = ({
    totalIncome,
    totalExpenses,
    netIncome,
    savingsRate,
    debtToIncomeRatio,
}) => {
    return (
        <Card className="col-span-full bg-gradient-to-br from-primary-50 to-blue-50 border border-primary-100">
            <div className="flex items-start justify-between mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                        <Sparkles className="w-6 h-6 text-primary-600" />
                        Financial Summary
                    </h2>
                    <p className="text-gray-600 mt-1">Your monthly financial overview</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    label="Total Income"
                    value={formatCurrency(totalIncome)}
                    trend="positive"
                    icon={<TrendingUp className="w-5 h-5" />}
                />
                <MetricCard
                    label="Total Expenses"
                    value={formatCurrency(totalExpenses)}
                    trend="negative"
                    icon={<TrendingDown className="w-5 h-5" />}
                />
                <MetricCard
                    label="Net Income"
                    value={formatCurrency(netIncome)}
                    trend={netIncome > 0 ? 'positive' : 'negative'}
                    icon={netIncome > 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
                />
                <MetricCard
                    label="Savings Rate"
                    value={formatPercent(savingsRate)}
                    trend={savingsRate > 20 ? 'positive' : 'warning'}
                />
            </div>
        </Card>
    );
};

interface MetricCardProps {
    label: string;
    value: string;
    trend?: 'positive' | 'negative' | 'warning' | 'neutral';
    icon?: React.ReactNode;
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, trend = 'neutral', icon }) => {
    const trendColors = {
        positive: 'text-green-600 bg-green-50',
        negative: 'text-red-600 bg-red-50',
        warning: 'text-amber-600 bg-amber-50',
        neutral: 'text-gray-600 bg-gray-50',
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white p-4 rounded-xl shadow-sm border border-gray-100"
        >
            <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-medium text-gray-600">{label}</p>
                {icon && (
                    <div className={`p-2 rounded-lg ${trendColors[trend]}`}>
                        {icon}
                    </div>
                )}
            </div>
            <motion.p
                initial={{ scale: 0.5 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200, damping: 15, delay: 0.1 }}
                className="text-2xl font-bold text-gray-900"
            >
                {value}
            </motion.p>
        </motion.div>
    );
};
