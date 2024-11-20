"use client";

import { useState } from 'react';
import { useDropzone } from 'react-dropzone';

type UseVideoDropzoneReturn = {
    file: File | undefined;
    fileRejectionItems: JSX.Element[];
    onRemove: () => void;
    getRootProps: () => any;
    getInputProps: () => any;
};

export const useVideoDropzone = () => {
    const [file, setFile] = useState<File | undefined>();

    // Handler for when a file is dropped
    const onDrop = (acceptedFiles: File[]) => {
        setFile(acceptedFiles[0]);
    };

    // Handler for removing the selected file
    const onRemove = () => {
        setFile(undefined);
    };

    // Dropzone configuration
    const { fileRejections, getRootProps, getInputProps } = useDropzone({
        accept: {
            'video/mp4': ['.mp4'],
            'video/quicktime': ['.mov'],
            'video/webm': ['.webm'],
            'video/avi': ['.avi'],
        },
        maxSize: 100 * 1000 * 1000, // 100 MB limit
        maxFiles: 1,
        onDrop,
    });

    // File rejection error messages
    const fileRejectionItems = fileRejections.map(({ file, errors }) => {
        return (
            <ul key={file.name}>
                {errors.map((e) => (
                    <li key={e.code}>{e.message}</li>
                ))}
            </ul>
        );
    });

    return {
        file,
        fileRejectionItems,
        onRemove,
        getRootProps,
        getInputProps,
    };
};
