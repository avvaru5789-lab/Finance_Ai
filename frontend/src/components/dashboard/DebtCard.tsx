import React from 'react';
import { motion } from 'framer-motion';
import { CreditCard, TrendingDown, Calendar, AlertCircle } from 'lucide-react';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../lib/utils';

interface DebtCardProps {
    totalDebt: number;
    payoffStrategy: string;
    monthsToPayoff: number;
    recommendations: string[];
    recommendedMonthlyPayment?: number;
}

export const DebtCard: React.FC<DebtCardProps> = ({
    totalDebt,
    payoffStrategy,
    monthsToPayoff,
    recommendations,
    recommendedMonthlyPayment,
}) => {
    return (
        <Card className="border-l-4 border-red-500">
            <div className="flex items-start justify-between mb-4">
                <div>
                    <div className="flex items-center gap-2 mb-2">
                        <CreditCard className="w-6 h-6 text-red-600" />
                        <h3 className="text-xl font-bold text-gray-900">Debt Analysis</h3>
                    </div>
                    <motion.p
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ type: 'spring', duration: 0.8 }}
                        className="text-3xl font-bold text-red-600 mb-1"
                    >
                        {formatCurrency(totalDebt)}
                    </motion.p>
                    <p className="text-sm text-gray-600">Total Debt</p>
                </div>
            </div>

            <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <div className="bg-red-50 p-3 rounded-lg">
                        <div className="flex items-center gap-2 mb-1">
                            <TrendingDown className="w-4 h-4 text-red-600" />
                            <p className="text-sm font-medium text-gray-700">Strategy</p>
                        </div>
                        <p className="text-lg font-semibold text-gray-900">{payoffStrategy}</p>
                    </div>

                    <div className="bg-red-50 p-3 rounded-lg">
                        <div className="flex items-center gap-2 mb-1">
                            <Calendar className="w-4 h-4 text-red-600" />
                            <p className="text-sm font-medium text-gray-700">Timeline</p>
                        </div>
                        <p className="text-lg font-semibold text-gray-900">{monthsToPayoff} months</p>
                    </div>
                </div>

                {recommendedMonthlyPayment && (
                    <div className="bg-amber-50 border border-amber-200 p-3 rounded-lg">
                        <p className="text-sm text-amber-800 font-medium">
                            Recommended Payment: <span className="font-bold">{formatCurrency(recommendedMonthlyPayment)}/mo</span>
                        </p>
                    </div>
                )}

                <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <AlertCircle className="w-4 h-4" />
                        Recommendations
                    </h4>
                    <ul className="space-y-2">
                        {recommendations.slice(0, 3).map((rec, index) => (
                            <motion.li
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="flex items-start gap-2 text-sm text-gray-700"
                            >
                                <span className="text-red-600 font-bold">•</span>
                                <span>{rec}</span>
                            </motion.li>
                        ))}
                    </ul>
                </div>
            </div>
        </Card>
    );
};
