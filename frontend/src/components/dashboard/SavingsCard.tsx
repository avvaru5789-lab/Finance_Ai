import React from 'react';
import { motion } from 'framer-motion';
import { Wallet, Target, Clock, Lightbulb } from 'lucide-react';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../lib/utils';

interface SavingsCardProps {
    monthlySavingsGoal: number;
    emergencyFundGap: number;
    monthsToEmergencyFund: number;
    recommendations: string[];
    monthlySavingsCapacity?: number;
}

export const SavingsCard: React.FC<SavingsCardProps> = ({
    monthlySavingsGoal,
    emergencyFundGap,
    monthsToEmergencyFund,
    recommendations,
    monthlySavingsCapacity,
}) => {
    const progress = monthlySavingsCapacity
        ? Math.min((monthlySavingsCapacity / monthlySavingsGoal) * 100, 100)
        : 0;

    return (
        <Card className="border-l-4 border-green-500">
            <div className="flex items-start justify-between mb-4">
                <div>
                    <div className="flex items-center gap-2 mb-2">
                        <Wallet className="w-6 h-6 text-green-600" />
                        <h3 className="text-xl font-bold text-gray-900">Savings Strategy</h3>
                    </div>
                    <motion.p
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ type: 'spring', duration: 0.8 }}
                        className="text-3xl font-bold text-green-600 mb-1"
                    >
                        {formatCurrency(monthlySavingsGoal)}<span className="text-lg text-gray-600">/mo</span>
                    </motion.p>
                    <p className="text-sm text-gray-600">Monthly Goal</p>
                </div>
            </div>

            <div className="space-y-4">
                <div className="bg-green-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                            <Target className="w-4 h-4 text-green-600" />
                            <p className="text-sm font-medium text-gray-700">Emergency Fund Gap</p>
                        </div>
                        <p className="text-sm font-bold text-gray-900">{formatCurrency(emergencyFundGap)}</p>
                    </div>
                    <div className="w-full bg-green-200 rounded-full h-2 overflow-hidden">
                        <motion.div
                            className="h-full bg-green-600"
                            initial={{ width: 0 }}
                            animate={{ width: `${progress}%` }}
                            transition={{ duration: 1, ease: 'easeOut' }}
                        />
                    </div>
                    <div className="flex items-center gap-2 mt-2">
                        <Clock className="w-4 h-4 text-green-600" />
                        <p className="text-xs text-gray-600">
                            {monthsToEmergencyFund} months to full emergency fund
                        </p>
                    </div>
                </div>

                {monthlySavingsCapacity && (
                    <div className="bg-blue-50 border border-blue-200 p-3 rounded-lg">
                        <p className="text-sm text-blue-800 font-medium">
                            Current Capacity: <span className="font-bold">{formatCurrency(monthlySavingsCapacity)}/mo</span>
                        </p>
                    </div>
                )}

                <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <Lightbulb className="w-4 h-4" />
                        Tips
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
                                <span className="text-green-600 font-bold">✓</span>
                                <span>{rec}</span>
                            </motion.li>
                        ))}
                    </ul>
                </div>
            </div>
        </Card>
    );
};
