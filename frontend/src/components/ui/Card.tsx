import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';

interface CardProps {
    children: React.ReactNode;
    className?: string;
    hover?: boolean;
    glow?: boolean;
}

export const Card: React.FC<CardProps> = ({
    children,
    className,
    hover = true,
    glow = false,
}) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            whileHover={hover ? { y: -4, boxShadow: '0 10px 30px rgba(0,0,0,0.1)' } : undefined}
            className={cn(
                'bg-white rounded-xl shadow-md p-6 transition-shadow duration-300',
                glow && 'shadow-glow',
                className
            )}
        >
            {children}
        </motion.div>
    );
};
