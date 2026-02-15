import React, { useCallback, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

interface FileUploadProps {
    onFileSelect: (file: File) => void;
    isUploading: boolean;
    uploadProgress?: number;
    error?: string | null;
    success?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({
    onFileSelect,
    isUploading,
    uploadProgress = 0,
    error,
    success,
}) => {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    }, []);

    const handleDragIn = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer.items && e.dataTransfer.items.length > 0) {
            setIsDragging(true);
        }
    }, []);

    const handleDragOut = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                setSelectedFile(file);
                onFileSelect(file);
            }
        }
    }, [onFileSelect]);

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                setSelectedFile(file);
                onFileSelect(file);
            }
        }
    }, [onFileSelect]);

    return (
        <div className="w-full max-w-2xl mx-auto">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className={cn(
                    'relative border-2 border-dashed rounded-2xl p-12 transition-all duration-300',
                    isDragging
                        ? 'border-primary-500 bg-primary-50 scale-105'
                        : 'border-gray-300 bg-white hover:border-primary-400 hover:bg-gray-50'
                )}
                onDragEnter={handleDragIn}
                onDragLeave={handleDragOut}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    accept=".pdf"
                    onChange={handleFileInput}
                    disabled={isUploading}
                />

                <AnimatePresence mode="wait">
                    {success ? (
                        <motion.div
                            key="success"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center justify-center text-center"
                        >
                            <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1, rotate: 360 }}
                                transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                            >
                                <CheckCircle2 className="w-20 h-20 text-green-500 mb-4" />
                            </motion.div>
                            <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                                Upload Successful!
                            </h3>
                            <p className="text-gray-600">
                                Processing your financial statement...
                            </p>
                        </motion.div>
                    ) : isUploading ? (
                        <motion.div
                            key="uploading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center justify-center text-center"
                        >
                            <Loader2 className="w-16 h-16 text-primary-600 mb-4 animate-spin" />
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Uploading...
                            </h3>
                            <div className="w-full max-w-xs mt-4">
                                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                                    <motion.div
                                        className="h-full bg-gradient-to-r from-primary-500 to-primary-600"
                                        initial={{ width: 0 }}
                                        animate={{ width: `${uploadProgress}%` }}
                                        transition={{ duration: 0.3 }}
                                    />
                                </div>
                                <p className="text-sm text-gray-600 mt-2">{uploadProgress}%</p>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.label
                            key="idle"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            htmlFor="file-upload"
                            className="flex flex-col items-center justify-center cursor-pointer text-center"
                        >
                            <motion.div
                                animate={{
                                    y: isDragging ? -10 : [0, -10, 0],
                                }}
                                transition={{
                                    duration: 2,
                                    repeat: isDragging ? 0 : Infinity,
                                    ease: 'easeInOut',
                                }}
                            >
                                {selectedFile ? (
                                    <FileText className="w-20 h-20 text-primary-600 mb-4" />
                                ) : (
                                    <Upload className="w-20 h-20 text-gray-400 mb-4" />
                                )}
                            </motion.div>

                            <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                                {selectedFile ? selectedFile.name : 'Upload Bank Statement'}
                            </h3>
                            <p className="text-gray-600 mb-4">
                                {selectedFile
                                    ? 'Ready to analyze'
                                    : 'Drag & drop your PDF here, or click to browse'}
                            </p>
                            <div className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors">
                                Choose File
                            </div>
                        </motion.label>
                    )}
                </AnimatePresence>

                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3"
                    >
                        <XCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-red-800">{error}</p>
                    </motion.div>
                )}
            </motion.div>

            <p className="text-center text-sm text-gray-500 mt-4">
                Supported format: PDF • Max file size: 10MB
            </p>
        </div>
    );
};
