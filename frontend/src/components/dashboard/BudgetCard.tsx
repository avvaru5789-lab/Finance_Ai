import React from 'react';
import { motion } from 'framer-motion';
import { PieChart as PieIcon, DollarSign, Zap, ChevronDown } from 'lucide-react';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../lib/utils';

interface BudgetCardProps {
    monthlySavingsPotential: number;
    overspendingCategories: string[];
    quickWins: string[];
    recommendedBudget?: Record<string, number>;
}

export const BudgetCard: React.FC<BudgetCardProps> = ({
    monthlySavingsPotential,
    overspendingCategories,
    quickWins,
    recommendedBudget,
}) => {
    const [expanded, setExpanded] = React.useState(false);

    return (
        <Card className="border-l-4 border-blue-500">
            <div className="flex items-start justify-between mb-4">
                <div>
                    <div className="flex items-center gap-2 mb-2">
                        <PieIcon className="w-6 h-6 text-blue-600" />
                        <h3 className="text-xl font-bold text-gray-900">Budget Optimizer</h3>
                    </div>
                    <motion.p
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ type: 'spring', duration: 0.8 }}
                        className="text-3xl font-bold text-blue-600 mb-1"
                    >
                        {formatCurrency(monthlySavingsPotential)}<span className="text-lg text-gray-600">/mo</span>
                    </motion.p>
                    <p className="text-sm text-gray-600">Savings Potential</p>
                </div>
            </div>

            <div className="space-y-4">
                <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <DollarSign className="w-4 h-4" />
                        Overspending Areas
                    </h4>
                    <div className="space-y-2">
                        {overspendingCategories.slice(0, 3).map((cat, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="flex items-center justify-between bg-amber-50 p-2 rounded-lg"
                            >
                                <span className="text-sm font-medium text-gray-700">{cat}</span>
                            </motion.div>
                        ))}
                    </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                    <h4 className="text-sm font-semibold text-green-800 mb-2 flex items-center gap-2">
                        <Zap className="w-4 h-4" />
                        Quick Wins
                    </h4>
                    <ul className="space-y-1">
                        {quickWins.slice(0, 2).map((win, index) => (
                            <motion.li
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="text-sm text-green-800"
                            >
                                • {win}
                            </motion.li>
                        ))}
                    </ul>
                </div>

                {recommendedBudget && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className="w-full flex items-center justify-between text-sm text-primary-600 hover:text-primary-700 font-medium"
                    >
                        <span>View Recommended Budget</span>
                        <motion.div
                            animate={{ rotate: expanded ? 180 : 0 }}
                            transition={{ duration: 0.3 }}
                        >
                            <ChevronDown className="w-4 h-4" />
                        </motion.div>
                    </button>
                )}

                {expanded && recommendedBudget && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="space-y-2 pt-2 border-t"
                    >
                        {Object.entries(recommendedBudget).map(([category, amount], index) => (
                            <div key={index} className="flex items-center justify-between text-sm">
                                <span className="text-gray-700">{category}</span>
                                <span className="font-semibold text-gray-900">{formatCurrency(amount)}</span>
                            </div>
                        ))}
                    </motion.div>
                )}
            </div>
        </Card>
    );
};
