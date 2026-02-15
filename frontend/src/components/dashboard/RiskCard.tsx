import React from 'react';
import { motion } from 'framer-motion';
import { Shield, AlertTriangle, CheckCircle, XCircle, Circle } from 'lucide-react';
import { Card } from '../ui/Card';
import { getRiskColor, getRiskLevel, getRiskBgColor } from '../../lib/utils';

interface RiskCardProps {
    overallScore: number;
    riskLevel: string;
    debtRiskScore?: number;
    savingsRiskScore?: number;
    topPriorities: string[];
}

export const RiskCard: React.FC<RiskCardProps> = ({
    overallScore,
    riskLevel,
    debtRiskScore,
    savingsRiskScore,
    topPriorities,
}) => {
    const riskColor = getRiskColor(overallScore);
    const riskBg = getRiskBgColor(overallScore);
    const level = getRiskLevel(overallScore);

    const getIcon = () => {
        if (overallScore < 34) return <CheckCircle className="w-6 h-6 text-green-600" />;
        if (overallScore < 67) return <AlertTriangle className="w-6 h-6 text-amber-600" />;
        return <XCircle className="w-6 h-6 text-red-600" />;
    };

    // Circle progress calculation
    const circumference = 2 * Math.PI * 45; // radius = 45
    const strokeDashoffset = circumference - (overallScore / 100) * circumference;

    return (
        <Card className={`border-l-4 ${overallScore < 34 ? 'border-green-500' : overallScore < 67 ? 'border-amber-500' : 'border-red-500'}`}>
            <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                        <Shield className="w-6 h-6 text-gray-700" />
                        <h3 className="text-xl font-bold text-gray-900">Risk Score</h3>
                    </div>
                    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${riskBg}`}>
                        {getIcon()}
                        <span className={`text-sm font-semibold ${riskColor}`}>{level} Risk</span>
                    </div>
                </div>

                <div className="relative w-24 h-24">
                    <svg className="transform -rotate-90" width="96" height="96">
                        <circle
                            cx="48"
                            cy="48"
                            r="45"
                            stroke="currentColor"
                            strokeWidth="6"
                            fill="none"
                            className="text-gray-200"
                        />
                        <motion.circle
                            cx="48"
                            cy="48"
                            r="45"
                            stroke="currentColor"
                            strokeWidth="6"
                            fill="none"
                            strokeLinecap="round"
                            className={riskColor}
                            initial={{ strokeDashoffset: circumference }}
                            animate={{ strokeDashoffset }}
                            transition={{ duration: 1.5, ease: 'easeOut' }}
                            strokeDasharray={circumference}
                        />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <motion.span
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5, type: 'spring' }}
                            className={`text-2xl font-bold ${riskColor}`}
                        >
                            {overallScore}
                        </motion.span>
                    </div>
                </div>
            </div>

            <div className="space-y-4">
                {(debtRiskScore !== undefined || savingsRiskScore !== undefined) && (
                    <div className="grid grid-cols-2 gap-3">
                        {debtRiskScore !== undefined && (
                            <div className="bg-gray-50 p-3 rounded-lg">
                                <p className="text-xs text-gray-600 mb-1">Debt Risk</p>
                                <p className="text-lg font-bold text-gray-900">{debtRiskScore}/100</p>
                            </div>
                        )}
                        {savingsRiskScore !== undefined && (
                            <div className="bg-gray-50 p-3 rounded-lg">
                                <p className="text-xs text-gray-600 mb-1">Savings Risk</p>
                                <p className="text-lg font-bold text-gray-900">{savingsRiskScore}/100</p>
                            </div>
                        )}
                    </div>
                )}

                <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                        <Circle className="w-4 h-4" fill="currentColor" />
                        Top Priorities
                    </h4>
                    <ul className="space-y-2">
                        {topPriorities.slice(0, 3).map((priority, index) => (
                            <motion.li
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="flex items-start gap-3 text-sm"
                            >
                                <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-white font-bold text-xs ${overallScore < 34 ? 'bg-green-600' : overallScore < 67 ? 'bg-amber-600' : 'bg-red-600'}`}>
                                    {index + 1}
                                </span>
                                <span className="text-gray-700 flex-1">{priority}</span>
                            </motion.li>
                        ))}
                    </ul>
                </div>
            </div>
        </Card>
    );
};
