import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Brain, TrendingUp } from 'lucide-react';
import { FileUpload } from '../components/upload/FileUpload';
import { uploadStatement } from '../lib/api';

export const Home: React.FC = () => {
    const navigate = useNavigate();
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const handleFileSelect = async (file: File) => {
        setIsUploading(true);
        setError(null);
        setUploadProgress(0);

        // Simulate progress
        const progressInterval = setInterval(() => {
            setUploadProgress((prev) => {
                if (prev >= 90) {
                    clearInterval(progressInterval);
                    return prev;
                }
                return prev + 10;
            });
        }, 200);

        try {
            const result = await uploadStatement(file);
            clearInterval(progressInterval);
            setUploadProgress(100);
            setSuccess(true);

            // Navigate to results after a short delay
            setTimeout(() => {
                navigate(`/analysis/${result.analysis_id}`, { state: { data: result } });
            }, 1500);
        } catch (err: any) {
            clearInterval(progressInterval);
            const detail = err.response?.data?.detail || err.response?.data?.error || err.message || 'Upload failed. Please try again.';
            setError(typeof detail === 'string' ? detail : JSON.stringify(detail));
            setIsUploading(false);
            setUploadProgress(0);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
            {/* Header */}
            <header className="pt-12 pb-8">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="container mx-auto px-4 text-center"
                >
                    <div className="flex items-center justify-center gap-3 mb-4">
                        <motion.div
                            animate={{ rotate: [0, 10, -10, 0] }}
                            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                        >
                            <Brain className="w-12 h-12 text-primary-600" />
                        </motion.div>
                        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                            AI Financial Coach
                        </h1>
                    </div>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Upload your bank statement and get AI-powered insights to transform your financial health
                    </p>
                </motion.div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-12">
                <FileUpload
                    onFileSelect={handleFileSelect}
                    isUploading={isUploading}
                    uploadProgress={uploadProgress}
                    error={error}
                    success={success}
                />

                {/* Features */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
                >
                    <FeatureCard
                        icon={<Sparkles className="w-8 h-8 text-primary-600" />}
                        title="AI-Powered Analysis"
                        description="4 specialized AI agents analyze your finances from every angle"
                    />
                    <FeatureCard
                        icon={<TrendingUp className="w-8 h-8 text-green-600" />}
                        title="Actionable Insights"
                        description="Get personalized recommendations to optimize your budget"
                    />
                    <FeatureCard
                        icon={<Brain className="w-8 h-8 text-purple-600" />}
                        title="Smart Strategies"
                        description="Debt payoff plans, savings goals, and risk assessment"
                    />
                </motion.div>
            </main>

            {/* Footer */}
            <footer className="py-8 text-center text-gray-500 text-sm">
                <p>Powered by OpenRouter AI • Secure & Private</p>
            </footer>
        </div>
    );
};

interface FeatureCardProps {
    icon: React.ReactNode;
    title: string;
    description: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => {
    return (
        <motion.div
            whileHover={{ y: -4 }}
            className="bg-white p-6 rounded-xl shadow-md text-center"
        >
            <div className="flex justify-center mb-4">{icon}</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
            <p className="text-gray-600 text-sm">{description}</p>
        </motion.div>
    );
};
