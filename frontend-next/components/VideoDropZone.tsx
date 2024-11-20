"use client";

import { useVideoDropzone } from "@/hooks/useVideoDropzone";
import { UploadIcon } from "./icons/upload";
import { Button } from '@nextui-org/react';
import { useState } from "react";

const VideoDropZone = () => {
    const [response, setResponse] = useState<Response>();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [isImageDetected, setIsImageDetected] = useState<boolean>(false);
    const { file, fileRejectionItems, onRemove, getRootProps, getInputProps } =
        useVideoDropzone();

    const handleSubmit = async () => {
        setIsImageDetected(true);
        setIsLoading(true);

        try {
            if (!file) return;

            //const response = await getDetection(file);

            setResponse(response);
        } catch (error) {
            console.error(error);
        }
        setIsLoading(false);
    }

    return (
        <div className="flex gap-12 items-center">
            <div className="flex flex-col gap-4 items-center">
                <section
                    className="border-2 border-dashed border-warning rounded-md"
                    style={{ borderStyle: "dashed", padding: "8rem" }}
                >
                    <div {...getRootProps()}>
                        <input {...getInputProps()} />
                        <div className="flex flex-col gap-4 items-center">
                            <UploadIcon
                                width={100}
                                height={100}
                            />
                            <p className="text-white">Drag and drop some files here, or click to select files</p>
                        </div>
                    </div>
                </section>
                <Button
                    type="submit"
                    onClick={handleSubmit}
                    variant="solid"
                    style={{
                        opacity: !file ? 0.5 : 1,
                        cursor: !file ? 'not-allowed' : 'pointer',
                    }}
                    color="warning"
                    disabled={!file}
                    className="text-white bg-warning"
                >
                    Detect
                </Button>
            </div>
        </div>
    );
};

export default VideoDropZone;
